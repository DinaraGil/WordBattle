from abc import abstractmethod
#main player class

class IPlayer:
    def __init__(self, game, user_id, name: str, health: float):
        self._game = game
        self._index: int = -1
        self._name: str = name
        self._health: float = health
        self._user_id: int = user_id

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

    def new_word(self, *args, **kwargs):
        pass

    def get_reply_str(self):
        pass

    @property
    def user_id(self):
        return self._user_id
