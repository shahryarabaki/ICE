import nltk
import re
import string
import nltk.data
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import punkt
import sys
from unidecode import unidecode
from pos_tagger import POS_Tagger


def string_to_ascii(x):
    x = unidecode(x)
    
    x = ''.join(filter(lambda char: char in string.printable, x))

    return x



def pos_tagged_ngrams_without_sentences(_input_file_path, _verbose):
    _input_text = open(_input_file_path).readlines()

    # A Python list to store sentences from input text after removing non-ascii characters
    _input_sentences = []
    # Output text file to save the clean text after removing any non-ascii characters present
    _output_file_path_ascii_only = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'ascii.txt')
    if _verbose:
        print("\n\tClean text after removing non-ascii characters is saved to the file:\n\t%s" %(_output_file_path_ascii_only), file = _output_file_verbose)

    # Removing non-ascii characters
    # All non-ascii characters have a value < 128
    _output_file_ascii_only = open(_output_file_path_ascii_only, 'w')
    for _line in _input_text:
        _line = string_to_ascii(_line)
        _input_sentences.append(_line)
        _output_file_ascii_only.write(_line)
    _output_file_ascii_only.close()


    # Output text file to write the text after replacing the contractions
    _output_file_path_no_contractions = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'no_contractions.txt')
    _output_file_no_contractions = open(_output_file_path_no_contractions, 'w')
    for _sentence in _input_sentences_no_contractions:
        _output_file_no_contractions.write(_sentence)
    _output_file_no_contractions.close()
    if _verbose:
        print("\tText after contractions are replaced is written to the file:\n\t%s" %(_output_file_path_no_contractions), file = _output_file_verbose)



    # POS tagging the input file using NLTK POS Tagger
    # A list to store the POS tagged input sentences
    pos_tagger = POS_Tagger()
    _pos_tagged_input_sentences = []

    try:
        if _verbose:
            print("\tPOS tagging the input text...", file = _output_file_verbose)
        for _sentence in _input_sentences_no_contractions:
            _sentence = _sentence.strip('\n')
            _tokenized_sentence = nltk.word_tokenize(_sentence)
            _pos_tagged_sentence = pos_tagger.tag(_tokenized_sentence)
            _pos_tagged_input_sentences.append(_pos_tagged_sentence)
    except Exception as e:
        if _verbose:
            print("\tException: POS tagging the input text\n%s" %(str(e)), file = _output_file_verbose)
            print("\t\tERROR POS tagging the input text\n\t\t", str(e))
    
    # Output file to save the pos-tagged text after removing the punctuation
    _output_file_path_pos_tagged = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'pos_tagged.txt')
    
    # Ignoring punctuation when extracting collocations
    # A list to store the POS tagged sentences without punctuation
    _pos_tagged_input_sentences_no_punctuation = []

    # Punctuation from String module
    _punctuation = set(string.punctuation)

    try:
        # Appending POS tagged sentences to the list without punctuation
        for _sentence in _pos_tagged_input_sentences:
            _pos_tagged_sentence_without_punctuation = ""
            for _word_pos_token in _sentence:
                if not _word_pos_token[0] in _punctuation:
                    _pos_tagged_sentence_without_punctuation += _word_pos_token[0] + '_' + _word_pos_token[1] + ' '
            # Append the sentence to the list after removing the additional trailing space that is added in the step above
            _pos_tagged_input_sentences_no_punctuation.append(_pos_tagged_sentence_without_punctuation)
            _output_file_pos_tagged = open(_output_file_path_pos_tagged, 'a')
            _output_file_pos_tagged.write(str(_pos_tagged_sentence_without_punctuation ).rstrip(' ') + '\n')
            _output_file_pos_tagged.close()
        if _verbose:
            print("\tPunctuation is successfully removed", file = _output_file_verbose)
    except Exception as e:
        if _verbose:
            print("\tERROR removing punctuation from POS tagged input text\n%s" %(str(e)), file = _output_file_verbose)
            print("\tERROR while removing punctuation form POS tagged input text\n%s" %(str(e)))
    else:
        if _verbose:
            print("\tPOS tagged input text is saved to the file:\n\t%s" %(_output_file_path_pos_tagged), file = _output_file_verbose)

    # The POS tagged sentences without punctuation are input for extracting collocations


