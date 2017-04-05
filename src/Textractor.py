#! /usr/bin/env python3.5
"""

@author: Vasanthi Vuppuluri
Date created: May 5, 2015
Last Date modified: May 13, 2015



----------------------------------------------------------------
Textractor_V1.py - METHODS 
----------------------------------------------------------------

Can extract N-grams, Collocations and MWEs. Below is a brief description of the methods involved

pos_tagged_ngrams():
- Extracts n-grams and POS tags the words before extraction

collocations():
- Extracts collocations
- Considers whether POS restrictions are to be implied

Collocations_Method_1():
- Implementation of Dictionary based technique

Collocations_Method_2():
- Implementation of Title_Url based technique

Collocations_Method_3():
- Implementation of statistical value technique
- Takes into consideration which resource is to be considered for obtaining search results
    From, Bing search API, 20 News groups, ANC, BNC, DUC, reuters, voice, Wiki 2006, Wiki 2007
    Options:
        - If Bing is chosen only Bing is searched for as it takes a large amount of time for the program to fetch search results
        - Rest of the index resources can be chosen individually or in combination

Collocations_Method_5():
- Implementation of probability based technique
- Both with and without n! adjustment are implemented

MWE_extraction():
- Implementation of MWE extraction technique




----------------------------------------------------------------
Textractor_V1.py - EXECUTION FLOW 
----------------------------------------------------------------


----------------------------------------------------------------

"""

from .bing_search_api import BingSearchAPI
from .collocations_method_1 import Collocations_Method_1
# from collocations_method_2 import Collocations_Method_2
from .collocations_method_2_parallel import Collocations_Method_2_paralllel
from .collocations_method_3 import Collocations_Method_3
from .collocations_method_5_V3 import Collocations_Method_5
from .n_grams import ngrams_from_file_lines
from .pos_tagger import POS_tag_cleaner
from .n_grams_old import pos_tagged_ngrams_from_file, pos_tagged_ngrams_from_sentences
from .Idiom.MWE_well_defined import mwe
import nltk
import os
import re
import string
import subprocess
import sys
import argparse
import os.path
from functools import partial
import logging


