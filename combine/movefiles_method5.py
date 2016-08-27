import os
import shutil
from nltk.stem.snowball import SnowballStemmer
from src.n_grams import POS_tag_cleaner, ngrams_from_file_lines
import string
import re

#Typical path of a extracted collocation file:
#/home/an/Desktop/method 3/n-2/Bearing an Hourglass/Bearing an Hourglass.txt
#Root of the path, the path we ask for is: /home/an/Desktop/method 3/
#Title of the article we ask for is Bearing an Hourglass
#Name of the .txt we ask for is: collocations_statistic
#Path to store results is: /home/an/Desktop/method 3/results

table_remove_punctuation = str.maketrans("", "", string.punctuation)


def formatPath(s):
	return s.replace('//', '/')


def normal(input_string):
	x = filter(lambda x: x.strip() != '', input_string.split())
	x = ' '.join(map(lambda x: x.strip(), x))
	x = POS_tag_cleaner(x)
	x = "".join(filter(lambda h: h in string.printable, x))
	x = x.lower()
	return x.translate(table_remove_punctuation).strip(' ')


def sub(unmodifiedSet):
	subcolloSet = set()

	for x in unmodifiedSet:
		if x != '':
			subcolloSet.add(x)
			words = x.split()
			for i in range(2, len(words)):
				for j in range(0, len(words) - i + 1):
					sub = ' '.join(words[j: (j + i)])
					subcolloSet.add(normal(sub))

	return (unmodifiedSet | subcolloSet)


def set_of_collocations_from_file(file_path):
	unmodifiedSet = set(map(normal, ngrams_from_file_lines(file_path, 
		injected_tagger = final_tagger)))
	return unmodifiedSet, sub(unmodifiedSet)


path_source = input("Root path: ")
file_name = input("Common name of the .txt files containing extracted collocations: ")

path_dest = input("Destination path: ")

range_input = input("Range of the n in n-grams: ")
start = int(range_input.split()[0])
end = int(range_input.split()[1])



_descricriptoin = input("Description wanted: ")

_2nd_description = "Method 5 Web search and independence, using pipeline with method 1 and 2"
doSetUp = True
while doSetUp:
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
	while _c_temp <= end_c_value and _c_increment > 0:
		string_values_of_c.append("{number:.{decimal}f}".format(number = _c_temp, decimal = _c_decimal))
		_c_temp += _c_increment
	print("Values of 'c' constant: " + str(string_values_of_c))

	#set up the possible values of power
	print('\n')
	good_input = False
	while not good_input:
		try:
			start_p_value, end_p_value = map(float, input("Please enter the power values' range start and end: ").split(" "))
			_p_increment = float(input("Please enter the amount of increase on power value: "))
			_p_decimal = eval(input("Please enter the number of decimals on power value: "))
			good_input = True
		except Exception as e:
			print("ERROR Input, message: {0}".format(str(e)))
	string_values_of_p = []
	_p_temp = start_p_value
	while _p_temp <= end_p_value and _p_increment > 0:
		string_values_of_p.append("{number:.{decimal}f}".format(number = _p_temp, decimal = _p_decimal))
		_p_temp += _p_increment
	print("Values of power: " + str(string_values_of_p))

	#Ask to redo or continue
	_redo_answer = input("Enter Y if you want to continue with the calculation. We re-setup the values otherwise: ")
	if _redo_answer.lower() == 'y':
		doSetUp = False

highest_f_score_sub = 0
highest_p_sub = 0
highest_c_sub = 0

highest_f_score_unm = 0
highest_p_unm = 0
highest_c_unm = 0

doCalculation = True
save_output_string_unmo = ''
save_output_string_subc = ''

training_sents = brown.tagged_sents()
patterns = [ # for regexp tagger
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*es$', 'VBZ'),
    (r'.*ould$', 'MD'),
    (r'.*\'s$', 'POS'),
    (r'.*s$', 'NNS'),
    (r'(The|the|A|a|An|an)$', 'AT'),
    (r'.*able$', 'JJ'),
    (r'.*ly$', 'RB'),
    (r'.*s$', 'NNS'),
    (r'.*', 'NN')]
