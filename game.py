from board import Board
from player import Player


class Game:
    def __init__(self, player1: Player, player2: Player, dimensions: int):
        if player1.byte_color == "X":
            self.playerX = player1
            self.playerO = player2
        else:
            self.playerX = player2
            self.playerO = player1

        self.play_turn = "X"
        self.board = Board()
        self.board.initialize_board(dimensions)

    def show_state(self):
        self.board.print_board()

    def is_board_state_valid(self):
        return self.board.is_state_valid()

    def is_board_empty(self):
        return self.board.is_empty()

    def has_player_won(self):
        if self.playerX.score > 3 * self.board.dim // 8 // 2:
            return True
        if self.playerO.score > 3 * self.board.dim // 8 // 2:
            return True
        return False

    def is_game_over(self):
        return self.is_board_empty() or self.has_player_won()

    def start_game(self):
        while True:
            if(self.is_board_state_valid()):
                self.show_state()
            if(self.is_game_over()):
                break

            if self.play_turn == "X":
                if self.playerX.isHuman == True:
                    if self.playerX.play_move(self.board):
                        self.play_turn = "O"
                        continue
                    input()
                else:
                    #self.playerX.play_best_move()
                    print('Computer turn')
            else:
                if self.playerO.isHuman == True:
                     if self.playerO.play_move():
                        self.play_turn = "X"
                        continue
                     input()
                else:
                    #self.playerO.play_best_move()
                    print('Computer turn')

        print("The game is over.")