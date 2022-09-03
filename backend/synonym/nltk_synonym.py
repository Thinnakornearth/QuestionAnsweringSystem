'''
Requirements: NLTK installed
NLTK corpus (Wordnet/Popular set) is downloaded
'''

# nltk.download('popular')
#     To download the corpus for nltk (needed for first-time only)
import nltk
from nltk.corpus import wordnet 
#if docker-compose, need to download 
#nltk.download('popular')
    # To download the corpus for nltk (needed for first-time only)

# qword = input("Insert word to query: ")


# for syn in wordnet.synsets(qword):
#     for l in syn.lemmas():
#         synonyms.append(l.name())

# synonyms = list(set(synonyms))
# print("This is the unsorted list : " )


def get_synonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            name = l.name()
            if name not in synonyms:
                if "_" in name:
                    a = name.split("_")
                    word2 = a[len(a)-1].capitalize()
                    name = a[0] + "s" + word2
                elif "-" in name:
                    a = name.split("-")
                    word2 = a[len(a)-1].capitalize()
                    name = a[0] + "s" + word2  
                if name == word:
                    synonyms.insert(0, name)
                else:
                    synonyms.append(name)
    print("Synonyms: ", synonyms)
    return synonyms


def get_noun_syn(kws):
    arr = []
    for i in kws:
        syn_array = get_synonym(i[0])
        for j in syn_array:
            arr.append((j, 'empty'))
    print("Keyword and Synonyms ", arr)
    return arr
    

array = [('management', 0.04491197687864554)]
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
