import logging

from Game import Game
from Settings import Settings
from Settings import WordTags
from BotPlayer import BotPlayer
from AlicePlayer import AlicePlayer


logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("AliceLogic_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class AliceLogic:
    def __init__(self):
        setup_logger()
        self._games = {}

    def to_first_word(self, game):
        player2 = game.get_current_player()

        first_word = game.get_first_word()

        player2.new_word(first_word)

        player1 = game.get_current_player()

        return player1.get_reply_str()

    def start(self, session_id, user_id, is_session_new=True):
        game = self.get_or_create_game(session_id)
        game.start()

        logger.info('Game started. session_id = {}'.format(session_id))

        self.add_player(session_id, user_id)
        self.add_player(session_id, Settings.ALICE_ID)

        if is_session_new:
            return Settings.HELP_MESSAGE + 'Я начинаю игру. ' + self.to_first_word(game)

        return 'Я начинаю игру. ' + self.to_first_word(game)

    def get_or_create_game(self, session_id: int):
        game = self._games.get(session_id, None)
        if game is None:
            game = Game()
            self._games[session_id] = game

        return game

    def add_player(self, session_id, user_id):
        game = self.get_or_create_game(session_id)
        health = Settings.player_initial_health

        if self.get_player(session_id, user_id) is None:
            if user_id == Settings.ALICE_ID:
                player = BotPlayer(game, user_id, Settings.ALICE_NAME, health)

            else:
                player = AlicePlayer(game, user_id, health)

            game.add_player(player)

        logger.info('Add new player. Session_id = {}, user_id = {}'.format(session_id, user_id))

    def get_player(self, session_id, user_id):
        game = self.get_or_create_game(session_id)

        for player in game.get_players():
            if player.user_id == user_id:
                return player

    def process_user_message(self, text, session_id, user_id):
        game = self.get_or_create_game(session_id)

        player = self.get_player(session_id, user_id)

        if game.get_current_player() != player:
            return

        word_checking_result = game.word_checking(text)

        if word_checking_result == WordTags.not_exist:
            logger.info("Word doesn't exist. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_exist

        if word_checking_result == WordTags.not_normal_form:
            logger.info("Not normal form of word. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_normal_form

        if word_checking_result == WordTags.not_noun:
            logger.info("Not noun. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_noun

        if game.is_word_used(text):
            logger.info("Word used. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.used.format(text)

        player.new_word(text)

        attacked_player = game.get_current_player()

        return attacked_player.get_reply_str()

    def process_bot_message(self, session_id):
        game = self.get_or_create_game(session_id)
        bot_player = game.get_current_player()

        bot_player.new_word(bot_player.formed_word)

        attacked_player = game.get_current_player()

        return attacked_player.get_reply_str()

    def get_bot_word(self, session_id, text):
        game = self.get_or_create_game(session_id)

        bot_player = game.get_current_player()
        bot_player.create_new_word(text)

        return bot_player.formed_word

    def is_gameover(self, session_id):
        game = self.get_or_create_game(session_id)
        return game.is_gameover()

    def get_gameover_message(self, session_id):
        game = self.get_or_create_game(session_id)
        if game.get_winner().name == Settings.ALICE_NAME:
            return 'Игра окончена. Я выиграл. У меня осталолось {} жизней. Начать заново?'.format(game.get_winner().health)
        else:
            return 'Игра окончена. Вы выиграли. У вас осталолось {} жизней. Начать заново?'.format(game.get_winner().health)
