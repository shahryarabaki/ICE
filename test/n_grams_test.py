import unittest
from unittest.mock import mock_open, patch
from src.n_grams import (
    ascii_normalize, 
    POS_tag_cleaner, 
    expand_contractions, 
    tokenize_to_words,
    POS_tag_tokenized_phrases,
    remove_selected_strings_from_tokenized_POS_phrases,
    join_tokenized_tagged_phrases,
    split_sentence_from_text,
    split_subsentence_using_quotes,
    remove_tagged_quotes)
from nltk.corpus import brown
import nltk
import builtins
import string


class n_grams_test(unittest.TestCase):

    def test_canary(self):
        self.assertTrue(True)


    def test_weird_quote_characters_for_ascii(self):
        self.assertEqual(["''"], 
            ascii_normalize(["’‛"]))


    def test_translate_to_ascii_from_bytes_string(self):
        self.assertEqual(["Gavin O'Connor"], 
            ascii_normalize([u'Gavin O’Connor']))


    def test_translate_to_ascii_unidecode_special_alphabet_char(self):
        self.assertEqual(['e'], 
            ascii_normalize(['é']))


    def test_POS_cleaner_noun_verb(self):
        self.assertEqual('to you', POS_tag_cleaner('to_VB you_NN'))


    def test_POS_tag_cleaner_join_s_possessive_at_the_end(self):
        self.assertEqual("noun's", POS_tag_cleaner("noun_NN 's_POS"))


    def test_POS_tag_cleaner_join_s_posesssive_at_the_middle(self):
        self.assertEqual("noun's love", 
            POS_tag_cleaner("noun_NN 's_POS love_NN"))


    def test_POS_tag_cleaner_join_s_posesssive_without_proper_tag(self):
        self.assertEqual("noun's love", 
            POS_tag_cleaner("noun_NN 's_PO love_NN"))


    def test_POS_tag_cleaner_join_s_posesssive_with_lot_middles_spaces(self):
        self.assertEqual("noun's love", 
            POS_tag_cleaner("noun_NN    's_PO love_NN"))



    def test_POS_tag_cleaner_clear_left_and_right_spaces(self):
        self.assertEqual("noun's love", 
            POS_tag_cleaner("   noun_NN 's_POS love_NN   "))


    def test_expand_contractions_with_one_sentence(self):
        TEST_TEXT = ["haven't\thave not", "shouldn't\tshould not"]
        m = unittest.mock.mock_open(read_data='\n'.join(TEST_TEXT))
        m.return_value.__iter__ = lambda x: x
        m.return_value.__next__ = lambda x: x.readline()
        with patch('builtins.open', m):
            self.assertEqual(
                ["You should not try to study when you're tired"],
                expand_contractions((
                ["You shouldn't try to study when you're tired"])))


    def test_tokenize_to_words_also_tokenzie_punctuation(self):
        self.assertEqual(
            [ ['who', 'are', 'your', 'friend', "'s", 'here', '?'] ],
            tokenize_to_words(["who are   your friend's here?"]))


    def test_tokenize_words_double_quotes_to_double_single_forward(self):
        self.assertEqual(
            [ ['who', 'are', '``', 'your', "''", 'friend', "'s", 'here', '?'] ],
            tokenize_to_words([ "who are   \"your\" friend's here?" ]))


    def test_POS_tag_tokenize_words_simple_test(self):
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
        
        final_tagger = trigram_tagger

        self.assertEqual(
            [[('who', 'WPS'),
            ('are', 'BER'),
            ('your', 'PP$'),
            ('friend', 'NN'),
            ("'s", 'POS'),
            ('here', 'RB'),
            ('?', '.')]],
            POS_tag_tokenized_phrases(
                [ ['who', 'are', 'your', 'friend', "'s", 'here', '?'] ],
                final_tagger))


    def test_remove_punc_not_quotes_from_tokenized_POS_phrases(self):
        punctuation = set(string.punctuation)
        quotes = set(['\"','\'','``','\'\''])
        punc_without_quotes = punctuation - quotes

        self.assertEqual(
            [ [('who', 'WPS'), 
            ('are', 'BER'), 
            ('``', '``'), 
            ('your', 'PP$'), 
            ("''", "''"), 
            ('friend', 'NN'), 
            ("'s", 'POS'), 
            ('here', 'RB')] ],
            remove_selected_strings_from_tokenized_POS_phrases(
                [ [('who', 'WPS'), 
                ('are', 'BER'), 
                ('``', '``'), 
                ('your', 'PP$'), 
                ("''", "''"), 
                ('friend', 'NN'), 
                ("'s", 'POS'), 
                ('here', 'RB'), 
                ('?', '.')] ], punc_without_quotes))


    def test_join_tokenized_pos_tagged_has_space_between(self):
        sentence = ([[
            ('who', 'WPS'), 
            ('are', 'BER'), 
            ('``', '``'), 
            ('your', 'PP$-HL'), 
            ("''", "''"), 
            ('friend', 'NN'), 
            ("'s", 'POS'), 
            ('here', 'RB'), 
            ('?', '.')]])
        self.assertEqual(
            join_tokenized_tagged_phrases(sentence),
            [("who_WPS are_BER ``_`` your_PP$-HL ''_'' "
                "friend_NN 's_POS here_RB ?_.")])


    def test_split_sentence_from_multiple_paragraphs(self):
        text_lines = ([
            "Who am i kidding? I am not a good programmer.\n",
            "Are you kidding me? You are the best programmer I know!\n"])

        self.assertEqual(
            split_sentence_from_text(text_lines),
            ["Who am i kidding?", 
            "I am not a good programmer.",
            "Are you kidding me?",
            "You are the best programmer I know!"])


    def test_subsentence_splitter_to_split_double_forward_quotes(self):
        text = ('who am i "_" nah "_" ``_`` '
            'fucking crazy die to day ''_'' '
            '\'_\' who should i vote for \'_\' people die?')

        self.assertEqual(
            split_subsentence_using_quotes([text]),
            ['who am i "_" nah "_" ', 
            'fucking crazy die to day ', 
            'who should i vote for ', 
            ' people die?'])


    def test_remove_tagged_quotes_from_sentences(self):
        text = 'who am i "_" nah ''_'' '

        self.assertEqual(
            remove_tagged_quotes([text]),
            ['who am i nah'])



