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
import time
from urllib.request import quote
import os
import http, urllib


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
        
    def search(self, params):

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        result = json.loads(data)
        conn.close()

        return result

    def search_total(self, _verbose, _search_phrase):

        def _cache_abs_path(cache_rel_path):
            script_dir = os.path.dirname(__file__)
            return os.path.join(script_dir, cache_rel_path)

        #_search_phrase_parsed = "%22" + _search_phrase.replace(' ', '+').strip(' ') + "%22" # %22 acts as quotes, facilitating a phrase search
        #_search_phrase_parsed = "%22" + quote(_search_phrase.strip(' ')) + "%22"
        #_bing_parameters = {'$format': 'json', '$top': 2}
        _search_phrase_parsed = _search_phrase.strip(' ')
        _bing_parameters = urllib.parse.urlencode({
            # Request parameters
            'q': _search_phrase_parsed,
            'count': '2',
            'offset': '0',
            'mkt': 'en-us',
            'safesearch': 'Moderate',
        })

        if _search_phrase in self.diction:
            return self.diction[_search_phrase], self.key
        else:
            #Set up a cache to remember the total number of hit searches retried
            #Update the diction if search_phrase is not found
            with open(_cache_abs_path("cache/bing_search_totals.cache"), 'r') as f:
                if _verbose:
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
                        res = self.search(_bing_parameters)
                        if len(res["rankingResponse"]) == 0:
                            total_search_results = 0
                        else:
                            total_search_results = res["webPages"]["totalEstimatedMatches"]
                        if _verbose:
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
                            #self.key = input("Please enter another Bing API key: ")
                            time.sleep(2)
                            count = 0
                            #return -1, _bing_api_key