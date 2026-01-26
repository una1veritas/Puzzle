'''
Created on 2025/04/16

@author: sin
'''

from collections import deque

class bitarray:
    BITWIDTH = 6
    BITMASK = (1 << BITWIDTH) - 1
    
    def __init__(self, bitwidth = 6, initval = 0):
        bitarray.BITWIDTH = bitwidth
        bitarray.BITMASK = (1 << bitarray.BITWIDTH) - 1
        self.bits = initval
        #print(f'width {bitarray.BITWIDTH}, mask {bitarray.BITMASK}')
    
    def __len__(self):
        val = self.bits
        counter = 0
        while val > 0 :
            val >>= self.BITWIDTH
            counter += 1
        return counter
    
    def __getitem__(self, index):
        # supports single index or slice automatically because self._data does
        return self.BITMASK & (self.bits >> (bitarray.BITWIDTH * index))
    
    def set(self, ix, val):
        val &= bitarray.BITMASK
        self.bits &= ~(self.BITMASK << (bitarray.BITWIDTH * ix))
        self.bits |= (val << (bitarray.BITWIDTH * ix))
        
    def __setitem__(self, index, value):
        # validate values before storing
        if isinstance(index, slice):
            # allow assigning an iterable of ints for slices
            if not all(isinstance(x, int) for x in value):
                raise ValueError("slice assignment requires integers")
            self.set(index, value)
        else:
            if not isinstance(value, int):
                raise ValueError("only integers allowed")
            self.set(index, value)
    
    def __repr__(self):
        return 'bitarray(' + str(self)
    
    def __bin__(self):
        return bin(self.bits)
    
    def __str__(self):
        return str(tuple([self[i] for i in range(len(self))]))
    def intvalue(self):
        return self.bits

    def hex(self):
        return hex(self.bits)
    
    def bin(self):
        return bin(self.bits)

class TicTacToe:
    SYMBOLS = ' XO'
    
    def __init__(self, board = None):
        if board == None :
            self.board = bitarray(2)
            self.next_turn = 0 # first X player
        elif isinstance(board, TicTacToe) :
            self.board = bitarray(2, board.board.intvalue())
            self.next_turn = board.next_turn
    
    def __str__(self):
        rows = ''
        for row in range(5):
            if (row & 1) == 1 :
                rows += '-+-+-'
            else:
                r = row>>1
                rows += '|'.join([self.SYMBOLS[self.board[r*3 + i]] for i in range(3)])
            rows += '\n'
        return rows
    
    def place(self,row, col):
        if self.board[3*row + col] != 0 :
            return False
        if self.next_turn == 0 :
            self.board[3*row+col] = 1
        else: 
            self.board[3*row+col] = 2
            #print(self.board[3*row+col])
        self.next_turn = (self.next_turn + 1) % 2
        return True
    
    def winner(self):
        for s in ((0, 1, 2), (3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)) :
            if all([self.board[ix] == 1 for ix in s]) :
                #print([self.cell_top(ix) % 2 for ix in s])
                return 1
            elif all([ self.board[ix] == 2 for ix in s]) :
                return -1
        return 0
    
    
def DepthFirstTicTacToe(ttt):
    settled = set()
    path = deque()
    path.append( [ttt, 0] )
    while len(path) > 0 :
        t3board, lastmove = path[-1]
        for ix in range(lastmove, 9):
            newt3 = TicTacToe(t3board)
            if newt3.place(ix//3, ix %3) :
                wonby = newt3.winner()
                if wonby != 0 and newt3.board.intvalue() not in settled :
                    print(f'won by {wonby}\n{newt3}\n')
                    settled.add(newt3.board.intvalue())
                else:
                    path[-1][1] = ix+1
                    path.append( [newt3, 0] )
                    #print(f'move {(ix//3, ix%3)}\n{newt3}\n')
                    break
        else:
            path.pop()
    print(len(settled))            
        
        
if __name__ == '__main__':
    ttt = TicTacToe()
    DepthFirstTicTacToe(ttt)