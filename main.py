#!/usr/bin/python3
from game import Game
from player import Player

player1 = Player(True, 'X')
player2 = Player(False, 'O')

new_game = Game(player1, player2, 8)

new_game.start_game()