default_tagger = nltk.DefaultTagger('NN')
regexp_tagger = nltk.RegexpTagger(patterns, backoff=default_tagger)
unigram_tagger = nltk.UnigramTagger(training_sents, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(training_sents, backoff=unigram_tagger)
trigram_tagger = nltk.TrigramTagger(training_sents, backoff=bigram_tagger)        
final_tagger = trigram_tagger

while doCalculation:
	folder_name = input("\nArticle folder name: ").strip(" ")
	_annotation_path = formatPath(path_dest + "/" + folder_name + "/annotation.txt")

	_2nd_description = "Method 5"

	unmodifiedAntSet = set([])
	subCollocaAntSet = set([])
	unmodifiedAntSet, subCollocaAntSet = set_of_collocations_from_file(_annotation_path)

	#Two seperate evaluation ways of 
	#1st Method: all subcollocatoins of a phrases are added to collocation set
	count = 0
	number_of_instances = len(string_values_of_p) * len(string_values_of_c)
	count_p = 0


	#2 collocations set from method 1 and 2
	subcollocaExtSet_1_2 = set([])
	unmodifiedExtSet_1_2 = set([])
	for i in range(start, end + 1):
		#method 2 file
		s_path = formatPath(path_source + "/n-{n}/{article}/{filename}.txt".format(n = str(i), article = folder_name, 
			filename = 'collocations_title_url'))
		temp_unmo_set, temp_subcol_set = set_of_collocations_from_file(s_path)
		unmodifiedExtSet_1_2.update(temp_unmo_set)
		subcollocaExtSet_1_2.update(temp_subcol_set)
		#method 1 file
		s_path = formatPath(path_source + "/n-{n}/{article}/{filename}.txt".format(n = str(i), article = folder_name, 
			filename = 'collocations_wordnet'))
		temp_unmo_set, temp_subcol_set = set_of_collocations_from_file(s_path)
		unmodifiedExtSet_1_2.update(temp_unmo_set)
		subcollocaExtSet_1_2.update(temp_subcol_set)

	for p_string in string_values_of_p:
		count_c = 0
		for c_string in string_values_of_c:
			count += 1
			print("{c}/{d}".format(c = count, d = number_of_instances))

			_folder_dest = formatPath(path_dest + "/{article}/p{p}/c{c}/".format(article = folder_name, p = p_string, c = c_string))
			if not os.path.exists(_folder_dest):
				os.makedirs(_folder_dest)

			#2 general collocation set
			subcollocaExtSet = subcollocaExtSet_1_2.copy()
			unmodifiedExtSet = unmodifiedExtSet_1_2.copy()


			for i in range(start, end + 1):
				#method 5 file
				s_path = formatPath(path_source + "/n-{n}/{article}/p{p}/{c}/{filename}.txt".format(n = str(i), article = folder_name, 
					p = p_string, c = c_string, filename = file_name))

				temp_unmo_set, temp_subcol_set = set_of_collocations_from_file(s_path)
				subcollocaExtSet.update(temp_subcol_set)
				unmodifiedExtSet.update(temp_unmo_set)
									

				
			_result_file = formatPath(_folder_dest + "result.txt")
			with open(_result_file, 'w') as f:
				print("Title of article: {title}".format(title = folder_name), file = f)
				print("1st description: {descri}".format(descri = _descricriptoin), file = f)
				print(_2nd_description + "\n", file = f)
				
				try:
					print("Unmodified, NO auto-adding sub-colocations:", file = f)
					extLength = len(unmodifiedExtSet)
					print(" Extraction size: %d" % (extLength), file = f)
					antLength = len(unmodifiedAntSet)
					print(" Annotation size: %d" % (antLength), file = f)
					interLength = len(unmodifiedAntSet.intersection(unmodifiedExtSet))
					print(" Intersection size: %d" % (interLength), file = f)
					precision = float(interLength) / (extLength)
					print(" Precision: %f" % (precision), file = f)
					recall = float(interLength) / (antLength)
					print(" Recall: %f" % (recall), file = f)
					f_score = 2 * precision * recall  / (precision + recall)
					print(" F1 score: %f" % (f_score), file = f)
					if highest_f_score_unm < f_score:
						highest_f_score_unm = f_score
						highest_p_unm = p_string
						highest_c_unm = c_string
				except Exception as e:
					print("Unmodified calculation error: %s" % (str(e)))
					f_score = 0
				print("\n", file = f)

				try:
					print("Sub-collocation, including all sub-collocations:", file = f)
					extLength = len(subcollocaExtSet)
					print(" Extraction size: %d" % (extLength), file = f)
					antLength = len(subCollocaAntSet)
					print(" Annotation size: %d" % (antLength), file = f)
					interLength = len(subCollocaAntSet.intersection(subcollocaExtSet))
					print(" Intersection size: %d" % (interLength), file = f)
					precision = float(interLength) / (extLength)
					print(" Precision: %f" % (precision), file = f)
					recall = float(interLength) / (antLength)
					print(" Recall: %f" % (recall), file = f)
					f_score = 2 / (1 / precision + 1 / recall)
					print(" F1 score: %f" % (f_score), file = f)
					if highest_f_score_sub < f_score:
						highest_f_score_sub = f_score
						highest_p_sub = p_string
						highest_c_sub = c_string
				except Exception as e:
					print("Subcollocation calculation error: %s" % (str(e)))
					f_score = 0
			count_c += 1
		count_p += 1
	highest_result = formatPath(path_dest + "/{article}/highest_result.txt".format(article = folder_name))
	with open(highest_result, 'w') as f:
		print("Unmodified highest f: {0}".format(highest_f_score_unm), file = f)
		print("Unmodified highest f: {0}".format(highest_f_score_unm))
		print("P: {p} C: {c}".format(p = highest_p_unm, c = highest_c_unm), file = f)
		print("P: {p} C: {c}".format(p = highest_p_unm, c = highest_c_unm))

		print("Subcollocation highest f: {0}".format(highest_f_score_sub), file = f)
		print("Subcollocation highest f: {0}".format(highest_f_score_sub))
		print("P: {p} C: {c}".format(p = highest_p_sub, c = highest_c_sub), file = f)
		print("P: {p} C: {c}".format(p = highest_p_sub, c = highest_c_sub))


	x = []
	y = []
	y_increment = len(string_values_of_p) // 10
	x_increment = len(string_values_of_c) // 10
	for i in range(0, len(string_values_of_p)):
		if i % y_increment == 0:
			y.append('p' + string_values_of_p[i])
		else:
			y.append('')

	for i in range(0, len(string_values_of_c)):
		if i % x_increment == 0:
			x.append('c' + string_values_of_c[i])
		else:
			x.append('')

	redo = input("Do you want to redo with another article? (Enter NO to exit): ")
	if redo.upper() == "NO":
		doCalculation = False


