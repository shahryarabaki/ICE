import nltk
from nltk.corpus import ptb
from nltk.corpus import treebank
import re


def POS_tag_cleaner(phrase_with_POS):
    phrase_with_POS = phrase_with_POS + ' '
    _ngram_without_pos = re.sub(r'_.*? ', ' ', phrase_with_POS)
    _ngram_without_pos = re.sub(r" +'s ", "'s ", _ngram_without_pos)
    _ngram_without_pos = _ngram_without_pos.strip()
    return _ngram_without_pos


class POS_Tagger():


    def __init__(self):
        training_sents = treebank.tagged_sents()
        patterns = [  # for regexp tagger
            (r'^[\.|\?|!]$', '.'),
            (r'^,$', ','),
            (r'^\'$', '\'\''),
            (r'^\"$', '\"'),
            (r'^\($', '('),
            (r'^\)$', ')'),
            (r'^[=|/]$', 'SYM'),
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
            (r'^[0-9][0-9]*$', 'CD'),
            (r'^[0-9]([0-9]*[-|.|,|/][0-9]*)*$', 'CD'),
            (r'^([0-9]*\.[0-9]*)*$', 'CD'),
            (r'^[^a-zA-Z]*$', ':'),
            (r'[A-Z].*', 'NNP'),
            (r'.*', 'NN')]

        default_tagger = nltk.DefaultTagger('NN')
        regexp_tagger = nltk.RegexpTagger(patterns, backoff=default_tagger)
        unigram_tagger = nltk.UnigramTagger(training_sents, backoff=regexp_tagger)
        bigram_tagger = nltk.BigramTagger(training_sents, backoff=unigram_tagger)
        trigram_tagger = nltk.TrigramTagger(training_sents, backoff=bigram_tagger)

        self.final_tagger = trigram_tagger


    def tag(self, sentence):
        return self.final_tagger.tag(sentence)