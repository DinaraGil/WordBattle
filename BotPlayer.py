import typing
from typing import Optional

from Game import Game
from IPlayer import IPlayer
from Settings import WordToBits
import random
from Word import Word
from Settings import create_range_of_indexes


class BotPlayer(IPlayer):
    def __init__(self, game: Game, user_id: int, name: str, health: float):
        super().__init__(game, user_id, name, health)
        self._game = game
        self._name = name
        self._reply_str = ''
        self._user_id = user_id
        self._formed_word = ''
        self._attack_word = ''

    def new_word(self, attack_word):
        self._game.on_player_word(self, attack_word)

    def create_new_word(self, game_level): #attack_word
        used_indexes = []
        best_point = 0
        best_word = None

        # attack_word = self._attack_word.lower().replace('ё', 'е')

        attack_word_bin = Word(self._attack_word)
        attack_word_bin_number = attack_word_bin.bin_number

        random_word: Optional[Word] = None
        random_index = 0

        while len(used_indexes) != 50:
            if game_level == 1:
                random_index = random.randint(0, len(WordToBits.WORDS_FIRST_LEVEL) - 1)
            elif game_level == 2:
                range_of_indexes = create_range_of_indexes(self._attack_word)
                random_index = random.choice(range_of_indexes)
            elif game_level == 3:
                random_index = random.randint(0, len(WordToBits.WORDS_SECOND_LEVEL) - 1)

            if random_index in used_indexes:
                continue

            used_indexes.append(random_index)

            if game_level == 1:
                random_word = WordToBits.WORDS_FIRST_LEVEL[random_index]
            elif game_level == 2 or game_level == 3:
                random_word = WordToBits.WORDS_SECOND_LEVEL[random_index]

            if self._attack_word == '':
                best_word = random_word
                break

            if random_word.word in self._game.get_used_words():
                continue

            bin_word_number = random_word.bin_number

            mask = bin_word_number & attack_word_bin_number

            same_bits = 0
            while mask:
                same_bits += mask & 1
                mask >>= 1

            if same_bits > best_point:
                best_point = same_bits
                best_word = random_word

        self._formed_word = best_word.word

    @property
    def formed_word(self):
        return self._formed_word

    def on_attack(self, attack_word: str):
        self._attack_word = attack_word
        self._reply_str = 'Игрок {} ({} жизней) атакован заклинанием "{}"'.format(self._name, self.health, attack_word)

    def get_reply_str(self):
        return self._reply_str

