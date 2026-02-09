'''
Created on 2026/02/01

@author: sin
'''
import sys
import struct
from collections import deque
from bitarray import bitarray
from array import array
from math import log, ceil, floor
from sqlite_int64pairs_set import Int64PairStorage

class Mancala():
    '''
    classdocs
    '''

    def __init__(self, arg1 = None):
        '''
        default setting
        '''
        num_of_pits = 6 # except one house (store) per player
        pieces_in_pit = 3    # in pits
        
        if arg1 == None :
            self.board = [pieces_in_pit if pix % (num_of_pits + 1) < num_of_pits else 0 \
                          for pix in range( 2 * (num_of_pits + 1) )] + [0]
        elif isinstance(arg1, (list, tuple) ) :
            num_of_pits = (len(arg1)>>1) - 1
            self.board = [arg1[pix] for pix in range((num_of_pits + 1)* 2)] + [0]
            if len(arg1) > (num_of_pits+1) * 2 :
                self.board[-1] = arg1[(num_of_pits + 1) * 2]
        elif isinstance(arg1, Mancala ) :
            #print(arg1.board)
            self.board = [ea for ea in arg1.board]
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
        mid = self.number_of_pits()+1
        t = self.board[:mid]
        t[mid-1] |= self.turn()<<7
        t += self.board[mid:mid<<1]
        return bytes(t)
    
    def __int__(self):
        intval = self.turn()
        for e in self.board :
            intval <<= 6
            intval += e & 0x3f
        return intval
    
    def intpair(self):
        b = bytes(self)
        mid = self.number_of_pits()+1
        if mid > 8 :
            raise ValueError(f'bit length for one player exceeded 64')
        l = 0
        for v in b[:mid] :
            l <<= 8
            l |= v
        r = 0
        for v in b[mid:] :
            r <<= 8
            r |= v
        return (l,r)
        
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
    
def search_moves(mboard : Mancala, pairdb : set):
    moves = deque() # board, the next move to try, expect min, expect max
    moves.append( [mboard, 0] )
    while len(moves) > 0 :
        last = moves[-1]
        intpair = last[0].intpair()
        if  last[0].won_by(0) :
            if intpair not in pairdb :
                pairdb.add(intpair[0], intpair[1])
                print(len(pairdb), [hex(v) for v in intpair], 0)
            moves.pop() 
        elif last[0].won_by(1) :
            if intpair not in pairdb :
                pairdb.add(intpair[0], intpair[1])
                print(len(pairdb), [hex(v) for v in intpair], 1)
            moves.pop()
        # dig
        currboard, restartix = last
        for mix in currboard.valid_moves(restartix) :
            newboard = Mancala(currboard)
            newboard.move(mix)
            if newboard.intpair() in pairdb :
                continue
            last[1] = mix + 1
            moves.append( [newboard, 0] )
            break
        else:
            # search within the children of currboard is exhausted.
            last = moves.pop()
    return


if __name__ == "__main__":
    mancalaboard = Mancala([3,3,3,3,0,3,3,3,3,0, 0])
    print(mancalaboard)
    print(bytes(mancalaboard))
    
    with Int64PairStorage() as db :
        search_moves(mancalaboard, db)
    
    #print('\nresult:')
    # with open('data.txt', 'w') as f:
    #     for each in games:
    #         f.write(f'{each.board}')
    #         f.write('\n')
    #for each in settled_games:
    #    print(each)
    #print(f'size = {len(settled_games)}')
    print('finished.')