from Game import Game
from IPlayer import IPlayer
from Settings import Settings


class AlicePlayer(IPlayer):
    def __init__(self, game: Game, user_id: int, health: float):
        super().__init__(game, user_id, Settings.USERNAME, health)
        self._game: Game = game
        self._user_id = user_id
        self._username = Settings.USERNAME
        self._reply_str = ''

    def new_word(self, word):
        new_word = word
        self._game.on_player_word(self, new_word)

    def on_attack(self, attack_word: str):
        self._reply_str = 'Игрок {} ({} жизней) атакован заклинанием "{}"'.format(self._name, self.health, attack_word)

    def get_reply_str(self):
        return self._reply_str

    @property
    def user_id(self):
        return self._user_id
