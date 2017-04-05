"""
    Created by An Nguyen
    Oct, 2015
    Modified version of method 2, attempt to do parallel programming.
"""


#!/usr/bin/Python2
# --coding:utf-8--

import os
from bs4 import BeautifulSoup
from .bing_search_api import BingSearchAPI
import snowballstemmer
import unicodedata
import re
import multiprocessing as mp
import requests
import urllib
import time
from random import sample
from .pos_tagger import POS_tag_cleaner
from .bing_search_api import InvalidKeyException

# Python list with words synonymous to 'Wikipedia', 'dictionary', 'definition'
_list_of_synonymous_words = ['dictionary', 'lexicon', 'definition', 'meaning', 'unabridged', 'gazetteer',
'spellchecker', 'spellingchecker', 'thesaurus', 'synonymfinder', 'wordfinder', 'wikipedia', 'investorwords',
'investopedia', 'wiktionary']


#Changing isalnum to fit Python3 syntax
def isalphanum(input_value):
    try:
        result = input_value.isalnum()
    except Exception as e:
        return False
    return result

#Parallel the requests
def parallel_request(_search_title, _search_url, file_path, x, _n_gram_lower, _n_gram_lower_no_spaces, _verbose):
    gram_match = False

    
    #_search_title = ""
    #_search_title = _search_titles[x]
    _search_title_lower_case = _search_title.lower()
    #_search_title_lower_case_no_spaces = "".join(_char for _char in _search_title_lower_case if _char.isalnum())
    _search_title_lower_case_no_spaces = "".join(filter(isalphanum, _search_title_lower_case))
    #_search_url = ""
    #_search_url = _search_urls[x]
    _search_url_lower_case = _search_url.lower()
    #_search_url_lower_case_no_spaces = "".join(_char for _char in _search_url_lower_case if _char.isalnum())
    _search_url_lower_case_no_spaces = "".join(filter(isalphanum, _search_url_lower_case))

    _output_file_string = ""

    if _verbose:
        _output_file_string += ("\t%d:\n\tSearch title: %s\n\tSearch Url: %s" %(x + 1, _search_title, _search_url))
    for _synonym in _list_of_synonymous_words:
        _synonym_match = False
        # Check if _synonym is present in the tile
        _title_match = re.search(_synonym, _search_title_lower_case_no_spaces)
        # check if _synonym is present in the url
        _url_match = re.search(_synonym, _search_url_lower_case_no_spaces)
        # If a match is found either in title or the url, open the link and check if the 
        # <title> </title> tag from the html has a match with the keyword
        if _title_match:
            _synonym_match = True
        elif _url_match:
            _synonym_match = True
        else:
            continue
        if _synonym_match:
            # Reading HTML from url
            req = requests.Session()
            _text_from_title = ""
            requests.max_redirects = 3
            count = 0
            try:
                r = req.get(_search_url, timeout = 4.0, stream = True)
                text = ''
                for chunk in r.iter_content(chunk_size = 512):
                    count += 1
                    soup = BeautifulSoup(chunk, 'lxml')
                    #print(str(soup) + '\n')
                    try:
                        _text_from_title = soup.find('title').text
                    except Exception as e:
                        #print('test')
                        if count >= 4:
                            break
                        continue
                    break   
            except Exception as e:
                print("\tException - Method-2 - Reading HTML%s\n" %(str(e)))
                print("-----------------\n" + _search_url + "\n---------------\n")

            req.close()
            # Extracting text in between <h1> tag
            try:
                # Comments are to excluded, this part is to coded
                
                #_text_from_title = _beautiful_html.find('h1').text
                #print(_beautiful_html.find('h1').text + "\n")
                #print("sss" + _beautiful_html.title.string + '\n')
                #_text_from_title = _beautiful_html.title.string0
                # Remove any non-ascii characters from the text extracted
                _text_from_title_ascii_only = "".join(_char for _char in _text_from_title if ord(_char)<128)
                _text_from_title_ascii_only = _text_from_title_ascii_only.lower()
            except:
                # If failed to extract text from <h1>
                _text_from_title_ascii_only = ""

            """
            # ------- FOR Stemmed match ------------
            # Stem the title text extracted and the n-gram phrase
            # If the stemmed n-gram phrase is present in the stemmed title, 
            # that n-gram phrase is a collocation
            _n_gram_lower_stemmed = ""
            for _word in _n_gram_lower.split(' '):
                _n_gram_lower_stemmed = " " + stemmer.stemWord(_word)
            _text_from_title_ascii_only_stemmed = ""
            for _word in _text_from_title_ascii_only.split(' '):
                _text_from_title_ascii_only_stemmed = " " + stemmer.stemWord(_word)
            if _verbose:
                print "\t\tStemmed search title: %s\n\t\tStemmed phrase: %s" %(_text_from_title_ascii_only_stemmed, _n_gram_lower_stemmed)
            if _n_gram_lower_stemmed in _text_from_title_ascii_only_stemmed:
                _number_of_valid_titles += 1
                if _verbose:
                    print "\t\t\tMatch"
            else:
                if _verbose:
                    print "\t\t\tNot a match"
            # ---------------------------------------
            """
            # ------------ FOR Exact title match -------------
            if _verbose:
                _output_file_string += ("\t\tSearch TITLE processed: %s\n\t\tPhrase processed: %s" %(_text_from_title_ascii_only, _n_gram_lower))
            if _n_gram_lower in _text_from_title_ascii_only:
                #_number_of_valid_titles += 1
                if _verbose:
                    _output_file_string += ("\t\t\tMatch")
                    gram_match = True
            else:
                if _verbose:
                    _output_file_string += ("\t\t\tNot a match")
            # ------------------------------------------------
            # Remove punctuation and numbers from Url and see if the n-gram / phrase is present in it
            # If yes, then that n-gram is a collocation
            _search_url_lower_case_no_spaces_no_punctuation = "".join([_char for _char in _search_url_lower_case_no_spaces if not _char.isdigit()])
            if _verbose:
                _output_file_string += ("\t\tSearch URL processed: %s\n\t\tPhrase processed: %s" %(_search_url_lower_case_no_spaces_no_punctuation, _n_gram_lower_no_spaces))
            if _n_gram_lower_no_spaces in _search_url_lower_case_no_spaces_no_punctuation:
                #number_of_valid_urls += 1
                if _verbose:
                    _output_file_string += ("\t\t\tMatch")
                    gram_match = True
            else:
                if _verbose:
                    _output_file_string += ("\t\t\tNot a match")
            break
        else:
            continue
    file_write = open(file_path, 'a')
    file_write.write(_output_file_string)
    file_write.close()
    return gram_match


