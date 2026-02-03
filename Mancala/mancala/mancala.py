'''
Created on 2026/02/01

@author: sin
'''
from collections import deque
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
            self.board = bitarray(6, 15, 0)
            self.set_turn(0) # info, player id of the current turn 
            for pix in range(14):
                if pix % 7 < 6 :
                    self.board[pix] = 3
                else:
                    self.board[pix] = 0
        elif isinstance(initval, (bitarray, int, Mancala263) ) :
            self.board = bitarray(6, 15, int(initval))
        elif isinstance(initval, (list, tuple) ) :
            self.board = bitarray(6, 15, 0)
            for ix in range(0, min(len(initval), 15)) :
                self.board[ix] = initval[ix]
            if len(initval) < 15 :
                self.set_turn(0)
        else:
            raise ValueError(f'Not implemented')
    
    def __str__(self):
        outstr = 'Mancala( ('
        outstr += ', '.join([str(self.board[ix]) for ix in range(6)]) + '; ' + str(self.board[7]) 
        outstr += ' / ' + ', '.join( ([str(self.board[ix]) for ix in range(7,13)]) ) + '; ' + str(self.board[14])
        outstr += '), ' + str(self.turn()) + ') '
        return outstr
    def __repr__(self):\
        return self.__str__()
    
    def __int__(self):
        return int(self.board)
    
    def __eq__(self, other):
        if isinstance(other, Mancala263) :
            return self.board == other.board
        else:
            return False
    def __hash__(self):
        return hash(self.board)
    
    def turn(self):
        return self.board[15]
    
    def set_turn(self, val):
        self.board[15] = val
    
    def turnover(self):
        self.set_turn( (self.turn() + 1 ) % 2)
    
    def valid_moves(self, startix = 0):
        for pix in range(startix, 6):
            if self.board[pix + self.turn() * 7] > 0 :
                yield pix
    
    def won_by(self, pid):
        total = 0
        for ix in range(7*pid, 7*(pid + 1) - 1) :
            total += self.board[ix]
        return total == 0
        
    def move(self, pix):
        if 0 <= pix + self.turn() * 7 < 15 :
            pix = pix + self.turn() * 7
            if self.board[pix] == 0 :
                raise ValueError(f'empty pit {pix} of player {self.turn()} selected.')
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
            return False # current player's turn continues
        
        if self.won_by(self.turn()) :
            return False    # the has been settled so does ont switch the player
        
        self.turnover()
        return True # turnover-ed
    
def search_moves(mboard : Mancala263, settled : set):
    moves = deque() # board, the next move to try
    moves.append( (mboard, 0) )
    while len(moves) > 0 :
        if  moves[-1][0].won_by(0) or moves[-1][0].won_by(1):
            if moves[-1][0] not in settled :
                settled.add( moves[-1][0] )
                print(f'{len(settled)}, {str(moves[-1][0])}, {hex(int(moves[-1][0]))}')
            moves.pop()
        # dig
        currboard, nxstartmv = moves[-1]
        for mix in currboard.valid_moves(nxstartmv) :
            newboard = Mancala263(currboard)
            newboard.move(mix)
            moves[-1] = (currboard, mix + 1)
            moves.append( (newboard, 0) )
            break
        else:
            # search within the children of currboard is exhausted.
            moves.pop()
    
    return settled


if __name__ == "__main__":
    mancalaboard = Mancala263([1,1,1,0,0,0,0,1,1,1,0,0,0,0])
    print(mancalaboard)
    settled_games = set()
    search_moves(mancalaboard, settled_games)
    print('\nresult:')
    for each in settled_games:
        print(each)
    print(f'size = {len(settled_games)}')