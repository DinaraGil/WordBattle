import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from Game import Game
from Settings import Settings
from TelegramPlayer import TelegramPlayer


class TelegramClient:
    def __init__(self):
        self._updater = Updater(Settings.TOKEN, use_context=True, request_kwargs=Settings.REQUEST_KWARGS)

        self._games = {}

        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text, self.get_message))

        self._updater.start_polling()

        self._updater.idle()

    def start(self, update, context):
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        username = update.message.from_user.full_name

        game = self.get_or_create_game(chat_id)

        game.add_player(self.get_or_create_player(chat_id, user_id, username))

        game.start()

    def get_or_create_game(self, chat_id: int):
        game = self._games.get(chat_id, None)
        if game is None:
            game = Game()
            self._games[chat_id] = game

        return game

    def get_or_create_player(self, chat_id, user_id, username):
        game = self.get_or_create_game(chat_id)

        for player in game.get_players():
            if player.user_id == user_id:
                return None

        health = Settings.player_initial_health

        return TelegramPlayer(game, user_id, username, health)

    def get_message(self, update, context):
        self.game



