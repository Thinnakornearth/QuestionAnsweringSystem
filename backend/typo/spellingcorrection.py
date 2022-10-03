from textblob import TextBlob
from textblob.en import Spelling        
import re
import os


def fix_typo(word):
	textToLower = ""
	with open(f"{os.getcwd()}/typo/dranpto+en-spelling.txt","r",encoding="utf-8") as f2:           # Open our source file

		text = f2.read()                                  # Read the file                 
		textToLower = text.lower()                        # Lower all the capital letters

	words = re.findall("[a-z]+", textToLower)             # Find all the words and place them into a list    
	oneString = " ".join(words) 

	pathToFile = "train2.txt"                              # The path we want to store our stats file at
	spelling2 = Spelling(path = pathToFile)                # Connect the path to the Spelling object
	spelling2.train(oneString, pathToFile)                 # Train

	##################
	print('textblob + trained text:')
	words = word.split()
	corrected = ""
	for i in words :
		corrected = corrected +" "+ spelling2.suggest(i)[0][0] # Spell checking word by word
	newWord = corrected[1:]
	print(newWord)

	return newWord