# Title-Url based technique
def Collocations_Method_2_paralllel(_bing_api_key, _n_grams_from_input_text_file, _input_file_path, _apply_POS_restrictions, _verbose):
    _output_file_verbose_path = "verbose.txt"
    if _verbose:
        # A file to save the verbose output of the program
        _output_file_verbose_path = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
        _output_file_verbose = open(_output_file_verbose_path, 'a')
        print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
        print("\tMethod-2: Title-Url - Extracting collocations:", file = _output_file_verbose)
        print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)
        print("\tMethod-2: Title-Url - Extracting collocations ...")

    # A list to store n-gram phrases that are collocations
    title_url_collocations = []
    # A list to store n-gram phrases that are not collocations
    n_grams_not_collocations = []

    # Snowball stemmer is used to stem words
    stemmer = snowballstemmer.stemmer('english')
    # Call to Bing search API
    _bing_search = BingSearchAPI(_bing_api_key)

    _cached_resuls = {}
    try:
        method2_cache_path = os.path.join(os.path.dirname(__file__), "method2.result.cache")
        with open(method2_cache_path, 'r') as method2_cache:
            for line in method2_cache:
                line_cache_result = line.split('|')
                if line_cache_result[1].strip(' \n') == "True":
                    _cached_resuls[line_cache_result[0]] = True
                elif line_cache_result[1].strip(' \n') == "False":
                    _cached_resuls[line_cache_result[0]] = False
    except FileNotFoundError as e:
        print("Error: %s" % (str(e))) 

    
    count = 0
    for _n_gram in _n_grams_from_input_text_file:
        if _verbose:
            print("\n%s:" %(_n_gram), file = _output_file_verbose)
        if _n_gram in title_url_collocations or _n_gram in n_grams_not_collocations:
            # If a particular n-gram phrase is checked if it is a collocation before,
            # it will be present in one of the lists, wordnet_collocations OR n_grams_not_collocations
            # Hence, we move on to the next n-gram / phrase
            continue
        else:
            # Before checking if the n-gram is a collocation we check if atlease one
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
                    continue # We move on to the next phrase

            # If POS restrictions are not to be applied on the n-gram
            _n_gram_no_POS_tag = POS_tag_cleaner(_n_gram)
            _n_gram_lower = _n_gram_no_POS_tag.lower()
            if _n_gram_lower not in _cached_resuls:

                _n_gram_lower_search_phrase = 'define "%s"' %(_n_gram_lower) # Bing - Phrase search
                successful_Request = False
                unsuccessful_Count = 0

                #_bing_search_parameters = {'$format': 'json', '$top': 10}  # Top 10 search results
                _bing_search_parameters = urllib.parse.urlencode({
                    # Request parameters
                    'q': _n_gram_lower_search_phrase,
                    'count': '10',
                    'offset': '0',
                    'mkt': 'en-us',
                    'safesearch': 'Moderate',
                })
                while not successful_Request:
                    try:
                        _search_results = _bing_search.search(_bing_search_parameters)
                        if "statusCode" in _search_results:
                            raise InvalidKeyException(_search_results["statusCode"])
                        if "webPages" in _search_results:
                            _search_result_count = _search_results["webPages"]["value"]
                        else:
                            _search_result_count = 0
                            successful_Request = True
                        #_search_result_count = len(_search_results["webPages"]["value"])
                    except InvalidKeyException as e:
                        if _verbose:
                            print("\tERROR: Method-2 - Bing search - Title-Url\n%s" % (str(e)), file=_output_file_verbose)
                            print("\tERROR: Method-2 - Bing search - Title-Url\n%s" % (str(e)))
                        _search_result_count = 0
                        unsuccessful_Count += 1
                        if unsuccessful_Count < 10:
                            bing_api_cache = os.path.join(os.path.dirname(__file__), "cache/Bing_API_keys.cache")
                            with open(bing_api_cache) as keys_file:
                                keys = list()
                                for line in keys_file:
                                    keys.append(line)
                                _bing_api_key = ''.join(filter(lambda x: (ord(x) < 128), sample(keys, 1)[0].strip(' \t\n\r')))
                                unsuccessful_Count = 0
                            _bing_search._set_Bing_API_key(_bing_api_key)
                    except Exception as e:
                        if _verbose:
                            print('\tERROR: in bing.search() - search total\n\t' + str(e))
                        print('\tERROR: in bing.search() - search total\n\t' + str(e))
                        unsuccessful_Count = 0
                        exit(-1)
                # List to save top 10 search Titles
                _search_titles = []
                # List to store top 10 search Urls
                _search_urls = []
                # We iterate through each of the search result and append search titles and Urls to their respective lists
                for x in range(0, _search_result_count):
                    #_url = _search_results["d"]["results"][0]["Web"][x]["Url"]
                    #_title = _search_results["d"]["results"][0]["Web"][x]["Title"]
                    _url = _search_results["webPages"]["value"][x]["url"]
                    _title = _search_results["webPages"]["value"][x]["name"]
                    _title = unicodedata.normalize('NFKD', _title).encode('ascii','ignore').decode("utf-8")
                    _url = unicodedata.normalize('NFKD', _url).encode('ascii','ignore').decode("utf-8")
                    _search_titles.append(_title)
                    _search_urls.append(_url)
                # removing punctuation, special characters and spaces from the keyword
                #_n_gram_lower_no_spaces = ''.join(_char for _char in _n_gram_lower if _char.isalnum())
                _n_gram_lower_no_spaces = "".join(filter(isalphanum, _n_gram_lower))
                _n_gram_lower_no_spaces = _n_gram_lower_no_spaces.replace(' ', '')
                _number_of_search_results_returned = len(_search_urls) # No. of search urls = titles
                # Variable to store the count of titles and urls that have valid keywords and match with the search phrase
                _number_of_valid_titles = 0
                _number_of_valid_urls = 0
                #for x in xrange(0, _number_of_search_results_returned):


                #_search_title = ""
                #_search_title = _search_titles[x]
                #_search_title_lower_case = _search_title.lower()
                #_search_title_lower_case_no_spaces = "".join(_char for _char in _search_title_lower_case if _char.isalnum())
                #_search_url = ""
                #_search_url = _search_urls[x]
                #_search_url_lower_case = _search_url.lower()
                #_search_url_lower_case_no_spaces = "".join(_char for _char in _search_url_lower_case if _char.isalnum())
                output = []

                def log_output(result):
                    output.append(result)

                if _verbose:
                    print(_n_gram_lower_search_phrase)
                with mp.Pool(processes=4) as pool:
                    for x in range(0, _number_of_search_results_returned):
                        result = pool.apply_async(parallel_request, args=(_search_titles[x], _search_urls[x], _output_file_verbose_path, x, _n_gram_lower, _n_gram_lower_no_spaces, _verbose,), callback = log_output)
                        try:
                            result.get(timeout = 10)
                        except Exception as e:
                            print(str(e))

                    #output = [p.get() for p in results]#results
                    #print(output)
                    #count += 1
                if _verbose:
                    print(output)

                #if count % 1000 == 0:
                #   #print('.')
                #   if len(pool._cache) > 4e6:
                #       print("waiting for cache to clear...")
                #       last.wait()

                #parallel_request(_search_title, _search_url, _list_of_synonymous_words, file_path)

            #if _number_of_valid_titles > 0 or _number_of_valid_urls > 0:

                with open(method2_cache_path, 'a') as method2_cache:
                    if True in output:
                        title_url_collocations.append(_n_gram)
                        print(_n_gram_lower + "|True", file = method2_cache)
                        if _verbose:
                            print("\n\tA match", file = _output_file_verbose)
                            #print("\n\tTotal number of valid titles: %d\n\tTotal number of valid urls: %d\n\t- Collocation -\n"\
            #%(_number_of_valid_titles, _number_of_valid_urls), file = _output_file_verbose)
                    else:
                        n_grams_not_collocations.append(_n_gram)
                        print(_n_gram_lower + "|False", file = method2_cache)
                        if _verbose:
                            print("\t- Not a collocation -\n", file = _output_file_verbose)
            elif _cached_resuls[_n_gram_lower]:
                title_url_collocations.append(_n_gram)
            elif not _cached_resuls[_n_gram_lower]:
                n_grams_not_collocations.append(_n_gram)


    # Output text file to save collocations
    _output_file_path_title_url_collocations = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'collocations_title_url.txt')
    _output_file_title_url_collocations = open(_output_file_path_title_url_collocations, 'w')
    for _collocation in title_url_collocations:
        _output_file_title_url_collocations.write(POS_tag_cleaner(_collocation) + '\n')
    _output_file_title_url_collocations.close()
    if _verbose:
        print("\nMethod-2: Title-Url - Collocations are written to the file:\n%s" %(_output_file_path_title_url_collocations), file = _output_file_verbose)

    # Output text file to save n-grams that are not collocations
    _output_file_path_title_url_not_collocations = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'not_collocations_title_url.txt')
    _output_file_title_url_not_collocations = open(_output_file_path_title_url_not_collocations, 'w')
    for _n_gram in n_grams_not_collocations:
        _output_file_title_url_not_collocations.write(_n_gram + '\n')
    _output_file_title_url_not_collocations.close()
    if _verbose:
        print("Method-2: Title-Url - N-grams that are not collocations are written to the file:\n%s" %(_output_file_path_title_url_not_collocations), file = _output_file_verbose)
    
    if _verbose:
        print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
        print("\tMethod-2: Title-Url - Extracting collocations - Complete", file = _output_file_verbose)
        print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)

    # Returning n-grams that are collocations and n-grams that are not
    if _verbose:
        print("\t\tMethod-2: Collocation extraction successful")
    return title_url_collocations, n_grams_not_collocations