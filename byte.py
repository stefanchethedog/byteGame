from typing import Tuple

class Byte:
    def __init__(self, col: str, coords: Tuple[int,int]):
        self.colors = []
        self.colors.extend(list(col))
        self.coords = coords

    def get_color(self, ind):
        try:
            if(len(self.colors)==0):
                return -1
            return self.colors[ind]
        except:
            print("Indexing error: ", ind)
            return -1
        
    def to_string(self):
        returningString = '['
        for color in self.colors:
            returningString += color
        returningString += ']'
        return returningString
    
    def move_to_byte(self, byte, startingIndex):
        if(not self.is_movable(byte, startingIndex)):
            return False
        self.colors.append(byte.colors)

    def is_movable(self, byte, startingIndex):
        #To be implemented in the next phase
        i = 0