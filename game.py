from os import system
from board import Board
from player import Player
import mappings


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

    def find_all_possible_moves(self):
        """A function that returns the list of all possible moves of the current player"""
        i = 0
        j = 0
        possibleMoves = []

        while i < self.board.dim:
            j = 0 if i % 2 == 0 else 1
            while j < self.board.dim:
                for k in range(0, len(self.board.board[i][j].colors)):
                    currentIndexColor = self.board.board[i][j].get_color(k)
                    if currentIndexColor == self.play_turn:
                        areNeighboursEmpty = self.board.are_neighbours_empty(i, j)
                        if areNeighboursEmpty:
                            # DFS za GL, GD, DL, DD i da se nadje broj poteza do steka
                            GL = self.board.find_nearest_stack_iterative(i, j, i - 1, j - 1)
                            GD = self.board.find_nearest_stack_iterative(i, j, i - 1, j + 1)
                            DL = self.board.find_nearest_stack_iterative(i, j, i + 1, j - 1)
                            DD = self.board.find_nearest_stack_iterative(i, j, i + 1, j + 1)

                            minimum = min([GL, GD, DL, DD])
                            if GL == minimum:
                                srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                possibleMoves.append((srcByte, "GL", k))
                            if GD == minimum:
                                srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                possibleMoves.append((srcByte, "GD", k))
                            if DL == minimum:
                                srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                possibleMoves.append((srcByte, "DL", k))
                            if DD == minimum:
                                srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                possibleMoves.append((srcByte, "DD", k))
                        else:
                            GL = self.board.is_movable_from_to(i - 1, j - 1, i, j, k)
                            GD = self.board.is_movable_from_to(i - 1, j + 1, i, j, k)
                            DL = self.board.is_movable_from_to(i + 1, j - 1, i, j, k)
                            DD = self.board.is_movable_from_to(i + 1, j + 1, i, j, k)
                            if GL:
                                if not self.board.board[i-1][j-1].is_empty():
                                    srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                    possibleMoves.append((srcByte, "GL", k))
                            if GD:
                                if not self.board.board[i-1][j+1].is_empty():
                                    srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                    possibleMoves.append((srcByte, "GD", k))
                            if DL:
                                if not self.board.board[i+1][j-1].is_empty():
                                    srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                    possibleMoves.append((srcByte, "DL", k))
                            if DD:
                                if not self.board.board[i+1][j+1].is_empty():
                                    srcByte = mappings.numbers_to_letters[i] + str(j + 1)
                                    possibleMoves.append((srcByte, "DD", k))
                j += 2
            i += 1
        return possibleMoves

    def start_game(self):
        while True:
            if self.is_board_state_valid():
                self.show_state()
            if self.is_game_over():
                break

            if self.play_turn == "X":
                # nadji moguce potezeX
                possibleMoves = self.find_all_possible_moves()
                if(len(possibleMoves) == 0):
                    self.play_turn = "O"
                    continue
                
                print(possibleMoves)
                if self.playerX.isHuman == True:
                    (isPlayed, lenOfByte, iTo, jTo) = self.playerX.play_move(self.board, self.play_turn, possibleMoves)
                    if(isPlayed):
                        if(lenOfByte != False):
                            topColor = self.board.board[iTo][jTo].get_color(7)
                            if topColor == 'X':
                                self.playerX.score += 1
                            else:
                                self.playerO.score += 1
                            self.board.board[iTo][jTo].colors = ''
                        self.play_turn = "O"
                        continue
                    input()
                else:
                    # self.playerX.play_best_move()
                    print("Computer turn")
            else:
                possibleMoves = self.find_all_possible_moves()
                if(len(possibleMoves) == 0):
                    self.play_turn = "X"
                    continue
                print(possibleMoves)
                if self.playerO.isHuman == True:
                    # nadji moguce potezeO
                    (isPlayed, lenOfByte, iTo, jTo) = self.playerO.play_move(self.board, self.play_turn, possibleMoves)
                    if(isPlayed):
                        if(lenOfByte != False):
                            topColor = self.board.board[iTo][jTo].get_color(7)
                            if topColor == 'X':
                                self.playerX.score += 1
                            else:
                                self.playerO.score += 1
                            self.board.board[iTo][jTo].colors = ''
                        self.play_turn = "X"
                        continue
                    input()
                else:
                    # self.playerO.play_best_move()
                    print("Computer turn")
        print("The game is over.")
