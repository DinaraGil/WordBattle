from BotLevel import BotLevel
from Settings import Word
from typing import Optional


def create_bot_word(game, attack_word, level):  # attack_word
    used_indexes = []
    best_point = 0
    best_word = None

    attack_word_bin = Word(attack_word)
    attack_word_bin_number = attack_word_bin.bin_number

    random_word: Optional[Word] = None
    random_index = 0

    while len(used_indexes) != 100:
        random_index = level.get_random_index()
        random_word = level.get_random_word()

        if random_index in used_indexes:
            continue

        used_indexes.append(random_index)

        if attack_word == '':
            best_word = random_word
            break

        if random_word.word in game.get_used_words():
            continue

        bin_word_number = random_word.bin_number

        mask = bin_word_number & attack_word_bin_number

        same_bits = 0
        while mask:
            same_bits += mask & 1
            mask >>= 1

        if same_bits > best_point:
            best_point = same_bits
            best_word = random_word

    formed_word = best_word.word
    return formed_word
