from Settings import Settings, WordTags
from TelegramLogic import TelegramLogic
from Settings import GameModes
from BotLevel import BotLevel, FirstLevel


class Server:
    def __init__(self, game_mode):
        self.game_mode = game_mode

        self.logic = TelegramLogic(game_mode)
        self.level = BotLevel(1).get_level()

        self.chat_id = 1


    def start(self, user_id, username):

        logic_message = self.logic.start(self.chat_id, user_id, username)

        # if self.game_mode == GameModes.with_users:
        #     update.message.reply_text(logic_message, reply_to_message_id=True)
        #     return

        print(logic_message)

    def choose_level(self):
        print('Выберите уровень: 1, 2, 3')

    def add_player(self):
        if self.gameover_check_and_reply():
            return

        print('Введите ваше имя')

    def gameover_check_and_reply(self):
        if self.logic.is_gameover(self.chat_id):
            print(self.logic.get_gameover_message(self.chat_id))
            return True
        return False

    def get_message(self, text, user_id):
        if self.gameover_check_and_reply():
            return

        if self.game_mode == GameModes.with_bot:
            if text.isdigit():
                if int(text) in Settings.AVAILABLE_LEVELS:
                    self.level = BotLevel(int(text)).get_level()
                    return

        logic_message = self.logic.process_user_message(text, self.chat_id, user_id)

        if self.gameover_check_and_reply():
            return

        if logic_message is None:
            return

        print(logic_message)

        if self.game_mode == GameModes.with_users:
            return

        if logic_message in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form,
                             WordTags.not_noun]:
            return

        print(self.logic.get_bot_word(self.chat_id, self.level))

        print(self.logic.process_bot_message(self.chat_id))


# client = Server(GameModes.with_bot)
# client.start(1, 'a')
#
# while True:
#     client.get_message(input(), 1)


client = Server(GameModes.with_users)
client.start(1, 'a')
client.add_player()
client.get_message('a', 1)
client.get_message('b', 2)

n = 0
while True:
    print('введите номер игрока')
    n = int(input())
    print('введите сообщение игрока')
    client.get_message(input(), n)
