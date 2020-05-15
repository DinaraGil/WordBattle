from ConsolePlayer import ConsolePlayer
from Game import Game
from Settings import Settings

game = Game()

player1 = ConsolePlayer(game, 'Tim', Settings.player_initial_health)
player2 = ConsolePlayer(game, 'Robert', Settings.player_initial_health)

game.add_player(player1)
game.add_player(player2)

game.start()