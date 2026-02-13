'''
Created on 2026/02/01

@author: sin
'''
import sys
import struct
from collections import deque
#from bitarray import bitarray
from array import array
from math import log, ceil, floor
from sqlite_intpair_dict import SQLiteDict
#from bitset import BitSet

class Mancala():
    '''
    classdocs
    '''
    
    def __init__(self, params = None):
        '''
        default setting
        '''
        num_of_pits = 6 # except one house (store) per player
        pieces_in_pit = 3    # in pits
        
        if params == None :
            self.board = [pieces_in_pit if pix % (num_of_pits + 1) < num_of_pits else 0 \
                          for pix in range( 2 * (num_of_pits + 1) )] + [0]
        elif isinstance(params, (list, tuple) ) and len(params) == 2 :
            # the number of pits and intpair
            lval, rval = params
            llen = len(f'{lval:b}')
            rlen = len(f'{rval:b}')
            num_of_pits = (max(llen - 1, rlen - 1) - 1) // 6
            print(hex(lval), llen, hex(rval), rlen, num_of_pits)
            self.board = [0] * ( (num_of_pits + 1) * 2 + 1)
            if bool(params[0]>>((num_of_pits + 1) * 6) & 1) :
                self.board[-1] = 0
            elif bool(params[1]>>((num_of_pits + 1) * 6) & 1) :
                self.board[-1] = 1
            else:
                raise ValueError(f'turn is unknown.')
            print(self)
            for ix in range(num_of_pits,-1,-1) :
                self.board[ix] = lval & 0x3f
                lval >>= 6
            for ix in range(num_of_pits, -1, -1) :
                self.board[num_of_pits + 1 + ix] = rval & 0x3f
                rval >>= 6
        elif isinstance(params, (list, tuple) ) and len(params) > 3 :
            num_of_pits = (len(params)>>1) - 1
            self.board = [params[pix] for pix in range((num_of_pits + 1)* 2)] + [0]
            if len(params) > (num_of_pits+1) * 2 :
                self.board[-1] = params[(num_of_pits + 1) * 2]
        elif isinstance(params, Mancala ) :
            #print(params.board)
            self.board = [ea for ea in params.board]
        else:
            raise ValueError(f'Not implemented')
    
    def __str__(self):
        outstr = 'Mancala('
        num = self.number_of_pits() + 1
        outstr += '(' + ', '.join([str(v) for v in self.board[:num-1]])
        outstr += '; ' + str(self.board[num-1]) + '), '
        outstr += '(' + ', '.join([str(v) for v in self.board[num:2*num-1]])
        outstr += '; ' + str(self.board[2*num-1]) + '), '
        outstr += str(self.turn())
        outstr += ') '
        return outstr
    
    def __repr__(self):
        return self.__str__()
    
    # def __int__(self):
    #     return int(self.board)
    
    def __eq__(self, other):
        if not isinstance(other, Mancala) :
            return False
        return self.board == other.board
    
    def __hash__(self):
        return hash(tuple(self.board) )
    
    def __bytes__(self):
        return bytes(self.board)
    
    def __int__(self):
        val = 1 if self.turn() == 0 else 0
        for e in self.board[:self.number_of_pits()+1] :
            val <<= 6
            val += e & 0x3f
        val <<= 1
        val |= 1 if self.turn() == 1 else 0
        for e in self.board[self.number_of_pits()+1:-1] :
            val <<= 6
            val += e & 0x3f
        return val
    
    def intpair(self):
        lval = 1 if self.turn() == 0 else 0
        for e in self.board[:self.number_of_pits()+1] :
            lval <<= 6
            lval += e & 0x3f
        rval = 1 if self.turn() == 1 else 0
        for e in self.board[self.number_of_pits()+1:-1] :
            rval <<= 6
            rval += e & 0x3f
        return (lval,rval)
        
    def turn(self):
        return self.board[-1]
    
    def number_of_pits(self):
        return (len(self.board)>>1) - 1
    
    def turnover(self):
        self.board[-1] = (self.turn() + 1) % 2
    
    def valid_moves(self, startix = 0):
        for pix in range(startix, self.number_of_pits()):
            if self.board[pix + self.turn() * (self.number_of_pits() + 1)] > 0 :
                yield pix
    
    def won_by(self, pid):
        total = 0
        for ix in range( (self.number_of_pits() + 1)*pid, (self.number_of_pits() + 1)*(pid + 1) - 1) :
            total += self.board[ix]
        return total == 0
        
    def move(self, pix):
        if not ( 0 <= pix <= self.number_of_pits() ) :
            raise ValueError(f'invalid pit index {pix}')
        
        if self.turn() == 1 :
            pix += self.number_of_pits() + 1
        
        if self.board[pix] == 0 :
            raise ValueError(f'empty pit {pix} of player {self.turn()} selected.')
        
        pieces = self.board[pix]
        self.board[pix] = 0
        ix = pix
        while pieces > 0 :
            ix = ix + 1
            ix %= 2*(self.number_of_pits() + 1)
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
    
def search_moves(mboard : Mancala, db : dict):
    moves = deque() # board, the next move to try, expect min, expect max
    moves.append( [mboard, 0, 0] ) # board, next move, the empty set {} for player 0
    while len(moves) > 0 :        
        intpair = moves[-1][0].intpair()
        if moves[-1][0].won_by(0) :
            if intpair not in db :
                db[intpair] = (len(moves)<<8) | 1
                print(len(db), moves[-1][0], [hex(v) for v in intpair], len(moves), 1)
                #print(moves)
            moves.pop()
        elif moves[-1][0].won_by(1) :
            if intpair not in db :
                db[intpair] = (len(moves)<<8) | 2
                print(len(db), moves[-1][0], [hex(v) for v in intpair], len(moves), 2)
                #print(moves)
            moves.pop()
        # dig the tree
        currboard, restartix, winner = moves[-1]
        for mvix in currboard.valid_moves(restartix) :
            newboard = Mancala(currboard)
            newboard.move(mvix)
            mw = db.get(newboard.intpair())
            if mw is None :
                moves[-1][1] = mvix + 1   #register the next (?) index as a restart index
                moves.append( [newboard, 0, 0] )
                break
            else:
                winnerbit = mw & 0xff
                moves[-1][2] |= winnerbit
                continue
        else:
            # exhausted the searches within the children of current board
            prevboard, restartix, winnerbit = moves.pop()
            if winnerbit in (1,2) :
                if prevboard.intpair() not in db:
                    db[ prevboard.intpair()] = (len(moves)<<8) | winnerbit
                    print(len(db), moves[-1], [hex(v) for v in intpair], len(moves), winnerbit)
                    #print(prevboard, mmset)
            if len(moves) != 0 :
                moves[-1][2] |= winnerbit
    return


if __name__ == "__main__":
    mancalaboard = Mancala([3, 3, 3, 3, 0, 3, 3, 3, 3, 0, 0])
    print(mancalaboard)
    print(bytes(mancalaboard))
    print(int(mancalaboard))
    print(mancalaboard.intpair())
    #db = dict()
    #search_moves(mancalaboard, db)
    with SQLiteDict('/Volumes/SSD256G/pairdict.db') as db :
        search_moves(mancalaboard, db)
    
    print('\nresult:')
    #print(db)
    # with open('data.txt', 'w') as f:
    #     for each in games:
    #         f.write(f'{each.board}')
    #         f.write('\n')
    #for each in settled_games:
    #    print(each)
    #print(f'size = {len(settled_games)}')
    print('finished.')