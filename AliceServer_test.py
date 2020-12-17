import unittest
from AliceServer import AliceServer
import logging

logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('wordbattle.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class TestAliceServer(unittest.TestCase):
    def test_something(self):
        setup_logger()
        server = AliceServer(logger)
        session_id = 1
        user_id = 12345
        text = input()
        print(server.get_message(session_id, user_id, text))
        for i in range(50):
            text = input()
            print(server.get_message(session_id, user_id, text))


if __name__ == '__main__':
    unittest.main()
