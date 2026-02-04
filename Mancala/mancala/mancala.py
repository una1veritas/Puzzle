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
            return False    # the game has been settled and so no more switches of turn 
        
        self.turnover()
        return True # turnover-ed
    
def search_moves(mboard : Mancala263, settled : set):
    moves = deque() # board, the next move to try, expect min, expect max
    moves.append( [mboard, 0, 1, 0] )
    while len(moves) > 0 :
        if  moves[-1][0].won_by(0) :
            moves[-1][2] = 0
            moves[-1][3] = 0
            if moves[-1][0] not in settled :
                settled.add( moves[-1][0] )
                print(len(settled), moves[-1])
            moves.pop()
            moves[-1][2] = min(moves[-1][2], 0)
        elif moves[-1][0].won_by(1) :
            moves[-1][2] = 1
            moves[-1][3] = 1
            if moves[-1][0] not in settled :
                settled.add( moves[-1][0] )
                print(len(settled), moves[-1])
            moves.pop()
            moves[-1][2] = max(moves[-1][3], 1)
        # dig
        currboard, nxstartmv, knownmin, knownmax = moves[-1]
        for mix in currboard.valid_moves(nxstartmv) :
            newboard = Mancala263(currboard)
            newboard.move(mix)
            if newboard in settled :
                continue
            moves[-1][1] = mix + 1
            moves.append( [newboard, 0, 1, 0] )
            break
        else:
            # search within the children of currboard is exhausted.
            lastpopped = moves.pop()
            if len(moves) > 0 :
                moves[-1][2] = min(moves[-1][2], lastpopped[2])
                moves[-1][3] = max(moves[-1][3], lastpopped[3])
                if lastpopped[2] == lastpopped[3] :
                    settled.add(lastpopped[0])
    
    return settled


if __name__ == "__main__":
    mancalaboard = Mancala263([1,1,1,1,1,1,0,1,1,1,1,1,1,0])
    print(mancalaboard)
    settled_games = set()
    search_moves(mancalaboard, settled_games)
    #print('\nresult:')
    with open('data.txt', 'w') as f:
        for each in settled_games:
            f.write(str(each))
            f.write('\n')
    #for each in settled_games:
    #    print(each)
    #print(f'size = {len(settled_games)}')
    print('finished.')