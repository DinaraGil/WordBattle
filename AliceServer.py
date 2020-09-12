from flask import Flask, request
import logging
import json
from AliceLogic import AliceLogic
from Settings import WordTags
from Settings import Settings

app = Flask(__name__)

logger = None

logic = AliceLogic()


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def start(session_id, user_id, is_session_new=True):
    logger.info('Game started')

    logic_message = logic.start(session_id, user_id, is_session_new)

    return logic_message


def gameover_check(session_id):
    if logic.is_gameover(session_id):
        return True
    return False


def gameover_reply(session_id, user_id, text):
    if text.lower() == 'да': #вариативность ответов
        return start(session_id, user_id, is_session_new=False)

    return logic.get_gameover_message(session_id)


def get_message(session_id, user_id, text):
    if text.lower() == 'помощь':
        return Settings.HELP_MESSAGE

    if gameover_check(session_id):
        return gameover_reply(session_id, user_id, text)

    logic_message = logic.process_user_message(text, session_id, user_id)

    if gameover_check(session_id):
        return gameover_reply(session_id, user_id, text)

    if logic_message in [WordTags.not_exist, WordTags.used.format(text), WordTags.not_normal_form, WordTags.not_noun]:
        return logic_message

    logic_message += '\n' + logic.get_bot_word(session_id, text)

    logic_message += '\n' + logic.process_bot_message(session_id)

    return logic_message


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON, 
# который отправила нам Алиса в запросе POST
def main():
    setup_logger()

    logger.info(f'Request: {request.json!r}')

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
        response['response']['text'] = start(session_id, user_id)

        logger.info(f'Response:  {response!r}')

        return json.dumps(response)

    text = req['request']['original_utterance']

    response['response']['text'] = get_message(session_id, user_id, text)

    logger.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


if __name__ == '__main__':
    app.run()