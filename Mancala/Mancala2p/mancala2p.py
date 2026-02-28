'''
Created on 2026/02/01

@author: sin
'''
import sys
#import struct
from collections import deque
#from bitarray import bitarray
#from array import array
#from math import log, ceil, floor
from sqlite_blobkeydict import SQLiteBlobDict
#from bitset import BitSet

class Mancala():
    '''
    classdocs
    '''
    
    def __init__(self, params = None, num_of_pits = 6, pieces_in_pit = 3):
        '''
        default setting
        '''
        # num_of_pits = the number of pits per player except a house (store)
        # pieces_in_pit = the initial number of pieces in pits
        
        if params == None :
            self.board = bytearray((num_of_pits + 1) * 2 + 1)
            for ix in range(len(self.board[:-1])) :
                self.board[ix] = pieces_in_pit if ix % (num_of_pits + 1) < num_of_pits else 0
        elif isinstance(params, (list, tuple, bytes) ) and len(params) > 3 :
            num_of_pits = (len(params)>>1) - 1
            self.board = bytearray([params[pix] for pix in range((num_of_pits + 1)* 2)] + [0])
            if len(params) > (num_of_pits+1) * 2 :
                self.board[-1] = params[(num_of_pits + 1) * 2]
        elif isinstance(params, Mancala ) :
            #print(params.board)
            self.board = bytearray(params.board)
        else:
            raise ValueError(f'Not implemented')
    
    def __str__(self):
        outstr = 'Mancala('
        num = len(self.board)>>1
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
    
    # the first pit goes highest bit
    def __int__(self):
        bw = sum(self.board[:-1]).bit_length()
        val = 0
        for e in self.board[:-1] :
            val <<= bw
            val |= e
        val <<= 1
        val |= self.turn() & 1
        return val
    
    def packed_bytes(self, bitwidth = 6):
        num = self.number_of_pits()
        val = 0
        for c in self.board[:num]:
            val <<= bitwidth
            val |= c
        for c in self.board[num+1:2*num+1]:
            val <<= bitwidth
            val |= c
        val <<= 1
        val |= self.turn() & 1
        return val.to_bytes( (val.bit_length() + 7)//8 or 1 )
        
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
        if moves[-1][0].won_by(0) or moves[-1][0].won_by(1) :
            wonby = 1 if moves[-1][0].won_by(0) else 2
            packed = moves[-1][0].packed_bytes()
            mw = db.get(packed)
            if mw is None or (mw>>8 & 0xff > len(moves) - 1):
                if mw is not None :
                    wonby |= mw & 0xff
                db[packed] = ((len(moves)-1)<<8) | wonby
                #print(len(db), moves[-1][0], len(moves), wonby, packed)
            moves.pop()
        
        # dig the tree
        currboard, restartix, wonby = moves[-1]
        for mvix in currboard.valid_moves(restartix) :
            newboard = Mancala(currboard)
            newboard.move(mvix)
            mw = db.get(newboard.packed_bytes())
            if mw is None :
                moves[-1][1] = mvix + 1   #register the next (?) index as a restart index
                moves.append( [newboard, 0, 0] )
                break
            else:
                moves[-1][2] |= mw & 0xff
                continue
        else:
            # exhausted the searches within the children of current board
            currboard, restartix, wonby = moves.pop()
            packed = currboard.packed_bytes()
            mw = db.get(packed) 
            if mw is None or (mw>>8 & 0xff > len(moves)):
                wonby |= 0 if mw is None else (mw & 0xff)
                db[packed] = (len(moves)<<8) | wonby 
                # if wonby in (1, 2) :
                #     print(len(db), currboard, len(moves), wonby, packed)
            if len(moves) != 0 : 
                moves[-1][2] |= wonby
    return


if __name__ == "__main__":
    # interpret command-line arguments 
    params = dict()
    params['num_of_pits'] = 3
    params['pieces_in_pit']=3
    if len(sys.argv) > 1 :
        argix = 1
        while argix < len(sys.argv) :
            arg = sys.argv[argix]
            if arg.startswith( '--' ) :
                params[arg[2:]] = True
                argix += 1
            elif arg.startswith( '-' ) :
                values = sys.argv[argix][1:].split('=')
                if values[0] == 'file' :
                    params['file'] = values[1]
                else:
                    params[values[0]] = int(values[1])
                argix += 1
    print(params)
    mancalaboard = Mancala(num_of_pits=params['num_of_pits'], pieces_in_pit=params['pieces_in_pit'])
    if 'test' in params :
        m = Mancala()
        print(m)
        print(mancalaboard)
        print(bytes(mancalaboard))
        print(int(mancalaboard))
        print(mancalaboard.packed_bytes())
        #exit()
        db = dict()
        search_moves(mancalaboard, db)
    #exit()
    
    if 'search' in params and 'file' in params:
        with SQLiteBlobDict(params['file']) as db :
            try:
                search_moves(mancalaboard, db)
            except KeyboardInterrupt:
                print('caught KeyboardInterrupt. search_moves terminated.')
    elif 'search' in params:
        with SQLiteBlobDict(':mem:') as db :
            try:
                search_moves(mancalaboard, db)
            except KeyboardInterrupt:
                print('caught KeyboardInterrupt. search_moves terminated.')
    
    if 'forcedwin' in params :
        print('\nresult:')
        count = 0
        with SQLiteBlobDict(params['file']) as db :
            for key, value in db.items() :
                if (value & 0x03).bit_count() == 1 and (value>>8) < 16 :
                    print(Mancala(key), value & 3, value>>8)
                    count += 1
                    if count > 100 :
                        break

    print('finished.')