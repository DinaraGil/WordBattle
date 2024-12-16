from flask import Flask, request
import logging
from AliceServer import AliceServer
import psutil

app = Flask(__name__)
alice_server = AliceServer()


def setup_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('wordbattle-alice.log', 'w', 'utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(file_handler)


# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
@app.route('/post', methods=['POST'])
def main():
    return alice_server.process_request(request)


if __name__ == '__main__':
    setup_logger()
    print(f"Память: {psutil.Process().memory_info().rss / 1024 ** 2:.2f} МБ")
    app.run()
