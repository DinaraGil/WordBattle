from Game import Game
from IPlayer import IPlayer
from Settings import WordToBits
import random
from Word import Word
from CreateBotWord import create_bot_word
from BotPlayer import BotPlayer
from BotLevel import BotLevel
import typing


class AliceBot(BotPlayer):
    def __init__(self, game: Game, user_id: int, name: str, health: float, level: int):
        super().__init__(game, user_id, name, health) #level
        self._game = game
        self._name = name
        self._reply_str = ''
        self._user_id = user_id
        self._formed_word = ''
        self._attack_word = ''
        self._level = BotLevel(level).get_level()

    def new_word(self, attack_word):
        self._game.on_player_word(self, attack_word)

    def create_new_word(self):  # attack_word
        self._formed_word = create_bot_word(self._game, self._attack_word, self._level)

    @property
    def formed_word(self):
        return self._formed_word

    def on_attack(self, attack_word: str):
        self._reply_str = 'Я атакован заклинанием "{}". Жизней осталось {}'.format(attack_word, self.health)
        self._attack_word = attack_word

    def get_attack_word(self):
        return self._attack_word

    def get_reply_str(self):
        return self._reply_str
