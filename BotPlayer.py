from Game import Game
from IPlayer import IPlayer
from Settings import WordToBits
import random
from Word import Word
import typing
import time


class BotPlayer(IPlayer):
    def __init__(self, game: Game, name: str, health: float):
        super().__init__(game, name, health)
        self._game = game
        self._name = name
        self._reply_str = ''

    def new_word(self, attack_word):
        used_indexes = []
        best_point = 0
        best_word = None

        attack_word_bin = Word(attack_word)
        attack_word_bin_number = attack_word_bin.bin_number

        while len(used_indexes) != 50:
            random_index = random.randint(0, 50851)

            if random_index in used_indexes:
                continue

            used_indexes.append(random_index)

            bin_word = WordToBits.BIN_WORDS[random_index]
            bin_word_number = bin_word.bin_number

            mask = bin_word_number & attack_word_bin_number

            same_bits = 0
            while mask:
                same_bits += mask & 1
                mask >>= 1

            if same_bits > best_point:
                best_point = same_bits
                best_word = bin_word

        print(best_word.word)

        self._game.on_player_word(self, best_word)

    def on_attack(self, attack_word: str):
        self._reply_str = 'Игрок {} ({}❤) атакован заклинанием "{}""'.format(self._name, self.health, attack_word)

    def get_reply_str(self):
        return self._reply_str
