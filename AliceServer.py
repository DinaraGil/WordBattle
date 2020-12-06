from flask import Flask, request
import logging
import json
from AliceLogic import AliceLogic
from Settings import WordTags
from Settings import Settings
from Level import GameLevel

app = Flask(__name__)

logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class AliceServer:
    def __init__(self, logger):
        self.logger = logger
        self.logic = AliceLogic()
        self.level = GameLevel(1).get_level()
        self.is_level_chosen = False

    def start(self, session_id, user_id, is_session_new):
        self.logger.info('Game started')

        self.level = GameLevel(1).get_level()
        self.is_level_chosen = False

        logic_message = self.logic.start(session_id, user_id, is_session_new)

        return logic_message

    def gameover_check(self, session_id):
        if self.logic.is_gameover(session_id):
            return True
        return False

    def gameover_reply(self, session_id, user_id, text):
        if text.lower() == 'да': #вариативность ответов
            return self.start(session_id, user_id, False)

        return self.logic.get_gameover_message(session_id)

    def get_message(self, session_id, user_id, text):
        if text.lower() in ['помощь', 'что ты умеешь?', 'что ты умеешь']:
            return Settings.HELP_MESSAGE

        if text.lower() in ['1 уровень', '2 уровень', '3 уровень'] and not self.is_level_chosen:
            if text.lower() == '1 уровень': #изменить на нормальный подход
                self.level = GameLevel(1).get_level()
            elif text.lower() == '2 уровень':
                self.level = GameLevel(2).get_level()
            elif text.lower() == '3 уровень':
                self.level = GameLevel(3).get_level()
            self.is_level_chosen = True
            return self.logic.to_first_word(session_id)
        elif not self.is_level_chosen:
            return 'Выберите уровень'

        if self.gameover_check(session_id):
            return self.gameover_reply(session_id, user_id, text)

        logic_message = self.logic.process_user_message(text, session_id, user_id)

        if self.gameover_check(session_id):
            return self.gameover_reply(session_id, user_id, text)

        if logic_message in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form, WordTags.not_noun]:
            return logic_message

        logic_message += '\n' + self.logic.get_bot_word(session_id, self.level)

        logic_message += '\n' + self.logic.process_bot_message(session_id)

        return logic_message


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON, 
# который отправила нам Алиса в запросе POST
def main():
    setup_logger()

    logger.info(f'Request: {request.json!r}')

    server = AliceServer(logger)

    req = request.json

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

    session_id = req['session']['session_id']
    user_id = req['session']['user']['user_id']

    if req['session']['new']:
        response['response']['text'] = server.start(session_id, user_id, True)

        logger.info(f'Response:  {response!r}')

        return json.dumps(response)

    text = req['request']['original_utterance']

    response['response']['text'] = server.get_message(session_id, user_id, text)

    logger.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


if __name__ == '__main__':
    app.run()
