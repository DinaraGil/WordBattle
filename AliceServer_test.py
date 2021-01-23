import unittest
from AliceServer import AliceServer
import logging
from Settings import Settings
from AliceLogic import AliceLogic


def setup_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class TestAliceServer(unittest.TestCase):
    def test_something(self):
        setup_logger()
        logic = AliceLogic()
        session_id = 1
        is_session_new = True
        user_id = 12345

        for i in range(50):
            if is_session_new:
                print(Settings.HELP_MESSAGE + '\n Выберите уровень.')
                is_session_new = False
            else:
                text = input()
                print(logic.process_message(session_id, user_id, text))


if __name__ == '__main__':
    unittest.main()
