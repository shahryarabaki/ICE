# -*- coding: utf-8 -*-

"""
Created on Tue July 29, 2014
@author: Vasanthi Vuppuluri
Last Modified on: August 5, 2014

"""

"""
PURPOSE:
--------
- Extracts MWEs given collocations
- Steps:
	 - POS tags the definitions
- Requirements:
	nltk, snowballstemmer, itertools, copy, re, unicodedata, BeautifulSoup, mechanize
	use nltk.download() to install all corpora and collections
"""
import logging
from collections import defaultdict
import nltk, snowballstemmer, itertools, copy, re, os, unicodedata#, Collocations_NVAA #, pos_collocations
from ..pos_tagger import POS_tag_cleaner
from .wordnet_definitions import definitions, definitions_no_pos
from .internet_def import internet_search
from .definitions_mechanize import definitions_m
from .word_nik import wordnik_def, wordnik_def_no_POS # wordnik_def: Takes as input, (word, POS, debug), wordnik_def_no_POS: takes as input (word, debug)
from .urban_dict import urban_dict # Takes as input, (word, debug)
from .gcide_xml import extract_definitions as gcide_definitions # import extract_definitions # Webster dictionary definitions form gcide_xml.py

def mwe(collocations, intersection_union = "I", debug = "", output_file = None, Bing_API_key = "U7QYkY2HPcaOWIw0CTJnJhxkmv/3FabDtLKFx1CLSk8"):
	debug = debug # debug option
	key = Bing_API_key # Bing search API key

	intersection_union_map = {
		"Intersection": "I", 
		"Union": "U",
		"Both": "B",
		"U": "U", 
		"I": "I",
		"B": "B"}

	if intersection_union not in intersection_union_map:
		raise Exception("Wrong Option")

	option = intersection_union_map[intersection_union] # U | I | B

	#Set up output file
	if output_file:
		output_file_Union = str(output_file) + "_Union" # To store MWEs
		if os.path.isfile(output_file_Union): # Checks and deletes the output file if it already exists
			os.remove(output_file_Union)
		output_file_Intersection = str(output_file) + "_Intersection" # To store MWEs
		if os.path.isfile(output_file_Intersection): # Checks and deletes the output file if it already exists
			os.remove(output_file_Intersection)
		output_file_not_MWEs = str(output_file) + "_not_MWEs" # To store Collocations that are not MWEs
		if os.path.isfile(output_file_not_MWEs): # Checks and deletes the output file if it already exists
			os.remove(output_file_not_MWEs)

	webster_dictionary = gcide_definitions() # Webster dictionary definitions

	l = len(collocations) # Number of collocations in the list
	if (debug == '--debug'):
		print("Total number of collocations:%d\nCollocations:\n%s" %(l, collocations))

	counter = 0 # To count number of collocations that were declared as MWEs
	counter_union = 0 # When 'Both' option is used, to count the number of collocations that were declared as MWEs using Union
	counter_intersection = 0 # When 'Both' option is used, to count the number of collocations that were declared as MWEs using Intersection
	all_definitions_returned = defaultdict(list) # A dictionary to store the list of definitions of each of the word after they are returned. This is to avoid un-necessary 
								  # calls for obtaining definitions of the words whose definitions are already obtained

	intersection_result = []
	union_result = []
	both_result = []
	none_result = []

	for x in range(0,l):
		if (debug == '--debug'):
			print(x+1)
		# Here collocations[x] is the collocation
		word_with_pos = collocations[x].split() # Obtaining individual words from the collocation, collocations[x]
		w = [] # A list to store the individial words from the collocation
		pos_of_word = [] # A list to store the pos tags of each word from the collocation
		for i in word_with_pos:
			i = i.replace('_', ' ')
			w.append(i.split()[0])
			pos_of_word.append(i.split()[1])
		if (debug == '--debug'):
			print("List of words in the collocation '%s':%s\nList of POS tags in the collocation '%s':%s" %(collocations[x], w, collocations[x], pos_of_word))
		
		# For WordNet to recognize 'red tape' as one word, space is to be replaced with an underscore
		#c = collocations[x].replace('', '_')
		c = POS_tag_cleaner(collocations[x]) # Removes POS tags attached to each word in the collocation
		c_mechanize = c
		c_wordnet = c_mechanize.replace(' ', '_') # Converts it to wordnet understandable form
		print(c_wordnet)
		c_mechanize = c_mechanize.replace(' ', '+')
		#print c, c_mechanize, c_wordnet

		# extracting POS tagging the collocation
		c1 = nltk.word_tokenize(c)
		tag = nltk.pos_tag(c1)
		tag = tag[0][1]

		if('NN' in tag):
			tag = 'noun'
		elif('VB' in tag):
			tag = 'verb'
		elif('ADJ' in tag):
			tag = 'adj'
		elif('ADV' in tag):
			tag = 'adv'
		else:
			tag = 'noun'

		if (debug == '--debug'):
			print("\n---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---")
			print("---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---\n")

		if c in all_definitions_returned: # Checks if the meanings of the collocation are already obtained
			def_c = all_definitions_returned[c]
			if(def_c == 0): # If no definitions were obtained the previous time same word a=was searched for, the process moves on to the next word in the list
				continue
		else:
			# Searches for definitions of the collocation in the WordNet dictionary
			#def_c = definitions(c_wordnet, tag, debug)
			def_c = definitions_no_pos(c_wordnet, debug) # To extract definitions from WordNet dictionary without considering thr POS of the collocation
			
			if ((def_c == 0) or (len(def_c) == 0)): # i.e. if WordNet does not have any definitions
				#def_c = wordnik_def(c, tag, debug)
				wordnik_def_no_POS(c, debug) # To extract definitions from WordNik online dictionary without considering thr POS of the collocation

				if ((def_c == 0) or (len(def_c) == 0)):
					(pos_c, def_c) = definitions_m(c_mechanize, debug)
					if not ((len(def_c) == 0) and (len(pos_c) == 0)):
						list_of_collocation_definitions = []
						for _x in range(0, len(pos_c)):
							list_x = []
							list_x = def_c[pos_c[_x]]
							for i in list_x:
								# list elements here are in unicode format.Converting them to strings first
								i = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
								list_of_collocation_definitions.append(i)
						def_c = list_of_collocation_definitions
					else:			
						if ((def_c == 0) or (len(def_c) == 0)):
							#def_c = urban_dict(c, debug)
							def_c = 0 # Purposefully ignoring the definitions returned by Urban Dictionary to improve precision

							if ((def_c == 0) or (len(def_c) == 0)): # i.e. if definitions_mechanize.py does not have any definitions
								def_c = internet_search(debug, c_mechanize, key) # searches internet using Bing to fetch the definitions
				
								if ((def_c == 0) or (len(def_c) == 0)): # i.e. if even Bing does not return any definitions
									if (debug == '--debug'):
										print('No definitions found for the collcation "%s"!!' %(collocations[x].upper()))
										print('\nMoving to next collocation in the list ...\n') # Script moves to next available collocation as no definitions are returned
										all_definitions_returned[c].append(0)
										out_file_not_MWEs = open(output_file_not_MWEs, 'a')
										out_file_not_MWEs.write(collocations[x] + '\n')
										out_file_not_MWEs.close()
									continue # to continue to next iteration, i.e. next collocation from the collocations[]
								else:
									all_definitions_returned[c].append(def_c)
							else:
								all_definitions_returned[c].append(def_c)
						else:
							all_definitions_returned[c].append(def_c)
				else:
					all_definitions_returned[c].append(def_c)
			else:
				all_definitions_returned[c].append(def_c)

		if (debug == '--debug'):
			print("Definitions of collocation '%s':" %(c))
			print(def_c)

		#tags = [] # To store the pos tags of the individual words
		lists = [] # To store list names
		lists_new = []

		for y in range(0,len(w)): # POS tags the individual words of collocation
			
			if (debug == '--debug'):
				print("POS of the word '%s' in the input file: %s" %(w[y], pos_of_word[y]))
			
			l = 'list' + str(y + 1) # Creates a list for each word present in the collocation
			lists.append(l)
			lists_new.append(l)

		# Following are the POS tags we are concerned with
		valid_tags = []
		valid_tags.append('NN')
		valid_tags.append('VB')
		valid_tags.append('ADV')
		valid_tags.append('ADJ')		

		for z in range(0,len(w)):
			tag = pos_of_word[z]
			if (debug == '--debug'):
				print(tag)
			if('NN' in tag):
				tag = 'noun'
			elif('VB' in tag):
				tag = 'verb'
			elif('ADJ' in tag):
				tag = 'adj'
			elif('RB' in tag):
				tag = 'adv'
			else:
				tag = 'null'
				#lists[z] = [] # If the POS tag is not a valid one, no defiitions are obtained for that word
				if (debug == '--debug'):
					print("The POS of the word is not amongst {Noun, Verb, Adjective, Adverb}")###\nSo no definitions are obtained!!"
					###print "Definitions of word", w[z], ":", lists[z]
				###continue # And we move on to the next word in the list of words, 'w'
			
			word_with_pos = w[z] + '_' + pos_of_word[z] # Word along with its POS tag
			if(word_with_pos in all_definitions_returned):
				lists[z] = all_definitions_returned[word_with_pos]
			else:	
				# definitions for each word from WordNet are obtained
				lists[z] = definitions(w[z], tag, debug) 
				if((lists[z] == 0) or (len(lists[z]) == 0)): 
					lists[z] = webster_dictionary[w[z]]
					if((lists[z] == 0) or (len(lists[z]) == 0)): 
						print("No definitions in Webster dictionary!!")
						if (tag == "null"):
							lists[z] = wordnik_def_no_POS(w[z], debug)
							print("WordNik without POS tag info", lists[z])
						else:
							lists[z] = wordnik_def(w[z], tag, debug)
							print("WordNik with POS tag info", lists[z])
						if((lists[z] == 0) or (len(lists[z]) == 0)): # If WordNik does not have any definition, online dictionary is used 
							print("I'm HERE!! -  A")
							(pos_definitions, lists[z]) = definitions_m(w[z], debug)
							if(len(lists[z]) > 0):
								list_of_word_definitions = []
								list_x = []
								list_x = lists[z][tag]
								for i in list_x:
									# list elements here are in unicode format.Converting them to strings first
									i = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
									list_of_word_definitions.append(i)
								lists[z] = list_of_word_definitions
								print("I'm HERE!! -  B")
						
							elif(len(lists[z]) == 0):
								print("I'm HERE!! -  C")
								print("No definitions from dictionary.reference.com!!")
								lists[z] = urban_dict(w[z], debug)
							
								if(lists[z] == 0): # If online dictionaries does not have any definition, Bing is used
									print("No definitions from Urban dictionary!!")
									lists[z] = internet_search(debug, w[z], key)
								
									if(lists[z] == 0):
										if (debug == '--debug'):
											print('No definitions found!!')
										lists[z] = [] # If no definitions are returned, assign an empty list
										all_definitions_returned[word_with_pos].append(lists[z])
									else:
										all_definitions_returned[word_with_pos].append(lists[z])
								else:
									all_definitions_returned[word_with_pos].append(lists[z])
							else:
								all_definitions_returned[word_with_pos].append(lists[z])
						else:
							all_definitions_returned[word_with_pos].append(lists[z])
					else:
						all_definitions_returned[word_with_pos].append(lists[z])
						#print "Definitions from Webster dictionary:", lists[z]
				else:
					all_definitions_returned[word_with_pos].append(lists[z])

			if (debug == '--debug'):
				print("Definitions of word %s:" %(w[z]))
				print(lists[z])

		if (debug == '--debug'):
			print('=================================================================')
			print(def_c)
			print('=================================================================')
			for i in lists:
				print(i)
				print('=================================================================')

		def_c_new = [] # A new list to store the definions of the collocation from "def_c"
		for i in def_c:
			definition = i
			def_c_new.append(c + " means " + str(definition))
		
		for j in range(0,len(lists)):
			individual_word = w[j]
			word_list = copy.deepcopy(lists[j])
			lists_new[j] = []
			for k in range(0, len(word_list)):
				definition = str(word_list[k])
				lists_new[j].append(individual_word + " means " + str(definition))

		if (debug == '--debug'):
			print('=================================================================\n\n')
			print('New lists are as follows:')
			print('=================================================================\n')
			print(def_c_new)
			print('=================================================================')
			for i in lists_new:
				print(i)
				print('=================================================================')

		# Stemming the definitions of the n-gram
		stemmed_def_c_new = []
		for a in def_c_new:
			tokens = nltk.word_tokenize(a)
			pos_tags = nltk.pos_tag(tokens)
			if (debug == '--debug'):
				print("\n\n", pos_tags)
				
			n_in_ngram = len(w) # Gives the number of words present in the n-gram
			# Ignoring n+1 words from the beginning leaves us with the initial definiion which is now POS tagged
			# pos_tags[(n_in_ngram + 1):] = To consider only the list elements that correspond to actual defintion
			reconstructing_definition = '' # String used to construct the definition from stemmed words

			for b in range(0, (len(pos_tags) - n_in_ngram - 1)):
				pos_of_word_in_definition = pos_tags[n_in_ngram + 1 + b][1]
				if(('NN' in pos_of_word_in_definition) or ('VB' in pos_of_word_in_definition) or ('ADV' in pos_of_word_in_definition) or ('ADJ' in pos_of_word_in_definition)):
					Stemmer = snowballstemmer.stemmer('english')
					stemmed_word = str(Stemmer.stemWord(pos_tags[n_in_ngram + 1 + b][0]))
					reconstructing_definition = reconstructing_definition + stemmed_word + ' '

					if (debug == '--debug'):
						print('Stemming', pos_tags[n_in_ngram + 1 + b], ':', pos_tags[n_in_ngram + 1 + b][0], '-->', Stemmer.stemWord(pos_tags[n_in_ngram + 1 + b][0]))
				
			stemmed_def_c_new.append(reconstructing_definition) # Stemmeddefinitions are appended to the list
			if (debug == '--debug'):
				print("Stemmed definitions of the collocation '%s' are: \n\t%s" %(collocations[x], stemmed_def_c_new))
			
		# Stemming the definitions of the individual words present in the n-gram
		# Definitions are stored into a list of lists, named lists_new[]
		# Each list corresponds to the list of definitions of each word in the n-gram
		stemmed_list_of_lists = [] # To store the stemmed definions of each of the individual word
		for a_list in lists_new:
			list_of_definitions = [] # To store the reconstructed definitions as elements of the list
			for a_definion in a_list:
				tokens = nltk.word_tokenize(a_definion)
				pos_tags = nltk.pos_tag(tokens)
				if (debug == '--debug'):
					print("\n\n", pos_tags)
		
				reconstructing_definition = ''
				
				for b in range(0, (len(pos_tags) - 2)):
					# Here 2 is subtracted from the length of the pos_tags list because, we have to ignore the first two words which does not correspond to the actual definion
					pos_of_word_in_definition = pos_tags[2 + b]
					if(('NN' in pos_of_word_in_definition) or ('VB' in pos_of_word_in_definition) or ('ADV' in pos_of_word_in_definition) or ('ADJ' in pos_of_word_in_definition)):
						Stemmer = snowballstemmer.stemmer('english')
						stemmed_word = str(Stemmer.stemWord(pos_tags[2 + b][0]))
						reconstructing_definition = reconstructing_definition + stemmed_word + ' '

						if (debug == '--debug'):
							print('Stemming: ', pos_tags[2 + b], ':', pos_tags[2 + b][0], '-->', str(Stemmer.stemWord(pos_tags[2 + b][0])))
				list_of_definitions.append(reconstructing_definition)

			if (len(list_of_definitions) > 0): # To append only non-empty list of definitions to the stemmed list of lists as
				# this is used in the next steps to obtain combinations of stemmed definitions and any empty lists creates 
				# no combinations at all when using itertools to obtain the combinations
				stemmed_list_of_lists.append(list_of_definitions) # Saving the list of definitions as elements of the list, 'stemmed_list_of_lists'
		
		# "stemmed_def_c_new" is the list of definions of the collocation that are stemmed
		# "stemmed_list_of_lists" is the list of lists, with each list element being a list of stemmed definitions of each word in the collocation
		#print stemmed_list_of_lists, stemmed_def_c_new

		# ---------------------------------------------------------------------------------------------------
		# Obtaining all possible combinations of the stemmed definitions
		# 		- Obtain all the unique words from each combinations
		# 		- check if the collocation definition is present in the unique words obtained
		# Number of possible combinations = product of number of definions for each word in the collcation
		# The 'itertools' package helps to obtain all possible combinations of the elements in the list of lists
		# combinations of individual meanings from list of lists = 'definition_combination_list'
		
		definition_combination_list = list(itertools.product(*stemmed_list_of_lists))
		
		if (debug == '--debug'):
			print("combinations of definitions of each word in the collocation:")
			print(definition_combination_list)

		# Each of the definition combinations are tuples in a list
		# Converting the tuples to be elements in a list
		recreated_def_combination_list = []
		for a_tuple in definition_combination_list:
			recreated_combination = ""
			for tuple_element in a_tuple:
				recreated_combination = recreated_combination + tuple_element + " "
			recreated_def_combination_list.append(recreated_combination)
		
		if (debug == '--debug'):
			print("Recreated combinations of definitions:")
			print(recreated_def_combination_list)

		# converting string of list elements to a list of words
		new_recreated_def_combination_list = []
		for each_definition in recreated_def_combination_list:
			new_recreated_def_combination_list.append(each_definition.split())
		#print new_recreated_def_combination_list

		# Subtracting each of the combination from the stemmed definitions of the collocation
		# And creating a new list converting the string of definitions to list of words in each definition
		new_stemmed_def_c_new = []
		for collocation_def in stemmed_def_c_new:
			new_stemmed_def_c_new.append(collocation_def.split())

		# Each of the definition combination is subtracted from the definitions of the collocation
		# Subtraction output is saved to a list
		subtraction_results = []
		for each_of_collocation_definition in new_stemmed_def_c_new:
			
			for each_of_word_definition in new_recreated_def_combination_list:
				copy_of_collocation_definition = copy.deepcopy(each_of_collocation_definition) # copy this, do not use the reference
				#copy_of_collocation_definition = set(copy_of_collocation_definition)
				
				"""
				# Method I
				# Using set subtractions to subtract the comnination of definitions from the definition of the collocation
				"""
				#'''
				subtraction_output = set(copy_of_collocation_definition) - set(each_of_word_definition)
				#print subtraction_output
				subtraction_results.append(subtraction_output)
				#'''

				"""
				# METHOD II
				# Using lists
				# Searches for individual words in the combination in the collocation definition,
				# which is a list of words and removes the words from the list
				"""
				'''
				for each_of_word in each_of_word_definition:
					if(each_of_word in copy_of_collocation_definition):
						copy_of_collocation_definition.remove(each_of_word)
				
				if(len(copy_of_collocation_definition) == 0):
					print "Union of subtraction results is an empty string"
				else:
					subtraction_results.append(copy_of_collocation_definition)
				#'''

		
		try:
			d = defaultdict(int) 
			for results in subtraction_results:	
				for a_word in results:
					d[a_word] += 1 # 'd' stores the count of each of the word
		except:
			print("Exception raised!! while trying to count the number of occurrances of each word in the subtraction result")

		if (debug == '--debug'):
			print('\n', type(d), '-->', len(d), 'unique words in the combination -->', d, '--> combinations:', len(subtraction_results))
		
		# d.items() ia a list of items in 'd'
		d_list = copy.deepcopy(list(d.items()))
		d_list_counter = [] # A list to store the counter values
		for d_list_item in range(0, len(d_list)):
			d_list_counter.append(d_list[d_list_item][1]) # Appends the count value to the d_list_counter list

		if (debug == '--debug'):
			print("\nCount of each word that survived subtraction: ", d, '\n')
		
		if(option == 'U'):
			if (len(subtraction_results) > 0):
				counter = counter + 1
				union_result.append(collocations[x])

				if output_file:
					out_file = open(output_file_Union, 'a')
					out_file.write(collocations[x] + '\n')
					out_file.close()

				if (debug == '--debug'):
					print("Subtraction result is non empty!!")
					print('collocation "%s" is a MWE' %(collocations[x].upper()))
			else:
				if (debug == '--debug'):
					print("None of the words survived subtraction!!")
					print('collocation "%s" is a not a MWE' %(collocations[x].upper()))
		elif (option == 'I'):
			match = 0 # To count the number of words whose counter matched the number of combinations
			for counter_value in d_list_counter:
				if(counter_value == len(subtraction_results)):
					match = match + 1
			if(match > 0):
				counter = counter + 1
				intersection_result.append(collocations[x])
				if output_file:
					out_file = open(output_file_Intersection, 'a')
					out_file.write(collocations[x] + '\n')
					out_file.close()
				if (debug == '--debug'):
					print("Altest one of the unique words survived all subtractions!")
					print('collocation "%s" is a MWE' %(collocations[x].upper()))
			else:
				if (debug == '--debug'):
					print("None of the unique words in the combinations survived all subtractions!")
					print('collocation "%s" is not a MWE' %(collocations[x].upper()))
		elif (option == 'B'):
			if (debug == '--debug'):
				print("Using 'UNION':")
			if (len(subtraction_results) > 0):
				counter_union = counter_union + 1
				union_result.append(collocations[x])
				if output_file:
					out_file = open(output_file_Union, 'a')
					out_file.write(collocations[x] + '\n')
					out_file.close()
				if (debug == '--debug'):
					print("Subtraction result is non empty!!")
					print('collocation "%s" is a MWE' %(collocations[x].upper()))
					print('\n---------------------------------------------------------------')
					print("\nUsing INTERSECTION:")
				match = 0 # To count the number of words whose counter matched the number of combinations
				for counter_value in d_list_counter:
					if(counter_value == len(subtraction_results)):
						match = match + 1
				if(match > 0):
					counter_intersection = counter_intersection + 1
					if output_file:
						out_file = open(output_file_Intersection, 'a')
						out_file.write(collocations[x] + '\n')
						out_file.close()
					intersection_result.append(collocations[x])
					if (debug == '--debug'):
						print("Altest one of the unique words survived all subtractions!")
						print('collocation "%s" is a MWE' %(collocations[x].upper()))
				else:
					if (debug == '--debug'):
						print("None of the unique words in the combinations survived all subtractions!")
						print('collocation "%s" is not a MWE' %(collocations[x].upper()))

			else:
				none_result.append(collocations[x])
				if output_file:
					out_file_not_MWEs = open(output_file_not_MWEs, 'a')
					out_file_not_MWEs.write(collocations[x] + '\n')
					out_file_not_MWEs.close()
				if (debug == '--debug'):
					print("None of the words survived subtraction!!")
					print('collocation "%s" is a not a MWE' %(collocations[x].upper()))
			

	if ((option == 'I') or (option == 'U')):
		if (debug == '--debug'):
			print("\nTotal number of collocations that were MWEs:%d" %counter)

		if option == 'I':
			return intersection_result
		else:
			return union_result

	elif (option == 'B'):
		return (intersection_result, union_result)
		if (debug == '--debug'):
			print("\nTotal number of collocations that were MWEs - UNION:%d" %counter_union)
			print("Total number of collocations that were MWEs - INTERSECTION:%d" %counter_intersection)

