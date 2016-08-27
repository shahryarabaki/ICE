"""
	Created by An Nguyen
	Oct, 2015
	Modified version of method 2, attempt to do parallel programming.
"""


#!/usr/bin/Python2
# --coding:utf-8--

from __future__ import print_function
from bs4 import BeautifulSoup
from bing_search_api import BingSearchAPI
import snowballstemmer
import unicodedata
import urllib2
import re
import httplib2
import multiprocessing as mp
import requests

def main():
	req = requests.Session()
	requests.max_redirects = 3
	count = 0
	try:
		r = requests.get('http://dictionary.sensagent.com/become%20visible/en-en/', timeout = 2.0, stream = True)
		text = ''
		for chunk in r.iter_content(chunk_size = 1024):
			count += 1
			soup = BeautifulSoup(chunk, 'lxml')
			#print(str(soup) + '\n')
			try:
				print(soup.find('title').text)
			except Exception as e:
				#print('test')
				if count >= 4:
					print('failure')
					break
				continue
			print('\n')
			break	
	except Exception as e:
		print("\tException - Method-2 - Reading HTML\n%s" %(str(e)))
		print("-----------------\n" + "\n---------------\n")

	req.close()

	
		
	#_text_from_title = soup.title.string0
	#print(_text_from_title)
		


if __name__ == "__main__":
    main()