class CollocationExtractor:


    def __init__(self):
        self._normal_mode = False
        self._extract_n_grams = False
        self._collocation_method_1 = False
        self._collocation_method_2 = False
        self._collocation_method_3 = False
        self._collocation_method_5 = False
        self._collocation_method_5_version = 1
        self._input_file_path = ""
        self._collocation_corpora = ['B']
        self._stop_word_removal = False
        self._which_phrase_extraction = ''
        self._extract_collocations = False
        self._extract_n_grams = False
        self._bing_api_key = "Temp"
        self._apply_POS_restrictions = False
        self._n_value_for_ngram_extraction = 0
        self._verbose = False
        self._bing_api_key = ''
        self._allowed_range_of_n = range(2, 9)


    @classmethod
    def with_collocation_pipeline(cls, pipeline = 'T1', bing_key = "", pos_check = False, verbose = False):
        textractor = cls()

        textractor._extract_collocations = True

        if pipeline == "T1":
            textractor._collocation_method_1 = True
            textractor._collocation_method_2 = True
            textractor._collocation_method_3 = False
            textractor._collocation_method_5 = True
            textractor._collocation_method_5_version = 1
        elif pipeline == "T2":
            textractor._collocation_method_1 = True
            textractor._collocation_method_2 = True
            textractor._collocation_method_3 = False
            textractor._collocation_method_5 = True
            textractor._collocation_method_5_version = 2
        elif pipeline == "SUB":
            textractor._collocation_method_1 = True
            textractor._collocation_method_2 = True
            textractor._collocation_method_3 = True
            textractor._collocation_method_5 = False

        textractor._bing_api_key = bing_key
        textractor._apply_POS_restrictions = pos_check
        textractor._verbose = verbose
        return textractor


    def get_collocations_of_length(self, sentences = [], length = 2):
        n_value = length
        _n_grams_from_input_text_file = pos_tagged_ngrams_from_sentences(sentences, n_value, False, False)


        final_collocations = []

        if self._extract_collocations:
            if self._collocation_method_1:
                # Extracting Collocations - Method-1 - Dictionary search
                wordnet_collocations, n_grams_not_collocations = Collocations_Method_1(_n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, self._verbose)
                _n_grams_from_input_text_file = n_grams_not_collocations
                final_collocations.extend(wordnet_collocations)


            if self._collocation_method_2:
                # Extracting Collocations - Method-2 - Bing search API: Title_Url based technique
                title_url_collocations, n_grams_not_collocations = Collocations_Method_2_paralllel(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, self._verbose)
                _n_grams_from_input_text_file = n_grams_not_collocations
                final_collocations.extend(title_url_collocations)

            if self._collocation_method_3:
                # Extracting Collocations - Method-3 - Statistical technique
                # self._collocation_corpora is a list of corpora selected by the user
                # Depending upon the _corpus selected, that paticular corpus will be used for obtaining search result totals
                statistical_collocations, n_grams_not_collocations, _phrase_search_total_dictionary = Collocations_Method_3(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._collocation_corpora, self._apply_POS_restrictions, self._verbose)
                final_collocations.extend(statistical_collocations)


            if self._collocation_method_5:
                # Extracting collocations - Probability technique
                # If Method-3 was already called, we have a search totals of the input phrases already, else, we need to obtain phrase totals before we proceed

                
                _corpus = 'Bing'
                _bing_search = BingSearchAPI(self._bing_api_key)
                if not self._collocation_method_3:
                    # A dictionary to store phrase totals
                    _phrase_search_total_dictionary = {}
                    # Obtain the phrase search totals
                    count = 0
                    length = len(_n_grams_from_input_text_file)
                    if self._verbose:
                        print(length)
                    int_percent = 0
                    for _n_gram in _n_grams_from_input_text_file:
                        count += 1
                        if int((count * 100) / length) > int_percent:
                            int_percent = int((count * 100) / length)
                            if self._verbose:
                                print(str(int_percent) + "%")
                        # Remove the POS tags attached
                        _n_gram = POS_tag_cleaner(_n_gram)
                        _phrase_search_total_dictionary[_n_gram], self._bing_api_key = _bing_search.search_total(False, _n_gram)
                        #if self._verbose:
                        #    print(_n_gram + '\t' + str(_phrase_search_total_dictionary[_n_gram]), file = _output_file_verbose)

                # A dictionary to store the search results of individual words in the n-grams
                count = 0
                int_percent = 0
                _individual_word_hit_results = {}
                for _n_gram in _n_grams_from_input_text_file:
                    count += 1
                    if int((count * 100) / length) > int_percent:
                        int_percent = int((count * 100) / length)
                        if self._verbose:
                            print(int_percent)
                    ## TODO: don't search for words that appear only in n-grams with wrong POS tags
                    # Remove the POS tags attached
                    _n_gram = POS_tag_cleaner(_n_gram)
                    # Obtain a list of word in the n-gram
                    _words_in_n_gram = _n_gram.split(' ')

                    for _word in _words_in_n_gram:
                        _word = _word.lstrip(' ').rstrip(' ').strip('\n')
                        if not _word in _individual_word_hit_results:
                            _individual_word_hit_results[_word], self._bing_api_key = _bing_search.search_total(False, _word)
                            #if self._verbose:
                            #    print(_word + '\t' + str(_individual_word_hit_results[_word]), file = _output_file_verbose)

                # A file to write the search totals of individual words and n-gram phrases
                output_file_path_word_totals = str(self._input_file_path).replace(self._input_file_path.split('/')[-1], 'Bing_Individual_word_totals.txt')
                output_file_word_totals = open(output_file_path_word_totals, 'w')
                for _word in _individual_word_hit_results:
                    output_file_word_totals.write(_word + '\t' + str(_individual_word_hit_results[_word]) + '\n')
                output_file_word_totals.close()

                output_file_path_phrase_totals = str(self._input_file_path).replace(self._input_file_path.split('/')[-1], 'Bing_Phrase_totals.txt')
                output_file_phrase_totals = open(output_file_path_phrase_totals, 'w')
                for _phrase in _phrase_search_total_dictionary:
                    output_file_phrase_totals.write(_phrase + '\t' + str(_phrase_search_total_dictionary[_phrase]) + '\n')
                output_file_phrase_totals.close()

                # When other corpora are used, we need to pass the original search phrases as well, as some of the words will be replaced by a
                #       '?' by lucene parser. But when Bing is being used, since, we don't need to pass the search phrases, we pass an empty string
                #       The same is repeated with individual words from the input phrases as well
                original_input_queries_file = ""
                individual_words = ""

                # Call collocations Method-5
                independence_collocations, self._bing_api_key = Collocations_Method_5(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, _phrase_search_total_dictionary, _individual_word_hit_results, _corpus, original_input_queries_file, individual_words, self._verbose, _version = 1)
                final_collocations.extend(independence_collocations)

        # temporary fix for ["John likes the blue house at the end of the street."] input
        final_collocations = list(map(POS_tag_cleaner, final_collocations))

        return final_collocations




    def is_valid_file(self, parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return arg

    def custom_verbose_print(self):

        def custom_print(string_to_print, open_file = None, 
            console = True):
            print(string_to_print, file = open_file)
            if console:
                print(string_to_print)

        return custom_print if self._verbose else lambda *a, **k: None


    def argument_parser(self):
        if not len(sys.argv) > 1:
            self._normal_mode = True
            return

        parser = argparse.ArgumentParser()

        running_mode = parser.add_argument_group(title = "What to do?")

        running_mode.add_argument("-collocation",
                        help=("Collocation extraction. "
                            "Can be run with n-gram extracted from sentences or"
                            " run with n-grams on each line."),
                        action="store_true")

        running_mode.add_argument("--ngram", 
                        help=("n-gram extraction from sentences. "
                        "Can be ran with collocation extraction or alone."
                        "This option must be supplied with an 'n' value."),
                        action="store_true")


        methods_to_run = parser.add_argument_group(
            title = "What methods to be ran?")

        methods_to_run.add_argument("-method1", 
                        help="Method 1: Dictionary based",
                        action="store_true")
        methods_to_run.add_argument("-method2", 
                        help="Method 2: Web title based",
                        action="store_true")
        methods_to_run.add_argument("-method3", 
                        help="Method 3: Substitution based",
                        action="store_true")
        methods_to_run.add_argument("-method5", 
                        help="Method 5: Independence based",
                        action="store_true")

        parser.add_argument("-i", dest="filename", required=True,
                        help="Input file path.", metavar="FILE",
                        type=lambda x: self.is_valid_file(parser, x))
        parser.add_argument("-n", dest="nvalue", required=False,
                        help="n-value for n-grams extraction",
                        type=int, choices = range(2, 9))
        parser.add_argument("-key", dest="bingkey", required=True,
                        help="Bing API key", type=str)


        options = parser.add_argument_group(title = 'Optional settings')

        options.add_argument("-v", "--verbose", help="verbose output.",
                        action="store_true")
        options.add_argument("--pos", help="pos-check filter",
                        action="store_true")
        options.add_argument("--stopwords", help="stop words removal",
                        action="store_true")



        args = parser.parse_args()


        if args.collocation:
            self._extract_collocations = True
            if self._verbose:
                print("Collocation extraction turned on")

        if args.ngram:
            self._extract_n_grams = True
            if self._verbose:
                print("Extract n-grams from sentences, temporarily this.")
        else:
            self._extract_n_grams = False


        if args.method1:
            if self._verbose:
                print("Method 1 Dictionary enabled")
            self._collocation_method_1 = True

        if args.method2:
            if self._verbose:
                print("Method 2 web title enabled")
            self._collocation_method_2 = True            

        if args.method3:
            if self._verbose:
                print("Method 3 substitution enabled")
            self._collocation_method_3 = True

        if args.method5:
            if self._verbose:
                print("Method 5 independence enabled")
            self._collocation_method_5 = True

        if args.bing:
            self._collocation_corpora = ['B']
            if self._verbose:
                print("Bing corpura included, temporarily bing api key not needed")
        elif args.other:
            self._collocation_corpora = args.other
            if self._verbose:
                print("Corpora used: ", end = '')
                print(self._collocation_corpora)


        self._apply_POS_restrictions = args.pos
        if self._apply_POS_restrictions:
            if self._verbose:
                print("POS enabled")

        self._stop_word_removal = args.stopwords
        if self._stop_word_removal:
            if self._verbose:
                print("Stop-words removal enabled")

        self._input_file_path = args.filename
        if self._verbose:
            print("File location: {}".format(self._input_file_path))

        if args.nvalue:
            self._n_value_for_ngram_extraction = args.nvalue
            if self._verbose:
                print("N-value: %d" % (self._n_value_for_ngram_extraction))

        self._verbose = args.verbose
        if self._verbose:
            print("Verbose output turned on.")

    def normal_run(self):
        if not self._normal_mode:
            return

        self._which_phrase_extraction = input((
            "\nA series of questions are to be answered to initiate the "
            "execution process!\nWhich phrase?\n\t"
            "Select C for collocation extraction\n\t"
            "Select N for n-gram extraction\nSelection = ")).upper()

        if not self._which_phrase_extraction in ['C', 'N']:
            print((
                "\nWrong selection.\n"
                "Please choose one character from {C, N}.\n"
                "Exiting the program...\n"))
            sys.exit(0)    

        if self._which_phrase_extraction == 'C':
            self._extract_collocations = True
        elif self._which_phrase_extraction == 'N':
            self._extract_n_grams = True


        if self._extract_collocations:
            self._extract_n_grams = (input((
                "\nYou chose to extract collocations.\n"
                "Do you wish to extract n-grams "
                "before extracting collocations? (Y|N)\n"
                "Choose Y if your input file consits of sentences and "
                "you want to extract collocation phrases of length 'n'.\n"
                "If your input text file has phrases with one phrase per "
                "line and you wish to determine if a phrase is a "
                "collocation, choose N.\n"
                "Selection = ")).upper() == 'Y')

            self._collocation_method_1 = (input((
                "\nPlease select which of the techniques "
                "you want to use to extract collocations:\n"
                "Method-1: Dictionary based (Y|N) ")).upper() == 'Y')

            self._collocation_method_2 = (input((
                "Method-2: Title-Url based (Y|N) ")).upper() == 'Y')
            if self._collocation_method_2:
                self._bing_api_key = input((
                    "\tMethod-2 uses Bing search API internally.\n"
                    "\tPlease enter a Bing search API key: "))

            self._collocation_method_3 = (input((
                "Method-3: Statistical technique (Y|N) ")).upper() == 'Y')
            if self._collocation_method_3:
                if not self._bing_api_key:
                    self._bing_api_key = input(
                        "\tPlease enter a Bing search API key: ")

            # Method-4 is implemented along with method-3 as a default
            _collocation_method_4 = ''
            print("Method-4: Mean and Standard deviation (Y|N) Y")

            self._collocation_method_5 = (input((
                "Method-5: Probability based (Y|N) ")).upper() == 'Y')
            if self._collocation_method_5:
                if not self._bing_api_key:
                    self._bing_api_key = input(
                        "\tPlease enter a Bing search API key: ")

            self._apply_POS_restrictions = (input((
                "Do you want to apply POS restrictions on the phrase "
                "in determining if the phrase is a collocation? (Y|N) "
                )).upper() == 'Y')


        if self._extract_n_grams:
            try:
                self._n_value_for_ngram_extraction = int(input(("\n"
                    "Enter an 'n' (> 1) value to extract n-grams from the"
                    "input text file. 'n' should be a positive integer.\n"
                    "Selection = ")))
                if (self._n_value_for_ngram_extraction not in 
                    self._allowed_range_of_n):
                    print(("\nERROR: Please choose a positive integer > "
                        "1 for 'n'.\nExiting the program...\n"))
                    sys.exit(0)
            except Exception as e:
                print( ("\n"
                    "ERROR: Please choose a positive integer for 'n'!\n"
                    "{}\nExiting the program...\n".format(str(e))) )
                sys.exit(0)
            else:
                self._stop_word_removal = (input((
                    "Do you want to remove stopwords "
                    "from the input file? (Y|N) ")).upper()  == 'Y')


        self._input_file_path = input(("\n"
            "A lot of intermediate files will be created "
            "during the execution process.\n"
            "Please make sure you have your input file in "
            "a seperate directory.\n"
            "Input file: "))

        self._verbose = ((input(("Would you like to see the detailed "
                        "execution process? (Y|N) ")).upper() ) == 'Y')



    def main(self):
        self.argument_parser()
        self.normal_run()

        _output_file_verbose = None
        if self._verbose:
            verbose_file_path = (self._input_file_path.rpartition('/')[0] + 
                '/verbose.txt')
            print(("Step-by-step execution process is written to the file, {}"
                .format(verbose_file_path)))
            _output_file_verbose = open(verbose_file_path, 'w')

        verboseprint = partial(self.custom_verbose_print(), 
            open_file = _output_file_verbose)

        if self._extract_n_grams:
            # Extracting n-grams from the input text file
            _n_grams_from_input_text_file, self._input_file_path = (
                pos_tagged_ngrams_from_file(
                    self._input_file_path, 
                    self._n_value_for_ngram_extraction, 
                    self._stop_word_removal, 
                    self._verbose))
        else:
            _n_grams_from_input_text_file = (
                ngrams_from_file_lines(
                    self._input_file_path,
                    output = True,
                    verboseprint = verboseprint))

                
        if self._extract_collocations:
            if self._collocation_method_1:
                # Extracting Collocations - Method-1 - Dictionary search
                wordnet_collocations, n_grams_not_collocations = Collocations_Method_1(_n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, self._verbose)
                _n_grams_from_input_text_file = n_grams_not_collocations

            if self._collocation_method_2:
                # Extracting Collocations - Method-2 - Bing search API: Title_Url based technique
                title_url_collocations, n_grams_not_collocations = Collocations_Method_2_paralllel(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, self._verbose)
                _n_grams_from_input_text_file = n_grams_not_collocations

            if self._collocation_method_3:
                # Extracting Collocations - Method-3 - Statistical technique
                # self._collocation_corpora is a list of corpora selected by the user
                # Depending upon the _corpus selected, that paticular corpus will be used for obtaining search result totals
                statistical_collocations, n_grams_not_collocations, _phrase_search_total_dictionary = Collocations_Method_3(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._collocation_corpora, self._apply_POS_restrictions, self._verbose)

            if self._collocation_method_5:
                # Extracting collocations - Probability technique
                # If Method-3 was already called, we have a search totals of the input phrases already, else, we need to obtain phrase totals before we proceed

                
                _corpus = 'Bing'
                _bing_search = BingSearchAPI(self._bing_api_key)
                if not self._collocation_method_3:
                    # A dictionary to store phrase totals
                    _phrase_search_total_dictionary = {}
                    # Obtain the phrase search totals
                    count = 0
                    length = len(_n_grams_from_input_text_file)
                    print(length)
                    int_percent = 0
                    for _n_gram in _n_grams_from_input_text_file:
                        count += 1
                        if int((count * 100) / length) > int_percent:
                            int_percent = int((count * 100) / length)
                            print(str(int_percent) + "%")
                        # Remove the POS tags attached
                        _n_gram = POS_tag_cleaner(_n_gram)
                        _phrase_search_total_dictionary[_n_gram], self._bing_api_key = _bing_search.search_total(False, _n_gram)
                        if self._verbose:
                            print(_n_gram + '\t' + str(_phrase_search_total_dictionary[_n_gram]), file = _output_file_verbose)

                # A dictionary to store the search results of individual words in the n-grams
                count = 0
                int_percent = 0
                _individual_word_hit_results = {}
                for _n_gram in _n_grams_from_input_text_file:
                    count += 1
                    if int((count * 100) / length) > int_percent:
                        int_percent = int((count * 100) / length)
                        print(int_percent)
                    ## TODO: don't search for words that appear only in n-grams with wrong POS tags
                    # Remove the POS tags attached
                    _n_gram = POS_tag_cleaner(_n_gram)
                    # Obtain a list of word in the n-gram
                    _words_in_n_gram = _n_gram.split(' ')

                    for _word in _words_in_n_gram:
                        _word = _word.lstrip(' ').rstrip(' ').strip('\n')
                        if not _word in _individual_word_hit_results:
                            _individual_word_hit_results[_word], self._bing_api_key = _bing_search.search_total(False, _word)
                            if self._verbose:
                                print(_word + '\t' + str(_individual_word_hit_results[_word]), file = _output_file_verbose)

                # A file to write the search totals of individual words and n-gram phrases
                output_file_path_word_totals = str(self._input_file_path).replace(self._input_file_path.split('/')[-1], 'Bing_Individual_word_totals.txt')
                output_file_word_totals = open(output_file_path_word_totals, 'w')
                for _word in _individual_word_hit_results:
                    output_file_word_totals.write(_word + '\t' + str(_individual_word_hit_results[_word]) + '\n')
                output_file_word_totals.close()

                output_file_path_phrase_totals = str(self._input_file_path).replace(self._input_file_path.split('/')[-1], 'Bing_Phrase_totals.txt')
                output_file_phrase_totals = open(output_file_path_phrase_totals, 'w')
                for _phrase in _phrase_search_total_dictionary:
                    output_file_phrase_totals.write(_phrase + '\t' + str(_phrase_search_total_dictionary[_phrase]) + '\n')
                output_file_phrase_totals.close()

                # When other corpora are used, we need to pass the original search phrases as well, as some of the words will be replaced by a
                #       '?' by lucene parser. But when Bing is being used, since, we don't need to pass the search phrases, we pass an empty string
                #       The same is repeated with individual words from the input phrases as well
                original_input_queries_file = ""
                individual_words = ""

                # Call collocations Method-5
                self._bing_api_key = Collocations_Method_5(self._bing_api_key, _n_grams_from_input_text_file, self._input_file_path, self._apply_POS_restrictions, _phrase_search_total_dictionary, _individual_word_hit_results, _corpus, original_input_queries_file, individual_words, self._verbose)

        _output_file_verbose.close()

class IdiomExtractor:

    def __init__(self, debug_level = logging.INFO):
        logger = logging.getLogger(__name__)
        logger.setLevel(debug_level)

    def get_idioms_of_length(self, sentences = [], length = 2, method = "I"):
        n_value = length
        _n_grams_from_input_text_file = pos_tagged_ngrams_from_sentences(sentences, n_value, False, False)

        result_idioms = mwe(_n_grams_from_input_text_file, method)
        non_pos_idioms = list(map(POS_tag_cleaner, result_idioms))

        return non_pos_idioms


                    
if __name__ == "__main__":
    textractor = CollocationExtractor()
    textractor.main()
