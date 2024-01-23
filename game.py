from copy import deepcopy
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
        if self.playerX.score > (self.board.dim // 2 - 1) * self.board.dim // 8 // 2: # d * (d/2 - 1) // 8 // 2
            return True
        if self.playerO.score > (self.board.dim // 2 - 1) * self.board.dim // 8 // 2:
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
                            if k == 0:
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
    
    def utility(self):
        util = 0

        self.play_turn = "X"
        possibleMovesX = self.find_all_possible_moves()
        self.play_turn = "O"
        possibleMovesO = self.find_all_possible_moves()
        util += (len(possibleMovesX) - len(possibleMovesO))*2
        self.play_turn = "X"

        for i in range(self.board.dim):
            for j in range(self.board.dim):
                if not self.board.is_tile_white(i, j):
                    stack_height = len(self.board.board[i][j].colors)

                    for k in range(0, stack_height):
                        if k == 0:
                            if self.board.board[i][j].get_color(0) == "X":
                                util += 5
                            else:
                                util -= 5
                        elif k == 7:
                            if self.board.board[i][j].get_color(k) == "X":
                                util += 300
                            else:
                                util -= 300
                        elif k == stack_height - 1:
                            if k < 4:
                                if self.board.board[i][j].get_color(k) == "X":
                                    util += (6 if len(possibleMovesX) > 10 else 12)
                                else:
                                    util -= (6 if len(possibleMovesX) > 10 else 12)
                            else:
                                if self.board.board[i][j].get_color(k) == "X":
                                    util += (8 if len(possibleMovesX) > 10 else 16)
                                else:
                                    util -= (8 if len(possibleMovesX) > 10 else 16)
                        else:
                            if self.board.board[i][j].get_color(k) == "X":
                                util += 4
                            else:
                                util -= 4

        if self.playerX.score == 1:
            util += 150
        if self.playerX.score == 2:
            util += 200 if self.board.dim <= 8 else 50000
        if self.playerX.score == 3:
            util += 50000

        if self.playerO.score == 1:
            util -= 150
        if self.playerO.score == 2:
            util -= 200 if self.board.dim <= 8 else 50000
        if self.playerO.score == 3:
            util -= 50000

        return util

    def make_move(self, move):
        srcByte, direction, indexInByte = move

        srcByteJ = int(srcByte[1]) if len(srcByte) == 2 else int (srcByte[1] + srcByte[2])
        iFrom, jFrom = mappings.letters_to_numbers[srcByte[0]], srcByteJ - 1
        iTo, jTo = iFrom + (1 if direction[0] == 'D' else -1), jFrom + (1 if direction[1] == 'D' else -1)

        lenOfByte = self.board.board[iFrom][jFrom].move_to_byte(self.board.board[iTo][jTo], indexInByte)

        if lenOfByte == 8:
            topColor = self.board.board[iTo][jTo].get_color(7)
            if topColor == 'X':
                self.playerX.score += 1
            else:
                self.playerO.score += 1
            self.board.board[iTo][jTo].colors = ''
        self.play_turn = "O" if self.play_turn == "X" else "X"

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.utility()

        possible_moves = self.find_all_possible_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                current_state = deepcopy(self)
                current_state.make_move(move)
                eval = current_state.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    return alpha

            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                current_state = deepcopy(self)
                current_state.make_move(move)
                eval = current_state.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    return beta

            return min_eval
    
    def get_best_move(self):
        best_move = None
        max_eval = float('-inf')
        min_eval = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        current_depth = 3 

        possible_moves = self.find_all_possible_moves()

        if(len(possible_moves) < 30):
            current_depth = 3
        if (len(possible_moves) < 25):
            current_depth = 4
        if (len(possible_moves) < 17):
            current_depth = 5
        if(len(possible_moves) < 12):
            current_depth = 6
        if(len(possible_moves) < 8):
            current_depth = 7
        if(len(possible_moves) < 5):
            current_depth = 9

        for move in possible_moves:
            current_state = deepcopy(self)
            current_state.make_move(move)
            eval = current_state.minimax(current_depth, alpha, beta, False)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max(alpha, eval)

            


        current_depth += 1
        return best_move


    def start_game(self):
        ai_move = ''
        while True:
            if self.is_board_state_valid():
                self.show_state()
            if self.is_game_over():
                break
            print()
            print("Player X score: " + str(self.playerX.score) + "        Player O score: " + str(self.playerO.score))
            print()
            print("Last computer move: " + str(ai_move))
            print()
            print('=============================================================================')
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
                        if(lenOfByte == 8):
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
                    print("Computer turn X")
                    ai_move = self.get_best_move()
                    print("AI moves: ", ai_move)
                    possibleMoves = self.find_all_possible_moves()

                    if(len(possibleMoves) == 0):
                        self.play_turn = "O"

                    if ai_move == None:
                        ai_move = possibleMoves[0]
                    (isPlayed, lenOfByte, iTo, jTo) = self.playerX.play_move(self.board, self.play_turn, possibleMoves, ai_move)
                    if(isPlayed):
                        if(lenOfByte == 8):
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
                possibleMoves = self.find_all_possible_moves()
                if(len(possibleMoves) == 0):
                    self.play_turn = "X"
                    continue
                
                print(possibleMoves)
                if self.playerO.isHuman == True:
                    (isPlayed, lenOfByte, iTo, jTo) = self.playerO.play_move(self.board, self.play_turn, possibleMoves)
                    if(isPlayed):
                        if(lenOfByte == 8):
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
                    print("Computer turn O")
                    ai_move = self.get_best_move()
                    print("AI moves: ", ai_move)
                    possibleMoves = self.find_all_possible_moves()
                    if(len(possibleMoves) == 0):
                        self.play_turn = "X"

                    if ai_move == None:
                        ai_move = possibleMoves[0]

                    (isPlayed, lenOfByte, iTo, jTo) = self.playerO.play_move(self.board, self.play_turn, possibleMoves, ai_move)
                    if(isPlayed):
                        if(lenOfByte == 8):
                            topColor = self.board.board[iTo][jTo].get_color(7)
                            if topColor == 'X':
                                self.playerX.score += 1
                            else:
                                self.playerO.score += 1
                            self.board.board[iTo][jTo].colors = ''
                        self.play_turn = "X"
                        continue
                    input()
        print("The game is over.")
        print("The winner is player " + ('X' if self.playerX.score > self.playerO.score else 'O'))
