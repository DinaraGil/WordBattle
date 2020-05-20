from abc import abstractmethod


class IPlayer:
    def __init__(self, game, name: str, health: float):
        self._game = game
        self._index: int = -1
        self._name: str = name
        self._health: float = health

    @property
    def game(self):
        return self._game

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int):
        self._index = index

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, health: float):
        self._health = health

    @abstractmethod
    def on_attack(self, attack_word: str):
        pass

    def new_word(self, text):
        pass
