import random
from Settings import WordToBits
from Settings import Settings


class Level:
    def __init__(self, random_index, random_word):
        self.random_index = 0
        self.random_word = ''

    @property
    def get_random_index(self):
        return self.random_index

    @property
    def get_random_word(self):
        return self.random_word


class First_level(Level):
    def __init__(self):
        range_of_indexes = list(range(0, Settings.LEN_MARKS[4] + 1))
        random_index = random.choice(range_of_indexes)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)


class Second_level(Level):
    def __init__(self):
        range_of_indexes = list(range(0, Settings.LEN_MARKS[6] + 1))
        random_index = random.choice(range_of_indexes)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)


class Third_level(Level):
    def __init__(self):
        random_index = random.randint(0, len(WordToBits.WORDS_SECOND_LEVEL) - 1)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)
