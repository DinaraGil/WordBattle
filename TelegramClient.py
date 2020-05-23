import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Settings import Settings
from TelegramClientLogic import TelegramClientLogic

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

        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler('add_player', self.add_player))
        dp.add_handler(MessageHandler(Filters.text, self.get_message))

        self.logic = TelegramClientLogic()

        self._updater.start_polling()

        self._updater.idle()

    def start(self, update, context):
        logger.info('Got command /start')

        chat_id = update.message.chat_id

        self.logic.start(chat_id)

        update.message.reply_text('Для игры нужно 2 игрока. Для добавление игрока воспользуйтесь коммандой /add_player',
                                  reply_to_message_id=True)

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
        text = update.message.text
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id

        if self.gameover_check_and_reply(update, context):
            return

        logic_message = self.logic.get_message(text, chat_id, user_id)

        if logic_message is None:
            return

        update.message.reply_text(logic_message, reply_to_message_id=True)


telegram_client = TelegramClient()
