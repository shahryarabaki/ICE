#!/usr/bin/python3.5

#To-Do List:
# - Change _c_evalution cancel by inputting -1
# - Fix integer number extraction of 0 results queries

from .bing_search_result_totals_V2 import bing_search_total
from .bing_search_api import BingSearchAPI
from .pos_tagger import POS_tag_cleaner
from collections import Counter # To count the number of occurrances of each word in the n-gram
import math
import re
import sys
import os

"""
Procedure:
----------
- Given an input text file, punctuation and non-ascii characters are removed from the text
- All the unique words from the input file are extracted and total search results are extracted using Bing search API
- The total number of search results for the alphabet 'a' are obtained. Since 'a' is both an alphabet and a word in English, it gives us a
	universe of all English pages from the web which serves us as a denominator when trying to find the probability value
- Given a phrase 'x y z', probability are calculated as follows:
	probability(x y z) = search_result_total(x y z) / search_result_total(a)
	probability(x) = probability of the word 'x' = search_result_total(x) / search_result_total(a)
	probability(y) = probability of the word 'y' = search_result_total(y) / search_result_total(a)
	probability(z) = probability of the word 'z' = search_result_total(z) / search_result_total(a)
- Technique-1:
	If probability(x y z) > (probability(x) * probability(y) * probability (z)) / search_result_total(a),
	we conclude that the phrase 'x y z' is a Collocation
- Technique-2:
	Takes into consideration, the uniqueness of the words in the n-gram into consideration. Details in Thesis documentation OR read the code below

"""

def POS_Check(_n_gram):
	valid_POS_tags = ['NN', 'VB', 'RB', 'JJ']
	for _pos_tag in valid_POS_tags:
		if ('_' + _pos_tag) in _n_gram:
			return True
	return False


