import unittest
from CreateBotWord import create_bot_word
from BotPlayer import BotPlayer
from Game import Game
from BotLevel import BotLevel
from TelegramPlayer import TelegramPlayer
from TelegramLogic import TelegramLogic


class TestCreateBotWord(unittest.TestCase):
    def test_something(self):
        game = Game()
        
        bot_player = BotPlayer(game, user_id=1, name='Bot', health=10)
        player = TelegramPlayer(game, user_id=2, name='User', health=10)
        
        game.add_player(bot_player)
        game.add_player(player)
        
        level = BotLevel(1).get_level()
        
        for i in range(5):
            player.new_word(input())

            print(bot_player.get_reply_str())
        
            bot_player.create_new_word(level)

            print(bot_player.formed_word)

            bot_player.new_word(bot_player.formed_word)

            print(player.get_reply_str())


if __name__ == '__main__':
    unittest.main()
