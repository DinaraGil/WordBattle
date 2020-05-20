import sys
from typing import List
from IPlayer import IPlayer
from Settings import Settings


class Game:
    def __init__(self):
        self._players: List[IPlayer] = []
        self._last_attack_word: str = ''
        self._current_player_index: int = 0
        self._used_words: List[str] = []
        self._gameover = False
        self._winner: IPlayer

    def start(self):
        self._current_player_index = 0
        self._players: List[IPlayer] = []
        self._last_attack_word: str = ''
        self._used_words = []
        self._gameover = False
        self._winner: IPlayer

    def on_player_word(self, player: IPlayer, word: str): # -> bool:
        if player.index != self._current_player_index:
            return

        self._calculate_player_health(player, word)

        if player.health <= 0:
            self._select_next_player()
            self._winner = self._players[self._current_player_index]
            self._gameover = True
            return

        self._select_next_player()

        self._attack(word)

        self._used_words.append(word.lower())

    def is_word_correct(self, word):
        if word.lower() in Settings.WORDS:
            return True
        return False

    def is_word_used(self, word):
        if word.lower() in self._used_words:
            return True
        return False

    def add_player(self, player: IPlayer):
        if len(self._players) == 2:
            raise RuntimeError('players cannot be more than two')

        player.index = len(self._players) - 1
        self._players.append(player)

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
    def _get_word1_diff_number(word1: str, word2: str) -> int:
        word1 = word1.lower()
        word2 = word2.lower()

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
        word1 = word1.lower()
        word2 = word2.lower()

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

    def get_current_player(self):
        return self._players[self._current_player_index]

    def get_winner(self):
        return self._winner

    def is_gameover(self):
        return self._gameover

    def get_players(self) -> List[IPlayer]:
        return self._players
