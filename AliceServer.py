from flask import Flask, request
import logging
import json
from AliceLogic import AliceLogic
from Settings import WordTags
from Settings import Settings
from Level import GameLevel

app = Flask(__name__)


def setup_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('wordbattle-alice.log', 'w', 'utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(file_handler)


class AliceServer:
    def __init__(self):
        self.logic = AliceLogic()
        self.level = GameLevel(1).get_level()
        self.is_level_chosen = False
        self.is_new_game = True

    def start(self, session_id, user_id):
        logging.info('Game started')
        #
        # self.level = GameLevel(1).get_level()
        # self.is_level_chosen = False

        logic_message = self.logic.start(session_id, user_id)

        return logic_message

    def gameover_check(self, session_id):
        if self.logic.is_gameover(session_id):
            return True
        return False

    def gameover_reply(self, session_id, user_id, text):
        if text.lower() == 'да':  # вариативность ответов
            self.is_level_chosen = False
            # self.start(session_id, user_id)
            return 'Выберите уровень'

        return self.logic.get_gameover_message(session_id)

    def get_message(self, session_id, user_id, text):
        if text.lower() in ['помощь', 'что ты умеешь?', 'что ты умеешь']:
            return Settings.HELP_MESSAGE

        if not self.is_level_chosen:
            if text.lower() in ['1 уровень', '2 уровень', '3 уровень']:
                level = 0
                if text.lower() == '1 уровень':
                    level = 1
                elif text.lower() == '2 уровень':
                    level = 2
                elif text.lower() == '3 уровень':
                    level = 3
                self.is_level_chosen = True
                self.level = GameLevel(level).get_level()
                return self.start(session_id, user_id)
            else:
                return 'Пожалуйста выберите уровень'

        if self.gameover_check(session_id):
            return self.gameover_reply(session_id, user_id, text)

        logic_message = self.logic.process_user_message(text, session_id, user_id)

        if self.gameover_check(session_id):
            return self.gameover_reply(session_id, user_id, text)

        if logic_message in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form,
                             WordTags.not_noun]:
            return logic_message

        logic_message += '\n' + self.logic.get_bot_word(session_id, self.level)

        logic_message += '\n' + self.logic.process_bot_message(session_id)

        return logic_message


server = AliceServer()


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON, 
# который отправила нам Алиса в запросе POST
def main():
    logging.info(f'Request: {request.json!r}')

    req = request.json

    session_id = req['session']['session_id']
    user_id = req['session']['user']['user_id']

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': req['session'],
        'version': req['version'],
        'response': {
            'end_session': False
        }
    }

    if req['session']['new']:
        response['response']['text'] = Settings.HELP_MESSAGE + '\n Выберите уровень.'

        logging.info(f'Response:  {response!r}')

        return json.dumps(response)

    text = req['request']['original_utterance']

    response['response']['text'] = server.get_message(session_id, user_id, text)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


if __name__ == '__main__':
    setup_logger()
    app.run()
