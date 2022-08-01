'''
Requirements: NLTK installed
NLTK corpus (Wordnet/Popular set) is downloaded
'''

# nltk.download('popular')
#     To download the corpus for nltk (needed for first-time only)
import nltk
from nltk.corpus import wordnet
from torch import symeig

qword = input("Insert word to query: ")


# for syn in wordnet.synsets(qword):
#     for l in syn.lemmas():
#         synonyms.append(l.name())

# synonyms = list(set(synonyms))
# print("This is the unsorted list : " )


def get_synonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() not in synonyms:
                if l.name() == word:
                    synonyms.insert(0, l.name())
                else:
                    synonyms.append(l.name())
    print(synonyms)
    return synonyms


get_synonym(qword)

# ''' ---- This code below is to turn the common words text file to list ---- '''
# common_words = []
# with open(r'words.txt') as common_words_txt:
#     for line in common_words_txt:
#         line = line.strip()
#         common_words.append(line)
# ''' ------------------------------------------------------------------ '''

# for i in synonyms:
#     if i in common_words:
#         synonyms.remove(i)
#         synonyms.insert(0,i)

# print("This is the sorted list : " )
# print(synonyms)
