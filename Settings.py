from Word import Word
import random


class Settings:
    player_initial_health: float = 10
    TOKEN = '1237582120:AAHgVWV0UrKKm6cvaYHLqEI7dk0JKw2zNnA'
    REQUEST_KWARGS = {'proxy_url': 'https://163.172.189.32:8811'}
    BOT_NAME = 'Бот'
    BOT_ID = 1237582120
    ALICE_NAME = 'Алиса'
    ALICE_ID = 1


class WordTags:
    not_exist = "Такого слова не существует"
    not_normal_form = "Форма слова должна быть начальной"
    used = 'Слово {} уже встречалось'


class WordToBits:
    with open('data/russian_nouns_sorted_by_len.txt', 'r', encoding='utf-8') as file:
        words = file.read().splitlines()

    BIN_WORDS = []
    for word in words:
        BIN_WORDS.append(Word(word))


class LenMarks:
    LEN_MARKS = [0, 54, 524, 2129, 5602, 10432, 16746, 23602, 30169, 35627, 40162, 43640, 46349, 48313,
                 49405, 50076, 50423, 50640, 50752, 50810, 50838, 50849]


class GameModes:
    with_bot = 'with_bot'
    with_users = 'with_users'


class FirstWords:
    with open('data/first_words.txt', 'r', encoding='utf-8') as file:
        first_words = file.read().splitlines()