# def pos_tagged_ngrams_from_file(_input_file_path, _n_value_for_ngram_extraction, _stop_word_removal, _verbose):


# Method to extract POS tagged n-grams
def pos_tagged_ngrams_from_sentences(_input_sentences, _n_value_for_ngram_extraction, _stop_word_removal, _verbose):
    # Dictionary
    contraction_dictionary = {}
    # Read the text from the file, "English_contractions.txt"
    _contractions = open("English_contractions.txt").readlines()
    for _each_contraction in _contractions:

        _contraction, _expansion = _each_contraction.strip('\n').split('\t')[0], _each_contraction.strip('\n').split('\t')[1]
        _contraction = _contraction.rstrip()#here was also a problem before as the contraction is given with a space in the end inside the dictionnary we have to remove it
        contraction_dictionary[_contraction.lower()] = _expansion.lower()
        
    # Now that our contraction dictionary is ready, we replace each contraction with the respective expansion in
    #       the input text text with non-ascii characters removed. And then let's POS tag the text.
    # A list to save the text after expanding the contractions
    _input_sentences_no_contractions = []
    for _sentence in _input_sentences:
        for _word in _sentence.split(' '):
            if _word.lower().strip('\n') in contraction_dictionary:
                _sentence = _sentence.replace(_word.strip('\n'), contraction_dictionary[_word.lower().strip('\n')])
                
        _input_sentences_no_contractions.append(_sentence)

    #print("_input_sentences_no_contractions",_input_sentences_no_contractions)
                


    
    
    # Output file to save the pos-tagged text after removing the punctuation
            
    # Ignoring punctuation when extracting n-grams
    # A list to store the POS tagged sentences without punctuation
    #_pos_tagged_input_sentences_no_punctuation = []

    # Punctuation from String module
    #_punctuation = set(string.punctuation)
    


    _pos_tagged_input_sub_sentences = []

    # train on all of (tagged) Brown corpus
    
    pos_tagger = POS_Tagger()
        
    # tokenize input into sentences
    #sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #_input_sentences_with_sub_sentences = sent_tokenizer.tokenize(input_file_lines)
        
    
    tokenized_sents = []
    for source_sent in  _input_sentences_no_contractions:
        
        tokenized_sents.append(nltk.word_tokenize(source_sent))
        
    tagged_sents = []
    
    for tokenized_sent in tokenized_sents:
        tagged_sents.append(pos_tagger.tag(tokenized_sent))
        #tagged_sents.append(pos_tag(tokenized_sent))

    #Set up punctuation and quotes base for removal
    _punctuation = set(string.punctuation)
    _quotes = ['\"','\'','``','\'\'']
    table_remove_punctuation = str.maketrans('', '', string.punctuation)
    try:
        for tagged_sent in tagged_sents:
            _pos_tagged_sentence_without_punctuation = ""

            i = 0
            while i < len(tagged_sent):
                tagged_word = tagged_sent[i]
                #if tagged_word[0] != tagged_word[1]:
                if tagged_word[0].translate(table_remove_punctuation) != "":
                    _pos_tagged_sentence_without_punctuation += tagged_word[0]
                    _pos_tagged_sentence_without_punctuation += '_' + tagged_word[1] + ' '
                i += 1

            _pos_tagged_input_sub_sentences.append(_pos_tagged_sentence_without_punctuation)
        
    except Exception as e:
        pass
    #####splitting the sentences before the n_grams extraction

    _input_sentences_with_sub_sentences_quotes = []
    _input_sentences_with_sub_sentences = []

    #print('_input_sentences merged',_input_sentences)
    tokenized_sub_sents = []
    _input_sentences2=[]


    _sentences_for_n_gram_extraction = []

    # Removing stopwords
    # POS tagged input sentences with punctuation are considered here for removing stopwords
    try:
        if _stop_word_removal:
            # Output text file to save the text after removing stopwords
            
            
            # A Python list to save the sentences after removing stopwords
            _clean_sentences = []

            # Caching the stop words to make the program run faster
            CachedStopWords = stopwords.words('english')

            _output_file_no_stopwords = open(_output_file_path_no_stopwords, 'w')

            #Consider replace _pos_tagged_input_sub_sentences into here as they are truly used for stop word removal
            for _sentence in _pos_tagged_input_sub_sentences:
                _words = _sentence.split(' ')
                _sentence = ""
                _sentence = ' '.join(_word for _word in _words if _word.split('_')[0] not in CachedStopWords)
                _sentence = _sentence.lstrip(' ') # Removing the space at the beginning of the sentence
                _output_file_no_stopwords.write(_sentence + '\n')
                _sentences_for_n_gram_extraction.append(_sentence)
    except Exception as e:
        pass
    

    # N-gram extraction
    # A list to store n-grams
    _n_grams_from_input_text_file = []

    if not _stop_word_removal:
        #_sentences_for_n_gram_extraction = _pos_tagged_input_sentences_no_punctuation
        # _sentences_for_n_gram_extraction = _input_sentences2
        _sentences_for_n_gram_extraction = _pos_tagged_input_sub_sentences

    try:
        for _sentence in _sentences_for_n_gram_extraction:
            #cleaning the text from single quotes after splitting the sentences
            #_sentence = ''.join(word for word in _sentence if word not in _quotes)
            # Removing the space at the end of the sentence
            _sentence = _sentence.lstrip(' ')
            _sentence = _sentence.rstrip(' ')
            # Split the sentence at spaces
            _words_in_sentence = _sentence.split(' ')
            # Check if the number of words in the sentence are less than number of n-grams to be generated
            if len(_words_in_sentence) >= _n_value_for_ngram_extraction:
                # A list to store n-grams from each individual sentences
                _n_grams_from_this_sentence = []
                # Extracting n-grams from the sentence
                for i in range(len(_words_in_sentence) - _n_value_for_ngram_extraction + 1):
                    if "'s_POS" not in _words_in_sentence[i]:
                        # A list to store n-grams that are extracted as sub-lists from the POS tagged sentence
                        _ngram_with_words_as_list_elements = []

                        word_index = i
                        count_words = 0
                        while (count_words < _n_value_for_ngram_extraction) and (word_index < len(_words_in_sentence)):
                            _ngram_with_words_as_list_elements.append(_words_in_sentence[word_index])
                            if "'s_POS" not in _words_in_sentence[word_index] :
                                count_words += 1
                            word_index += 1
                        #_ngram_with_words_as_list_elements = _words_in_sentence[i : i + _n_value_for_ngram_extraction]
                                                # n-gram as a phrase
                        _ngram_phrase = ""
                        #_ngram_phrase += ' '.join(_word for _word in _ngram_with_words_as_list_elements)
                        if count_words == _n_value_for_ngram_extraction:
                            #TEMP: Remove quotes from the start of words except for possessive forms
                            _ngram_phrase += ' '.join((_word.lstrip(''.join(_quotes)) if _word != "'s_POS" else _word) for _word in _ngram_with_words_as_list_elements if _word not in _quotes)
                            _ngram_phrase = _ngram_phrase.lstrip(' ') # Removes the space from the beginning of the sentence
                            _n_grams_from_this_sentence.append(_ngram_phrase)
                            _n_grams_from_input_text_file.append(_ngram_phrase)
                
        try:
            # Writing N-grams with POS tags attached to an output text file
            _output_file_path_n_grams_with_pos = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'N_grams_with_POS.txt')
            _output_file_n_grams_with_pos = open(_output_file_path_n_grams_with_pos, 'w')
            for _n_gram_phrase_with_pos in _n_grams_from_input_text_file:
                _output_file_n_grams_with_pos.write(_n_gram_phrase_with_pos + '\n')
            _output_file_n_grams_with_pos.close()
            
            # Writing N-grams with out POS tags attached to an output text file
            _output_file_path_n_grams_with_out_pos = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'N_grams.txt')
            _output_file_n_grams_with_out_pos = open(_output_file_path_n_grams_with_out_pos, 'w')
            for _n_gram_phrase_with_pos in _n_grams_from_input_text_file:
                _ngram_without_pos = ""
                # Removing POS tags
                # Space is added at the end of the phrase to properly remove the tags
                #_ngram_without_pos = re.sub(r'_.*? ', ' ', _n_gram_phrase_with_pos + ' ')
                #_ngram_without_pos = _ngram_without_pos.rstrip(' ') # Removing the beginning space
                _ngram_without_pos = POS_tag_cleaner(_n_gram_phrase_with_pos)
                _output_file_n_grams_with_out_pos.write(_ngram_without_pos + '\n')
        except Exception as e:
            pass
    except Exception as e:
        pass
            


    # This method returns n-grams extracted with POS tags attached
    return _n_grams_from_input_text_file

