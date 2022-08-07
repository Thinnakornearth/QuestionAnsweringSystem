import yake
import spacy   
from spacy.matcher import Matcher
from spacy.util import filter_spans

def extract_verb(sentences):
    nlp = spacy.load('en_core_web_sm') 
    sentence = sentences
    pattern = [{'POS': 'VERB', 'OP': '?'},
            {'POS': 'ADV', 'OP': '*'},
            {'POS': 'AUX', 'OP': '*'},
            {'POS': 'VERB', 'OP': '+'}]
    # Create Matcher
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", [pattern])
    doc = nlp(sentence) 
    # Find match
    matches = matcher(doc)
    #Split each keyword in a list (array)
    spans = [doc[start:end] for _, start, end in matches]
    print ("Verbs", filter_spans(spans))  
    return spans



def extract_kw(keyword):
    kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)
    keywords = kw_extractor.extract_keywords(keyword)
    return keywords

