class Settings:
    player_initial_health: float = 10
    TOKEN = '1237582120:AAHgVWV0UrKKm6cvaYHLqEI7dk0JKw2zNnA'
    REQUEST_KWARGS = {'proxy_url': 'https://51.15.80.136:3128'}


class WordTags:
    not_exist = "Такого слова не существует"
    not_normal_form = "Форма слова должна быть начальной"

    # with open('data/russian_nouns.txt', 'r', encoding='utf-8') as file:
    #     WORDS = set(file.read().splitlines())
