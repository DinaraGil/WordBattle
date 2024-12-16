import unittest
from AliceLogic import AliceLogic
from Game import Game
from Settings import Settings, WordTags


class TestAliceLogicWithoutMock(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляр AliceLogic перед каждым тестом."""
        self.alice_logic = AliceLogic()
        self.session_id = 1
        self.user_id = "user_123"
        self.level = 1

    def test_get_or_create_game(self):
        """Тестируем создание новой игры."""
        game = self.alice_logic.get_or_create_game(self.session_id)
        self.assertIsNotNone(game)
        self.assertIsInstance(game, Game)

    def test_add_player(self):
        """Тестируем добавление игроков в игру."""
        self.alice_logic.add_player(self.session_id, self.user_id, self.level)
        player = self.alice_logic.get_player(self.session_id, self.user_id)
        self.assertIsNotNone(player)
        self.assertEqual(player.user_id, self.user_id)

    def test_start_game(self):
        """Тестируем начало игры."""
        response = self.alice_logic.start(self.session_id, self.user_id, self.level)
        self.assertIsInstance(response, str)
 #       self.assertTrue("слово" in response or "атака" in response)

    def test_process_user_message(self):
        """Тестируем обработку пользовательского сообщения."""
        self.alice_logic.start(self.session_id, self.user_id, self.level)
        word = "дом"  # предполагаем, что слово допустимо
        response = self.alice_logic.process_user_message(word, self.session_id, self.user_id)
        self.assertNotIn(response, [WordTags.not_exist, WordTags.used.format(word), WordTags.not_normal_form, WordTags.not_noun])

    def test_gameover(self):
        """Тестируем окончание игры."""
        self.alice_logic.start(self.session_id, self.user_id, self.level)

        # Уменьшаем здоровье игрока до 0 для проверки конца игры
        game = self.alice_logic.get_or_create_game(self.session_id)
        for player in game.get_players():
            player.health = 0

 #       self.assertTrue(self.alice_logic.is_gameover(self.session_id))
 #       response = self.alice_logic.gameover_message(self.session_id)
 #       self.assertTrue("Игра окончена" in response)

    # def test_process_bot_message(self):
    #     """Тестируем ответ бота."""
    #     self.alice_logic.start(self.session_id, self.user_id, self.level)
    #     response = self.alice_logic.process_bot_message(self.session_id)
    #     self.assertIsInstance(response, str)
    #     self.assertTrue(len(response) > 0)

    def test_process_message(self):
        """Тестируем полный цикл обработки сообщений."""
        start_response = self.alice_logic.process_message(self.session_id, self.user_id, "дом")
        self.assertIsInstance(start_response, str)
        self.assertTrue("Выберите уровень" in start_response or "слово" in start_response)

        self.alice_logic.process_message(self.session_id, self.user_id, "помощь")
        self.assertEqual(Settings.HELP_MESSAGE, self.alice_logic.process_message(self.session_id, self.user_id, "помощь"))


if __name__ == "__main__":
    unittest.main()