from Word import Word


class Settings:
    player_initial_health: float = 10
    TOKEN = '1237582120:AAHgVWV0UrKKm6cvaYHLqEI7dk0JKw2zNnA'
    REQUEST_KWARGS = {'proxy_url': 'https://51.15.80.136:3128'}


class WordTags:
    not_exist = "Такого слова не существует"
    not_normal_form = "Форма слова должна быть начальной"


class WordToBits:
    with open('data/russian_nouns_sorted_by_len.txt', 'r', encoding='utf-8') as file:
        words = file.read().splitlines()

    BIN_WORDS = []
    for word in words:
        BIN_WORDS.append(Word(word))


class LenMarks:
    LEN_MARKS = [0, 54, 524, 2129, 5602, 10432, 16746, 23602, 30169, 35627, 40162, 43640, 46349, 48313,
                 49405, 50076, 50423, 50640, 50752, 50810, 50838, 50849]