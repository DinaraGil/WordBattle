import unittest
from unittest.mock import MagicMock
from AliceServer import AliceServer
from AliceLogic import AliceLogic
import json


class TestAliceServer(unittest.TestCase):
    def setUp(self):
        """Настраиваем экземпляр AliceServer перед каждым тестом."""
        self.server = AliceServer()
        self.server._logic = MagicMock(spec=AliceLogic)  # Мокаем AliceLogic

    def test_process_request_new_session(self):
        """Тестируем начальный запрос (новая сессия)."""
        request = MagicMock()
        request.json = {
            'session': {
                'new': True,
                'session_id': 'test_session_id',
                'user_id': 'test_user_id'
            },
            'version': '1.0',
            'request': {}
        }

        expected_response = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False,
                'text': 'Привет! Это словесная игра. Выберите уровень.'
            }
        }

        # Проверяем ответ сервера
        response = self.server.process_request(request)
        self.assertEqual(json.loads(response), expected_response)

    def test_process_request_existing_session(self):
        """Тестируем запрос для существующей сессии."""
        request = MagicMock()
        request.json = {
            'session': {
                'new': False,
                'session_id': 'test_session_id',
                'user_id': 'test_user_id'
            },
            'version': '1.0',
            'request': {
                'original_utterance': 'Пример слова'
            }
        }

        # Мокаем логику обработки сообщения
        self.server._logic.process_message.return_value = 'Ответ от логики'

        expected_response = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False,
                'text': 'Ответ от логики'
            }
        }

        # Проверяем ответ сервера
        response = self.server.process_request(request)
        self.assertEqual(json.loads(response), expected_response)
        self.server._logic.process_message.assert_called_once_with(
            'test_session_id', 'test_user_id', 'Пример слова'
        )

    def test_process_request_invalid_request(self):
        """Тестируем поведение при некорректном запросе."""
        request = MagicMock()
        request.json = {}  # Пустой запрос

        with self.assertRaises(KeyError):
            self.server.process_request(request)


if __name__ == '__main__':
    unittest.main()