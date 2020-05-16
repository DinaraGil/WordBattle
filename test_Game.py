from unittest import TestCase

from Game import Game
#1

class TestGame(TestCase):
    def test__get_word1_diff_number(self):
        self.assertEqual(0, Game._get_word1_diff_number('', ''))
        self.assertEqual(0, Game._get_word1_diff_number('', 'one'))
        self.assertEqual(3, Game._get_word1_diff_number('one', ''))
        self.assertEqual(0, Game._get_word1_diff_number('one', 'one'))
        self.assertEqual(0, Game._get_word1_diff_number('o', 'one'))
        self.assertEqual(1, Game._get_word1_diff_number('ones', 'one'))
        self.assertEqual(0, Game._get_word1_diff_number('one', 'ones'))
        self.assertEqual(2, Game._get_word1_diff_number('one', 'two'))
        self.assertEqual(3, Game._get_word1_diff_number('blah', 'hope'))

    def test__get_word2_diff(self):
        self.assertEqual('', Game._get_word2_diff('', ''))
        self.assertEqual('eno', Game._get_word2_diff('', 'one'))
        self.assertEqual('', Game._get_word2_diff('one', ''))
        self.assertEqual('', Game._get_word2_diff('one', 'one'))
        self.assertEqual('en', Game._get_word2_diff('o', 'one'))
        self.assertEqual('', Game._get_word2_diff('ones', 'one'))
        self.assertEqual('s', Game._get_word2_diff('one', 'ones'))
        self.assertEqual('tw', Game._get_word2_diff('one', 'two'))
        self.assertEqual('eop', Game._get_word2_diff('blah', 'hope'))
