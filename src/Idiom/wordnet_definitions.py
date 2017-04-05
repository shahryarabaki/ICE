# -*- coding: utf-8 -*-

"""
Created on Wed June 20, 2014
@author: Vasanthi Vuppuluri
Last Modified on: June 23, 2014

"""

"""
PURPOSE:
--------
- Uses WordNet from NLTK corpus to obtain definitions of the words when both the word and it's sense are passed as inputs
- This script is different from definitions.py in a way that, instead of accepting inputs as command line arguments,
	this script takes input as function arguments

"""

import sys, os, nltk
from nltk.corpus import wordnet as wn

def definitions(word, pos, debug):
		word = str(word).lower() # word whose definitions are to be found
		sense = str(pos).upper() # Sense of the word
		debug = str(debug) # Debug option
		
		if(debug == '--debug'):
			print("Using WordNet:")
			print("\nWord: '%s'\nPOS: '%s' " %(word, sense))
		
		words = [] # To store all the definitions into a list
		# Extracting the definitions of a given word from WordNet
		if(sense == 'VERB'):
			syn_sets = wn.synsets(word, pos=wn.VERB)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				print('\tWordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					definitions = synset.definition()
					words.append(definitions)
					if(debug == '--debug'):
						print('  ', definitions)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
						
		elif(sense == 'NOUN'):
			syn_sets = wn.synsets(word, pos=wn.NOUN)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				if (debug == '--debug'):
					print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					definitions = synset.definition()
					words.append(definitions)
					if(debug == '--debug'):
						print('  ', definitions)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
					
		elif(sense == 'ADJ'):
			syn_sets = wn.synsets(word, pos=wn.ADJ)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					definitions = synset.definition()
					words.append(definitions)
					if(debug == '--debug'):
						print('  ', definitions)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
				
		elif(sense == 'ADV'):
			syn_sets = wn.synsets(word, pos=wn.ADV)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					definitions = synset.definition()
					words.append(definitions)
					if(debug == '--debug'):
						print('  ', definitions)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
				
		else:
			print('Choose from one of the following senses: {VERB, NOUN, ADJ, ADV}')

		# The list, 'words' might have duplicates which are to be removed
		words = set(words) # converting list to set
		words = list(words) # converting the set back to list as sets doesnot support indexing
		if (len(words) == 0):
			print("----------------------------------------------------------")
			return 0
		else:
			if(debug == '--debug'):
				print("\nUnique definitions of '%s' are: %d" %(word, len(words)))
				for x in range(0,len(words)):
					print("%d: %s" %(x+1, words[x]))
				print("----------------------------------------------------------")
			return words

# To extract definitions without considering POS 
def definitions_no_pos(word, debug):
	word = str(word).lower() # word whose definitions are to be found
	words = [] # To store all the definitions into a list
		
	syn_sets = wn.synsets(word)
	if(debug == '--debug'):
		print('\nDefinitions from WordNet:')
	if(len(syn_sets) == 0):
		print('WordNet does not have any synsets for the given word!')
		return 0
	else:
		for synset in syn_sets:
			definitions = synset.definition()
			words.append(definitions)
			if(debug == '--debug'):
				print('  ', definitions)
		if(debug == '--debug'):
			print('\nTotal number of definitions returned: ', len(words))
		return words

"""
word = 'ethnic_group'
pos = 'noun'
debug = '--debug'
definitions_no_pos(word, debug)
#"""

def main_block():
	print("Enter file name: ")
	input_file = str(input())

	debug = '--debug'
    
	valid_output_file = input_file + '.WordNet_VALID'
	if os.path.isfile(valid_output_file):
		os.remove(valid_output_file)
    
	invalid_output_file = input_file + '.WordNet_INVALID'
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
			tokenized_keyword = nltk.word_tokenize(keyword)
			pos_tagged_keyword = nltk.pos_tag(tokenized_keyword) # Is a list of pos tagged words from each sentence
			print(pos_tagged_keyword[1])
			defnitions_returned = definitions(keyword, pos_tagged_keyword[1], debug)
			if (defnitions_returned == 0):
				of = open(invalid_output_file, 'a')
				of.write(keyword1)
				of.close
			else:
				of = open(valid_output_file, 'a')
				of.write(keyword1)
				of.close()
#main_block()

"""
To extract synonyms of the same sense for a word from wordnet
"""
def synonyms_wordnet(word, pos, debug):
		word = str(word).lower() # word whose synonyms are to be found
		sense = str(pos).upper() # Sense of the word
		debug = str(debug) # Debug option
		
		if(debug == '--debug'):
			print("Using WordNet for synonyms:")
			print("\nWord: '%s'\nPOS: '%s' " %(word, sense))
		
		words = [] # To store all the synonyms into a list
		# Extracting the definitions of a given word from WordNet
		if(sense == 'VERB'):
			syn_sets = wn.synsets(word, pos=wn.VERB)
			if(debug == '--debug'):
				print('\nsynonyms from WordNet:')
			if(len(syn_sets) == 0):
				print('\tWordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					for synonyms_lemma in synset.lemmas:
						synonym = synonyms_lemma.name
						if not (synonym in words):
							words.append(synonym)
					#if(debug == '--debug'):
					#	print '  ', definitions
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
						
		elif(sense == 'NOUN'):
			syn_sets = wn.synsets(word, pos=wn.NOUN)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				if (debug == '--debug'):
					print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					for synonyms_lemma in synset.lemmas:
						synonym = synonyms_lemma.name
						if not (synonym in words):
							words.append(synonym)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
					
		elif(sense == 'ADJ'):
			syn_sets = wn.synsets(word, pos=wn.ADJ)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					for synonyms_lemma in synset.lemmas:
						synonym = synonyms_lemma.name
						if not (synonym in words):
							words.append(synonym)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
				
		elif(sense == 'ADV'):
			syn_sets = wn.synsets(word, pos=wn.ADV)
			if(debug == '--debug'):
				print('\nDefinitions from WordNet:')
			if(len(syn_sets) == 0):
				print('WordNet does not have any synsets for the given word and sense!')
			else:
				for synset in syn_sets:
					for synonyms_lemma in synset.lemmas:
						synonym = synonyms_lemma.name
						if not (synonym in words):
							words.append(synonym)
				if(debug == '--debug'):
					print('\nTotal number of definitions returned: ', len(words))
				
		else:
			print('Choose from one of the following senses: {VERB, NOUN, ADJ, ADV}')

		# The list, 'words' might have duplicates which are to be removed
		#words = set(words) # converting list to set
		#words = list(words) # converting the set back to list as sets doesnot support indexing
		if (len(words) == 0):
			print("----------------------------------------------------------")
			return words
		else:
			if(debug == '--debug'):
				print("\nUnique definitions of '%s' are: %d" %(word, len(words)))
				for x in range(0,len(words)):
					print("%d: %s" %(x+1, words[x]))
				print("----------------------------------------------------------")
			return words
#synonyms_wordnet('went', 'verb', '--debug')