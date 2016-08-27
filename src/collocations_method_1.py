from nltk.corpus import wordnet
import re
from pos_tagger import POS_tag_cleaner

# Method to determine if a phrase is a collocation based on dictionary based technique
# Uses WordNet from NLTK corpus to obtain definitions of the words when both
	# the word and it's sense are passed as inputs
def Collocations_Method_1(_n_grams_from_input_text_file, _input_file_path, _apply_POS_restrictions, _verbose):
	if _verbose:
		# A file to save the verbose output of the program
		_output_file_verbose = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
		_output_file_verbose = open(_output_file_verbose, 'a')
		
		print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
		print("\tMethod-1: WordNet - Extracting collocations:", file = _output_file_verbose)
		print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)
		print("\tMethod-1: Using WordNet to extract collocations ...")

	# A list to store n-gram phrases that are collocations
	wordnet_collocations = []
	# A list to store n-gram phrases that are not collocations
	n_grams_not_collocations = []

	for _n_gram in _n_grams_from_input_text_file:
		if _verbose:
			print("\n%s:" %(_n_gram), file = _output_file_verbose)
		if _n_gram in wordnet_collocations or _n_gram in n_grams_not_collocations:
			# If a particular n-gram phrase is checked if it is a collocation before,
			# it will be present in one of the lists, wordnet_collocations OR n_grams_not_collocations
			# Hence, we move on to the next n-gram
			continue
		else:
			# Before checking if the n-gram is defined in WordNet we check if atlease one
			# POS tag is from the valid POS tag list: {Noun, Verb, Adverb, Adjective} if
			# _apply_POS_restrictions is set to True
			if _apply_POS_restrictions:
				valid_POS_tags = ['NN', 'VB', 'RB', 'JJ']
				_valid_POS_tag_counter = 0 # A counter to count the number of valid POS tags in n-gram
				for _pos_tag in valid_POS_tags:
					if _pos_tag in _n_gram:
						_valid_POS_tag_counter += 1
				if _valid_POS_tag_counter == 0:
					# If no valid POS tag is present in the n-gram, it is not a collocation
					# when POS restrictions are applied
					n_grams_not_collocations.append(_n_gram)
					if _verbose:
						print("\t'%s' does not have valid POS tags\n\tMoving on to the next phrase ..." %(_n_gram), file = _output_file_verbose)
					continue # We move to the next n-gram in the list
				
			# If POS restrictions are not to be applied on the n-gram
			_n_gram_lower = _n_gram.lower() + ' ' # Lower case
			_n_gram_lower = re.sub(r'_.*? ', ' ', _n_gram_lower).rstrip(' ')
			_n_gram_lower = _n_gram_lower.replace(' ', '_')
			if _verbose:
				print("\tLooking for phrase definitions in WordNet ...", file = _output_file_verbose)
			syn_sets = wordnet.synsets(_n_gram_lower)
			if len(syn_sets) == 0:
				if _verbose:
					print("\tWordNet does not have definitions for '%s'" %(_n_gram_lower), file = _output_file_verbose)
				n_grams_not_collocations.append(_n_gram)
				continue
			else:
				wordnet_collocations.append(_n_gram)
				if _verbose:
					print("\tCOLLOCATION: '%s' is defined in WordNet" %(_n_gram_lower), file = _output_file_verbose)
				continue

	# Output text file to save collocations
	_output_file_path_wordnet_collocations = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_wordnet.txt')
	with open(_output_file_path_wordnet_collocations, 'w') as _output_file_wordnet_collocations:
		for _collocation in wordnet_collocations:
			print(POS_tag_cleaner(_collocation) + '\n', file = _output_file_wordnet_collocations)
	if _verbose:
		print("\n\tMethod-1: WordNet - Collocations are written to the file:\n\t%s" %(_output_file_path_wordnet_collocations), file = _output_file_verbose)

	# Output text file to save n-grams that are not collocations
	_output_file_path_wordnet_not_collocations = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'not_collocations_wordnet.txt')
	_output_file_wordnet_not_collocations = open(_output_file_path_wordnet_not_collocations, 'w')
	with open(_output_file_path_wordnet_not_collocations, 'w') as _output_file_wordnet_not_collocations:
		for _n_gram in n_grams_not_collocations:
			print(POS_tag_cleaner(_n_gram) + '\n', file = _output_file_wordnet_not_collocations)
	if _verbose:
		print("\n\tMethod-1: WordNet - N-grams that are not collocations are written to the file:\n\t%s" %(_output_file_path_wordnet_not_collocations), file = _output_file_verbose)
	
	if _verbose:
		print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
		print("\tMethod-1: WordNet - Collocation extraction - Complete", file = _output_file_verbose)
		print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)

	# Returning n-grams that are collocations and n-grams that are not
	if _verbose:
		print("\t\tCollocation extraction - Method-1 - successful")
	return wordnet_collocations, n_grams_not_collocations