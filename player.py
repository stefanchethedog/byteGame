from board import Board
from mappings import letters_to_numbers


class Player:
    def __init__(self, isHuman: bool, byte_color: str):
        self.score = 0
        self.isHuman = isHuman
        self.byte_color = byte_color

    def is_move_out_of_bound(self, board: Board, src_byte, move) -> bool:
        if src_byte[0] == "A" and move[0] == "G":
            return True
        if src_byte[0] == letters_to_numbers[board.dim] and move[0] == "D":
            return True
        if src_byte[1] == "1" and move[1] == "L":
            return True
        if src_byte[1] == str(board.dim) and move[1] == "D":
            return True
        return False

    def is_byte_empty(self, board: Board, src_byte) -> bool:
        return len(board.board[letters_to_numbers[src_byte[0]]][src_byte[1]]) > 0

    def is_index_in_byte_correct(self, board: Board, src_byte, index_in_byte) -> bool:
        if(board.board[letters_to_numbers[src_byte[0]]][int(src_byte[1])].get_color(index_in_byte) != -1):
            return True
        return False

    def test_move(self, board: Board, src_byte, move, index_in_byte):
        return (
            not self.is_move_out_of_bound(board, src_byte, move)
            and not self.is_byte_empty(board, src_byte)
            and not self.is_index_in_byte_correct(board, src_byte, index_in_byte)
        )

    def play_move(self, board: Board):
        print("It is your turn to play!")
        src_byte = ""
        move = ""
        index_in_byte = ""

        print("Source byte: ", end="")
        input(src_byte)

        print("Move: ", end="")
        input(move)

        print("Index of src byte: ", end="")
        input(index_in_byte)
        if not self.test_move(board, src_byte, move, index_in_byte):
            print("Bad move.")
            return False

        return True
