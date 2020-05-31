class Word:
    def __init__(self, word):
        self._word = word
        self._bin_number = self.make_number(self._word)

    def make_number(self, word: str):
        word = word.replace('ё', 'е')

        word_mask = 0
        for letter in word:
            letter_index = ord(letter) - ord('а')
            letter_mask = 1 << letter_index

            while (letter_mask & word_mask) != 0:
                letter_mask = letter_mask << 32

            word_mask = word_mask | letter_mask

        return word_mask

    @property
    def bin_number(self):
        return self._bin_number

    @property
    def word(self):
        return self._word

