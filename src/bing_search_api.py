"""
Created on Mon Apr 14 15:48:29 2014

@author: Vasanthi Vuppuluri
Original code inspired by: Tanmay Thakur
"""

# PURPOSE:
#---------
# This is designed for the new Azure Marketplace Bing Search API (released Aug 2012)
#
# Inspired by https://github.com/mlagace/Python-SimpleBing and 
# http://social.msdn.microsoft.com/Forums/pl-PL/windowsazuretroubleshooting/thread/450293bb-fa86-46ef-be7e-9c18dfb991ad

import requests # Get from https://github.com/kennethreitz/requests
import string
import json
from urllib.parse import urlencode
from random import randint, sample
from urllib.request import quote
import os


class BingSearchAPI():
    bing_api = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/Composite?" # Composite options searches everywhere, i.e. {web+image+video+news+spell}
    
    def __init__(self, key):
        self.key = key
        self.diction = {}

    def _set_Bing_API_key(self, key):
        self.key = key

    def replace_symbols(self, request):
        # Custom urlencoder.
        # They specifically want %27 as the quotation which is a single quote '
        # We're going to map both ' and " to %27 to make it more python-esque
        request = request.replace("'", '%27')
        request = request.replace('"', '%27')
        request = request.replace('+', '%2b')
        request = request.replace(' ', '%20')
        request = request.replace(':', '%3a')
        return request
        
    def search(self, sources, query, params):
        ''' This function expects a dictionary of query parameters and values.
            Sources and Query are mandatory fields. 
            Sources is required to be the first parameter.
            Both Sources and Query requires single quotes surrounding it.
            All parameters are case sensitive. Go figure.

            For the Bing Search API schema, go to http://www.bing.com/developers/
            Click on Bing Search API. Then download the Bing API Schema Guide
            (which is oddly a word document file...pretty lame for a web api doc)
        '''
        request =  'Sources="' + sources    + '"'
        request += '&Query="'  + str(query) + '"'
        for key, value in params.items():
            request += '&' + key + '=' + str(value)
        request = self.bing_api + self.replace_symbols(request)
        try:                
            result = requests.get(request, auth=(self.key, self.key), timeout = 4.0)
        except requests.exceptions.RequestException as e:
            print("Bing Seach Error, error message : {0}".format(str(e)))
        return result

    def search_total(self, _verbose, _search_phrase):

        def _cache_abs_path(cache_rel_path):
            script_dir = os.path.dirname(__file__)
            return os.path.join(script_dir, cache_rel_path)

        #_search_phrase_parsed = "%22" + _search_phrase.replace(' ', '+').strip(' ') + "%22" # %22 acts as quotes, facilitating a phrase search
        _search_phrase_parsed = "%22" + quote(_search_phrase.strip(' ')) + "%22"
        _bing_parameters = {'$format': 'json', '$top': 2}

        if _search_phrase in self.diction:
            return self.diction[_search_phrase], self.key
        else:
            #Set up a cache to remember the total number of hit searches retried
            #Update the diction if search_phrase is not found
            with open(_cache_abs_path("cache/bing_search_totals.cache"), 'r') as f:
                print(_search_phrase_parsed)
                for line in f:
                    phrase, hit = line.split('/----/')
                    try:
                        hit = ''.join(filter(lambda x: x.isdigit(), hit))
                        self.diction[phrase] = int(hit)
                    except Exception as e:
                        print("Diction cache error for " + hit)

        if _search_phrase in self.diction:
            return self.diction[_search_phrase], self.key
        else:
            with open(_cache_abs_path("cache/bing_search_totals.cache"), 'a') as f:
                count = 0
                while True:
                    count = count + 1
                    try:
                        res = self.search('web', _search_phrase_parsed, _bing_parameters).json()
                        total_search_results = res["d"]["results"][0]["WebTotal"]
                        print('-----' + str(total_search_results) + '-----------')
                        total = int(total_search_results)
                        if(isinstance(total, int)):
                            if _verbose:
                                print('\t', _search_phrase_parsed.replace('+', ' ').replace('%22', ''), total)
                                pass
                            print("%s/----/%d" % (_search_phrase, total), file = f)
                            return total, self.key
                    except Exception as e:
                        if _verbose:
                            print('\tERROR: in bing.search() - search total\n\t' + str(e))
                        print('\tERROR: in bing.search() - search total\n\t' + str(e))
                        print('\tEither network connection error or Bing Api key expired. Search phrase: ' + _search_phrase_parsed)
                        if count < 10:
                            with open(_cache_abs_path("cache/Bing_API_keys.cache")) as keys_file:
                                keys = list()
                                for line in keys_file:
                                    keys.append(line)
                                self.key = ''.join(filter(lambda x: (ord(x) < 128), sample(keys, 1)[0].strip(' \t\n\r')))
                        else:
                            self.key = input("Please enter another Bing API key: ")
                            count = 0