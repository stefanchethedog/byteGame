import queue
from byte import Byte
from typing import Tuple, Set
from copy import deepcopy
from os import system
import mappings

class Board:
    def __init__(self):
        self.dim = -1
        self.board = []

    def initialize_board(self, dim):
        """Initialize the board dimension: dim x dim, and set the figures. Note: dim in range 8 - 16"""
        if dim < 8 or dim > 16:
            return False
        if (dim - 2) * dim / 2 % 8 != 0:
            return False


        self.dim = dim
        for i in range(0, dim):
            self.board.append([])
            for j in range(0, dim):
                if (i + j) % 2 == 0:
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
            row += 1
            black = not black

    def print_board(self):
        system('cls')
        for i in range(1, self.dim + 1):
            print("         " + str(i), end= "")
        print()
        for i in range(0, self.dim * 10 + 4):
            print("=", end="")
        print()
        print()
        for i in range(0, self.dim):
            print(str(mappings.numbers_to_letters[i]) + " ||", end="")
            for j in range(0, self.dim):
                if self.board[i][j] == False:
                    print("          ", end="")
                elif len(self.board[i][j].colors) == 0:
                    print("__________", end="")
                else:
                    n = 8 - len(self.board[i][j].colors)
                    print(self.board[i][j].to_string(), end="")
                    for k in range(0, n):
                        print("_", end="")
            print("||", end="")
            print()
            print()
        for i in range(0, self.dim * 10 + 4):
            print("=", end="")
        print()

    def is_empty(self) -> bool:
        flag = True
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if (
                    self.board[i][j] != None
                    and self.board[i][j] != False
                    and len(self.board[i][j].colors) != 0
                ):
                    flag = False
        return flag

    def is_tile_black(self, i, j):
        return (i + j) % 2 == 0

    def is_tile_white(self, i, j):
        return (i + j) % 2 == 1

    def is_state_valid(self) -> bool:
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.is_tile_white(i, j) and self.board[i][j] != False:
                    return False
                if self.is_tile_black(i, j) and len(self.board[i][j].colors) > 8:
                    return False
        return True

    def are_neighbours_empty(self, i, j):
        gl = (i - 1, j - 1)
        gd = (i - 1, j + 1)
        dl = (i + 1, j - 1)
        dd = (i + 1, j + 1)

        flag = True

        if gl[0] >= 0 and gl[1] >= 0:
            flag = self.board[gl[0]][gl[1]].is_empty()

        if flag == True and gd[0] >= 0 and gd[1] < self.dim:
            flag = self.board[gd[0]][gd[1]].is_empty()

        if flag == True and dl[0] < self.dim and dl[1] >= 0:
            flag = self.board[dl[0]][dl[1]].is_empty()

        if flag == True and dd[0] < self.dim and dd[1] < self.dim:
            flag = self.board[dd[0]][dd[1]].is_empty()

        return flag

    def is_movable_from_to(self, iFrom, jFrom, iTo, jTo, startingIndex):
        '''
        Returns True if its possible to move the stack on position (iFrom, jFrom), starting from the startingIndex, to (iTo, jTo)\n
        Returns False if the index is out of bound, if its not possible
        '''
        if(iFrom < 0 or iFrom >= self.dim or jFrom < 0 or jFrom >= self.dim):
            return False
        
        return self.board[iTo][jTo].is_movable(self.board[iFrom][jFrom], startingIndex)
    
    def find_nearest_stack_iterative(self, iStart, jStart, iCurrent, jCurrent):
        if iCurrent < 0 or iCurrent >= self.dim or jCurrent < 0 or jCurrent >= self.dim:
            return 100000 
        nodesToVisit = queue.Queue(self.dim*self.dim/2)
        nodesToVisit.put((iCurrent, jCurrent, 1))
        visitedNodes = set()

        while not nodesToVisit.empty():
            currentNode = nodesToVisit.get()
            iCur = currentNode[0]
            jCur = currentNode[1]
            roadLen = currentNode[2]

            if(not (iCur, jCur) in visitedNodes):
                visitedNodes.add((iCur, jCur))
                if (not self.board[iCur][jCur].is_empty()) and (iCur != iStart or jCur != jStart):
                    return roadLen
                if iCur - 1 >= 0 and jCur - 1 >= 0 and not (iCur-1,jCur-1) in visitedNodes:
                    nodesToVisit.put((iCur - 1, jCur - 1, roadLen + 1))
                if iCur - 1 >= 0 and jCur + 1 < self.dim and not (iCur-1,jCur+1) in visitedNodes:
                    nodesToVisit.put((iCur - 1, jCur + 1, roadLen + 1))
                if iCur + 1 < self.dim and jCur - 1 >= 0 and not (iCur+1,jCur-1) in visitedNodes:
                    nodesToVisit.put((iCur + 1, jCur - 1, roadLen + 1))
                if iCur + 1 < self.dim and jCur + 1 < self.dim and not (iCur+1,jCur+1) in visitedNodes:
                    nodesToVisit.put((iCur + 1, jCur + 1, roadLen + 1))