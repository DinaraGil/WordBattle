import telegram
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from Game import Game
from Settings import Settings
from TelegramPlayer import TelegramPlayer

logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class TelegramClient:
    def __init__(self):
        setup_logger()

        self._updater = Updater(Settings.TOKEN, use_context=True, request_kwargs=Settings.REQUEST_KWARGS)

        self._games = {}

        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler('add_player', self.add_player))
        dp.add_handler(MessageHandler(Filters.text, self.get_message))

        self._updater.start_polling()

        self._updater.idle()

    def start(self, update, context):
        logger.info('Got command /start')

        chat_id = update.message.chat.id
        game = self.get_or_create_game(chat_id)
        game.start()

        update.message.reply_text('Для игры нужно 2 игрока. Для добавление игрока воспользуйтесь коммандой /add_player',
                                  reply_to_message_id=True)

    def add_player(self, update, context):
        logger.info('Got command /add_player')

        chat_id = update.message.chat_id
        game = self.get_or_create_game(chat_id)

        if self.gameover_check_and_reply(game):
            return

        update.message.reply_text('Введите ваше имя', reply_to_message_id=True)

    def get_or_create_game(self, chat_id: int):
        game = self._games.get(chat_id, None)
        if game is None:
            game = Game()
            self._games[chat_id] = game

        return game

    def create_player(self, chat_id, user_id, username):
        game = self.get_or_create_game(chat_id)
        health = Settings.player_initial_health

        player = TelegramPlayer(game, user_id, username, health)
        game.add_player(player)

    def get_player(self, chat_id, user_id):
        game = self.get_or_create_game(chat_id)

        for player in game.get_players():
            if player.user_id == user_id:
                return player

    def gameover_check_and_reply(self, update, context, game):
        if game.is_gameover():
            update.message.reply_text('''Игра окончена. Выиграл игрок {}.
                                      Чтобы начать новую игру используйте комманду /start'''.format(game.get_winner().name),
                                      reply_to_message_id=True)
            return True
        return False

    def get_message(self, update, context):
        text = update.message.text
        chat_id = update.message.chat.id
        game = self.get_or_create_game(chat_id)
        user_id = update.message.from_user.id

        if self.gameover_check_and_reply(update, context, game):
            return

        if len(game.get_players()) < 2:
            self.create_player(chat_id, user_id, text)

            logger.info('Got new username. chat_id = {}, username = {}, from {}'.format(chat_id, text, user_id))

            if len(game.get_players()) == 2:
                update.message.reply_text('Игра началась. Первым ходит игрок {}'.format(game.get_current_player().name),
                                          reply_to_message_id=True)
        else:
            player = self.get_player(chat_id, user_id)

            if game.get_current_player() != player:
                return

            if not game.is_word_correct(text):
                update.message.reply_text('Такого слова нет', reply_to_message_id=True)
                return

            if game.is_word_used(text):
                update.message.reply_text('Слово {} уже встречалось'.format(text), reply_to_message_id=True)
                return

            player.new_word(text)

            if self.gameover_check_and_reply(update, context, game):
                return

            attacked_player = game.get_current_player()

            logger.info('Got word. chat_id = {}, word = {}, from {}, attacked_player {}'.format(chat_id,
                                                                                                text,
                                                                                                user_id,
                                                                                                attacked_player.user_id))

            update.message.reply_text(attacked_player.get_reply_str(), reply_to_message_id=True)


telegram_client = TelegramClient()


