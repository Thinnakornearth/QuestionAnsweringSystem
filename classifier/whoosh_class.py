from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh import qparser
import os



class Whoosh_Ag:

    def __init__(self, ag_server, schema):
        self.ag_server = ag_server
        self.schema = schema
        self.ix = None

    def create_index(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        self.ix = index.create_in(dir_name, self.schema)
    
    def add_document(self):
        if self.ix:
            doc = self.ag_server.get_all_triples()
            writer = self.ix.writer()
            for i in doc:
                if i["p"] == "comment":
                    writer.add_document(title=i["s"], content=i["o"],
                            path=u"/a")
            writer.commit()   
        else:
            print("Create index or open index first !")

    def display_match(self, search_word):
        if self.ix:
            with self.ix.searcher() as searcher:
                query = MultifieldParser(["title", "content"], self.ix.schema).parse(search_word)
                results = searcher.search(query, terms=True)
                if not results:
                    qp = qparser.QueryParser("title", self.ix.schema)
                    q = qp.parse(search_word)
                    with self.ix.searcher() as s:
                        corrected = s.correct_query(q, search_word)
                        if corrected.query != q:
                            user_input = input("Did you mean '{0}': ".format(corrected.string))
                            if user_input.lower() == "yes":
                                self.display_match(corrected.string)
                            else: 
                                print("Wrong type!")
                else:
                    for r in results:
                        print (r, r.score)
                        #Is it matched?
                        if results.has_matched_terms():
                            #How many words are matched?
                            print(results.matched_terms())
            
                    #What terms are matched in each round?
                if results:
                    print ("matched terms")
                    for hit in results:
                        print(hit.matched_terms())
               
        else:
            print("Create index or open index first !")

    def open_index(self, dir_name):
        self.ix = index.open_dir(dir_name)



  




