from byte import Byte


class Board:
    def __init__(self):
        self.dim = -1
        self.board = []

    def initialize_board(self, dim):
        if (dim - 2) * dim / 2 % 8 != 0:
            return False
        self.dim = dim
        for i in range(0,dim):
            self.board.append([])
            for j in range(0,dim):
                if((i+j)%2 == 0):
                    self.board[i].append(None)
                else:
                    self.board[i].append(False)
        row = 1
        black = True
        while row < dim - 1:
            column = 1 if row % 2 == 1 else 0
            while column < dim:
                self.board[row][column] = (
                    Byte("", (row, column))
                    if row <= 1 and row >= dim - 2
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
                if self.board[i][j] == None:
                    print("__________", end='')
                elif self.board[i][j] == False:
                    print("          ", end='')
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