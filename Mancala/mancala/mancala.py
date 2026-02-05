'''
Created on 2026/02/01

@author: sin
'''
from collections import deque
from bitarray import bitarray
from math import log, ceil, floor

class Mancala():
    '''
    classdocs
    '''

    def __init__(self, initval = None):
        '''
        default setting
        '''
        players = 2
        num_of_pits = 6 # except one house (store) per player
        initial_number = 3 # in pits
        if initval == None :
            self.board = bitarray(0, ceil(log(initial_number * num_of_pits * 2 + 1, 2)), (num_of_pits + 1) * 2 + 1) # + 1 for id of player in turn
            self.set_turn(0) # info, player id of the current turn (id of player who moves the next move)
            for pix in range((num_of_pits + 1) * 2):
                if pix % (num_of_pits + 1) < num_of_pits :
                    self.board[pix] = initial_number
                else:
                    self.board[pix] = 0  # since this is house (store)
        elif isinstance(initval, (list, tuple) ) :
            num_of_pits = len(initval) // 2 - 1
            pieces = sum(initval[:num_of_pits*2])
            bitw = ceil(log(pieces + 1, 2))
            print(pieces, bitw, num_of_pits)
            self.board = bitarray(0, bitw, (num_of_pits + 1) * 2 + 1)
            for ix in range(len(initval)) :
                self.board[ix] = initval[ix]
        elif isinstance(initval, Mancala ) :
            print(initval.board)
            self.board = bitarray(initval.board)
        else:
            raise ValueError(f'Not implemented')
        
    
    def __str__(self):
        outstr = 'Mancala( '
        outstr += str(self.board)
        outstr += ') '

        return outstr
    def __repr__(self):\
        return self.__str__()
    
    def __int__(self):
        return int(self.board)
    
    def __eq__(self, other):
        if isinstance(other, Mancala) :
            return self.board == other.board
        else:
            return False
    def __hash__(self):
        return hash(self.board)
    
    def number_of_pits(self):
        return (len(self.board) - 1) // 2 - 1
    
    def turn(self):
        return self.board[-1]
    
    def set_turn(self, val):
        self.board[-1] = val
    
    def turnover(self):
        self.set_turn( (self.turn() + 1 ) % 2)
    
    def valid_moves(self, startix = 0):
        for pix in range(startix, self.number_of_pits()):
            if self.board[pix + self.turn() * (self.number_of_pits() + 1)] > 0 :
                yield pix
    
    def won_by(self, pid):
        total = 0
        for ix in range((self.number_of_pits() + 1)*pid, (self.number_of_pits() + 1)*(pid + 1) - 1) :
            total += self.board[ix]
        return total == 0
        
    def move(self, pix):
        if not ( 0 <= pix <= self.number_of_pits() ) :
            raise ValueError(f'invalid pit index {pix}')
        
        pix += self.turn() * (self.number_of_pits() + 1)
        #print(f'self.board = {self.board}, pix = {pix}')
        if self.board[pix] == 0 :
            raise ValueError(f'empty pit {pix} of player {self.turn()} selected.')
        pieces = self.board[pix]
        self.board[pix] = 0
        ix = pix
        while pieces > 0 :
            ix = (ix + 1) % (self.number_of_pits() + 1)
            self.board[ix] += 1
            pieces -= 1
        
        if ix % (self.number_of_pits() + 1) == self.number_of_pits() :
            return False # current player's turn continues
        
        if self.won_by(self.turn()) :
            return False    # the game has been settled and so no more switches of turn 
        
        #print(f'self.board = {self.board}')
        self.turnover()
        #print(f'self.board after turnover = {self.board}')
        return True # turnover-ed
    
def search_moves(mboard : Mancala, settled : set):
    moves = deque() # board, the next move to try, expect min, expect max
    moves.append( [mboard, 0, 1, 0] )
    while len(moves) > 0 :
        if  moves[-1][0].won_by(0) :
            moves[-1][2] = 0
            moves[-1][3] = 0
            if moves[-1][0] not in settled :
                settled.add( moves[-1][0] )
                print(len(settled), moves)
            moves.pop()
            moves[-1][2] = min(moves[-1][2], 0)
        elif moves[-1][0].won_by(1) :
            moves[-1][2] = 1
            moves[-1][3] = 1
            if moves[-1][0] not in settled :
                settled.add( moves[-1][0] )
                print(len(settled), moves)
            moves.pop()
            moves[-1][2] = max(moves[-1][3], 1)
        # dig
        currboard, nxstartmv, knownmin, knownmax = moves[-1]
        for mix in currboard.valid_moves(nxstartmv) :
            newboard = Mancala(currboard)
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
    mancalaboard = Mancala([1,1,1,0,1,1,1,0])
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