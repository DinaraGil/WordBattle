import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Settings import Settings, WordTags
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
        self.game_level = 1

        setup_logger()

        self._updater = Updater(Settings.TOKEN, use_context=True) #request_kwargs=Settings.REQUEST_KWARGS)

        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))

        if self.game_mode == GameModes.with_bot:
            dp.add_handler(CommandHandler("choose_level", self.choose_level))

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

        # if self.game_mode == GameModes.with_users:
        #     update.message.reply_text(logic_message, reply_to_message_id=True)
        #     return

        update.message.reply_text(logic_message, reply_to_message_id=True)

    def choose_level(self, update, context):
        logger.info('Got command /start')
        update.message.reply_text('Выберите уровень: 1, 2, 3', reply_to_message_id=True)

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

        if self.game_mode == GameModes.with_bot:
            if text in ['1', '2', '3']:
                self.game_level = int(text)
                return

        logic_message = self.logic.process_user_message(text, chat_id, user_id)

        if self.gameover_check_and_reply(update, context):
            return

        if logic_message is None:
            return

        update.message.reply_text(logic_message, reply_to_message_id=True)

        if self.game_mode == GameModes.with_users:
            return

        if logic_message in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form]:
            return

        update.message.reply_text(self.logic.get_bot_word(chat_id, self.game_level), reply_to_message_id=True)

        update.message.reply_text(self.logic.process_bot_message(chat_id), reply_to_message_id=True)
