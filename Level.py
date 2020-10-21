import random
from Settings import WordToBits
from Settings import Settings
from typing import Optional


class Level:
    def __init__(self, random_index, random_word):
        self.random_index = random_index
        self.random_word = random_word

    def get_random_index(self):
        return self.random_index

    def get_random_word(self):
        return self.random_word


class FirstLevel(Level):
    def __init__(self):
        self.range_of_indexes = list(range(0, Settings.LEN_MARKS[4] + 1))
        random_index = random.choice(self.range_of_indexes)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)

    def get_random_index(self):
        random_index = random.choice(self.range_of_indexes)
        return random_index

    def get_random_word(self):
        random_word = WordToBits.WORDS_SECOND_LEVEL[self.get_random_index()]
        return random_word


class SecondLevel(Level):
    def __init__(self):
        self.range_of_indexes = list(range(0, Settings.LEN_MARKS[6] + 1))
        random_index = random.choice(self.range_of_indexes)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)

    def get_random_index(self):
        random_index = random.choice(self.range_of_indexes)
        return random_index

    def get_random_word(self):
        random_word = WordToBits.WORDS_SECOND_LEVEL[self.get_random_index()]
        return random_word


class ThirdLevel(Level):
    def __init__(self):
        random_index = random.randint(0, len(WordToBits.WORDS_SECOND_LEVEL) - 1)
        random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

        super().__init__(random_index, random_word)

    def get_random_index(self):
        random_index = random.randint(0, len(WordToBits.WORDS_SECOND_LEVEL) - 1)
        return random_index

    def get_random_word(self):
        random_word = WordToBits.WORDS_SECOND_LEVEL[self.get_random_index()]
        return random_word


class GameLevel:
    def __init__(self, level_number):
        self.level: Optional[Level] = None
        if level_number == 1:
            self.level = FirstLevel()
        elif level_number == 2:
            self.level = SecondLevel()
        elif level_number == 3:
            self.level = ThirdLevel()

    def get_level(self):
        return self.level
