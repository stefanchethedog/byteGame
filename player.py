from board import Board
from mappings import letters_to_numbers, numbers_to_letters


class Player:
    def __init__(self, isHuman: bool, byte_color: str):
        self.score = 0
        self.isHuman = isHuman
        self.byte_color = byte_color

    def is_move_out_of_bound(self, board: Board, src_byte, move) -> bool:
        if src_byte[0] == "A" and move[0] == "G":
            return True
        if src_byte[0] == numbers_to_letters[board.dim - 1] and move[0] == "D":
            return True
        if src_byte[1:] == "1" and move[1] == "L":
            return True
        if src_byte[1:] == str(board.dim) and move[1] == "D":
            return True
        return False

    def is_byte_empty(self, board: Board, src_byte) -> bool:
        return board.board[letters_to_numbers[src_byte[0]]][int(src_byte[1:]) - 1].is_empty()

    def is_index_in_byte_correct(
        self, board: Board, src_byte, index_in_byte, playTurn
    ) -> bool:
        if (
            board.board[letters_to_numbers[src_byte[0]]][
                int(src_byte[1:]) - 1
            ].get_color(index_in_byte)
            != -1
        ):
            return True

        if (
            board.board[letters_to_numbers[src_byte[0]]][
                int(src_byte[1:]) - 1
            ].get_color(index_in_byte)
            == playTurn
        ):
            return True

        return False

    def test_move(self, board: Board, src_byte, move, index_in_byte, playTurn):
        return (
            not self.is_move_out_of_bound(board, src_byte, move)
            and not self.is_byte_empty(board, src_byte)
            and not self.is_index_in_byte_correct(
                board, src_byte, index_in_byte, playTurn
            )
        )

    def play_move(self, board: Board, playTurn, possibleMoves, aiMove = None):
        if aiMove == None:
            print("It is your turn to play! Color: " + self.byte_color)
            src_byte = ""
            move = ""
            index_in_byte = ""

            print("Source byte: ", end="")
            src_byte = input()
            possibleMovesFromSrcByte = list(filter(lambda current: src_byte == current[0] , possibleMoves))

            if len(possibleMovesFromSrcByte) == 0:
                print("Bad move. Please try again... Press anything to continue.")
                return (False, False, False, False)

            print(possibleMovesFromSrcByte)
            # izbacuje listu mogucih poteza za src_byte

            print("Index of src byte: ", end="")
            index_in_byte = input()
            possibleMovesFromIndex = list(filter(lambda current: int(index_in_byte) == current[2] , possibleMovesFromSrcByte))

            if len(possibleMovesFromIndex) == 0:
                print("Bad move. Please try again... Press anything to continue.")
                return (False, False, False, False)
            print(possibleMovesFromIndex)
            
            print("Move: ", end="")
            move = input()
            finalMove = list(filter(lambda current: move == current[1], possibleMovesFromIndex))

            if(len(finalMove) == 0):
                print("Bad move. Please try again... Press anything to continue.")
                return (False, False, False, False)

            if not self.test_move(board, src_byte, move, index_in_byte, playTurn):
                print("Bad move. Please try again... Press anything to continue.")
                return (False, False, False, False)

            iFrom = letters_to_numbers[src_byte[0]]
            jFrom = int(src_byte[1:]) - 1
            
            iTo = iFrom + (1 if move[0] == 'D' else -1)   # D - dole
            jTo = jFrom + (1 if move[1] == 'D' else -1)   # D - desno

            lenOfByte = board.board[iFrom][jFrom].move_to_byte(board.board[iTo][jTo], int(index_in_byte))
            return (True, lenOfByte, iTo, jTo)
        else:
            (src_byte, move, index_in_byte) = aiMove
            iFrom = letters_to_numbers[src_byte[0]]
            jFrom = int(src_byte[1:]) - 1
            
            iTo = iFrom + (1 if move[0] == 'D' else -1)   # D - dole
            jTo = jFrom + (1 if move[1] == 'D' else -1)   # D - desno

            lenOfByte = board.board[iFrom][jFrom].move_to_byte(board.board[iTo][jTo], int(index_in_byte))
            return (True, lenOfByte, iTo, jTo)