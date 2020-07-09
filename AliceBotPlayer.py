from Game import Game
from IPlayer import IPlayer
from Settings import WordToBits
import random
from Word import Word


class BotPlayer(IPlayer):
    def __init__(self, game: Game, user_id: int, name: str, health: float):
        super().__init__(game, user_id, name, health)
        self._game = game
        self._name = name
        self._reply_str = ''
        self._user_id = user_id
        self._formed_word = ''

    def new_word(self, attack_word):
        self._game.on_player_word(self, attack_word)

    def create_new_word(self, attack_word):
        used_indexes = []
        best_point = 0
        best_word = None

        attack_word = attack_word.lower().replace('ё', 'е')

        attack_word_bin = Word(attack_word)
        attack_word_bin_number = attack_word_bin.bin_number

        while len(used_indexes) != 50:
            random_index = random.randint(0, len(WordToBits.BIN_WORDS) - 1)

            if random_index in used_indexes:
                continue

            used_indexes.append(random_index)

            bin_word = WordToBits.BIN_WORDS[random_index]
            bin_word_number = bin_word.bin_number

            if bin_word.word in self._game.get_used_words():
                continue

            mask = bin_word_number & attack_word_bin_number

            same_bits = 0
            while mask:
                same_bits += mask & 1
                mask >>= 1

            if same_bits > best_point:
                best_point = same_bits
                best_word = bin_word

        self._formed_word = best_word.word

    @property
    def formed_word(self):
        return self._formed_word

    def on_attack(self, attack_word: str):
        self._reply_str = 'Игрок {} ({}❤) атакован заклинанием "{}"'.format(self._name, self.health, attack_word)

    def get_reply_str(self):
        return self._reply_str