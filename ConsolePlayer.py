import asyncio

from Game import Game
from IPlayer import IPlayer


class ConsolePlayer(IPlayer):
    def __init__(self, game: Game, name: str, health: float):
        super().__init__(game, name, health)
        self._game: Game = game
        self._name: str = name

    def on_attack(self, attack_word: str):
        print('Player {} ({}) attacked by word {}'.format(self._name, self.health, attack_word))
        asyncio.run(self._do_input())

    async def _do_input(self):
        new_word = input()
        self._game.on_player_word(self, new_word)
