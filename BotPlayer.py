import typing
from typing import Optional
from CreateBotWord import create_bot_word
from Game import Game
from IPlayer import IPlayer
from Settings import WordToBits
import random
from Word import Word
from BotLevel import BotLevel


class BotPlayer(IPlayer):
    def __init__(self, game: Game, user_id: int, name: str, health: float): #level
        super().__init__(game, user_id, name, health)
        self._game = game
        self._name = name
        self._reply_str = ''
        self._user_id = user_id
        self._formed_word = ''
        self._attack_word = ''
        self._level = BotLevel(1).get_level()

    def new_word(self, attack_word):
        self._game.on_player_word(self, attack_word)

    def create_new_word(self): #attack_word
        self._formed_word = create_bot_word(self._game, self._attack_word, self._level)

    @property
    def formed_word(self):
        return self._formed_word

    def on_attack(self, attack_word: str):
        self._attack_word = attack_word
        self._reply_str = 'Игрок {} ({} жизней) атакован заклинанием "{}"'.format(self._name, self.health, attack_word)

    def get_attack_word(self):
        return self._attack_word

    def get_reply_str(self):
        return self._reply_str
