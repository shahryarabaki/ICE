#!/usr/bin/Python2
# --coding:utf-8--

import unicodedata, re, os
from bs4 import BeautifulSoup
from bing_search_api import BingSearchAPI 

def bing_search_total(_verbose, _search_phrase, _bing_api_key):

    _search_phrase_parsed = "%22" + _search_phrase.replace(' ', '+').strip(' ') + "%22" # %22 acts as quotes, facilitating a phrase search
    _bing_search = BingSearchAPI(_bing_api_key)
    _bing_parameters = {'$format': 'json', '$top': 2}

    try:
        res = _bing_search.search('web', _search_phrase_parsed, _bing_parameters).json()
        total_search_results = res["d"]["results"][0]["WebTotal"]
        total = int(total_search_results)
        if(isinstance(total, int)):
            if _verbose:
                print('\t' + _search_phrase_parsed.replace('+', ' ').replace('%22', '') + total)
                pass
            return total
    except Exception as e:
        if _verbose:
            print('\tERROR: in bing.search() - search total\n\t' + str(e))
        print('\tERROR: in bing.search() - search total\n\t' + str(e))
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return 0
# Test
#bing_search_total(True, "Natural Language Processing", "U5Px9AJDGqcMOJVfwZLFa5GfCHi1e6DLwCl+0tt/NX4")
