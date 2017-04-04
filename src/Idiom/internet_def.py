# -*- coding: utf-8 -*-

"""
Created on June 25, 2014
@author: Vasanthi Vuppuluri
Last Modified on: June 25, 2014
"""

"""
PURPOSE:
--------
- To obtain definitions from Bing search
- The definitions displayed in the browser from Bing Dictionary are extracted

"""

import urllib.request, urllib.error, urllib.parse, re, os, random, time
from bs4 import BeautifulSoup

def internet_search(indebug, inquery, inkey):
    debug = str(indebug)
    query = str(inquery)
    key = str(inkey)

    try:
        # create credential for authentication
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        creds = (':%s' % key).encode('utf-8')[:-1]
        auth = 'Basic %s' % creds

        # Search query for Bing. To obtains definitions
        url = 'http://www.bing.com/search?q=define+"%s"' %query
        url = str(url)

        request = urllib.request.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)

        requestor = urllib.request.build_opener()
        result = requestor.open(request)

        soup = BeautifulSoup(result, 'lxml')
        out = soup.findAll('ol', {'class': 'b_dList'}) # Obtains the information of 'ol' tag whose class name is 'b_dList'
        out = str(out) # Converting class type to string type
        if(out == '[]'):
            if (debug == '--debug'):
                print(("No results found for '%s' using Bing Search" %(query)))
            return 0
        else:
            out = BeautifulSoup(out, 'lxml')
            out = out.findAll('li')
            out = str(out)
            out = str((re.compile(r'<li>(.*)</li>').search(out)).group()) # Extracting <li>..</li> tag information
            out = out.replace('>, <', '>\n<') # Breaks the list items / definitions into one per line
            out = out.split('\n') # outputs a list
            definitions = [] # A list to store the definitions
            for i in out:
                i = BeautifulSoup(i, 'lxml')
                i = i.text # Extracts text only leaving the html tags
                definitions.append(i) # Appends definitions to the list
            if (debug == '--debug'):
                #print "------------------------------------------------------"
                print(("Definitions of '%s' from Internet search:" %(query)))
                for x in range(0,len(definitions)):
                    print(('%d : %s' %(x+1, definitions[x])))
                print("------------------------------------------------------")
            return definitions
    except:
        print("Exception raised!! in obtaining definitions using Bing Search API")
        return 0

''' 
query = "pi+bond"
debug = '--debug'
key= 'RIhkTLQPGqVbob64zrh2Ydi67qriZaEoa1Gk+20s2Rk'
internet_search(debug, query, key)
#'''

def main_block():
    print("Enter file name: ")
    input_file = str(eval(input()))

    debug = '--debug'
    #key = 'RIhkTLQPGqVbob64zrh2Ydi67qriZaEoa1Gk+20s2Rk'
    #key = "xgQtVAZSi7Tgvrqbac1Aqal6q3ymEgm8tAiKMJ3ckWU" #  - "keyacount5.mwe@outlook.com"
    #key = "noLzIF83elZ0IySjp9aYUm/jWrB+VCNbpEgJKLHbd+A" # username: keyacount6.mwe@outlook.com; pwd: acc6acc6
    #key = "3zyWOojD+cT5Zaon+Ga0n6YnUyZpbVjw9UsLHFaITd0" # username: keyacount7.mwe@outlook.com; pwd: acc7acc7
    #key = " GDhSKWrDt6o8RV0z7IP+G5ZbvAIEuh6Woz9cKQL0H3s" # username: keyacount8.mwe@outlook.com; pwd: acc8acc8
    #key = "Nv4YviOB0LSss+sMHzO2WuhMUZEtX1BYucJvurzjBXw" # username: keyacount10.mwe@outlook.com; pwd: acc10acc10
    #key = "b0oa6SfvAzvHOkVO6bqneoUx7GWgkiNyo443GkFwQ1A" # key.acc12@outlook.com; mwe12mwe12
    #key = "IoLpo7GfbqqZsBJt8K7zs9wD9ZLIawdNTlFDeGCjfl8" # key.acc11@outlook.com; acc11acc11
    #key = "kZp6Evs+u2udAi/tsRccIGAnOpW2yj85l+ClamNTPz4" # username: final.acc1@outlook.com; pwd: 1234asdf
    #key = "S45VWpnRf+ogMl6WdeHeNWUuwG5vbZ6WCC9lWN8bNfw" # key.acc18@outlook.com; mwe18mwe18
    #key = "o9RlbuDv+bKa3zfzLX8xYOttTkc854Tt6PpAZsMolnU" # key.acc19@outlook.com; mwe19mwe19
    #key = "5vHXAhyyalf7F9mpVDhlhMwwIupAHPWyqwGchhyQ4Ho" # key.acc20@outlook.com; mwe20mwe20
    key = "GOHE1J+fE1uGN+QDprNGWtPq+7YGY9NUj1dpYu8nhbw" # key.acc21@outlook.com; mwe21mwe21
    #key = "lVgyxhU1ABUT7uNGp0B3QcQTU1K04/kHIQSWzGpON0E" # key.acc22@outlook.com; mwe22mwe22
    
    valid_output_file = input_file + '.BingDict_VALID'
    if os.path.isfile(valid_output_file):
        os.remove(valid_output_file)
    
    invalid_output_file = input_file + '.BingDict_INVALID'
    if os.path.isfile(invalid_output_file):
        os.remove(invalid_output_file)

    if (os.path.isfile(input_file) and (os.path.getsize(input_file) > 0)):
        f = open(input_file, 'r')
        keywords = f.readlines()
        f.close()
        #print keywords
        M = len(keywords)
        for x in range(0,M): 
            keyword = keywords[x]
            keyword1 = keyword
            keyword = keyword.strip('\n')
            print(keyword)
            #tokenized_keyword = nltk.word_tokenize(keyword)
            #pos_tagged_keyword = nltk.pos_tag(tokenized_keyword) # Is a list of pos tagged words from each sentence
            #print pos_tagged_keyword[1]
            defnitions_returned = internet_search(keyword, key, debug)
            if (defnitions_returned == 0):
                of = open(invalid_output_file, 'a')
                of.write(keyword1)
                of.close
            else:
                of = open(valid_output_file, 'a')
                of.write(keyword1)
                of.close()
            time.sleep(randomself.randint(20,40))

#main_block()