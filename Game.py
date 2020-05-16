import sys
from typing import List

from IPlayer import IPlayer
#1

class Game:
    def __init__(self):
        self._players: List[IPlayer] = []
        self._last_attack_word: str = ''
        self._current_player_index: int = 0

    def on_player_word(self, player: IPlayer, word: str) -> bool:
        if player.index != self._current_player_index:
            return False

        self._calculate_player_health(player, word)

        if player.health <= 0:
            self._game_over()

        self._select_next_player(player)

        self._attack_current_player(word)

        return True

    def add_player(self, player: IPlayer):
        if len(self._players) == 2:
            raise RuntimeError('players cannot be more than two')

        player.index = len(self._players)
        self._players.append(player)

    def get_players(self) -> List[IPlayer]:
        return self._players

    def start(self):
        if len(self._players) != 2:
            raise RuntimeError('should be two players')
        self._current_player_index = 0
        player = self._players[self._current_player_index]
        player.on_attack('')

    def _select_next_player(self):
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def _calculate_player_health(self, player: IPlayer, word: str):
        diff = self._get_word1_diff_number(self._last_attack_word, word)
        player.health -= diff

    def _attack(self, word: str):
        words_diff = self._get_word2_diff(self._last_attack_word, word)
        self._last_attack_word = words_diff

        player = self._players[self._current_player_index]
        player.on_attack(words_diff)

    @staticmethod
    def _game_over():
        sys.exit(0)

    @staticmethod
    def _get_word1_diff_number(word1: str, word2: str) -> int:
        diff = len(word1)
        if not word1 or not word2:
            return diff

        word1_sorted = sorted(list(word1))
        word2_sorted = sorted(list(word2))

        i = 0
        j = 0
        while i < len(word1_sorted):
            if j >= len(word2_sorted):
                break
            ch1 = word1_sorted[i]
            ch2 = word2_sorted[j]
            if ch1 == ch2:
                diff -= 1
                i += 1
                j += 1
            elif ch1 < ch2:
                i += 1
            else:
                j += 1

        return diff

    @staticmethod
    def _get_word2_diff(word1: str, word2: str) -> str:
        word1_sorted = sorted(list(word1))
        word2_sorted = sorted(list(word2))

        if not word1:
            return ''.join(word2_sorted)

        diff = ''

        i = 0
        j = 0
        while j < len(word2_sorted):
            if i >= len(word1_sorted):
                diff += ''.join(word2_sorted[j:])
                break
            ch1 = word1_sorted[i]
            ch2 = word2_sorted[j]
            if ch1 == ch2:
                i += 1
                j += 1
            elif ch2 < ch1:
                j += 1
                diff += ch2
            else:
                i += 1

        return diff
