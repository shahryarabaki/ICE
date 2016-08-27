#!/usr/bin/Python2
# --coding:utf-8--

from __future__ import print_function
import nltk
from nltk.corpus import stopwords
import re
import string

# Method to extract POS tagged n-grams
def pos_tagged_ngrams(_input_file_path, _n_value_for_ngram_extraction, _stop_word_removal, _verbose):
	if _verbose:
		# A file to save the verbose output of the program
		_output_file_verbose = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
		_output_file_verbose = open(_output_file_verbose, 'a')
		print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
		print("\tExtracting %d-grams:" %(_n_value_for_ngram_extraction), file = _output_file_verbose)
		print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)
		print("\tRemoving non-ascii characters from input text ...", file = _output_file_verbose)
		print("\tExtracting %d-grams ..." %(_n_value_for_ngram_extraction))
	# Reading text from input file
	_input_text = open(_input_file_path).readlines()

	# A Python list to store sentences from input text after removing non-ascii characters
	_input_sentences = []

	# Output text file to save the clean text after removing any non-ascii characters present
	_output_file_path_ascii_only = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'ascii.txt')
	if _verbose:
		print("\tClean text after removing non-ascii characters is saved to the file:\n\t%s"\
%(_output_file_path_ascii_only), file = _output_file_verbose)


	# Removing non-ascii characters
	# All non-ascii characters have a value < 128
	_output_file_ascii_only = open(_output_file_path_ascii_only, 'w')
	for _line in _input_text:
		_line = ''.join(_char for _char in _line if ord(_char) < 128)
		_input_sentences.append(_line)
		_output_file_ascii_only.write(_line)
	_output_file_ascii_only.close()


	# Let's expand the contractions before POS tagging
	# We don't want "don't" to be POS tagged as don_{POS} 't_{POS} for obvious reasons
	# I used the 'English contraction list' from Wikipedia
	#		URL: http://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
	# 		- only one expansion is used for each contraction
	# 		even though multiple optins are available for certain contractions
	#		Example: he'd = he had (OR) he would
	# Here, we read the text file, 'English_contractions.txt' and save the contractions and expansions in
	#		to a dictionary. When ever a contraction is matched it is replaced with the respective expansion
	# NOTE: If I missed any contraction, well, we should add it to the file, 'English_contractions.txt' ASAP
	if _verbose:
		print("\tExpanding the contractions ...", file = _output_file_verbose)
	# Dictionary
	contraction_dictionary = {}
	# Read the text from the file, "English_contractions.txt"
	_contractions = open("English_contractions.txt").readlines()
	for _each_contraction in _contractions:

		_contraction, _expansion = _each_contraction.strip('\n').split('\t')[0], _each_contraction.strip('\n').split('\t')[1]
		contraction_dictionary[_contraction.lower()] = _expansion.lower()
		
	# Now that our contraction dictionary is ready, we replace each contraction with the respective expansion in
	# 		the input text text with non-ascii characters removed. And then let's POS tag the text.
	# A list to save the text after expanding the contractions
	_input_sentences_no_contractions = []
	
	for _sentence in _input_sentences:
		
		for _word in _sentence.split(' '):
			print('sentence.split('')',_word)
			if _word.lower().strip('\n') in contraction_dictionary:
				_sentence = _sentence.replace(_word.strip('\n'), contraction_dictionary[_word.lower().strip('\n')])
		_input_sentences_no_contractions.append([_sentence])
				


	# Output text file to write the text after replacing the contractions
	_output_file_path_no_contractions = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'no_contractions.txt')
	_output_file_no_contractions = open(_output_file_path_no_contractions, 'w')
	for _sentence in _input_sentences_no_contractions:
		_output_file_no_contractions.write(str(_sentence.rstrip('[')))
	_output_file_no_contractions.close()
	if _verbose:
		print("\tText after contractions are replaced is written to the file:\n\t%s"\
%(_output_file_path_no_contractions), file = _output_file_verbose)







