import logging
import json
from AliceLogic import AliceLogic
from Settings import Settings


class AliceServer:
    def __init__(self):
        self._logic = AliceLogic()

    def process_request(self, request):
        logging.info(f'Request:  {request!r}')

        req = request.json

        session_id = req['session']['session_id']
        user_id = Settings.USER_ID  # req['session']['user']['user_id']

        # Начинаем формировать ответ, согласно документации
        # мы собираем словарь, который потом при помощи
        # библиотеки json преобразуем в JSON и отдадим Алисе
        response = {
            'session': req['session'],
            'version': req['version'],
            'response': {
                'end_session': False,
                'text': ''
            }
        }

        if req['session']['new']:
            response['response']['text'] = Settings.HELP_MESSAGE + '\n Выберите уровень.'

            logging.info(f'Response:  {response!r}')

            return json.dumps(response)

        text = req['request']['original_utterance']

        response['response']['text'] = self._logic.process_message(session_id, user_id, text)

        logging.info(f'Response:  {response!r}')

        # Преобразовываем в JSON и возвращаем
        return json.dumps(response)


