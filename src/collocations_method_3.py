#!/usr/bin/Python3.5
# --coding:utf-8--

import math
import os
import random
import re
from .bing_search_result_totals_V2 import bing_search_total
from .pos_tagger import POS_tag_cleaner
from .collocations_method_5_V3 import POS_Check
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def extract_int_number_results(num_results_for_query):
	if num_results_for_query != '0':
		try:
			return int( (num_results_for_query).replace(',', '').split(' ')[-2] ) 
		except Exception as e:
			print("Error extracting number of results, message: {error:s}".format(error = str(e)))
			print(serp.num_results_for_query)
	return 0

def min(a, b):
	return a if a < b else b

# Statistical technique
def Collocations_Method_3(_bing_api_key, _n_grams_from_input_text_file, _input_file_path, _collocation_corpora, _apply_POS_restrictions, _verbose):
	print(_n_grams_from_input_text_file)
	if _verbose:
		# A file to save the verbose output of the program
		_output_file_verbose = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
		_output_file_verbose = open(_output_file_verbose, 'a')
		print("\n----------------------------------------------------------------------------------------", file = _output_file_verbose)
		print("\tMethod-3: Statistical technique - Extracting collocations:", file = _output_file_verbose)
		print("----------------------------------------------------------------------------------------\n\n", file = _output_file_verbose)
		print("\tMethod-3: Statistical technique - Extracting collocations ...")

	# Obtain the path of this script to go to the TAGGED-FULL folder
	script_path = os.path.dirname(os.path.realpath(__file__))

	# Extracting words from the files in TAGGED-FULL folder
	# WH-adverbs are stored to the list 'WRB'
	WRB = script_path+'/TAGGED_Full/WRB1'
	f = open(WRB, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	WRB = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		WRB.append(i)

	# WH-pronouns, possessive are stored to the list 'WHP'
	WHP = script_path+'/TAGGED_Full/WP$1'
	f = open(WHP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	WHP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		WHP.append(i)

	# WH-pronouns are stored to the list 'WP'
	WP = script_path+'/TAGGED_Full/WP1'
	f = open(WP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	WP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		WP.append(i)

	# WDT: WH-determiner
	#   that what whatever which whichever
	# stored in the list 'WDT'
	WDT = script_path+'/TAGGED_Full/WDT1'
	f = open(WDT, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	WDT = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		WDT.append(i)

	# VBZ: verb, present tense, 3rd person singular
	#    bases reconstructs marks mixes displeases seals carps weaves snatches
	#    slumps stretches authorizes smolders pictures emerges stockpiles
	#    seduces fizzes uses bolsters slaps speaks pleads ...
	# Stored in the list 'VBZ'
	VBZ = script_path+'/TAGGED_Full/VBZ1'
	f = open(VBZ, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VBZ = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VBZ.append(i)

	# VBP: verb, present tense, not 3rd person singular
	#    predominate wrap resort sue twist spill cure lengthen brush terminate
	#    appear tend stray glisten obtain comprise detest tease attract
	#    emphasize mold postpone sever return wag ...
	# Stored in the list 'VBP'
	VBP = script_path+'/TAGGED_Full/VBP1'
	f = open(VBP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VBP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VBP.append(i)

	# VBN: verb, past participle
	#    multihulled dilapidated aerosolized chaired languished panelized used
	#    experimented flourished imitated reunifed factored condensed sheared
	#    unsettled primed dubbed desired ...
	# Stored in the list 'VBN'
	VBN = script_path+'/TAGGED_Full/VBN1'
	f = open(VBN, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VBN = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VBN.append(i)

	# VBG: verb, present participle or gerund
	#    telegraphing stirring focusing angering judging stalling lactating
	#    hankerin' alleging veering capping approaching traveling besieging
	#    encrypting interrupting erasing wincing ...
	# Stored in the list 'VBG'
	VBG = script_path+'/TAGGED_Full/VBG1'
	f = open(VBG, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VBG = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VBG.append(i)

	# VBD: verb, past tense
	#    dipped pleaded swiped regummed soaked tidied convened halted registered
	#    cushioned exacted snubbed strode aimed adopted belied figgered
	#    speculated wore appreciated contemplated ...
	# Stored in the list 'VBD'
	VBD = script_path+'/TAGGED_Full/VBD1'
	f = open(VBD, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VBD = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VBD.append(i)

	# VB: verb, base form
	#    ask assemble assess assign assume atone attention avoid bake balkanize
	#    bank begin behold believe bend benefit bevel beware bless boil bomb
	#    boost brace break bring broil brush build ...
	# Stored in the list 'VB'
	VB = script_path+'/TAGGED_Full/VB1'
	f = open(VB, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	VB = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		VB.append(i)

	# TO: "to" as preposition or infinitive marker
	#    to
	# Stored in the list 'TO'
	TO = script_path+'/TAGGED_Full/TO1'
	f = open(TO, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	TO = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		TO.append(i)

	# RP: particle
	#    aboard about across along apart around aside at away back before behind
	#    by crop down ever fast for forth from go high i.e. in into just later
	#    low more off on open out over per pie raising start teeth that through
	#    under unto up up-pp upon whole with you
	# Stored in the list 'RP'
	RP = script_path+'/TAGGED_Full/RP1'
	f = open(RP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	RP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		RP.append(i)
		
	# RBS: adverb, superlative
	#    best biggest bluntest earliest farthest first furthest hardest
	#    heartiest highest largest least less most nearest second tightest worst
	# Stored in the list 'RBS'
	RBS = script_path+'/TAGGED_Full/RBS1'
	f = open(RBS, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	RBS = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		RBS.append(i)

	# RBR: adverb, comparative
	#    further gloomier grander graver greater grimmer harder harsher
	#    healthier heavier higher however larger later leaner lengthier less-
	#    perfectly lesser lonelier longer louder lower more ...
	# Stored in the list 'RBR'
	RBR = script_path+'/TAGGED_Full/RBR1'
	f = open(RBR, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	RBR = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		RBR.append(i)

	# RB: adverb
	#    occasionally unabatingly maddeningly adventurously professedly
	#    stirringly prominently technologically magisterially predominately
	#    swiftly fiscally pitilessly ...
	# Stored in the list 'RB'
	RB = script_path+'/TAGGED_Full/RB1'
	f = open(RB, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	RB = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		RB.append(i)

	# PRP$: pronoun, possessive
	#    her his mine my our ours their thy your
	# Stored in the list 'PRP'
	PRP = script_path+'/TAGGED_Full/PRP$1'
	f = open(PRP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	PRP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		PRP.append(i)
	
	# PRP: pronoun, personal
	#    hers herself him himself hisself it itself me myself one oneself ours
	#    ourselves ownself self she thee theirs them themselves they thou thy us
	# Stored in the list 'PRPP'
	PRPP = script_path+'/TAGGED_Full/PRP1'
	f = open(PRPP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	PRPP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		PRPP.append(i)

	# PDT: pre-determiner
	#    all both half many quite such sure this
	# Stored in the list 'PDT'
	PDT = script_path+'/TAGGED_Full/PDT1'
	f = open(PDT, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	PDT = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		PDT.append(i)
		
	# NNS: noun, common, plural
	#    undergraduates scotches bric-a-brac products bodyguards facets coasts
	#    divestitures storehouses designs clubs fragrances averages
	#    subjectivists apprehensions muses factory-jobs ...
	# Stored in the list 'NNS'
	NNS = script_path+'/TAGGED_Full/NNS1'
	f = open(NNS, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	NNS = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		NNS.append(i)

	# NNPS: noun, proper, plural
	#    Americans Americas Amharas Amityvilles Amusements Anarcho-Syndicalists
	#    Andalusians Andes Andruses Angels Animals Anthony Antilles Antiques
	#    Apache Apaches Apocrypha ...
	# Stored in the list 'NNPS'
	NNPS = script_path+'/TAGGED_Full/NNPS1'
	f = open(NNPS, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	NNPS = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		NNPS.append(i)

	# NNP: noun, proper, singular
	#    Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
	#    Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
	#    Shannon A.K.C. Meltex Liverpool ...
	# Stored in the list 'NNP'
	NNP = script_path+'/TAGGED_Full/NNP1'
	f = open(NNP, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	NNP = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		NNP.append(i)

	# NN: noun, common, singular or mass
	#    common-carrier cabbage knuckle-duster Casino afghan shed thermostat
	#    investment slide humour falloff slick wind hyena override subhumanity
	#    machinist ...
	# Stored in the list 'NN'
	NN = script_path+'/TAGGED_Full/NN1'
	f = open(NN, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	NN = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		NN.append(i)

	# MD: modal auxiliary
	#    can cannot could couldn't dare may might must need ought shall should
	#    shouldn't will would
	# Stored in the list 'MD'
	MD = script_path+'/TAGGED_Full/MD1'
	f = open(MD, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	MD = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		MD.append(i)

	# JJS: adjective, superlative
	#    calmest cheapest choicest classiest cleanest clearest closest commonest
	#    corniest costliest crassest creepiest crudest cutest darkest deadliest
	#    dearest deepest densest dinkiest ...
	# Stored in the list 'JJS'
	JJS = script_path+'/TAGGED_Full/JJS1'
	f = open(JJS, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	JJS = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		JJS.append(i)

	# JJR: adjective, comparative
	#    bleaker braver breezier briefer brighter brisker broader bumper busier
	#    calmer cheaper choosier cleaner clearer closer colder commoner costlier
	#    cozier creamier crunchier cuter ...
	# Stored in the list 'JJR'
	JJR = script_path+'/TAGGED_Full/JJR1'
	f = open(JJR, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	JJR = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		JJR.append(i)

	# JJ: adjective or numeral, ordinal
	#    third ill-mannered pre-war regrettable oiled calamitous first separable
	#    ectoplasmic battery-powered participatory fourth still-to-be-named
	#    multilingual multi-disciplinary ...
	# Stored in the list 'JJ'
	JJ = script_path+'/TAGGED_Full/JJ1'
	f = open(JJ, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	JJ = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		JJ.append(i)

	# IN: preposition or conjunction, subordinating
	#    astride among uppon whether out inside pro despite on by throughout
	#    below within for towards near behind atop around if like until below
	#    next into if beside ...
	# Stored in the list 'IN'
	IN = script_path+'/TAGGED_Full/IN1'
	f = open(IN, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	IN = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		IN.append(i)

	# EX: existential there
	#    there
	# Stored in the list 'EX'
	EX = script_path+'/TAGGED_Full/EX1'
	f = open(EX, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	EX = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		EX.append(i)

	# DT: determiner
	#    all an another any both del each either every half la many much nary
	#    neither no some such that the them these this those
	# Stored in the list 'DT'
	DT = script_path+'/TAGGED_Full/DT1'
	f = open(DT, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	DT = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		DT.append(i)

	# CD: numeral, cardinal
	#    mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
	#    seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
	#    fifteen 271,124 dozen quintillion DM2,000 ...
	# Stored in the list 'CD'
	CD = script_path+'/TAGGED_Full/CD1'
	f = open(CD, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	CD = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		CD.append(i)

	# CC: conjunction, coordinating
	#    & 'n and both but either et for less minus neither nor or plus so
	#    therefore times v. versus vs. whether yet
	# Stored in the list 'CC'
	CC = script_path+'/TAGGED_Full/CC1'
	f = open(CC, 'r')
	t = f.readlines()
	f.close()
	t = set(t) # Removes duplicates from the list
	CC = [] # creates an empty list
	for i in t:
		i = i.strip('\n')
		CC.append(i)

	# Creating output files
	_stat_05_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_Stat>05.txt')
	if os.path.isfile(_stat_05_path):
		 os.remove(_stat_05_path)
   
	_stat_06_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_Stat>06.txt')
	if os.path.isfile(_stat_06_path):
		 os.remove(_stat_06_path)
   
	_stat_07_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_Stat>07.txt')
	if os.path.isfile(_stat_07_path):
		 os.remove(_stat_07_path)
   
	_stat_08_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_Stat>08.txt')
	if os.path.isfile(_stat_08_path):
		 os.remove(_stat_08_path)
   
	_stat_09_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_Stat>09.txt')
	if os.path.isfile(_stat_09_path):
		 os.remove(_stat_09_path)

	_stat_mean_sd_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'N_gram_Stat_Mean_SD_range.txt')
	if os.path.isfile(_stat_mean_sd_path):
		os.remove(_stat_mean_sd_path)

	range_zero = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_0txt')
	if os.path.isfile(range_zero):
		os.remove(range_zero)

	range_1l = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_1_left.txt')
	if os.path.isfile(range_1l):
		os.remove(range_1l)

	range_2l = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_2_left.txt')
	if os.path.isfile(range_2l):
		os.remove(range_2l)

	range_3l = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_3_left.txt')
	if os.path.isfile(range_3l):
		os.remove(range_3l)

	range_4l = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_4_left.txt')
	if os.path.isfile(range_4l):
		os.remove(range_4l)

	range_1r = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_1_right.txt')
	if os.path.isfile(range_1r):
		os.remove(range_1r)

	range_2r = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_2_right.txt')
	if os.path.isfile(range_2r):
		os.remove(range_2r)

	range_3r = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_3_right.txt')
	if os.path.isfile(range_3r):
		os.remove(range_3r)

	range_4r = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Stat_Mean_SD_range_4_right.txt')
	if os.path.isfile(range_4r):
		os.remove(range_4r)

	range_statistic = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'Collocations_Stat_Mean_SD.txt')
	if os.path.isfile(range_statistic):
		os.remove(range_statistic)


	auxiliary_verb_list = []
	auxiliary_verb_list.extend(("be", "am", "are", "arent", "is", "was", "were", "being", "can", "cant", "could", "do","dont",\
"did", "does", "doing", "have", "havent", "hadnt", "had", "has", "hasnt", "having", "may", "might", "mightnt", "maynt",\
"mustnt", "must", "shall", "should", "will", "neednt", "wont", "would", "wouldnt", "ought", "been", "cannot", "couldnt",\
"dare", "darent", "need", "shouldnt", "isnt", "wasnt", "werent", "oughtnot", "didnt", "doesnt", "dont"))

	if _apply_POS_restrictions:
		_n_grams_from_input_text_file = list(filter(POS_Check, _n_grams_from_input_text_file))

	# A list to store n-gram phrases that are collocations
	statistical_collocations = []
	# A list to store n-gram phrases that are not collocations
	n_grams_not_collocations = []
	# A dictionary  to store search queries as keys and its search results total as value
	search_queries = {}
	# A dictionary to save the Phrase search totals
	_phrase_search_total_dictionary = {}
	# A dictionary for n_gram and its replacement phrases
	_n_gram_replacement_phrases = {}

	#if we use the input text files
	_n_grams_from_input_text_file_not_have_replacements = []

	choose_input_replacement_phrases = input("Do you want to read the replacement phrases from the files?")
	_replacement_queries_from_files = {}
	if choose_input_replacement_phrases.upper() == "Y":
		try:
			with open("method3_replacement_phrases.cache", 'r') as input_file:
				for line in input_file:
					_temp_phrases = line.split('|')
					_temp_phrases = list(map(lambda x: x.rstrip(' ').lstrip(' ').strip('\n'), _temp_phrases))
					if _temp_phrases[0] not in _replacement_queries_from_files:
						_replacement_queries_from_files[_temp_phrases[0]] = []
					for i in range(1, len(_temp_phrases)):
						_replacement_queries_from_files[_temp_phrases[0]].append(_temp_phrases[i])
		except FileNotFoundError as e:
			print("Error: %s" % (str(e))) 

	for _phrase in _n_grams_from_input_text_file:
		_phrase = _phrase.rstrip(' ').lstrip(' ').strip('\n')
		clean_phrase = POS_tag_cleaner(_phrase)
		if clean_phrase in _replacement_queries_from_files:
			_n_gram_replacement_phrases[clean_phrase] = _replacement_queries_from_files[clean_phrase]
			search_queries[clean_phrase] = 0
			for _temp_phrase in _n_gram_replacement_phrases[clean_phrase]:
				search_queries[_temp_phrase] = 0
		else:
			_n_grams_from_input_text_file_not_have_replacements.append(_phrase)



	with open("method3_replacement_phrases.cache", 'a') as output_replacements_cache:
		for _n_gram in _n_grams_from_input_text_file_not_have_replacements:
			_n_gram = _n_gram.rstrip(' ').lstrip(' ').strip('\n') # To remove any right most trailing space. This can be an issue when n-grams are directly passed
			if _verbose:
				print("\n%s:" %(_n_gram), file = _output_file_verbose)
			if _n_gram in statistical_collocations or _n_gram in n_grams_not_collocations:
				# If a particular n-gram phrase is checked if it is a collocation before,
				# it will be present in one of the lists, statistical_collocations OR n_grams_not_collocations
				# Hence, we move on to the next n-gram
				continue
			else:
				# Before checking if the n-gram is a collocation we check if atlease one
				# POS tag is from the valid POS tag list: {Noun, Verb, Adverb, Adjective} if
				# _apply_POS_restrictions is set to True

				#Consider the replacement words

				# Removing pos tags from the phrase
				_search_phrase = POS_tag_cleaner(_n_gram)

				#_search_phrase = re.sub(r'_.*? ', ' ', _n_gram + ' ').rstrip(' ')
				if _verbose:
					print("\tSearch phrase: %s" %(_search_phrase), file = _output_file_verbose)

				# Add the n-gram itself to search queries
				# Total search results returned for the phrase
				# Using Bing search API
				# _verbose is set to 'False' as we don't want to print the search result twice
				if 'B' in _collocation_corpora:
					#_phrase_search_totals, _bing_api_key = bing_search_total(False, _search_phrase, _bing_api_key)
					#_phrase_search_total_dictionary[_search_phrase] = _phrase_search_totals
					search_queries[_search_phrase] = 0
					_n_gram_replacement_phrases[_search_phrase] = []
					#if _verbose:
					#	print("\tSearch result total of the phrase: %d" %(_phrase_search_totals), file = _output_file_verbose)

				# list to save the search result totals of the phrases with words replaced
				_list_of_search_result_totals = []

				# Splitting n-gram at spaces - a list of all words in the n-gram along with their POS tags
				_pos_tagged_word_in_ngram = _n_gram.split(' ')
				
				# Replace each word of the list and get search result totals
				for _pos_tagged_word in _pos_tagged_word_in_ngram:
					_word, _pos_tag = _pos_tagged_word.split('_') # As word and it's POS are linked by an underscore
					# Each word is to be replaced with 5 random words of the same POS
					# If any POS word list has < 5 words, it will be replaced with the words available
					# A list to store the _replacement_words
					_replacement_words = []
					if(_pos_tag == 'CC'):
						if(len(CC) > 4):
							_replacement_words = random.sample(CC, 5)
						else:
							_replacement_words = CC
					elif(_pos_tag == 'CD'):
						if(len(CD) > 4):
							_replacement_words = random.sample(CD, 5)
						else:
							_replacement_words = CD
					elif(_pos_tag == 'DT'):
						if(len(DT) > 4):
							_replacement_words = random.sample(DT, 5)
						else:
							_replacement_words = DT
					elif(_pos_tag == 'EX'):
						if(len(EX) > 4):
							_replacement_words = random.sample(EX, 5)
						else:
							_replacement_words = EX
					elif(_pos_tag == 'IN'):
						if(len(IN) > 4):
							_replacement_words = random.sample(IN, 5)
						else:
							_replacement_words = IN
					if(_pos_tag == 'VB'):
						if(len(VB) > 4):
							_replacement_words = random.sample(VB, 5)
						else:
							_replacement_words = VB
					elif(_pos_tag == 'VBP'):
						if(len(VBP) > 4):
							_replacement_words = random.sample(VBP, 5)
						else:
							_replacement_words = VBP
					elif(_pos_tag == 'WP$'):
						if(len(WHP) > 4):
							_replacement_words = random.sample(WHP, 5)
						else:
							_replacement_words = WHP
					elif(_pos_tag == 'JJ'):
						if(len(JJ) > 4):
							_replacement_words = random.sample(JJ, 5)
						else:
							_replacement_words = JJ
					elif(_pos_tag == 'JJR'):
						if(len(JJR) > 4):
							_replacement_words = random.sample(JJR, 5)
						else:
							_replacement_words = JJR
					elif(_pos_tag == 'JJS'):
						if(len(JJS) > 4):
							_replacement_words = random.sample(JJS, 5)
						else:
							_replacement_words = JJS
					elif(_pos_tag == 'MD'):
						if(len(MD) > 4):
							_replacement_words = random.sample(MD, 5)
						else:
							_replacement_words = MD
					elif(_pos_tag == 'NN'):
						if(len(NN) > 4):
							_replacement_words = random.sample(NN, 5)
						else:
							_replacement_words = NN
					elif(_pos_tag == 'VBD'):
						if(len(VBD) > 4):
							_replacement_words = random.sample(VBD, 5)
						else:
							_replacement_words = VBD
					elif(_pos_tag == 'VBZ'):
						if(len(VBZ) > 4):
							_replacement_words = random.sample(VBZ, 5)
						else:
							_replacement_words = VBZ
					elif(_pos_tag == 'WRB'):
						if(len(WRB) > 4):
							_replacement_words = random.sample(WRB, 5)
						else:
							_replacement_words = WRB
					elif(_pos_tag == 'NNP'):
						if(len(NNP) > 4):
							_replacement_words = random.sample(NNP, 5)
						else:
							_replacement_words = NNP
					elif(_pos_tag == 'NNPS'):
						if(len(NNPS) > 4):
							_replacement_words = random.sample(NNPS, 5)
						else:
							_replacement_words = NNPS
					elif(_pos_tag == 'NNS'):
						if(len(NNS) > 4):
							_replacement_words = random.sample(NNS, 5)
						else:
							_replacement_words = NNS
					elif(_pos_tag == 'PDT'):
						if(len(PDT) > 4):
							_replacement_words = random.sample(PDT, 5)
						else:
							_replacement_words = PDT
					elif(_pos_tag == 'PRP'):
						if(len(PRPP) > 4):
							_replacement_words = random.sample(PRPP, 5)
						else:
							_replacement_words = PRPP
					elif(_pos_tag == 'VBG'):
						if(len(VBG) > 4):
							_replacement_words = random.sample(VBG, 5)
						else:
							_replacement_words = VBG
					elif(_pos_tag == 'WDT'):
						if(len(WDT) > 4):
							_replacement_words = random.sample(WDT, 5)
						else:
							_replacement_words = WDT
					elif(_pos_tag == 'PRP$'):
						if(len(PRP) > 4):
							_replacement_words = random.sample(PRP, 5)
						else:
							_replacement_words = PRP
					elif(_pos_tag == 'RB'):
						if(len(RB) > 4):
							_replacement_words = random.sample(RB, 5)
						else:
							_replacement_words = RB
					elif(_pos_tag == 'RBR'):
						if(len(RB) > 4):
							_replacement_words = random.sample(RBR, 5)
						else:
							_replacement_words = RBR
					elif(_pos_tag == 'RBS'):
						if(len(RBS) > 4):
							_replacement_words = random.sample(RBS, 5)
						else:
							_replacement_words = RBS
					elif(_pos_tag == 'RP'):
						if(len(RP) > 4):
							_replacement_words = random.sample(RP, 5)
						else:
							_replacement_words = RP
					elif(_pos_tag == 'TO'):
						if(len(TO) > 4):
							_replacement_words = random.sample(TO, 5)
						else:
							_replacement_words = TO
					elif(_pos_tag == 'VBN'):
						if(len(VBN) > 4):
							_replacement_words = random.sample(VBN, 5)
						else:
							_replacement_words = VBN
					if _verbose:
						print("\tReplacement words chosen for the word %s: %s" %(_word, _replacement_words), file = _output_file_verbose)

					# word in the phrase is replaced with the replacement words and obtain the search totals
					# A maximum of 5 queries can be created, lets name them _search_query_1, 
					# 	_search_query_2, _search_query_3, _search_query_4, _search_query_5
					_search_query_1 = ""
					_search_query_2 = ""
					_search_query_3 = ""
					_search_query_4 = ""
					_search_query_5 = ""

					# Depending on the number of replacement words present in the list of _replacement_words, we'll have up to 5 queries
					# If there is atleast one word for replacement
					if len(_replacement_words) > 0:
						_search_query_1 = _search_phrase.replace(_word, _replacement_words[0].lstrip(' ').rstrip(' ').strip('\n'))
						print(_search_phrase, end = "", file = output_replacements_cache)
						print('|' + _search_query_1, end = "", file = output_replacements_cache)
						if 'B' in _collocation_corpora:
							#_search_total, _bing_api_key = bing_search_total(False, _search_query_1, _bing_api_key)
							search_queries[_search_query_1] = 0
							_n_gram_replacement_phrases[_search_phrase].append(_search_query_1)
						# Append the search total to the list iff it is non-zero (>= 0 always)
						#if not _search_total == 0:
						#	_list_of_search_result_totals.append(_search_total)
						#if _verbose:
						#	print("\t\tSearch query 1: \t%s\n\t\tSearch total: \t\t%d" %(_search_query_1, _search_total), file = _output_file_verbose)

						# If there are at least two words for replacement
						if len(_replacement_words) > 1:
							_search_query_2 = _search_phrase.replace(_word, _replacement_words[1].lstrip(' ').rstrip(' ').strip('\n'))
							print('|' + _search_query_2, end = "", file = output_replacements_cache)
							if 'B' in _collocation_corpora:
								#_search_total, _bing_api_key = bing_search_total(False, _search_query_2, _bing_api_key)
								search_queries[_search_query_2] = 0
								_n_gram_replacement_phrases[_search_phrase].append(_search_query_2)
							#if not _search_total == 0:
							#	_list_of_search_result_totals.append(_search_total)
							#if _verbose:
							#	print("\t\tSearch query 2: \t%s\n\t\tSearch total: \t\t%d" %(_search_query_2, _search_total), file = _output_file_verbose)

							# If there are at least 3 words for replacement
							if len(_replacement_words) > 2:
								_search_query_3 = _search_phrase.replace(_word, _replacement_words[2].lstrip(' ').rstrip(' ').strip('\n'))
								print('|' + _search_query_3, end = "", file = output_replacements_cache)
								if 'B' in _collocation_corpora:
									#_search_total, _bing_api_key = bing_search_total(False, _search_query_3, _bing_api_key)
									search_queries[_search_query_3] = 0
									_n_gram_replacement_phrases[_search_phrase].append(_search_query_3)
								#if not _search_total == 0:
								#	_list_of_search_result_totals.append(_search_total)
								#if _verbose:
								#	print("\t\tSearch query 3: \t%s\n\t\tSearch total: \t\t%d" %(_search_query_3, _search_total), file = _output_file_verbose)

								# If there are at least 4 words for replacement
								if len(_replacement_words) > 3:
									_search_query_4 = _search_phrase.replace(_word, _replacement_words[3].lstrip(' ').rstrip(' ').strip('\n'))
									print('|' + _search_query_4, end = "", file = output_replacements_cache)
									if 'B' in _collocation_corpora:
										#_search_total, _bing_api_key = bing_search_total(False, _search_query_4, _bing_api_key)
										search_queries[_search_query_4] = 0
										_n_gram_replacement_phrases[_search_phrase].append(_search_query_4)
									#if not _search_total == 0:
									#	_list_of_search_result_totals.append(_search_total)
									#if _verbose:
									#	print("\t\tSearch query 4: \t%s\n\t\tSearch total: \t\t%d" %(_search_query_4, _search_total), file = _output_file_verbose)

									# If there are at least 5 words for replacement
									if len(_replacement_words) > 4:
										_search_query_5 = _search_phrase.replace(_word, _replacement_words[4].lstrip(' ').rstrip(' ').strip('\n'))
										print('|' + _search_query_5, end = "", file = output_replacements_cache)
										if 'B' in _collocation_corpora:
											#_search_total, _bing_api_key = bing_search_total(False, _search_query_5, _bing_api_key)
											search_queries[_search_query_5] = 0
											_n_gram_replacement_phrases[_search_phrase].append(_search_query_5)
										#if not _search_total == 0:
										#	_list_of_search_result_totals.append(_search_total)
										#if _verbose:
										#	print("\t\tSearch query 5: \t%s\n\t\tSearch total: \t\t%d" %(_search_query_5, _search_total), file = _output_file_verbose)
						print("", file = output_replacements_cache)
				# A variable to point to the sum of search totals of the replacement phrases
				#_sum_of_replacement_search_totals = 0
				#try:
				#	for _search_total in _list_of_search_result_totals:
				#		_sum_of_replacement_search_totals += _search_total
				#except Exception as e:
				#	if _verbose:
				#		print("\tERROR while calculating the sum of replacement search totals\n\t\t%s" %(str(e)), file = _output_file_verbose)
				#		print("\tERROR while calculating the sum of replacement search totals\n\t\t%s" %(str(e)))

				# Average of all non-zero replacement search totals
				# _sum_of_replacement_search_totals / total number of replacement search totals
				if not len(_list_of_search_result_totals) == 0:
					_average_of_replacement_search_totals = float(_sum_of_replacement_search_totals) / len(_list_of_search_result_totals)
					if _verbose:
						print("\tList of non-zero search totals: %s" %(_list_of_search_result_totals), file = _output_file_verbose)
						print("\tAverage of all non-zero search totals: %f" %(_average_of_replacement_search_totals), file = _output_file_verbose)
				else:
					n_grams_not_collocations.append(_n_gram)
					if _verbose:
						print("\tThere are no non-zero search results.\n\tMoving on to the next n-gram ...", file = _output_file_verbose)
					continue

				# Calculating statistical value
				# If average is equals to zero OR search result of the phrase, we consider statistical_value of that phrase as zero,
				# to avoid 'division by zero' scenario
				if (_average_of_replacement_search_totals == 0) or (_phrase_search_totals == 0):
					_stat = 0
				else:
					_stat = 1 - (_average_of_replacement_search_totals / float(_phrase_search_totals))
					
				if _verbose:
					print("\tStatistical value: %f" %(_stat), file = _output_file_verbose)
				
	# Removing duplicates from the lists , statistical_collocations and n_grams_not_collocations
	#statistical_collocations = list(set(statistical_collocations))
	#n_grams_not_collocations = list(set(n_grams_not_collocations))

	#proxy_file_name = input("Name of the file containing proxies to use: ?")
	diction_search_hits_totals_from_file = {}
	with open("bing_search_totals.cache", 'r') as f:
		for line in f:
			phrase, hit = line.split('/----/')
			try:
				hit = ''.join(filter(lambda x: x.isdigit(), hit))
				diction_search_hits_totals_from_file[phrase] = int(hit)
			except Exception as e:
				print("Diction cache error for " + hit)
	search_queries_to_be_physicall_requested = []
	for _phrase in search_queries:
		if _phrase in diction_search_hits_totals_from_file:
			search_queries[_phrase] = diction_search_hits_totals_from_file[_phrase]
		else:
			search_queries_to_be_physicall_requested.append(_phrase)


	# Configure the settings for GoogleScraper
	

	if len(search_queries_to_be_physicall_requested) > 0:
		queries_with_quotes = [('"' + x + '"') for x in search_queries_to_be_physicall_requested]
		_bing_search = BingSearchAPI(self._bing_api_key)
		for bing_query in search_queries_to_be_physicall_requested:
			bing_query_with_quotes = '"' + bing_query + '"'
			search_queries[bing_query], self._bing_api_key = _bing_search.search_total(False, bing_query_with_quotes)
			

	doCalculation = True
	while doCalculation:

		#Set up the possible values of c
		good_input = False
		while not good_input:
			try:
				start_c_value, end_c_value = map(float, input("Please enter the constant 'c' values' range start and end: ").split(" "))
				_c_increment = float(input("Please enter the amount of increase on constant 'c' value: "))
				_c_decimal = eval(input("Please enter the number of decimals on constant 'c': "))
				good_input = True
			except Exception as e:
				print("ERROR Input, message: {0}".format(str(e)))
		string_values_of_c = []
		_c_temp = start_c_value
		while _c_temp <= end_c_value:
			string_values_of_c.append("{number:.{decimal}f}".format(number = _c_temp, decimal = _c_decimal))
			_c_temp += _c_increment
		print("Values of 'c' constant: " + str(string_values_of_c))

		for _string_c_value in string_values_of_c:
			_c_value = float(_string_c_value)

			if _verbose:
				print("\nNew standard c value for method 3: " + _string_c_value, file = _output_file_verbose)

			n_grams_not_collocations = []
			statistical_collocations = []
			
			for _n_gram, replacements in _n_gram_replacement_phrases.items():
				_list_of_search_result_totals = []
				_sum_of_replacement_search_totals = 0

				# Calculate the sum of the replacement phrases
				for replacement in replacements:
					number_result = search_queries[replacement]
					if number_result > 0:
						_list_of_search_result_totals.append(number_result)
						_sum_of_replacement_search_totals += number_result


				if not len(_list_of_search_result_totals) == 0:
					_average_of_replacement_search_totals = float(_sum_of_replacement_search_totals) / len(_list_of_search_result_totals)
					_phrase_search_total_dictionary[_n_gram] = search_queries[_n_gram]
					if search_queries[_n_gram] > _c_value * _average_of_replacement_search_totals:
						statistical_collocations.append(_n_gram)
						if _verbose:
							print("\Satisfied standard c value specified. Phrase added.\t" + _n_gram, file = _output_file_verbose)
					else:
						n_grams_not_collocations.append(_n_gram)

					if _verbose:
						print("\tList of non-zero search totals: %s" %(_list_of_search_result_totals), file = _output_file_verbose)
						print("\tAverage of all non-zero search totals: %f" %(_average_of_replacement_search_totals), file = _output_file_verbose)
				else:
					n_grams_not_collocations.append(_n_gram)
					if _verbose:
						print("\tThere are no non-zero search results.\n\tMoving on to the next n-gram ...", file = _output_file_verbose)
					continue

			# Output text file to save collocations
			_output_folder_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], '') + 'c' + _string_c_value + '/'

			#Check if the path exists, and creates if neccessary
			if not os.path.exists(_output_folder_path):
				os.makedirs(_output_folder_path)

			_output_file_path_statistical_collocations = _output_folder_path + 'collocations_statistic.txt'
			_output_file_statistical_collocations = open(_output_file_path_statistical_collocations, 'w')
			for _collocation in statistical_collocations:
				_output_file_statistical_collocations.write(_collocation + '\n')
			_output_file_statistical_collocations.close()
			if _verbose:
				print("\n\tMethod-3: Statistical - Collocations are written to the file:\n\t%s" %(_output_file_path_statistical_collocations), file = _output_file_verbose)

			# Output text file to save n-grams that are not collocations
			_output_file_path_statistical_not_collocations = _output_folder_path + 'not_collocations_statistical.txt'
			_output_file_statistical_not_collocations = open(_output_file_path_statistical_not_collocations, 'w')
			for _n_gram in n_grams_not_collocations:
				_output_file_statistical_not_collocations.write(_n_gram + '\n')
			_output_file_statistical_not_collocations.close()
			if _verbose:
				print("\n\tMethod-3: Statistical - N-grams that are not collocations are written to the file:\n\t%s" %(_output_file_path_statistical_not_collocations), file = _output_file_verbose)
		
		if _verbose:
			print("\n----------------------------------------------------------------------------------------", file = _output_file_verbose)
			print("\tMethod-3: Statistical technique - Extracting collocations:", file = _output_file_verbose)
			print("----------------------------------------------------------------------------------------\n\n", file = _output_file_verbose)
			print("\t\tMethod-3: Collocation extraction - successful")

		redo = input("Do you want to redo method 3 substitution with other c values? (Enter NOWAY to exit): ")
		if redo.upper() == "NOWAY":
			doCalculation = False
			if _verbose:
				_output_file_verbose.close()
			return statistical_collocations, n_grams_not_collocations, _phrase_search_total_dictionary