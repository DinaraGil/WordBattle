from Game import Game
from IPlayer import IPlayer


class AiPlayer(IPlayer):
    def __init__(self, game: Game, health: float):
        super().__init__(game, health)

    def on_attack(self, attack_word: str):
        pass
