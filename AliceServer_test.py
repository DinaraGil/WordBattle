import unittest
from AliceServer import AliceServer
import logging
from Settings import Settings
from AliceLogic import AliceLogic
import json


def setup_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


# class TestAliceLogic(unittest.TestCase):
#     def test_something(self):
#         setup_logger()
#         logic = AliceLogic()
#         session_id = 1
#         is_session_new = True
#         user_id = 12345
#
#         for i in range(50):
#             if is_session_new:
#                 print(Settings.HELP_MESSAGE + '\n Выберите уровень.')
#                 is_session_new = False
#             else:
#                 text = input()
#                 print(logic.process_message(session_id, user_id, text))


class TestAliceServer(unittest.TestCase):
    def test_something(self):
        setup_logger()
        server = AliceServer()
        session_id = 1
        is_session_new = True
        user_id = 12345

        request = "{'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 1, 'session_id': '9ab8bd64-fd11-4147-80fc-b31178760fb6', 'skill_id': '8cfb6e85-7c33-4f0a-a4cf-a7c45873875f', 'user': {'user_id': 'F15E87A7A58999D2CF2E3A3C87642EAE336AE4B62A0C60E21E0506364D46F8B6'}, 'application': {'application_id': 'FCF464A281E733B503AA6D8E8142E10C8F902A88DEAC053E7B597A22F2793724'}, 'user_id': 'FCF464A281E733B503AA6D8E8142E10C8F902A88DEAC053E7B597A22F2793724', 'new': False}, 'request': {'command': '1 уровень', 'original_utterance': '1 уровень', 'nlu': {'tokens': ['1', 'уровень'], 'entities': [{'type': 'YANDEX.NUMBER', 'tokens': {'start': 0, 'end': 1}, 'value': 1}], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}"
        request = json.loads(request)
        print(server.process_request(request))


if __name__ == '__main__':
    unittest.main()
