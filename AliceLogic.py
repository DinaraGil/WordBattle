import logging

from Game import Game
from Settings import Settings
from Settings import WordTags
from AlicePlayer import AlicePlayer
from AliceBot import AliceBot


class AliceLogic:
    def __init__(self):
        self._games = {}

    def get_or_create_game(self, session_id: int):
        game = self._games.get(session_id, None)
        if game is None:
            game = Game()
            self._games[session_id] = game

        return game

    def get_player(self, session_id, user_id):
        game = self.get_or_create_game(session_id)

        for player in game.get_players():
            if player.user_id == user_id:
                return player

    def add_player(self, session_id, user_id, level):
        game = self.get_or_create_game(session_id)
        health = Settings.player_initial_health

        if self.get_player(session_id, user_id) is None:
            if user_id == Settings.ALICE_ID:
                player = AliceBot(game, user_id, Settings.ALICE_NAME, health, level)
            else:
                player = AlicePlayer(game, user_id, health)

            game.add_player(player)

        logging.info('Add new player. Session_id = {}, user_id = {}'.format(session_id, user_id))

    def to_first_word(self, game):
        player2 = game.get_current_player()
        first_word = game.get_first_word()
        player2.new_word(first_word)
        player1 = game.get_current_player()

        return player1.get_reply_str()

    def start(self, session_id, user_id, level):
        game = self.get_or_create_game(session_id)
        game.start()

        logging.info('Game started. session_id = {}'.format(session_id))

        self.add_player(session_id, user_id, level)
        self.add_player(session_id, Settings.ALICE_ID, level)

        return self.to_first_word(game)

    def is_gameover(self, session_id):
        game = self.get_or_create_game(session_id)
        return game.is_gameover()

    def gameover_message(self, session_id):
        game = self.get_or_create_game(session_id)
        if game.get_winner().name == Settings.ALICE_NAME:
            return 'Игра окончена. Я выиграл. У меня осталось {} жизней. Начать заново?'.format(game.get_winner().health)
        else:
            return 'Игра окончена. Вы выиграли. У вас осталось {} жизней. Начать заново?'.format(game.get_winner().health)

    def process_user_message(self, text, session_id, user_id):
        game = self.get_or_create_game(session_id)

        player = self.get_player(session_id, user_id)

        if game.get_current_player() != player:
            return

        word_checking_result = game.word_checking(text)

        if word_checking_result == WordTags.not_exist:
            logging.info("Word doesn't exist. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_exist

        if word_checking_result == WordTags.not_normal_form:
            logging.info("Not normal form of word. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_normal_form

        if word_checking_result == WordTags.not_noun:
            logging.info("Not noun. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.not_noun

        if game.is_word_used(text):
            logging.info("Word used. session_id = {}, word = {}, user_id = {}".format(session_id, text, user_id))
            return WordTags.used.format(text)

        player.new_word(text)

        attacked_player = game.get_current_player()

        return attacked_player.get_reply_str()

    def get_bot_word(self, session_id):
        game = self.get_or_create_game(session_id)

        bot_player = game.get_current_player()
        bot_player.create_new_word()

        return bot_player.formed_word

    def process_bot_message(self, session_id):
        game = self.get_or_create_game(session_id)
        bot_player = game.get_current_player()

        bot_player.new_word(bot_player.formed_word)

        if self.is_gameover(session_id):
            return self.gameover_message(session_id)

        attacked_player = game.get_current_player()

        return attacked_player.get_reply_str()

    def process_message(self, session_id, user_id, text) -> str:
        if text.lower() in ['помощь', 'что ты умеешь?', 'что ты умеешь']:
            return Settings.HELP_MESSAGE

        if session_id in self._games:
            if self.is_gameover(session_id):
                if text.lower() in Settings.START_NEW_GAME:
                    self._games.pop(session_id, None)
                else:
                    return self.gameover_message(session_id)

        if session_id not in self._games:
            if text.lower() in Settings.FIRST_LEVEL_WORDS or text in Settings.SECOND_LEVEL_WORDS or text in Settings.THIRD_LEVEL_WORDS:
                level = None
                if text in Settings.FIRST_LEVEL_WORDS:
                    level = 1
                if text in Settings.SECOND_LEVEL_WORDS:
                    level = 2
                if text in Settings.THIRD_LEVEL_WORDS:
                    level = 3

                return self.start(session_id, user_id, level)
            else:
                return 'Выберите уровень'

        response = self.process_user_message(text, session_id, user_id)

        if self.is_gameover(session_id):
            return self.gameover_message(session_id)

        if response in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form,
                             WordTags.not_noun]:
            return response

        response += '\n' + self.get_bot_word(session_id)

        response += '\n' + self.process_bot_message(session_id)

        return response
