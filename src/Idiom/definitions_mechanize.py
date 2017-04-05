# -*- coding: utf-8 -*-

"""
Created on Thu Jul 24, 2014
@author: Vasanthi Vuppuluri
Last Modified on: July 24, 2014
"""

"""
PURPOSE:
--------
- To obatin definitions from online dictionaries using the mechanize module
    - For now, this script extracts definitions form dictionary.reference.com
- Mechanize is to be installed on the machine for this script to work - sudo pip install mechanize

"""

import requests, re
from bs4 import BeautifulSoup

def definitions_m(word, debug):
    _word = word
    debug = debug
    
    # Obtaining definitions of words from http://dictionary.reference.com/ along with thier POS
    try:
        url = "http://dictionary.reference.com/browse/%s?s=t" %(_word)
        result = requests.get(url)
    
        soup = BeautifulSoup(result.content, "lxml")
        #pos = soup.findAll('span', {'class': 'pg'})
        word_definitions = soup.findAll('div', {'class': 'def-list'})
        
        pos_of_word = [] # A list of all pos tags associated with the word definition from the webpage
        definitions_of_word = [] # A list of lists of definitions of the word
        if(len(word_definitions) > 0): # Makes sure there is atleast one definition for the given word
            for i in word_definitions:
                list_of_definitions = []
                result_pos = i.find('span', {'class': 'dbox-pg'})
                if result_pos:
                    pos_of_word.append(result_pos.text)
                    for div in i.findAll('div', {'class': 'def-content'}):
                        list_of_definitions.append(div.text.strip())
                    definitions_of_word.append(list_of_definitions)

            dictionary_of_word_pos_definitions = {} # A dictionary to store the definitions of the word based on its POS
            for x in range(0, len(pos_of_word)):
                dictionary_of_word_pos_definitions[pos_of_word[x]] = definitions_of_word[x]

            if(debug == '--debug'):
                print("Definitions from dictionary.reference.com: ", dictionary_of_word_pos_definitions)

            return (pos_of_word, dictionary_of_word_pos_definitions)
        else:
            pos_of_word = []
            dictionary_of_word_pos_definitions = {}
            return (pos_of_word, dictionary_of_word_pos_definitions)

    except Exception as e:
        if(debug == '--debug'):
            print("Exception raised!!")
            print(e)
        pos_of_word = []
        dictionary_of_word_pos_definitions = {}
        return (pos_of_word, dictionary_of_word_pos_definitions)

#definitions('ethnic+group', '--debug')