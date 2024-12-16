
from IPlayer import IPlayer
from Game import Game
from Settings import Settings
from abc import abstractclassmethod


class ConsolePlayer(IPlayer):
    def __init__(self, game: Game, user_id: int, name: str, health: float):
        super().__init__(game, user_id, name, health)
        self._game: Game = game
        self._user_id = user_id
        self._username = name
        self._reply_str = ''

    def new_word(self, word):
        new_word = word
        self._game.on_player_word(self, new_word)

    def on_attack(self, attack_word: str):
        self._reply_str = 'Игрок {} ({}❤) атакован заклинанием "{}"'.format(self._name, self.health, attack_word)

    def get_reply_str(self):
        return self._reply_str

    @property
    def user_id(self):
        return self._user_id


game = Game()

player1 = ConsolePlayer(game, 1, 'Аня', Settings.player_initial_health)
player2 = ConsolePlayer(game, 2, 'Петя', Settings.player_initial_health)

game.start()

game.add_player(player1)
game.add_player(player2)

for i in range(5):
    player2.new_word(input('Петя: '))
    print(player1.get_reply_str())

    player1.new_word(input('Аня: '))
    print(player2.get_reply_str())