"""
EXECUTION STEPS
"""		

if __name__ == '__main__':

	debug = '--debug'
	#key = "i8nYpjbawVX5WZmqJEWtuXe2AFTxG6mpVijVBo0iAIM"   
	#key = "z7593AMcSfv+whbs6Q3xaTfu/WrCI2PH/MiLg2vxuNU" # - exhausted
	#'RIhkTLQPGqVbob64zrh2Ydi67qriZaEoa1Gk+20s2Rk' - exhausted
	#key = "6xDZfk2F1YtJcT/mZJCK+msvW/KJCsg6N4OOBbmDHwk" 
	#key = "GhxpOGP6TbrRsI1i9wxj6KLbKoT9LY1NCv7PUnCYcwA"
	#key = "xgQtVAZSi7Tgvrqbac1Aqal6q3ymEgm8tAiKMJ3ckWU" #  - "keyacount5.mwe@outlook.com"
	#key = "noLzIF83elZ0IySjp9aYUm/jWrB+VCNbpEgJKLHbd+A" # username: keyacount6.mwe@outlook.com; pwd: acc6acc6
	#key = "3zyWOojD+cT5Zaon+Ga0n6YnUyZpbVjw9UsLHFaITd0" # username: keyacount7.mwe@outlook.com; pwd: acc7acc7
	#key = " GDhSKWrDt6o8RV0z7IP+G5ZbvAIEuh6Woz9cKQL0H3s" # username: keyacount8.mwe@outlook.com; pwd: acc8acc8
	#key = "Nv4YviOB0LSss+sMHzO2WuhMUZEtX1BYucJvurzjBXw" # username: keyacount10.mwe@outlook.com; pwd: acc10acc10
	#key = "5vHXAhyyalf7F9mpVDhlhMwwIupAHPWyqwGchhyQ4Ho" # key.acc20@outlook.com; mwe20mwe20
	#key = "GOHE1J+fE1uGN+QDprNGWtPq+7YGY9NUj1dpYu8nhbw" # key.acc21@outlook.com; mwe21mwe212
	#key = "AEAwFPUdMa5J3F4O2VP9B0uMFEgtVwTKLshYKpzReos" # key.acc15@outlook.com; mwe15mwe15
	key = "U7QYkY2HPcaOWIw0CTJnJhxkmv/3FabDtLKFx1CLSk8"

	"""
	TEST - 1
	"""
	"""
	print "Input file:"
	input_file = raw_input()
	opening_file = open(input_file, 'r')
	n_grams_from_file = opening_file.readlines()
	opening_file.close()

	collocations = []
	for n_gram in n_grams_from_file:
		collocations.append(n_gram.strip('\n'))
	#"""

	"""
	TEST - 2
	"""
	"""
	collocations = []
	#collocations.append("CROTON TIGLIUM")
	#collocations.append('top_JJ priority_NN ')
	#collocations.append('hot_JJ potato_NN ')
	#collocations.append('red tape')
	#collocations.append('credit rating')
	#collocations.append('black hole')
	collocations.append('ethnic_JJ group_NN ')
	#collocations.append('kick_NN the_DT bucket_NN ') # Dictionary.com doesn't work for idioms
	#"""

	print("Intersection, union or both? Select from (I | U | B)")
	intersection_union = input().upper()
	if (len(intersection_union) == 1):
		debug = "--debug"
		if (intersection_union == 'I' or intersection_union == 'U' or intersection_union == 'B'):

			"""
			FOR CICLing 2015
			"""

			"""
			idioms_with_definitions = open(raw_input()).readlines()
			print len(idioms_with_definitions)
			idiom_definitions = open(raw_input()).readlines()
			print len(idiom_definitions)
			#"""


			#(collocations, output_file) = Collocations_NVAA.main() # calls the main function of pos_collocations.py
			#"""
			
			infile = input("Enter input file name: ")
			ifile = open(infile, 'r')
			collocations_1 = ifile.readlines()
			ifile.close()

			collocations = []
			for i in collocations_1:
				collocations.append(i.strip('\n')+' ')

			
			output_file = input("Output file name: ")
			#"""
			"""	
			#collocations = ['called_VBN auric_JJ ', 'Ideal_NNP observer_NN ', 'equity_NN investment_NN ', 'model_NN facilitates_NNS ', 'studio_NN album_NN ', 'cold_JJ air_NN ', 'Full_NNP Draw_NNP ', 'Use_NN Conversion_NN ', 'nonnegative_JJ real_JJ ', 'Tennis_NNP Racquets_NNPS ', 'fava_NN beans_NNS ', 'many_JJ organs_NNS ', 'encoded_VBD messages_NNS ', 'first_JJ example_NN ', 'Grapple_NNP Gun_NNP ', 'Canadian_NNP Navy_NNP ', 'different_JJ sources_NNS ', 'Euphorbiaceae_NNP family_NN ', 'Canadian_JJ rock_NN ', 'create_VB applications_NNS ', 'paste_JJ porcelain_NN ', 'non_NN linear_NN ', 'inputs_NNS features_NNS ', 'Central_NNP America_NNP ', 'John_NNP Wheeler_NNP ', 'circuits_NNS representing_VBG ', '11th_JJ studio_NN ', 'Mortar_NNP headds_VBZ ', 'Harpoon_NNP missiles_NNS ', 'nonlinear_JJ electronic_JJ ', 'broad_JJ beans_NNS ', 'hard_RB paste_JJ ', 'device_NN servers_NNS ', 'Purging_NNP Croton_NNP ', 'called_VBN cryptanalysis_NN ', 'set_NN theory_NN ', 'including_VBG food_NN ', 'player_NN seeking_VBG ', 'remote_VBP interface_NN ', 'single_JJ instructions_NNS ', 'practical_JJ guides_NNS ', 'David_NNP Toska_NNP ', 'distinguish_VB conventional_JJ ', 'phone_NN card_NN ', 'muscular_JJ coat_NN ', 'using_VBG extremely_RB ', 'roller_NN caterpillars_NNS ', 'Kalmyk_NNP Steppe_NNP ', 'hair_JJ loss_NN ', 'Magnetic_NNP Headphones_NNP ', 'Navy_NNP carries_VBZ ', 'nuclear_JJ fusion_NN ', 'inference_NN system_NN ', 'film_NN camera_NN ', 'Halifax_NNP class_NN ', 'soft_JJ vacuum_NN ', 'vice_NN versa_NN ', 'fast_JJ food_NN ', 'deliver_VB control_NN ', 'EU_NNP policy_NN ', 'megalithic_JJ monuments_NNS ', 'conversion_NN rates_NNS ', 'Medway_NNP Megaliths_NNP ', 'sigma_NN bond_NN ', 'ground_NN breaking_VBG ', 'root_NN music_NN ', 'oxygen_NN gas_NN ', 'narrative_JJ verse_NN ', 'fuzzy_NN inference_NN ', 'software_NN necessary_JJ ', 'breaking_VBG ground_NN ', 'gourami_NN family_NN ', 'Eisenstein_NNP integer_NN ', 'aristocratic_JJ warriors_NNS ', 'Bulk_NNP SMS_NNP ', 'Advanced_NNP Physics_NNP ', 'achieve_VB nuclear_JJ ', 'Post_NNP code_VBP ', 'formal_JJ style_NN ', 'massive_JJ amounts_NNS ', 'agent_NN used_VBN ', 'large_JJ nocturnal_JJ ', 'electronic_JJ amplifier_NN ', 'SMS_NNP service_NN ', 'storage_NN tank_NN ', 'retrieve_JJ analyze_NN ', 'kids_NNS meal_VBP ', 'camera_NN refers_NNS ', 'ependymal_JJ cells_NNS ', 'share_NN ideas_NNS ', 'comic_JJ duo_NN ', 'fuzzy_NN set_NN ', 'Tree_NNP stands_VBZ ', 'chemical_JJ compound_NN ', 'collective_JJ name_NN ', 'perceptual_JJ system_NN ', 'real_JJ numbers_NNS ', 'industries_NNS including_VBG ', 'Lucius_NNP Fox_NNP ', 'circuit_NN place_NN ', 'European_JJ nations_NNS ', 'measurable_JJ sets_NNS ', 'Limoges_NNPS France_NNP ', 'other_JJ parts_NNS ', 'ones_NNS fire_VBP ', 'measure_NN space_NN ', 'alkylating_VBG agent_NN ', 'pure_NN alcohol_NN ', 'ecstatic_JJ transcendent_NN ', 'night_NN club_NN ', 'South_NNP East_NNP ', 'positive_JJ operator_NN ', 'space_NN filling_VBG ', 'offensive_JJ penalty_NN ', 'Quantum_NNP foam_NN ', 'cubic_JJ inches_NNS ', 'offered_VBD directly_RB ', 'Pontic_NNP steppe_NN ', 'Force_NNP concentration_NN ', 'combustion_NN engine_NN ', 'dual_JJ gauge_NN ', 'linear_NN device_NN ', 'estimated_VBN savings_NNS ', 'total_JJ mass_NN ', 'underlying_VBG susceptibility_NN ', 'antineoplastic_JJ agent_NN ', 'plant_NN species_NNS ', 'United_NNP States_NNPS ', 'cold_NN front_NN ', 'quantum_NN mechanics_NNS ', 'dividing_NN line_NN ', 'load_NN line_NN ', 'long_RB barrows_VBZ ', 'positive_JJ measure_NN ', 'as_RB double_JJ ', 'Physics_NNP Homework_NNP ', 'reinvestment_NN program_NN ', 'mechanics_NNS devised_VBD ', 'Neolithic_NNP chambered_VBD ', 'Information_NN Literacy_NN ', 'wasp_NN species_NNS ', 'Fall_NNP Semester_NNP ', 'main_JJ goals_NNS ', 'programming_NN language_NN ', 'together_RB compared_VBN ', 'other_JJ artists_NNS ', 'valve_NN amplifier_NN ', 'Center_NNP Opens_NNP ', 'hair_NN follicles_NNS ', 'Wayne_NNP Enterprises_NNP ', 'map_VB inputs_NNS ', 'defined_VBD differently_RB ', 'known_VBN digger_NN ', 'actions_NNS undertaken_VBN ', 'refine_VB metals_NNS ', 'network_NN software_NN ', 'Bronze_NNP Age_NNP ', 'interurban_VBP streetcar_NN ', 'automobile_NN less_NN ', 'lower_JJR valley_NN ', '20th_JJ Century_NNP ', 'bringing_VBG massive_JJ ', 'Early_NNP Neolithic_NNP ', 'provide_VB forums_NNS ', 'underlying_VBG network_NN ', 'Limoges_NNS porcelain_VBP ', 'Leaf_NNP roller_NN ', 'Special_JJ damages_NNS ', 'graphical_JJ analysis_NN ', 'Menkes_NNS syndrome_VBP ', 'Sea_NNP bounded_VBD ', 'cancer_NN treatment_NN ', 'servo_NN motor_NN ', 'dividend_NN reinvestment_NN ', 'Peano_NNP curve_NN ', 'Gold_NNP chloride_VBD ', 'camera_NN designs_NNS ', 'solves_NNS key_JJ ', 'several_JJ low_JJ ', 'breaking_NN encoded_VBD ', 'specialized_VBN software_NN ', 'Nursing_VBG interventions_NNS ', 'preferred_VBN Bulk_NNP ', 'burrowing_NN rodent_NN ', 'Kent_NNP South_NNP ', 'compute_NN engines_NNS ', 'other_JJ camera_NN ', 'added_VBD together_RB ', 'internal_JJ combustion_NN ', 'system_NN FIS_NNP ', 'cylinders_NNS arranged_VBD ', 'live_JJ streaming_NN ', 'key_JJ revocation_NN ', 'electronic_JJ circuits_NNS ', 'chambered_VBD long_RB ', 'Power_NN Windows_VBZ ', 'NEW_NNP Legacy_NNP ', 'more_RBR effective_JJ ', 'policy_NN areas_NNS ', 'defendants_NNS actions_NNS ', 'Risk_NNP management_NN ', 'Sodium_NN alginate_VBP ', 'street_NN railways_NNS ', 'Java_NNP programming_NN ', 'electrocyclic_JJ reaction_NN ', 'high_JJ purity_NN ', 'underlying_VBG company_NN ', 'affinity_NN groups_NNS ', 'occurs_VBZ due_JJ ', 'transition_NN zone_NN ', 'investigating_VBG how_WRB ', 'Eisenstein_NNP prime_NN ', 'false_NN start_VBD ', 'croaking_VBG gourami_NN ', 'air_NN mass_NN ', 'nocturnal_JJ burrowing_NN ', 'Croton_NNP tiglium_NN ', 'breathing_NN oxygen_NN ', 'new_JJ construction_NN ', 'agouti_NN paca_NN ', 'food_NN combination_NN ', 'postal_JJ system_NN ', 'heroic_JJ poetry_NN ', 'Photon_NNP density_NN ', 'fuzzy_NN classification_NN ', 'net_JJ result_NN ', 'internationally_RB acclaimed_VBN ', 'control_NN precision_NN ', 'hypothesis_VBZ driven_VBN ', 'Red_NNP Oxygen_NNP ', 'Conversion_NN Tracking_NNP ', 'Draw_NNP Archery_NNP ', 'VGA_NNP adapter_NN ', 'digger_NN wasp_NN ', 'wide_JJ variety_NN ', 'damages_NNS financially_RB ', 'memory_NN cells_NNS ', 'raising_VBG funds_NNS ', 'electrolytic_JJ process_NN ', 'African_NNP slaves_NNS ', 'option_NN offered_VBD ', 'based_VBN encryption_NN ', 'late_JJ copper_NN ', 'networked_VBN device_NN ', 'contemporary_JJ European_JJ ', 'small_JJ businesses_NNS ', 'screen_NN made_VBN ', 'interface_NN Compute_NNP ', 'often_RB centering_VBG ', 'monuments_NNS located_VBN ', 'salt_NN marsh_NN ', 'cisc_NN processor_NN ', 'COM_NNP port_NN ', 'mass_NN difference_NN ', 'watch_NN espn_NN ', 'Age_NNP culture_NN ', 'financially_RB compensate_VB ', 'West_NN Indies_NNPS ', 'standard_JJ drink_NN ', 'copper_NN ageearly_RB ', 'math_NN program_NN ', 'access_NN networked_VBN ', 'streaming_NN online_NN ', 'serial_JJ devices_NNS ', 'certificate_NN based_VBN ', 'suffered_VBD due_JJ ', 'opposite_JJ sides_NNS ', 'graphical_JJ systems_NNS ', 'acclaimed_VBN night_NN ', 'meal_NN tailored_VBD ', 'low_JJ cost_NN ', 'toy_NN camera_NN ', 'Hard_NNP vacuum_NN ', 'Millennium_NNP Tree_NNP ', 'Local_JJ connectivity_NN ', 'undirected_VBN graphs_NNS ', 'VIP_NNP ROOM_NNP ', 'Thermonuclear_NNP fusion_NN ', 'Hilbert_NNP space_NN ', 'Five_NNP CD_NNP ', 'engine_VBP capacity_NN ', 'streetcar_NN lines_NNS ', 'Yamna_NNP culture_NN ', 'labyrinth_NN fish_NN ', 'Steam_NNP railroad_VBD ', 'Planar_NNP Magnetic_NNP ', 'genus_NN Cuniculus_NNP ', 'systems_NNS model_NN ', 'rock_NN band_NN ', 'Asterix_NNP comics_NNS ', 'auric_JJ chloride_NN ', 'separate_JJ gauges_NNS ', 'early_JJ part_NN ', 'East_NNP England_NNP ', 'Wales_NNP Cornwall_NNP ', 'Semiregular_JJ variables_NNS ', 'Writing_VBG Center_NNP ', 'double_JJ roots_NNS ', 'enterprises_NNS small_JJ ', 'NOKAS_NNP robbery_NN ', 'port_NN redirector_NN ', 'mastermind_NN David_NNP ', 'card_NN options_NNS ', 'inexpensive_JJ film_NN ', 'Giuseppe_NNP Peano_NNP ', 'low_JJ level_NN ', 'Caspian_JJ Sea_NNP ', 'near_NN shore_NN ', 'fused_VBD ring_VBG ', 'freshwater_NN labyrinth_NN ', 'magnetic_JJ gas_NN ', 'visibly_RB pleased_VBN ', 'identification_NN assessment_NN ', 'business_NN units_NNS ', 'other_JJ megalithic_JJ ', 'warmer_NN air_NN ', 'poetry_NN narrative_JJ ', 'religious_JJ ritual_NN ', 'constraint_NN other_JJ ', 'individual_JJ roots_NNS ', 'designates_NNS hard_RB ', 'how_WRB information_NN ', 'St_NNP Tropez_NNP ', 'stone_NN usually_RB ', 'gas_NN powered_VBD ', 'pi_NN bond_NN ', 'SMS_NNP Gateway_NNP ', 'major_JJ EU_NNP ', 'uses_VBZ fuzzy_NN ', 'small_JJ freshwater_NN ', 'tidal_NN wetland_NN ', 'Androgenic_NNP alopecia_NN ', 'Gateway_NNP Email_NNP ', 'River_NNP Medway_NNP ', 'high_JJ temperatures_NNS ', 'rechargeable_JJ phone_NN ', 'reflex_NN cameras_VBD ', 'makes_VBZ use_VBP ', 'construction_NN project_NN ', 'railways_NNS interurban_VBP ', 'small_JJ segments_NNS ', 'transfer_VB breathing_NN ', 'VGASVGA_NNP monitor_NN ', 'oxygen_NN mask_NN ', 'Felis_NNP catus_NN ', 'Long_NNP Island_NNP ', 'shore_NN areas_NNS ', 'vacuum_NN tubes_NNS ', 'observer_NN analysis_NN ', 'ageearly_RB Bronze_NNP ', 'Great_NNP Britain_NNP ', 'alkyl_NN group_NN ', 'school_NN math_NN ', 'radiation_NN seen_VBN ', 'bardic_JJ name_NN ', 'porcelain_NN produced_VBN ', 'eisteddfod_NN movement_NN ', 'Royal_NNP Canadian_NNP ', 'tube_VB amplifier_JJR ', 'conventional_JJ heavy_JJ ', 'copper_NN levels_NNS ', 'northwest_JJS Caspian_JJ ', 'Light_NN Car_NN ', 'particular_JJ business_NN ', 'DVI_NNP I_NNP ', 'gauge_NN railway_NN ', 'Twin_NNP cylinder_NN ', 'injured_VBN person_NN ', 'investment_NN option_NN ']
			collocations = ['Ideal_NNP observer_NN ', 'equity_NN investment_NN ', 'studio_NN album_NN ', 'cold_JJ air_NN ', 'Use_NN Conversion_NN ', 'Tennis_NNP Racquets_NNPS ', 'fava_NN beans_NNS ', 'first_JJ example_NN ', 'Grapple_NNP Gun_NNP ', 'Canadian_JJ rock_NN ', 'non_NN linear_NN ', 'Central_NNP America_NNP ', 'John_NNP Wheeler_NNP ', 'broad_JJ beans_NNS ', 'hard_RB paste_JJ ', 'Purging_NNP Croton_NNP ', 'line_NN defined_VBD ', 'set_NN theory_NN ', 'including_VBG food_NN ', 'puns_NNS caricatures_NNS ', 'phone_NN card_NN ', 'muscular_JJ coat_NN ', 'hair_JJ loss_NN ', 'Navy_NNP carries_VBZ ', 'nuclear_JJ fusion_NN ', 'film_NN camera_NN ', 'soft_JJ vacuum_NN ', 'vice_NN versa_NN ', 'fast_JJ food_NN ', 'deliver_VB control_NN ', 'EU_NNP policy_NN ', 'megalithic_JJ monuments_NNS ', 'conversion_NN rates_NNS ', 'generate_VB heat_NN ', 'Medway_NNP Megaliths_NNP ', 'sigma_NN bond_NN ', 'ground_NN breaking_VBG ', 'root_NN music_NN ', 'oxygen_NN gas_NN ', 'narrative_JJ verse_NN ', 'breaking_VBG ground_NN ', 'Eisenstein_NNP integer_NN ', 'Post_NNP code_VBP ', 'formal_JJ style_NN ', 'agent_NN used_VBN ', 'electronic_JJ amplifier_NN ', 'SMS_NNP service_NN ', 'storage_NN tank_NN ', 'kids_NNS meal_VBP ', 'use_VBP information_NN ', 'ependymal_JJ cells_NNS ', 'share_NN ideas_NNS ', 'fuzzy_NN set_NN ', 'chemical_JJ compound_NN ', 'perceptual_JJ system_NN ', 'real_JJ numbers_NNS ', 'Lucius_NNP Fox_NNP ', 'European_JJ nations_NNS ', 'measurable_JJ sets_NNS ', 'level_NN operations_NNS ', 'other_JJ parts_NNS ', 'wide_JJ use_NN ', 'measure_NN space_NN ', 'alkylating_VBG agent_NN ', 'pure_NN alcohol_NN ', 'night_NN club_NN ', 'South_NNP East_NNP ', 'positive_JJ operator_NN ', 'space_NN filling_VBG ', 'Quantum_NNP foam_NN ', 'cubic_JJ inches_NNS ', 'offered_VBD directly_RB ', 'Force_NNP concentration_NN ', 'combustion_NN engine_NN ', 'dual_JJ gauge_NN ', 'linear_NN device_NN ', 'estimated_VBN savings_NNS ', 'band_NN Rush_NNP ', 'total_JJ mass_NN ', 'antineoplastic_JJ agent_NN ', 'plant_NN species_NNS ', 'United_NNP States_NNPS ', 'cold_NN front_NN ', 'quantum_NN mechanics_NNS ', 'dividing_NN line_NN ', 'load_NN line_NN ', 'long_RB barrows_VBZ ', 'positive_JJ measure_NN ', 'Information_NN Literacy_NN ', 'Fall_NNP Semester_NNP ', 'programming_NN language_NN ', 'valve_NN amplifier_NN ', 'hair_NN follicles_NNS ', 'Wayne_NNP Enterprises_NNP ', 'network_NN software_NN ', 'Bronze_NNP Age_NNP ', 'interurban_VBP streetcar_NN ', 'filling_VBG curve_NN ', '20th_JJ Century_NNP ', 'Early_NNP Neolithic_NNP ', 'cheek_NN stereotypes_NNS ', 'Limoges_NNS porcelain_VBP ', 'Leaf_NNP roller_NN ', 'nucleons_NNS added_VBD ', 'Special_JJ damages_NNS ', 'graphical_JJ analysis_NN ', 'Menkes_NNS syndrome_VBP ', 'cancer_NN treatment_NN ', 'servo_NN motor_NN ', 'dividend_NN reinvestment_NN ', 'Peano_NNP curve_NN ', 'Gold_NNP chloride_VBD ', 'Nursing_VBG interventions_NNS ', 'burrowing_NN rodent_NN ', 'added_VBD together_RB ', 'internal_JJ combustion_NN ', 'live_JJ streaming_NN ', 'electronic_JJ circuits_NNS ', 'Power_NN Windows_VBZ ', 'more_RBR effective_JJ ', 'Risk_NNP management_NN ', 'Sodium_NN alginate_VBP ', 'electrocyclic_JJ reaction_NN ', 'high_JJ purity_NN ', 'underlying_VBG company_NN ', 'affinity_NN groups_NNS ', 'transition_NN zone_NN ', 'false_NN start_VBD ', 'croaking_VBG gourami_NN ', 'air_NN mass_NN ', 'Croton_NNP tiglium_NN ', 'new_JJ construction_NN ', 'agouti_NN paca_NN ', 'food_NN combination_NN ', 'postal_JJ system_NN ', 'heroic_JJ poetry_NN ', 'Photon_NNP density_NN ', 'fuzzy_NN classification_NN ', 'net_JJ result_NN ', 'Red_NNP Oxygen_NNP ', 'Conversion_NN Tracking_NNP ', 'VGA_NNP adapter_NN ', 'digger_NN wasp_NN ', 'wide_JJ variety_NN ', 'memory_NN cells_NNS ', 'electrolytic_JJ process_NN ', 'African_NNP slaves_NNS ', 'small_JJ businesses_NNS ', 'often_RB centering_VBG ', 'salt_NN marsh_NN ', 'cisc_NN processor_NN ', 'COM_NNP port_NN ', 'mass_NN difference_NN ', 'watch_NN espn_NN ', 'West_NN Indies_NNPS ', 'standard_JJ drink_NN ', 'opposite_JJ sides_NNS ', 'low_JJ cost_NN ', 'toy_NN camera_NN ', 'Hard_NNP vacuum_NN ', 'undirected_VBN graphs_NNS ', 'VIP_NNP ROOM_NNP ', 'Thermonuclear_NNP fusion_NN ', 'Hilbert_NNP space_NN ', 'engine_VBP capacity_NN ', 'Yamna_NNP culture_NN ', 'labyrinth_NN fish_NN ', 'genus_NN Cuniculus_NNP ', 'rock_NN band_NN ', 'Asterix_NNP comics_NNS ', 'auric_JJ chloride_NN ', 'Semiregular_JJ variables_NNS ', 'Writing_VBG Center_NNP ', 'Giuseppe_NNP Peano_NNP ', 'low_JJ level_NN ', 'Caspian_JJ Sea_NNP ', 'near_NN shore_NN ', 'fused_VBD ring_VBG ', 'business_NN units_NNS ', 'religious_JJ ritual_NN ', 'St_NNP Tropez_NNP ', 'gas_NN powered_VBD ', 'pi_NN bond_NN ', 'SMS_NNP Gateway_NNP ', 'Androgenic_NNP alopecia_NN ', 'River_NNP Medway_NNP ', 'high_JJ temperatures_NNS ', 'reflex_NN cameras_VBD ', 'makes_VBZ use_VBP ', 'construction_NN project_NN ', 'affects_VBZ copper_NN ', 'oxygen_NN mask_NN ', 'Felis_NNP catus_NN ', 'Long_NNP Island_NNP ', 'vacuum_NN tubes_NNS ', 'Great_NNP Britain_NNP ', 'alkyl_NN group_NN ', 'radiation_NN seen_VBN ', 'bardic_JJ name_NN ', 'Royal_NNP Canadian_NNP ', 'tube_VB amplifier_JJR ', 'groups_NNS provide_VB ', 'conventional_JJ heavy_JJ ', 'Light_NN Car_NN ', 'DVI_NNP I_NNP ', 'Twin_NNP cylinder_NN ', 'injured_VBN person_NN ']
			#print len(list(set(collocations)))
			print "Total number of collocations:", len(collocations)
			collocations = list(set(collocations))
			print "Total number of unique collocations:", len(collocations)
			#for i in collocations:
			#	print i
			output_file = raw_input()
			#"""
			#output_file = ""
			mwe(collocations, intersection_union, debug, output_file, Bing_API_key = key)
		else:
			print("Choose one from (I, U, B)\nExiting the script...")
	else:
		print("Choose one from (I, U, B)\nExiting the script...") 