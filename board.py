from byte import Byte


class Board:
    def __init__(self):
        self.dim = -1
        self.board = []

    def initialize_board(self, dim):
        """Initialize the board dimension: dim x dim, and set the figures. Note: dim in range 8 - 16"""
        if(dim < 8 or dim > 16):
            return False
        if (dim - 2) * dim / 2 % 8 != 0:
            return False
        if (dim > 16):
            return False
        
        self.dim = dim
        for i in range(0,dim):
            self.board.append([])
            for j in range(0,dim):
                if((i+j)%2 == 0):
                    self.board[i].append(None)
                else:
                    self.board[i].append(False)
        row = 0
        black = False
        while row < dim:
            column = 1 if row % 2 == 1 else 0
            while column < dim:
                self.board[row][column] = (
                    Byte("", (row, column))
                    if row < 1 or row >= dim - 1
                    else Byte("X" if black else "O", (row, column))
                )
                column += 2
            row+=1
            black = not black
    
    def print_board(self):
        for i in range(0,self.dim*10+4):
            print("=", end="")
        print()
        print()
        for i in range(0,self.dim):
            print('||', end="")
            for j in range(0, self.dim):                    
                if self.board[i][j] == False:
                    print("          ", end='')
                elif len(self.board[i][j].colors) == 0:
                    print("__________", end='')
                else:
                    n = 8 - len(self.board[i][j].colors)
                    print(self.board[i][j].to_string(), end='')
                    for k in range(0,n):
                        print('_', end="")
            print('||',end="")
            print()
            print()
        for i in range(0,self.dim*10+4):
            print("=", end="")
        print()

    def is_empty(self)-> bool:
        flag = True
        for i in range(0,self.dim):
            for j in range(0, self.dim):
                if self.board[i][j] != None and self.board[i][j] != False and len(self.board[i][j].colors) != 0:
                    flag = False
        return flag
    
    def is_tile_black(self, i, j):
        return (i+j)%2==0
    
    def is_tile_white(self,i,j):
        return (i+j)%2==1

    def is_state_valid(self) -> bool:
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if(self.is_tile_white(i,j) and self.board[i][j] != False):
                    return False
                if(self.is_tile_black(i,j) and len(self.board[i][j].colors) > 8):
                    return False
        return True