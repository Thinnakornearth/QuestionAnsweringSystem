from random import triangular
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary.xmlschema import XMLSchema
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.rio.rdfformat import RDFFormat
from franz.openrdf.vocabulary import RDF
from requests import RequestException
from classifier.kw_extract import extract_kw, extract_verb
import re
from synonym.nltk_synonym import get_synonym
from synonym.nltk_synonym import get_noun_syn
from typo.spellingcorrection import fix_typo

class Allegrograph(object):
    def __init__(self, repo, host, port, user, pass_word, create=True, clear=True):
        self.repo = repo
        self.host = host
        self.port = port
        self.user = user
        self.pass_word = pass_word
        self.create = create
        self.clear = clear
        '''
        The default values of create and clear are True which mean if the repo is not existed, the new one will be created
        AND the statements will be cleared everytime we make new queries. If you don't want them to be clear, the clear param must 
        be False.
        '''
        self.conn = ag_connect(repo=self.repo, host=self.host, port=self.port, user=self.user, password=self.pass_word, create=self.create, clear=self.clear)

    def set_namespace(self, prefix, namespace_uri):
        self.conn.setNamespace(prefix, namespace_uri)


    def add_triples_literal(self, namespace_uri, subject, predicate, object, type=XMLSchema.STRING):
        # type means your literal type in which can be XMLSchema.INTEGER or XMLSchema.STRING and etc.
        uri = namespace_uri
        s = self.conn.createURI(namespace=uri, localname=subject)
        p = self.conn.createURI(namespace=uri, localname=predicate)
        o_literal = self.conn.createLiteral(object, datatype=type)
        statement = self.conn.createStatement(s, p, o_literal)
        self.conn.add(statement)
    
    def add_triples_rdf_type(self, namespace_uri, subject, object):
        uri = namespace_uri
        s = self.conn.createURI(namespace=uri, localname=subject)
        o_literal = self.conn.createURI(namespace=uri, localname=object)
        statement = self.conn.createStatement(s, RDF.TYPE, o_literal)
        self.conn.add(statement)


    def display_all_triples(self):
        self.conn.executeTupleQuery("""
        SELECT ?s ?p ?o WHERE {
                ?s ?p ?o .
        }""", output=True)
        '''<-------------------------------------The below codes work fine as well------------------->'''
        # query_string = "SELECT ?s ?p ?o  WHERE {?s ?p ?o . } ORDER BY ?s ?p ?o"
        # tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        # result = tuple_query.evaluate()
        # with result:
        #     for binding_set in result:
        #         s = binding_set.getValue("s")
        #         p = binding_set.getValue("p")
        #         o = binding_set.getValue("o")
        #         print("%s %s %s" % (s, p, o))
    
    def get_data(self) -> list:
        query_string = "SELECT ?s ?p ?o  WHERE {?s ?p ?o . } ORDER BY ?s ?p ?o"
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate(output_format=RDFFormat.JSONLD)
        temp = []
        for i in result:
            s = str(i.getValue("s"))
            p = str(i.getValue("p"))
            o = str(i.getValue("o"))
            dict = {"s": s,
                    "p": p,
                    "o": o
                    }
            #Convert to JSON
            # dict = {"s": s.replace("<", "&#60;").replace(">", "&#62;"),
            #         "p": p.replace("<", "&#60;").replace(">", "&#62;"),
            #         "o": o.replace("<", "&#60;").replace(">", "&#62;")
            #         }
            temp.append(dict)
        return temp

    #get all subject
    def get_all_subject(self):
        query_string = "SELECT ?s  WHERE {?s ?p ?o . } ORDER BY ?p ?o"
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        search_array = []
        for i in result:
            word = str(i["s"])
            slash = 0
            for j in range (len(word)):
                if word[j] == "/":
                    slash += 1
            raw_word = word.split("/")[slash].replace(">", "")
            search_array.append(raw_word)
        return search_array
    
    #get all triples
    def get_all_triples(self):
        query_string = "SELECT ?s ?p ?o { ?s ?p ?o . }"
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        array = []
        for i in result:
            s = self.delete_symbols(str(i["s"]), "s")
            p = self.delete_symbols(str(i["p"]), "p")
            o = self.delete_symbols(str(i["o"]), "o")
            dict = {"s": s, "p": p, "o": o}
            array.append(dict)
        return array
    
    def get_statement(self, word):
        word = fix_typo(word)
        kw = []
        keyword = extract_kw(word)
        if len(word.split()) > 1:
            if word.split()[0] == "who":
                return_value = self.get_who_search(word)
                if return_value:
                    return return_value
                                                          
            verbs = extract_verb(word)
            if verbs:
                for i in verbs:
                    verb = str(i).lower()
                    array_verb = get_synonym(verb)
                    for each in array_verb:
                        domain = self.get_domain(each)
                        if (domain):
                            print("Here is the actual domain and range: ")
                            print(domain, "\n")
                            index = 0
                            for j in range(len(keyword)):
                                w = keyword[j]
                                if (w[0] == each):
                                    index = j
                            if index > 0:
                                del keyword[index]
                            kw = keyword
                            for k in range(len(kw)):
                                result = kw[k][0]
                                keyword_synonyms = result.split(" ")
                                print("Keyword Synonym", keyword_synonyms)
                                for number_key in range(len(keyword_synonyms)):
                                    arr_syn = get_synonym(keyword_synonyms[number_key])
                                    for j in arr_syn:
                                        j = ''.join(char for char in j if char.isalnum())
                                        temp = result.replace(keyword_synonyms[number_key], j)
                                        temp = ' '.join(elem.capitalize() for elem in temp.split())
                                        print("Result: ", temp)
                                        if temp.lower() in domain[0]["o"].lower() or temp.lower() in domain[0]["o2"].lower():
                                            return self.get_statement(domain[0]["o2"])
                                        elif temp.lower() in domain[0]["o_comment"].lower() or temp.lower() in domain[0]["o2_comment"].lower():
                                           return self.get_statement(domain[0]["o2"])
                        #####Not Finish Noun Synonyms for this part !!!
                        else:
                            arr = []
                            if each[len(each)-1] == "e":
                                new_word = each[:len(each)-1] + "*"
                            else:
                                new_word = each + "*"
                            free_text = self.free_text_search(new_word)
                            if free_text:
                                for each_text in free_text:
                                    s = each_text["subject"].replace(" ", "")
                                    query_string = "SELECT ?o { i:%s <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?o . }" %s
                                    tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
                                    query = tuple_query.evaluate()
                                    for each_query in query:
                                        o = self.delete_symbols(str(each_query["o"]), "o")
                                        if "_" in o:
                                            for k in keyword:
                                                t = each_text["o"].replace('."@en', '')
                                                each_text["o"] = t
                                                split = each_text["o"].split()
                                                if k[0] in split and k[0] != each:
                                                    arr.append(each_text)
                                                    break
                                if arr:
                                    return arr
                                    
            
            #This else is for a query that has no verbs
            else:
                kw = keyword
            if (kw):
                array = []
                for key in kw:
                    result = key[0]
                    keyword_synonyms = result.split(" ")
                    for i in range(len(keyword_synonyms)):
                        if array:
                            break
                        arr_syn = get_synonym(keyword_synonyms[i])
                        for j in arr_syn:
                            j = ''.join(char for char in j if char.isalnum())
                            temp = result.replace(keyword_synonyms[i], j)
                            temp = ' '.join(elem.capitalize() for elem in temp.split())
                            print("Result: ", temp)
                            array = self.get_simple_search(temp)
                            if array:
                                break
                            else:
                                temp = temp.lower()

                           


                    # print("First keyword: ", result)
                    # print()
                    # result = ' '.join(elem.capitalize() for elem in result.split())
                    # array = self.get_simple_search(result)

            else:
                return
            if array:
                return array
            else:
                array = self.free_text_search(kw[0][0])
                if array:
                    return array
                else:
                    for i in range(len(kw) -1, 0, -1):
                        print("Keyword Iteration No.{0}: {1}".format(len(kw)-i, kw[i][0]))
                        return self.get_statement(kw[i][0])


        #This else if for statement that has only one word
        else:
            result= word
            array = self.get_simple_search(result)
            if array:
                return array
            else:
                array = self.free_text_search(result)
                if array:
                    return array
                else:
                    for i in range(len(kw) -1, 0, -1):
                        print("Keyword Iteration No.{0}: {1}".format(len(kw)-i, kw[i][0]))
                        return self.get_statement(kw[i][0])


    def get_who_search(self, word, original_query=None):
        verbs = extract_verb(word)
        array = []
        domain_temp = []
        if original_query:
            word_temp = original_query
        else:
            word_temp = word
        if verbs:
            for i in verbs:
                verb = str(i).lower()
                array_syn = get_synonym(verb)
                for each in array_syn:
                    domain = self.get_domain(each)
                    if (domain):
                        domain_temp = domain
                        query_string = "SELECT ?o { i:%s <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?o . }" %domain[0]["o2"]
                        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
                        query = tuple_query.evaluate()
                        for i in query:
                            if str(i["o"]) == "<http://www.semanticweb.org/zhenyuzhang/ontologies/DRANPTO/Person>":
                                keyword = extract_kw(word_temp)
                                index = 0
                                for j in range(len(keyword)):
                                    w = keyword[j]
                                    if (w[0] == each):
                                         index = j
                                if index > 0:
                                    del keyword[index]
                                kw = keyword
                                for k in range(len(kw)):
                                    if kw[k][0].lower() in domain[0]["o"].lower() or kw[k][0] in domain[0]["o2"].lower():
                                        array = [{"domain": domain[0]["o2"], "comment": domain[0]["o2_comment"]}]
                                    elif kw[k][0].lower() in domain[0]["o_comment"].lower() or kw[k][0] in domain[0]["o2_comment"].lower():
                                        array = [{"domain": domain[0]["o2"], "comment": domain[0]["o2_comment"]}] 
        if array:
            return array
        else:
            if domain_temp:
                return self.get_who_search(domain_temp[0]["Domain"][:len(domain_temp[0]["Domain"])-1], original_query=word_temp)
            else: 
                return
                                
                            
        
  
                            



    def get_simple_search(self, result):
        array = []
        result = result.replace(" ", "")
        query_string = "SELECT ?o { i:%s <http://www.w3.org/2000/01/rdf-schema#comment> ?o . }" %result
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        query = tuple_query.evaluate()
        for i in query:
            dict = {"subject": result, "o": str(i["o"])}
            array.append(dict)
        return array

    def free_text_search(self, result, questionMark=None):
        array = []
        pred = self.conn.createURI(namespace='http://www.w3.org/2000/01/rdf-schema#',
                            localname="label")
        self.conn.createFreeTextIndex("index1", predicates=[pred])
        if questionMark:
            result = result[:len(result)-1] + questionMark
            print(result)
        for triple in self.conn.evalFreeTextSearch(
            result, index="index1"):
            s = self.delete_symbols(triple[0], "s")
            p = self.delete_symbols(triple[1], "p")
            o = self.delete_symbols(triple[2], "o")
            dict = {"s": s, "p": p, "o": o}
            subject = dict["s"]
            #fixhere
            subject2 = ' '.join(elem.capitalize() for elem in subject.split())
            subject2 = subject.replace(" ", "")
            query_string = "SELECT ?o { i:%s <http://www.w3.org/2000/01/rdf-schema#comment> ?o . }" %subject2
            tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
            result = tuple_query.evaluate()
            if not result:
                query_string = "SELECT ?o { i:%s <http://www.w3.org/2000/01/rdf-schema#comment> ?o . }" %subject
                tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
            for i in result:
                dict = {"subject": subject, "o": str(i["o"])}
                array.append(dict)
        if array:
            return array
    
        
            # else:
            #     try:
            #         domain_dict = self.get_domain(kw[len(kw)-1][0])
            #         print("Second keyword: ", kw[len(kw)-1][0])
            #         if not domain_dict:
            #             return self.get_statement(kw[len(kw)-1][0])
            #         domain_word = domain_dict[0].get("o")
            #         return self.get_statement(domain_word)

            #     except:
            #         print("Third keyword: ", kw[1][0])
            #         array = self.get_domain(kw[1][0])
            #         if array:
            #             domain_word = array[0].get("o")
            #             return self.get_statement(domain_word)
            #         else:
            #             domain_dict = self.get_domain(kw[len(kw)-2][0])
            #             print("Fourth keyword: ", kw[len(kw)-2][0])
            #             domain_word = domain_dict[0].get("o")
            #             return self.get_statement(domain_word)


    def get_domain(self, word, ):
        if word[len(word)-1] == "s" and word[len(word)-2] == "s":
            subject = word + "es"
        elif word[len(word)-1] == "h" and word[len(word)-2] == "c":
            subject = word + "es"
        elif word[len(word)-1] == "y":
            subject = word.replace("y", "ies")
        elif word[len(word)-1] == "d" and word[len(word)-2] == "e" and word[len(word)-3] == "i":
            subject = word.replace("ied", "ies")
        elif word[len(word)-1] == "d" and word[len(word)-2] == "e":
            subject = word.replace("ed", "s")
        elif (any(x.isupper() for x in word)):
            subject = word
        else:
            subject = word + "s"
        subject = subject.replace(" ", "")
        query_string = "SELECT ?p ?o { i:%s ?p ?o . }" %subject
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        query = tuple_query.evaluate()
        array = []
        dict = {}
        for i in query:
            if "range" in str(i["p"]): 
                dict = {"Range": subject, "o": self.delete_symbols(str(i["o"]), "o")}
                print("\nHere is the range: ")
                print(dict)
                print()
            if "domain" in str(i["p"]):
                dict["Domain"] = subject
                dict["o2"] = self.delete_symbols(str(i["o"]), "o")
                print("\nHere is the domain: ")
                print(dict)
                print()
        if dict:
            query_string = "SELECT ?p ?o { i:%s ?p ?o . }" %dict["o"]
            tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
            domain_query = tuple_query.evaluate()
            for i in domain_query:
                if "comment" in str(i["p"]):
                    dict["o_comment"] = str(i["o"])
            query_string = "SELECT ?p ?o { i:%s ?p ?o . }" %dict["o2"]
            tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
            domain_query = tuple_query.evaluate()
            for i in domain_query:
                if "comment" in str(i["p"]):
                    dict["o2_comment"] = str(i["o"])
            array.append(dict)
            return array
 


    #Delete unnecessary symbols
    def delete_symbols(self, uri, method = None):
        if method == "s":
            slash = 0
            for i in range (len(uri)):
                if uri[i] == "/":
                    slash += 1
            raw_word = uri.split("/")[slash].replace(">", "")
            re_outer = re.compile(r'([^A-Z ])([A-Z])')
            re_inner = re.compile(r'\b[A-Z]+(?=[A-Z][a-z])')
            raw_word = re_inner.sub(r'\g<0> ', re_outer.sub(r'\1 \2', raw_word))
        elif method == "p":
            for i in range (len(uri)):
                try:
                    raw_word = uri.split("#")[1].replace(">", "")
                except:
                    slash = 0
                    for i in range (len(uri)):
                        if uri[i] == "/":
                            slash += 1
                    raw_word = uri.split("/")[slash].replace(">", "")
        elif method == "o":
            for i in range (len(uri)):
                try:
                    raw_word = uri.split("#")[1].replace(">", "")
                except:
                    slash = 0
                    for i in range (len(uri)):
                        if uri[i] == "/":
                            slash += 1
                    if slash <= 1:
                        raw_word = uri
                    else:
                        raw_word = uri.split("/")[slash].replace(">", "")
                        
                    try:
                        raw_word = raw_word.replace("@en", "")
                    except:
                        pass
        return raw_word





    '''<-------------------------------------Ignore the below codes------------------------------------------------->'''
    # def get_match_data(self, uri_to_search=None, literal=None, search=None) -> list:
    #     if search == "Subject":
    #         uri = self.conn.createURI(uri_to_search)
    #         statements = self.conn.getStatements(uri, None, None)
    #     elif search == "Predicate":
    #         uri = self.conn.createURI(uri_to_search)
    #         statements = self.conn.getStatements(None, uri, None)
    #     elif search == "Object":
    #         name1 = self.conn.createLiteral(literal, datatype=XMLSchema.STRING)
    #         statements = self.conn.getStatements(None, None, name1)
    #     else:
    #         print("No matching, please enter appropriate search, new words or check or correctness.")
    #     statements.enableDuplicateFilter()
    #     temp = []
    #     for statement in statements:
    #         temp.append(str(statement))
    #     return temp

    # def get_match_data(self, prefix=None, subject=None, predicate=None, object=None) -> list:
    #     if subject:
    #         s = "{0}:{1}".format(prefix, subject)
    #         query_string = "SELECT ?p ?o  WHERE {%s ?p ?o . } ORDER BY ?p ?o" % s
    #         tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
    #         result = tuple_query.evaluate()
    #         temp = []
    #         for i in result:
    #             try:
    #                 p = str(i.getValue("p")).replace("<", "").replace(">", "").split("#")[1]
    #             except Exception:
    #                 p = str(i.getValue("p")).replace("<", "").replace(">", "").split("/")[6]
    #             try:
    #                 o = str(i.getValue("o")).replace("<", "").replace(">", "").split("/")[6]
    #             except Exception as e:
    #                 #This exception catches literal.
    #                 o = str(i.getValue("o")).replace("<", "").replace(">", "").replace('"', "").split("@")[0]
    #             dict = {
    #                     "p": p,
    #                     "o": o
    #                     }
    #             temp.append(dict)
    #         return temp
    #     if predicate:
    #         p = "{0}:{1}".format(prefix, predicate)
    #         query_string = "SELECT ?s  ?o  WHERE {?s %s ?o . } ORDER BY ?s ?o" % p
    #         tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
    #         result = tuple_query.evaluate()
    #         temp = []
    #         for i in result:
    #             s = str(i.getValue("s")).replace("<", "").replace(">", "").split("#")[1]
    #             try:
    #                 o = str(i.getValue("o")).replace("<", "").replace(">", "").split("#")[1]
    #             except Exception as e:
    #                 #This exception catches literal.
    #                 o = str(i.getValue("o")).replace("<", "").replace(">", "")
    #             dict = {
    #                     "s": s,
    #                     "o": o
    #                     }
    #             temp.append(dict)
    #         return temp
    #     if object:
    #         o = object
    #         query_string = "SELECT ?s ?p  WHERE {?s ?p %s . } ORDER BY ?s ?p" % o
    #         tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
    #         result = tuple_query.evaluate()
    #         temp = []
    #         for i in result:
    #             s = str(i.getValue("s"))
    #             p = str(i.getValue("p"))
    #             dict = {
    #                     "s": s,
    #                     "p": p
    #                     }
    #             temp.append(dict)
    #         return temp
    '''<------------------------------------------------------------------------------------------------------------>'''








# server = Allegrograph(repo='dranpto', host="10.12.175.35", port=10035, user="thinnakorn", pass_word="Earth6210", create=True, clear=False)
# # # # server.set_namespace("ex", "ex://")
# # # # # server.add_triples_literal("ex://", "person1", "first-name", "Nopphatsorn")
# # # # data = server.get_match_data(prefix="i", subject="BackgroundOfPersonWithDementia")
# # # # for i in data:
# # # #     print(i)

# array = server.get_all_triples()
# print(array[0]["s"])
# for i in array:
#     if i["s"] == "Accepting Refusal":
#         print(i)