def Collocations_Method_5(_bing_api_key, _n_grams_from_input_text_file, _input_file_path, _apply_POS_restrictions, _input_queries_hit_results, _individual_word_hit_results, _corpus, original_input_queries_file, individual_words, _verbose, _p_value = 1.0, _c_value = 1.0, _version = 1):
	if _verbose:
		# A file to save the verbose output of the program
		_output_file_verbose = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
		_output_file_verbose = open(_output_file_verbose, 'a')
		print("\n----------------------------------------------------------------------------------------", file = _output_file_verbose)
		print("\tMethod-5: Probability technique - %s - Extracting collocations:" %(_corpus), file = _output_file_verbose)
		print("----------------------------------------------------------------------------------------\n\n", file = _output_file_verbose)
		print("\tMethod-5: Probability technique - %s - Extracting collocations ..." %(_corpus))

	Universe_of_the_webpages = 0
	_n_value = 0
	if _corpus == 'Bing':
		_bing_search = BingSearchAPI(_bing_api_key)
		Universe_of_the_webpages, _bing_api_key = _bing_search.search_total(False, 'a') # A total search result count from Bing.com of the word 'a'
	elif _corpus == 'Wiki_07':
		Universe_of_the_webpages = 1.7 * (10 ** 6)
	elif _corpus == 'Wiki_06':
		Universe_of_the_webpages = 1.5 * (10 ** 6)
	elif _corpus == 'Voice':
		Universe_of_the_webpages = 1695
	elif _corpus == 'Reuters':
		Universe_of_the_webpages = 806791
	elif _corpus == 'DUC':
		Universe_of_the_webpages = 47940
	elif _corpus == 'BNC':
		Universe_of_the_webpages = 4234
	elif _corpus == 'ANC':
		Universe_of_the_webpages = 1695
	elif _corpus == '20NewsGroups':
		Universe_of_the_webpages = 18828
	
	assert Universe_of_the_webpages != 0, _corpus
	# Python dictionary to save the hit-results of the input search queries
	_hitResults_input_queries = {}
	# A Python dictionary to save the hot-results of the individual words in the input search queries
	_hitResults_individual_words = {}

	if _apply_POS_restrictions:
		_n_grams_from_input_text_file = list(filter(POS_Check, _n_grams_from_input_text_file))
	
	# If _corpus used is 'Bing', search result totals of the phrases are passes in a dictionary
	if _corpus == 'Bing':
		_hitResults_input_queries = _input_queries_hit_results
	else:
		# Read input from the files, _input_queries_hit_results and _individual_word_hit_results
		#       And append the hit-results to the dictionaries created in the step above
		_input_queries_hitResults = open(_input_queries_hit_results).readlines()
		# Read original search queries
		_original_input_queries = open(original_input_queries_file).readlines()
		if len(_input_queries_hitResults) == len(_original_input_queries):
			for _x in xrange(0, len(_input_queries_hitResults)):
				_each_line = _input_queries_hitResults[_x].strip('\n').replace("Total # Hits for: ", '').split(" = ")
				# Last second element will be the query, enclosed in quotes followed by '~1' as long as the program retuns an exact match.
				#       Some times when an exact match is not found, an approximate match, i.e. hit-results for individual
				#       words are returned. This will be reflected in the search query returned by the program. hence, we
				#       look for an exact match. In these scenarios, query will not be enclosed in quoted
				_hitResults_input_queries[_original_input_queries[_x].strip('\n').replace('"', '').replace('~1', '')] = int(_each_line[-1])
		else:
			print("ERROR: Number of input queries does not match with the number of lucene hit-results.\nIn Method-5.")
			sys.exit(0)

		if _verbose:
			print("Hit results of individual n-grams:\n", _hitResults_input_queries, file = _output_file_verbose)

	# If _corpus used is 'Bing', search result totals of the words are passed in a dictionary
	if _corpus == 'Bing':
		_hitResults_individual_words = _individual_word_hit_results
	else:
		_individual_word_hitResults = open(_individual_word_hit_results).readlines()
		_individual_words = open(individual_words).readlines()

		if len(_individual_word_hitResults) == len(_individual_words):
			for _x in xrange(0, len(_individual_word_hitResults)):
				_each_line = _individual_word_hitResults[_x].strip('\n').replace("Total # Hits for: ", '').split(" = ")
				# Last second element will be the query, enclosed in quotes followed by '~1' as long as the program retuns an exact match.
				#       Some times when an exact match is not found, an approximate match, i.e. hit-results for individual
				#       words are returned. This will be reflected in the search query returned by the program. hence, we
				#       look for an exact match. In these scenarios, query will not be enclosed in quoted
				_hitResults_individual_words[_individual_words[_x].strip('\n').replace('"', '').replace('~1', '')] = int(_each_line[-1])
		else:
			print("ERROR: Number of individual words does not match with the number of lucene hit-results.\nIn Method-5.\n", _corpus)
			sys.exit(0)

		if _verbose:
			print("Hit results of individual words:\n", _hitResults_individual_words, file = _output_file_verbose)
	
	# Step 1: Calculating individual word probabilities
	

	word_probabilities = {} # A dictionary to store the probabilities of individual words
	if _verbose:
		print("\nWord \t\t Total search results \t\t Universe page count \t\t Probability", file = _output_file_verbose)
	for _word in _hitResults_individual_words:
		_probability = float(_hitResults_individual_words[_word]) / Universe_of_the_webpages
		word_probabilities[_word] = _probability
		if _verbose:
			print("%s \t\t %s \t\t %d \t\t %f" %(_word, _hitResults_individual_words[_word], Universe_of_the_webpages, _probability), file = _output_file_verbose)
					
	# Step 2: Calculating n-gram phrase probabilities
	phrase_probabilities = {} # A dictionary to store the probabilities of the n-gram phrases
	if _verbose:
		print("\nN-gram \t\t Total search results \t\t Universe page count \t\t Probability", file = _output_file_verbose)
	for n_gram in _n_grams_from_input_text_file:
		# Remove the POS tags attached
		_n_gram = POS_tag_cleaner(n_gram)
		if _n_value <= 0:
			_n_value = len(n_gram.split())
		#_n_gram = n_gram + ' '
		#_n_gram = re.sub(r'_.*? ', ' ', _n_gram.strip('\n').lstrip(' ')).rstrip(' ')
		try:
			n_gram_search_total = _hitResults_input_queries[_n_gram]
		except Exception as e:
			print(str(e))
			
		n_gram_probability = float(n_gram_search_total) / Universe_of_the_webpages
		if _verbose:
			print("%s \t\t %s \t\t %d \t\t %f" %(_n_gram, n_gram_search_total, Universe_of_the_webpages, n_gram_probability), file = _output_file_verbose)
		phrase_probabilities[_n_gram] = n_gram_probability


	Collocations_without_uniqueness = [] # A python list to store n-grams that are collocations, without uniqueness
	Just_ngrams_without_uniqueness = [] # A python script to store n-grams that are not collocations, without uniqueness

	_evaluate_value = pow(float(_c_value), pow(_n_value, _p_value) - 1)
	if _verbose:
		print(("\nTechnique-1: Uniqueness of words in the n-gram is not taken into consideration.\n\n"
			"N-gram \t\tProbability \t\t Product of individual word probabilities"), file = _output_file_verbose)
	for n_gram in phrase_probabilities:
	

		print("N value is %d" % (_n_value))
		print("Evaluate value is: " + str(_evaluate_value))

		_words_in_ngram = n_gram.lstrip(' ').rstrip(' ').strip('\n').split()
		product_of_individual_word_probabilities = 1
		for _word in _words_in_ngram:
			_word = _word.lstrip(' ').rstrip(' ').strip('\n')
			if _word in word_probabilities:
				product_of_individual_word_probabilities *= word_probabilities[_word]
			else: # If the word is not present in the word dictionary already, then probability is 0
				product_of_individual_word_probabilities *= float(0) / Universe_of_the_webpages
		if _verbose:
			print(n_gram, ' \t\t ', phrase_probabilities[n_gram], ' \t\t ', product_of_individual_word_probabilities, file = _output_file_verbose)
		if phrase_probabilities[n_gram] > _evaluate_value * product_of_individual_word_probabilities:
			Collocations_without_uniqueness.append(n_gram)
		else:
			Just_ngrams_without_uniqueness.append(n_gram)

	# Technique-2: Taking uniqueness of words into consideration
	Collocations_with_uniqueness = [] # A python list to store n-grams that are collocations
	Just_ngrams_with_uniqueness = [] # A python script to store n-grams that are not collocations

	if _verbose:
		print("\nTechnique-2: Uniqueness of words in n_gram is taken into consideration.\n", file = _output_file_verbose)
	for n_gram in phrase_probabilities:
		_words_in_ngram = n_gram.split() # Splits the n-gram at each occurrance of a space
		
		unique_word_count = len(set(re.findall('\w+', n_gram.lower()))) # counts the total number of unique words in a given collocation
		n_factorial = math.factorial(len(_words_in_ngram))
			
		if unique_word_count == len(_words_in_ngram):
			value_to_multiply_product_of_individual_probabilities = float(1) / n_factorial
			if _verbose:
				print("N-gram '%s' has unique words. n! = %d" %(n_gram, n_factorial), file = _output_file_verbose)
		else:
			factorial_of_unique_words = 1 # Store the product, 1! * 2! * 3! ... k! for 'k' unique words in the n-gram
			word_count = Counter(_words_in_ngram) # counts the number of times each word appears in the n-gram
			for _word in word_count:
				factorial_of_unique_words *= math.factorial(word_count[_word])
				if _verbose:
					print(_word, word_count[_word], factorial_of_unique_words, file = _output_file_verbose)
			value_to_multiply_product_of_individual_probabilities = float(factorial_of_unique_words) / n_factorial
			if _verbose:
				print("N-gram '%s' has repeated words! n! = %d, product of individual factorials = %d " %(n_gram, n_factorial, factorial_of_unique_words), file = _output_file_verbose)

		product_of_individual_word_probabilities = 1
		for _word in _words_in_ngram:
			_word = _word.lstrip(' ').rstrip(' ').strip('\n')
			try:
				product_of_individual_word_probabilities *= word_probabilities[_word]
			except Exception as e:
				print("ERROR: Method-5 \n\t%s" %(str(e)))
				product_of_individual_word_probabilities *= 1
		if _verbose:
			print(n_gram, phrase_probabilities[n_gram], value_to_multiply_product_of_individual_probabilities * product_of_individual_word_probabilities, file = _output_file_verbose)
		
		if phrase_probabilities[n_gram] > _evaluate_value * value_to_multiply_product_of_individual_probabilities * product_of_individual_word_probabilities:
			Collocations_with_uniqueness.append(n_gram)
		else:
			Just_ngrams_with_uniqueness.append(n_gram)


	if _version == 1:
		return Collocations_without_uniqueness, _bing_api_key
	else:
		return Collocations_with_uniqueness, _bing_api_key