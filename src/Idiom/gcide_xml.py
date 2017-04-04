# -*- coding: utf-8 -*-

"""
Created on Monday October 6, 2014
@author: Vasanthi Vuppuluri
Last Modified on: October 6, 2014
"""

"""
PURPOSE:
--------
- To extract definitions form GCIDE_XML files

FILE DESCRIPTION:
-----------------
- GCIDE_XML files are essentially alphabetically sorted
- They have definitions from Webster dictionary
- XML tag information:
	- <hw></hw> has the 'word' enclosed with in it, which is being defined
	- <pos></pos> has the POS of the word enclosed. Usually the abbreviation of the POS
	- <def></def> has the definition of the word enclosed in <hw></hw>
	- All these are enclosed with in <p></p>

PROCEDURE:
----------
- For a given word 'w', we open the respective .xml file that has definitions of words which start with with the same alphabet as 'w'
- We then see if 'w' is present in that file. If yes, we extract the definition of that word and close the file
- It is important to close the .xml file after extraction is complete as keeping everything in memory might slow the preocess down

"""

#import timing
import os
from collections import defaultdict
from xml.etree.ElementTree import iterparse

def cache_abs_path(cache_rel_path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, cache_rel_path)

def extract_definitions():
	# input_file = '/Users/vasanthi/Desktop/THESIS/COLL_COMPUTE/COLO2/SCRIPTS/xml_files/gcide_entries.xml'
	input_file = cache_abs_path('gcide_entries.xml')
	#tree = et.parse(input_file)
	#root = tree.getroot()

	"""
	# To print the root node and it's attributes; as well as child noes and their attributes
	print "root:\n\ttag: %s\n\tattributes: %s" %(root.tag, root.attrib)
	print "\nChild tags:"
	for child in root:
		print "\n\ttag: %s\n\tattributes: %s" %(child.tag, child.attrib)
	print '______________\n'
	"""

	webster_dictionary = defaultdict(list) # A dictionary to store the list of definitions of each of the word after they are returned.
	key_list = []
	definitions_list = []

	#for node in tree.iter():
	#for event, node in iterparse(input_file):
	
	# get an iterable
	#context = iterparse(input_file, events=("start", "end"))
	# turn it into an iterator
	#context = iter(context)
	# get the root element
	#event, root = context.next()
	#for event, node in context:

	for event, node in iterparse(input_file):
		#if (event == 'end' and node.tag == 'entry'):
		if (node.tag == 'entry'):
			key = node.attrib.get('key')
			#print key
			key_list.append(key)
			for child in node.iter():
				if (child.tag == 'def'):
					definition = (''.join(itertext(child)))
					#print definition
					definitions_list.append(child.text)
					#definitions = child.text
					if not(definition == None):
						definition = definition.replace("; as", " as")
						definition = definition.replace("; --", " ").strip('\n')
						list_of_definitions = definition.split(';') # As definitions are separated by a semi-colon in the gcide_entries.xml file
						for each_definition in list_of_definitions:
							# Non-Ascii characters are present in these definitions which are breaking the execution
							# Deleting all of those non-ascii characters
							ascii_text = ''
							ascii_text = ascii_text + ''.join(i for i in each_definition if ord(i) < 128)
							ascii_text = ascii_text.rstrip(' ').rstrip('\n')
							webster_dictionary[key].append(ascii_text) # Each of the definition is separately appended to the dictionary
			node.clear()
			#root.clear()

	print(len(key_list), len(definitions_list), len(webster_dictionary))
	return webster_dictionary

def itertext(self):
	key = self.tag
	if not isinstance(key, str) and key is not None:
		return
	if self.text:
		yield self.text
	for e in self:
		for s in e.itertext():
			yield s
		if e.tail:
			yield e.tail

if __name__ == '__main__':
	"""
	Test case I:
	"""
	#"""
	# dictionary = extract_definitions()
	# word = []
	# word.extend(('meanspirited','Meanness','Meantime'))
	# print(word)
	# for a_word in word:
	# 	print(a_word, '-->', dictionary[a_word])
	#"""