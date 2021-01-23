from Word import Word
import random


class Settings:
    player_initial_health: float = 10
    TOKEN = '1237582120:AAHgVWV0UrKKm6cvaYHLqEI7dk0JKw2zNnA'
    # REQUEST_KWARGS = {'proxy_url': 'https://163.172.189.32:8811'}
    BOT_NAME = 'Бот'
    BOT_ID = 1237582120
    ALICE_NAME = 'Я'
    ALICE_ID = 1
    USERNAME = 'Вы'
    HELP_MESSAGE = 'Вы запустили навык "Заклинатель слов". Это приватный навык. Правила игры: мы по очереди атакуем друг друга словами. ' \
                   'Каждое последующее слово должно содержать буквы предыдущего в любом порядке.' \
                   'В начале игры каждый имеет десять пунктов здоровья.' \
                   'Если при защите, ваше слово не содержит все буквы предыдущего, вам наносится урон в размере количества пропущенных букв.' \
                   'Слово должно быть существительным, в начальной форме. Выберите один из трех уровней сложности. ' \
                   'Для повторения правил скажите "Помощь" или "Что ты умеешь?".'
    LEN_MARKS = [0, 37, 421, 1792, 4796, 8985, 14329, 20040, 25421, 29835, 33431, 36125, 38228, 39746,
                 40558, 41080, 41353, 41519, 41604, 41648, 41667, 41676, 41678, 41679]  # создание марок сделать циклом
    AVAILABLE_LEVELS = [1, 2, 3]
    FIRST_LEVEL_WORDS = ['1 уровень', '1', 'один', 'первый', 'уровень 1', 'первый уровень', 'один уровень',
                         'уровень один', 'уровень первый']
    SECOND_LEVEL_WORDS = ['2 уровень', '2', 'два', 'второй', 'уровень 2', 'второй уровень', 'два уровень',
                          'уровень два', 'уровень второй']
    THIRD_LEVEL_WORDS = ['3 уровень', '3', 'три', 'третий', 'уровень 3', 'третий уровень', 'три уровень',
                         'уровень три', 'уровень третий']


class WordTags:
    not_exist = "Такого слова не существует"
    not_normal_form = "Форма слова должна быть начальной"
    used = 'Слово {} уже встречалось'
    not_noun = 'Можно использовать только существительные'


class WordToBits:
    # with open('data/russian_nouns_sorted_by_len.txt', 'r', encoding='utf-8') as file:
    with open('data/nouns_from_pymorphy.txt', 'r', encoding='utf-8') as file:
        words = file.read().splitlines()

    BIN_WORDS = []

    for word in words:
        BIN_WORDS.append(Word(word))


class GameModes:
    with_bot = 'with_bot'
    with_users = 'with_users'


class FirstWords:
    with open('data/first_words.txt', 'r', encoding='utf-8') as file:
        first_words = file.read().splitlines()
