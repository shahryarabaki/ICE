import nltk
from nltk.corpus import stopwords
import re
import string
import nltk.data
import itertools
from nltk.corpus import brown
from nltk.tokenize import punkt
import sys
from nltk.tag import pos_tag
from unidecode import unidecode


def ascii_normalize(input_lines):

    def string_to_ascii(x):
        x = unidecode(x)        
        x = ''.join(filter(lambda char: char in string.printable, x))
        return x

    return list(map(string_to_ascii, input_lines))


def expand_contractions(input_lines):

    contraction_dictionary = {}

    with open(sys.path[0] + "/English_contractions.txt", 'r') as f:
        for each_contraction in f:
            contraction, expansion = map(
                lambda x: x.strip().lower(),
                each_contraction.strip('\n').split('\t')[:2])
            contraction_dictionary[contraction] = expansion

    def replace_contraction_in_sentence(sentence):
        for _word in sentence.split(' '):
            if _word.lower().strip('\n') in contraction_dictionary:
                sentence = sentence.replace(
                    _word.strip(), 
                    contraction_dictionary[_word.lower().strip()])
        return sentence

    _input_sentences_no_contractions = list(map(replace_contraction_in_sentence,
        input_lines))

    return _input_sentences_no_contractions


def tokenize_to_words(phrases):
    return list(map(nltk.word_tokenize,
        phrases))


def POS_tag_tokenized_phrases(tokenized_phrases, tagger):
    return list(map(tagger.tag, tokenized_phrases))


def remove_selected_strings_from_tokenized_POS_phrases(POS_tagged_phrases,
    set_of_strings):

    def remove_punc_not_quotes_from_tagged_sentence(tagged_sentence):
        return list(filter(
            lambda tagged_word: tagged_word[0] not in set_of_strings,
            tagged_sentence))

    return list(map(
        remove_punc_not_quotes_from_tagged_sentence,
        POS_tagged_phrases))


def join_tokenized_tagged_phrases(POS_tagged_phrases):

    def join_sentence(tokenized_tagged_sentence):
        return " ".join(map(lambda token: token[0] + '_' + token[1], 
            tokenized_tagged_sentence))

    return list(map(join_sentence,
        POS_tagged_phrases))


def split_sentence_from_text(text_lines):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    sentences = map(
        lambda line: sent_detector.tokenize(line.strip()),
        text_lines)

    return list(itertools.chain.from_iterable(sentences))


def split_subsentence_using_quotes(sentences):
    subsentence_splitter = (re.compile(
        r'``_``\s*?((?:\w+\s+){2,})\s*?''_''|'
        '\'_\'\s*?((?:\w+\s+){2,})\s*?\'_\'|'
        '"_"\s*?((?:\w+\s+){2,})\s*?"_"'))

    def split_subsentence_re(sentence):
        return filter(lambda token: token and token.strip() != '', 
            subsentence_splitter.split(sentence))

    return list(itertools.chain.from_iterable(
        map(split_subsentence_re, sentences)))


def remove_tagged_quotes(sentences):
    quotes_match = re.compile('\s*(``_``|''_''|"_")\s*')

    def quotes_for_space(sentence):
        return quotes_match.sub(' ', sentence).strip()

    return list(map(quotes_for_space, sentences))


def output_to_file(file_path, lines):
    with open(file_path, 'w') as f:
        for line in lines:
            print(line, file = f)


def ngrams_from_file_lines(input_file_path, 
    verboseprint=lambda *a, **k: None,
    output = False,
    POS_clean = False,
    injected_tagger = None):
    
    output_print = output_to_file if output else lambda *a, **k: None
    

    with open(input_file_path, 'r') as f:
        input_lines = f.readlines()


    file_directory = input_file_path.rpartition('/')[0] + '/'


    file_path_ascii = file_directory + 'ascii.txt'

    verboseprint(("\n\tClean text after removing non-ascii characters is saved "
        "to the file:\n\t{}"
        .format(file_path_ascii)))

    ascii_lines = ascii_normalize(input_lines)

    output_print(file_path_ascii, ascii_lines)


    file_path_no_contractions = file_directory + 'no_contractions.txt'

    verboseprint("\tExpanding the contractions ...")

    no_contraction_lines = expand_contractions(ascii_lines)

    output_print(file_path_no_contractions, no_contraction_lines)

    verboseprint(("\tText after contractions are replaced is written "
        "to the file:\n\t{}".format(file_path_no_contractions)))


    tokenized_phrases = tokenize_to_words(no_contraction_lines)

    if not injected_tagger:
        training_sents = brown.tagged_sents()
        patterns = [ # for regexp tagger
            (r'.*ing$', 'VBG'),
            (r'.*ed$', 'VBD'),
            (r'.*es$', 'VBZ'),
            (r'.*ould$', 'MD'),
            (r'.*\'s$', 'POS'),
            (r'.*s$', 'NNS'),
            (r'(The|the|A|a|An|an)$', 'AT'),
            (r'.*able$', 'JJ'),
            (r'.*ly$', 'RB'),
            (r'.*s$', 'NNS'),
            (r'.*', 'NN')]
        default_tagger = nltk.DefaultTagger('NN')
        regexp_tagger = nltk.RegexpTagger(patterns, backoff=default_tagger)
        unigram_tagger = nltk.UnigramTagger(training_sents, backoff=regexp_tagger)
        bigram_tagger = nltk.BigramTagger(training_sents, backoff=unigram_tagger)
        trigram_tagger = nltk.TrigramTagger(training_sents, backoff=bigram_tagger)        
        injected_tagger = trigram_tagger

    tokenized_POS_tagged_phrases = POS_tag_tokenized_phrases(tokenized_phrases,
        injected_tagger)

    punctuation = set(string.punctuation)
    quotes = set(['\"','\'','``','\'\''])
    punc_with_quotes = punctuation - quotes
    removed_punc_phrases = remove_selected_strings_from_tokenized_POS_phrases(
        tokenized_POS_tagged_phrases,
        punc_with_quotes)

    phrases = join_tokenized_tagged_phrases(removed_punc_phrases)

    output_file_path_pos_tagged = file_directory + 'pos_tagged.txt'
    output_print(output_file_path_pos_tagged, no_contraction_lines)

    return phrases


def pos_tagged_ngrams(_input_file_path, _n_value_for_ngram_extraction, _stop_word_removal, _verbose):
    pass

    



