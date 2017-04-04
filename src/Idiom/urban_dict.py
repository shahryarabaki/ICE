# -*- coding: utf-8 -*-

"""
Created on Thu Jul 24, 2014
@author: Vasanthi Vuppuluri
Last Modified on: August 4, 2014
"""

"""
PURPOSE:
--------
- To obtain definitions from online dictionaries using the mechanize module - In this case, definitions are from http://www.urbandictionary.com/
- urbandict module is to be installed first,  sudo pip install urbandict
- This script can't be used when we need to extract definitions of a word based on it's POS. word_nik.py can be used for that purpose along with wordnet_definitions.py

"""

import urbandict, unicodedata, os

def urban_dict(word, debug):
	_word = word
	_debug = debug

	try:
		result = urbandict.define(_word)

		list_of_definitions = [] # A list to store all the definitions returned by online dictionary 'UrbanDictionary'
		for i in result:
			i = i['def'].strip('\n')
			i = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			list_of_definitions.append(i) # We strip all '\n' from the definitions before appending them to the list

		if(debug == '--debug'):
			print("Definitions from UrbanDictionary: ")
			print('\n', result, type(result), len(result), '\n')
			print('List of definitions:\n%s\nTotal number of definitions:%d\n' %(list_of_definitions, len(list_of_definitions)))

		if (len(list_of_definitions) == 0):
			return 0
		else:
			return list_of_definitions
	except Exception as e:
		print("Exception raised in Urban dictionary!!\n", e)
		return 0

#urban_dict("hot potato", "--debug")

def main_block():
	print("Enter file name: ")
	input_file = str(input())

	debug = '--debug'
    
	valid_output_file = input_file + '.UrbanDict_VALID'
	if os.path.isfile(valid_output_file):
		os.remove(valid_output_file)
    
	invalid_output_file = input_file + '.UrbanDict_INVALID'
	if os.path.isfile(invalid_output_file):
		os.remove(invalid_output_file)

	if (os.path.isfile(input_file) and (os.path.getsize(input_file) > 0)):
		f = open(input_file, 'r')
		keywords = f.readlines()
		f.close()
		#print keywords
		M = len(keywords)
		for x in range(0,M): 
			keyword = keywords[x]
			keyword1 = keyword
			keyword = keyword.strip('\n')
			print(keyword)
			#tokenized_keyword = nltk.word_tokenize(keyword)
			#pos_tagged_keyword = nltk.pos_tag(tokenized_keyword) # Is a list of pos tagged words from each sentence
			#print pos_tagged_keyword[1]
			defnitions_returned = urban_dict(keyword, debug)
			if (defnitions_returned == 0):
				of = open(invalid_output_file, 'a')
				of.write(keyword1)
				of.close
			else:
				of = open(valid_output_file, 'a')
				of.write(keyword1)
				of.close()

#main_block()