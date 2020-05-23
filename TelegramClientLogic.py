import logging
from Game import Game
from Settings import Settings
from TelegramPlayer import TelegramPlayer
from Settings import WordTags

logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("TelegramClientLogic_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class TelegramClientLogic:
    def __init__(self):
        setup_logger()
        self._games = {}

    def start(self, chat_id):
        game = self.get_or_create_game(chat_id)
        game.start()

        logger.info('Game started. Chat_id = {}'.format(chat_id))

    def get_or_create_game(self, chat_id: int):
        game = self._games.get(chat_id, None)
        if game is None:
            game = Game()
            self._games[chat_id] = game

        return game

    def add_player(self, chat_id, user_id, username):
        game = self.get_or_create_game(chat_id)
        health = Settings.player_initial_health

        player = TelegramPlayer(game, user_id, username, health)
        game.add_player(player)

        logger.info('Add new player. Chat_id = {}, username = {}, user_id = {}'.format(chat_id, username, user_id))

    def get_player(self, chat_id, user_id):
        game = self.get_or_create_game(chat_id)

        for player in game.get_players():
            if player.user_id == user_id:
                return player

    def get_message(self, text, chat_id, user_id):
        game = self.get_or_create_game(chat_id)

        if len(game.get_players()) < 2:
            self.add_player(chat_id, user_id, text)

            if len(game.get_players()) == 2:
                return 'Игра началась. Первым ходит игрок {}'.format(game.get_current_player().name)
        else:
            player = self.get_player(chat_id, user_id)

            if game.get_current_player() != player:
                return

            word_checking_result = game.word_checking(text)

            if word_checking_result == WordTags.not_exist:
                logger.info("Word doesn't exist. Chat_id = {}, word = {}, user_id = {}".format(chat_id, text, user_id))
                return WordTags.not_exist

            if word_checking_result == WordTags.not_normal_form:
                logger.info("Not normal form of word. Chat_id = {}, word = {}, user_id = {}".format(chat_id, text, user_id))
                return WordTags.not_normal_form

            if game.is_word_used(text):
                logger.info("Word used. Chat_id = {}, word = {}, user_id = {}".format(chat_id, text, user_id))
                return 'Слово {} уже встречалось'.format(text)

            player.new_word(text)

            attacked_player = game.get_current_player()

            return attacked_player.get_reply_str()

    def is_gameover(self, chat_id):
        game = self.get_or_create_game(chat_id)
        return game.is_gameover()

    def get_gameover_message(self, chat_id):
        game = self.get_or_create_game(chat_id)
        return 'Игра окончена. Выиграл игрок {} ({}❤). Чтобы начать новую игру используйте комманду /start'.format(
                game.get_winner().name,
                game.get_winner().health)
