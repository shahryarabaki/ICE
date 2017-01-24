import nltk
from nltk.corpus import ptb
from nltk.corpus import treebank
import re
import os, pickle


def POS_tag_cleaner(phrase_with_POS):
    phrase_with_POS = phrase_with_POS + ' '
    _ngram_without_pos = re.sub(r'_.*? ', ' ', phrase_with_POS)
    _ngram_without_pos = re.sub(r" +'s ", "'s ", _ngram_without_pos)
    _ngram_without_pos = _ngram_without_pos.strip()
    return _ngram_without_pos


class POS_Tagger():


    def __init__(self):
        if not self._load():
            self._train_tagger()
            self._save()


    def _train_tagger(self):
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


    def _load(self, rel_dump_path = "cache/pos_tagger.dump"):
        script_dir = os.path.dirname(__file__)
        obj_dump_path = os.path.join(script_dir, rel_dump_path)
        if os.path.isfile(obj_dump_path):
            with open(obj_dump_path, 'rb') as obj_dump:
                try:
                    self.final_tagger = pickle.load(obj_dump)
                    return True
                except Exception as e:
                    return False
        return False


    def _save(self, rel_dump_path = "cache/pos_tagger.dump"):
        script_dir = os.path.dirname(__file__)
        obj_dump_path = os.path.join(script_dir, rel_dump_path)
        with open(obj_dump_path, 'wb') as obj_dump_file:
            pickle.dump(self.final_tagger, obj_dump_file)


    def tag(self, sentence):
        return self.final_tagger.tag(sentence)