def pos_tagged_ngrams_from_file(_input_file_path, _n_value_for_ngram_extraction, _stop_word_removal, _verbose):
    if _verbose:
        # A file to save the verbose output of the program
        _output_file_verbose = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'verbose.txt')
        _output_file_verbose = open(_output_file_verbose, 'a')
        print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
        print("\tExtracting %d-grams:" %(_n_value_for_ngram_extraction), file = _output_file_verbose)
        print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)
        print("\tRemoving non-ascii characters from input text ...", file = _output_file_verbose)
        print("\tExtracting %d-grams ..." %(_n_value_for_ngram_extraction))
    # Reading text from input file
    _input_text = open(_input_file_path).readlines()

    # A Python list to store sentences from input text after removing non-ascii characters
    _input_sentences = []

    # Output text file to save the clean text after removing any non-ascii characters present
    _output_file_path_ascii_only = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'ascii.txt')
    if _verbose:
        print("\tClean text after removing non-ascii characters is saved to the file:\n\t%s"\
%(_output_file_path_ascii_only), file = _output_file_verbose)

    
    
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    _output_file_ascii_only = open(_output_file_path_ascii_only, 'w')
    for _line in _input_text:
        _line = string_to_ascii(_line)
        _output_file_ascii_only.write(_line)
        #after writing in the file and before appending we will split the lines into sentences and then add them to the list
        _line_new = sent_detector.tokenize(_line.strip())
        _input_sentences.append(_line_new)
    _output_file_ascii_only.close()
    

    # now we should treat some exeption like comm-a semicolen  - - [  ] {  } " " < > 

    #now we should merge all the sentences in one list so it become easy to work with
    _input_sentences = list(itertools.chain.from_iterable(_input_sentences))
    
    # Let's expand the contractions before POS tagging
    # We don't want "don't" to be POS tagged as don_{POS} 't_{POS} for obvious reasons
    # I used the 'English contraction list' from Wikipedia
    #       URL: http://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
    #       - only one expansion is used for each contraction
    #       even though multiple optins are available for certain contractions
    #       Example: he'd = he had (OR) he would
    # Here, we read the text file, 'English_contractions.txt' and save the contractions and expansions in
    #       to a dictionary. When ever a contraction is matched it is replaced with the respective expansion
    # NOTE: If I missed any contraction, well, we should add it to the file, 'English_contractions.txt' ASAP
    if _verbose:
        print("\tExpanding the contractions ...", file = _output_file_verbose)
    # Dictionary
    contraction_dictionary = {}
    # Read the text from the file, "English_contractions.txt"
    _contractions = open("English_contractions.txt").readlines()
    for _each_contraction in _contractions:

        _contraction, _expansion = _each_contraction.strip('\n').split('\t')[0], _each_contraction.strip('\n').split('\t')[1]
        _contraction = _contraction.rstrip()#here was also a problem before as the contraction is given with a space in the end inside the dictionnary we have to remove it
        contraction_dictionary[_contraction.lower()] = _expansion.lower()
        
    # Now that our contraction dictionary is ready, we replace each contraction with the respective expansion in
    #       the input text text with non-ascii characters removed. And then let's POS tag the text.
    # A list to save the text after expanding the contractions
    _input_sentences_no_contractions = []
    for _sentence in _input_sentences:
        for _word in _sentence.split(' '):
            if _word.lower().strip('\n') in contraction_dictionary:
                _sentence = _sentence.replace(_word.strip('\n'), contraction_dictionary[_word.lower().strip('\n')])
                
        _input_sentences_no_contractions.append(_sentence)

    #print("_input_sentences_no_contractions",_input_sentences_no_contractions)
                


    # Output text file to write the text after replacing the contractions
    _output_file_path_no_contractions = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'no_contractions.txt')
    _output_file_no_contractions = open(_output_file_path_no_contractions, 'w')
    for _sentence in _input_sentences_no_contractions:
        _output_file_no_contractions.write(_sentence+'\n')
    _output_file_no_contractions.close()
    if _verbose:
        print("\tText after contractions are replaced is written to the file:\n\t%s"\
%(_output_file_path_no_contractions), file = _output_file_verbose)


    
    
    # Output file to save the pos-tagged text after removing the punctuation
    _output_file_path_pos_tagged = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'pos_tagged.txt')
            
    # Ignoring punctuation when extracting n-grams
    # A list to store the POS tagged sentences without punctuation
    #_pos_tagged_input_sentences_no_punctuation = []

    # Punctuation from String module
    #_punctuation = set(string.punctuation)
    


    _pos_tagged_input_sub_sentences = []

    # train on all of (tagged) Brown corpus
    
    pos_tagger = POS_Tagger()
        
    # tokenize input into sentences
    #sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #_input_sentences_with_sub_sentences = sent_tokenizer.tokenize(input_file_lines)
        
    
    tokenized_sents = []
    for source_sent in  _input_sentences_no_contractions:
        
        tokenized_sents.append(nltk.word_tokenize(source_sent))
        
    tagged_sents = []
    
    for tokenized_sent in tokenized_sents:
        tagged_sents.append(pos_tagger.tag(tokenized_sent))
        #tagged_sents.append(pos_tag(tokenized_sent))

    #Set up punctuation and quotes base for removal
    _punctuation = set(string.punctuation)
    _quotes = ['\"','\'','``','\'\'']
    table_remove_punctuation = str.maketrans('', '', string.punctuation)
    with open(_output_file_path_pos_tagged, 'w') as _output_file_pos_tagged:
        try:
            for tagged_sent in tagged_sents:
                _pos_tagged_sentence_without_punctuation = ""

                i = 0
                while i < len(tagged_sent):
                    tagged_word = tagged_sent[i]
                    #if tagged_word[0] != tagged_word[1]:
                    if tagged_word[0].translate(table_remove_punctuation) != "":
                        _pos_tagged_sentence_without_punctuation += tagged_word[0]
                        _pos_tagged_sentence_without_punctuation += '_' + tagged_word[1] + ' '
                    i += 1

                _pos_tagged_input_sub_sentences.append(_pos_tagged_sentence_without_punctuation)
                print(str(_pos_tagged_sentence_without_punctuation).rstrip(' '), file = _output_file_pos_tagged)
            if _verbose:
                print("\tPunctuation is successfully removed", file = _output_file_verbose)
        except Exception as e:
            if _verbose:
                print("\tERROR removing punctuation from POS tagged input text", file = _output_file_verbose)
                print("\tERROR while removing punctuation from POS tagged input text\n%s" %(str(e)))
        else:
            if _verbose:
                print("\tPOS tagged input text is saved to the file:\n\t%s" %(_output_file_path_pos_tagged), file = _output_file_verbose)
    #####splitting the sentences before the n_grams extraction

    _input_sentences_with_sub_sentences_quotes = []
    _input_sentences_with_sub_sentences = []

    #print('_input_sentences merged',_input_sentences)
    tokenized_sub_sents = []
    _input_sentences2=[]


    _sentences_for_n_gram_extraction = []

    # Removing stopwords
    # POS tagged input sentences with punctuation are considered here for removing stopwords
    try:
        if _stop_word_removal:
            # Output text file to save the text after removing stopwords
            _output_file_path_no_stopwords = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'no_stopwords.txt')
            
            if _verbose:
                print("\tRemoving stopwords and saving the output to the file:\n\t%s" %(_output_file_path_no_stopwords), file = _output_file_verbose)

            # A Python list to save the sentences after removing stopwords
            _clean_sentences = []

            # Caching the stop words to make the program run faster
            CachedStopWords = stopwords.words('english')

            _output_file_no_stopwords = open(_output_file_path_no_stopwords, 'w')

            #Consider replace _pos_tagged_input_sub_sentences into here as they are truly used for stop word removal
            for _sentence in _pos_tagged_input_sub_sentences:
                _words = _sentence.split(' ')
                _sentence = ""
                _sentence = ' '.join(_word for _word in _words if _word.split('_')[0] not in CachedStopWords)
                _sentence = _sentence.lstrip(' ') # Removing the space at the beginning of the sentence
                _output_file_no_stopwords.write(_sentence + '\n')
                _sentences_for_n_gram_extraction.append(_sentence)
            _output_file_no_stopwords.close()
            if _verbose:
                print("\tStopwords are successfully removed", file = _output_file_verbose)
    except Exception as e:
        if _verbose:
            print("\tERROR removing stopwords from punctuation corrected POS tagged input text\n%s" %(str(e)), file = _output_file_verbose)
            print("\tERROR removing stopwords from punctuation corrected POS tagged input text\n%s", str(e))
    

    # N-gram extraction
    # A list to store n-grams
    _n_grams_from_input_text_file = []

    if _verbose:
        print("\n\t%d-grams from each sentence are as follows:\n" %(_n_value_for_ngram_extraction), file = _output_file_verbose)

    if not _stop_word_removal:
        #_sentences_for_n_gram_extraction = _pos_tagged_input_sentences_no_punctuation
        # _sentences_for_n_gram_extraction = _input_sentences2
        _sentences_for_n_gram_extraction = _pos_tagged_input_sub_sentences

    try:
        for _sentence in _sentences_for_n_gram_extraction:
            #cleaning the text from single quotes after splitting the sentences
            #_sentence = ''.join(word for word in _sentence if word not in _quotes)
            # Removing the space at the end of the sentence
            _sentence = _sentence.lstrip(' ')
            _sentence = _sentence.rstrip(' ')
            # Split the sentence at spaces
            _words_in_sentence = _sentence.split(' ')
            # Check if the number of words in the sentence are less than number of n-grams to be generated
            if len(_words_in_sentence) >= _n_value_for_ngram_extraction:
                # A list to store n-grams from each individual sentences
                _n_grams_from_this_sentence = []
                # Extracting n-grams from the sentence
                for i in range(len(_words_in_sentence) - _n_value_for_ngram_extraction + 1):
                    if "'s_POS" not in _words_in_sentence[i]:
                        # A list to store n-grams that are extracted as sub-lists from the POS tagged sentence
                        _ngram_with_words_as_list_elements = []

                        word_index = i
                        count_words = 0
                        while (count_words < _n_value_for_ngram_extraction) and (word_index < len(_words_in_sentence)):
                            _ngram_with_words_as_list_elements.append(_words_in_sentence[word_index])
                            if "'s_POS" not in _words_in_sentence[word_index] :
                                count_words += 1
                            word_index += 1
                        #_ngram_with_words_as_list_elements = _words_in_sentence[i : i + _n_value_for_ngram_extraction]
                                                # n-gram as a phrase
                        _ngram_phrase = ""
                        #_ngram_phrase += ' '.join(_word for _word in _ngram_with_words_as_list_elements)
                        if count_words == _n_value_for_ngram_extraction:
                            #TEMP: Remove quotes from the start of words except for possessive forms
                            _ngram_phrase += ' '.join((_word.lstrip(''.join(_quotes)) if _word != "'s_POS" else _word) for _word in _ngram_with_words_as_list_elements if _word not in _quotes)
                            _ngram_phrase = _ngram_phrase.lstrip(' ') # Removes the space from the beginning of the sentence
                            _n_grams_from_this_sentence.append(_ngram_phrase)
                            _n_grams_from_input_text_file.append(_ngram_phrase)
                if _verbose:
                    print("\t\tNumber of words in sentence '%s': %d\n\t\t%d n-grams generated. They are:\n\t%s\n"\
%(_sentence, len(_words_in_sentence) ,len(_n_grams_from_this_sentence), _n_grams_from_this_sentence), file = _output_file_verbose)
            else:
                # Leave the sentence, whose number of words are less than the n-gram number behind
                if _verbose:
                    print("\t\tNumber of words in the sentence, '%s' = %d < %d\n" %(_sentence, len(_words_in_sentence), _n_value_for_ngram_extraction), file = _output_file_verbose)
        # Writing N-grams to the output files
        try:
            # Writing N-grams with POS tags attached to an output text file
            _output_file_path_n_grams_with_pos = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'N_grams_with_POS.txt')
            _output_file_n_grams_with_pos = open(_output_file_path_n_grams_with_pos, 'w')
            for _n_gram_phrase_with_pos in _n_grams_from_input_text_file:
                _output_file_n_grams_with_pos.write(_n_gram_phrase_with_pos + '\n')
            _output_file_n_grams_with_pos.close()
            if _verbose:
                print("\tN-grams with POS tags attached are written to: %s" %(_output_file_path_n_grams_with_pos), file = _output_file_verbose)

            # Writing N-grams with out POS tags attached to an output text file
            _output_file_path_n_grams_with_out_pos = str(_input_file_path).replace(_input_file_path.split('/')[-1], 'N_grams.txt')
            _output_file_n_grams_with_out_pos = open(_output_file_path_n_grams_with_out_pos, 'w')
            for _n_gram_phrase_with_pos in _n_grams_from_input_text_file:
                _ngram_without_pos = ""
                # Removing POS tags
                # Space is added at the end of the phrase to properly remove the tags
                #_ngram_without_pos = re.sub(r'_.*? ', ' ', _n_gram_phrase_with_pos + ' ')
                #_ngram_without_pos = _ngram_without_pos.rstrip(' ') # Removing the beginning space
                _ngram_without_pos = POS_tag_cleaner(_n_gram_phrase_with_pos)
                _output_file_n_grams_with_out_pos.write(_ngram_without_pos + '\n')
            _output_file_n_grams_with_out_pos.close()
            if _verbose:
                print("\tN-grams without POS tags attached are written to: %s" %(_output_file_path_n_grams_with_out_pos), file = _output_file_verbose)
        except Exception as e:
            if _verbose:
                print("\tERROR writing n-grams to output file\n%s" %(str(e)), file = _output_file_verbose)
                print("\tERROR writing n-grams to output file\n%s" %(str(e)))
        if _verbose:
            print("\n--------------------------------------------------------------------------", file = _output_file_verbose)
            print("\t%d-gram extraction - Successful!!" %(_n_value_for_ngram_extraction), file = _output_file_verbose)
            print("--------------------------------------------------------------------------\n\n", file = _output_file_verbose)
    except Exception as e:
        if _verbose:
            print("\tERROR extracting n-grams!\n%s" %(str(e)), file = _output_file_verbose)
            print("\tERROR extracting n-grams\n%s" %(str(e)))

    # This method returns n-grams extracted with POS tags attached
    if _verbose:
        print("\t\t%d-gram extraction - successful" %(_n_value_for_ngram_extraction))
    return _n_grams_from_input_text_file, _input_file_path
