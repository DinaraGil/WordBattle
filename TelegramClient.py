import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Settings import Settings
from TelegramClientLogic import TelegramClientLogic
from Settings import GameModes

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
    def __init__(self, game_mode):
        self.game_mode = game_mode

        setup_logger()

        self._updater = Updater(Settings.TOKEN, use_context=True, request_kwargs=Settings.REQUEST_KWARGS)

        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))

        if self.game_mode == GameModes.with_users:
            dp.add_handler(CommandHandler('add_player', self.add_player))

        dp.add_handler(MessageHandler(Filters.text, self.get_message))

        self.logic = TelegramClientLogic(game_mode)

        self._updater.start_polling()

        self._updater.idle()

    def start(self, update, context):
        logger.info('Got command /start')

        chat_id = update.message.chat_id
        user_id = update.message.from_user.id

        username = update.message.from_user.full_name

        logic_message = self.logic.start(chat_id, user_id, username)

        if self.game_mode == GameModes.with_users:
            update.message.reply_text(logic_message, reply_to_message_id=True)
            return

        update.message.reply_text(logic_message, reply_to_message_id=True)

    def add_player(self, update, context):
        logger.info('Got command /add_player')

        if self.gameover_check_and_reply(update, context):
            return

        update.message.reply_text('Введите ваше имя', reply_to_message_id=True)

    def gameover_check_and_reply(self, update, context):
        chat_id = update.message.chat.id

        if self.logic.is_gameover(chat_id):
            update.message.reply_text(self.logic.get_gameover_message(chat_id), reply_to_message_id=True)
            return True
        return False

    def get_message(self, update, context):
        if self.gameover_check_and_reply(update, context):
            return

        text = update.message.text
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id

        logic_message = self.logic.get_message(text, chat_id, user_id)

        if self.gameover_check_and_reply(update, context):
            return

        if logic_message is None:
            return

        if self.game_mode == GameModes.with_users:
            update.message.reply_text(logic_message, reply_to_message_id=True)
            return

        if len(logic_message) >= 2:
            for message in logic_message:
                update.message.reply_text(message, reply_to_message_id=True)
                return

        update.message.reply_text(logic_message, reply_to_message_id=True)