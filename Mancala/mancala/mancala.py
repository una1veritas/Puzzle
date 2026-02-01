'''
Created on 2026/02/01

@author: sin
'''
from bitarray import bitarray

class Mancala263():
    '''
    classdocs
    '''

    def __init__(self, initval = None):
        '''
        Constructor
        '''
        if initval == None :
            self.board = bitarray(6, 0, 0)
            self.set_turn(0) # info, player id of the current turn 
            for pix in range(14):
                if pix % 7 < 6 :
                    self.board[pix] = 3
                else:
                    self.board[pix] = 0
        else:
            raise ValueError(f'Not implemented')
    
    def __str__(self):
        return str((self.board[:14], self.board[15]))
    
    def turn(self):
        return self.board[15]
    
    def set_turn(self, val):
        self.board[15] = val
    
    def turnover(self):
        self.set_turn( (self.turn() + 1 ) % 2)
    
    def valid_moves(self):
        for pix in range(6):
            if self.board[pix + self.turn() * 7] > 0 :
                yield pix
    
    def move(self, pix):
        if 0 <= pix + self.turn() * 7 < 15 :
            pix = pix + self.turn() * 7
            if self.board[pix] == 0 :
                raise ValueError(f'empty pit {pix} selected.')
            pieces = self.board[pix]
            self.board[pix] = 0
            ix = (pix + 1) % 14
            while True :
                self.board[ix] += 1
                pieces -= 1
                if pieces > 0 :
                    ix = (ix + 1) % 14
                else:
                    break
        else:
            raise ValueError(f'invalid pit index {pix}')
        
        if ix % 7 == 6 :
            return False # turn continues 
        return True #turnover
        
        
if __name__ == "__main__":
    mancalaboard = Mancala263()
    print(mancalaboard)
    print(mancalaboard.move(3))
    print(mancalaboard)
    for pix in mancalaboard.valid_moves():
        print(mancalaboard.move(pix))
        break
    print(mancalaboard)
    