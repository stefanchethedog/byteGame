from typing import Tuple


class Byte:
    def __init__(self, col: str, coords: Tuple[int, int]):
        self.colors = ''
        self.colors += col
        self.coords = coords

    def get_color(self, ind):
        try:
            if len(self.colors) == 0:
                return -1
            return self.colors[ind]
        except:
            print("Indexing error: ", ind)
            return -1

    def to_string(self):
        returningString = "["
        for color in self.colors:
            returningString += color
        returningString += "]"
        return returningString

    def is_empty(self):
        return len(self.colors) == 0

    def move_to_byte(self, byte, startingIndex):
        """Move from self[startingIndes] to byte[top]."""
        if not self.is_movable(byte, startingIndex):
            return False
        
        byte.colors = byte.colors + self.colors[startingIndex:]
        self.colors = self.colors[:startingIndex]
        return len(byte.colors)

    def is_movable(self, byte, startingIndex):
        # self.colors[startingIndex : ] -> byte
        lenByte = len(byte.colors)
        lenSelf = len(self.colors)

        # premestanje na prazno polje
        if lenByte == 0 and startingIndex == 0:
            return True
        
        # ukoliko bi duzina bila veca od 8
        if lenByte + lenSelf - startingIndex > 8:
            return False
        
        # ukoliko startingIndex dolazi na manju ili jednaku poziciju
        if startingIndex >= lenByte:
            return False
        
        # u suprotnom (ne premesta se prazno polje, duzina je manja ili jednaka 8, dize se na polje vece pozicije)
        return True

