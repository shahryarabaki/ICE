# !/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on Thu Jul 24, 2014
@author: Vasanthi Vuppuluri
Last Modified on: August 4, 2014
"""

"""
PURPOSE:
--------
- To obtain definitions from online dictionaries using Wordnik API 
- In this case, definitions are from https://www.wordnik.com/
- Requirements:
    wordnik module is to be installed first, sudo pip install wordnik
    API_Key for can be obtained after registering at wordnik.com
- Can extract definitions when POS is specified

FUNCTIONS:
----------
- There are multiple functions in this script:
    1. wordnik_def(word, POS, debug): When parts-of-speech of the word is specified
    2. wordnik_def_no_POS(word, debug): When there is no POS tag and definitions are to be obtained

"""

from wordnik import *
import os, nltk

def wordnik_def(word, POS, debug):

    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'c56eb932fde8155acc0060d90c609778b7a5b982ed1ae17cd' # API key should go here
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordApi.WordApi(client)
    
    word = word
    POS = POS
    debug = debug

    try:
        definitions = wordApi.getDefinitions(word, partOfSpeech=POS, limit=10)
        list_of_definitions = [] # To store definitions as elements of a list
        if definitions:
            deinition = definitions[0].text
            ascii_text = '' 
            ascii_text = ascii_text + ''.join(i for i in deinition if ord(i) < 128)
                # Removing ascii characters from definitions obtained
            list_of_definitions.append(ascii_text)

            if (debug == '--debug'):
                print("Definitions from WordNik dictionary: ", list_of_definitions)

            return list_of_definitions
            
        else:
            return 0
            
    except Exception as e:
        print("Here in pos")
        print("Exception raised in Wordnik!!\n", e)
        return 0

def wordnik_def_no_POS(word, debug):

    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'c56eb932fde8155acc0060d90c609778b7a5b982ed1ae17cd' # API key should go here
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordApi.WordApi(client)

    word = word
    debug = debug

    try:
        definitions = wordApi.getDefinitions(word, limit=10)
        
        list_of_definitions = [] # To store definitions as elements of a list
        if definitions:
            list_of_definitions = [definitions[0].text]
            if (debug == '--debug'):
                print("Definitions from WordNik dictionary: ",list_of_definitions)
            return list_of_definitions
        else:
            return 0
            
    except Exception as e:
        print(word)
        print("Here in no pos")
        print("Exception raised in Wordnik!!\n", e)
        return 0

def main_block():
    print("Enter file name: ")
    input_file = str(input())

    debug = '--debug'
    
    valid_output_file = input_file + '.WordNik_VALID'
    if os.path.isfile(valid_output_file):
        os.remove(valid_output_file)
    
    invalid_output_file = input_file + '.WordNik_INVALID'
    if os.path.isfile(invalid_output_file):
        os.remove(invalid_output_file)

    if (os.path.isfile(input_file) and (os.path.getsize(input_file) > 0)):
        f = open(input_file, 'r')
        keywords = f.readlines()
        f.close()
        M = len(keywords)
        for x in range(0,M): 
            keyword = keywords[x]
            keyword1 = keyword
            keyword = keyword.strip('\n')
            print(keyword)
            tokenized_keyword = nltk.word_tokenize(keyword)
            pos_tagged_keyword = nltk.pos_tag(tokenized_keyword)
                # Is a list of pos tagged words from each sentence
            print(pos_tagged_keyword[1])
            defnitions_returned = wordnik_def(keyword, pos_tagged_keyword[1], debug)
            if (defnitions_returned == 0):
                of = open(invalid_output_file, 'a')
                of.write(keyword1)
                of.close
            else:
                of = open(valid_output_file, 'a')
                of.write(keyword1)
                of.close()
