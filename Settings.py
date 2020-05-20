class Settings:
    player_initial_health: float = 10
    TOKEN = '1237582120:AAHgVWV0UrKKm6cvaYHLqEI7dk0JKw2zNnA'
    REQUEST_KWARGS = {'proxy_url': 'https://140.238.19.197:3128'}
    with open('data/russian_nouns.txt', 'r', encoding='utf-8') as file:
        WORDS = file.read().splitlines()
