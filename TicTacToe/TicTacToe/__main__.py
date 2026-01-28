'''
Created on 2025/04/16

@author: sin
'''

from collections import deque
import operator

class bitarray:
    BITWIDTH = 6
    BITMASK = (1 << BITWIDTH) - 1
    
    @staticmethod
    def set_bitwidth(width = 6):
        bitarray.BITWIDTH = width
        bitarray.BITMASK = (1 << bitarray.BITWIDTH) - 1
    
    def __init__(self, initval = 0):
        if isinstance(initval, bitarray) :
            self.bits = initval.bits
        elif isinstance(initval, int) :
            self.bits = initval
        else:
            raise NotImplementedError('{initval} is invalid as initializer.')
    
    def __int__(self):
        return self.bits
    
    def __len__(self):
        val = self.bits
        counter = 0
        while val > 0 :
            val >>= self.BITWIDTH
            counter += 1
        return counter
    
    def __getitem__(self, index):
        if not isinstance(index, slice):
            ix = operator.index(index)  # accepts int-like objects
            return self.BITMASK & (self.bits >> (bitarray.BITWIDTH * ix))
        
        raise NotImplementedError('get item with slice is not implemented')
        # slice index -> return same type (copy) for safety
        # slice.indices normalizes start/stop/step and handles negatives/out-of-range
        start, stop, step = index.indices(len(self))
        
        newbits = 0
        for ix in range(start, stop, step) :
            val = self.BITMASK & (self.bits >> (bitarray.BITWIDTH * ix))
            newbits |= (val << (bitarray.BITWIDTH * ix))
        return bitarray(bitarray.BITWIDTH, newbits)
    
    def set(self, ix, val):
        val &= bitarray.BITMASK
        self.bits &= ~(self.BITMASK << (bitarray.BITWIDTH * ix))
        self.bits |= (val << (bitarray.BITWIDTH * ix))
        
    def __setitem__(self, index, value):
        # validate values before storing
        if not isinstance(index, slice):
            ix = operator.index(index)
            self.set(ix, value)
            return
        
        raise NotImplementedError('set item with slice is not implemented')
        # slice assignment
        start, stop, step = index.indices(len(self))
        indices = list(range(start, stop, step))
        vals = list(value)  # materialize the RHS
        if len(vals) != len(indices):
            raise ValueError(
                f"attempt to assign sequence of size {len(vals)} "
                f"to extended slice of size {len(indices)}"
            )
        for i, v in zip(indices, vals):
            self.set(i, v)
        return
    
    def __repr__(self):
        return 'bitarray(' + str(self)
    
    def __bin__(self):
        return bin(self.bits)
    
    def __str__(self):
        return str(tuple([self[i] for i in range(len(self))]))

    def rotright(self, start, stop, moves):
        part = [self[i] for i in range(start, stop)]
        #print(start, stop, moves,part)
        for ix in range(start, stop) :
            self[ix] = part[(ix + moves) % len(part)]
            #print(self, ix,  (ix + moves) % len(part))
        return
    
    def reverse(self, start, stop):
        part = [self[i] for i in range(start, stop)]
        #print(start, stop, moves,part)
        for ix in range(len(part)) :
            #print(ix, len(part) - 1  - ix, start + len(part) - 1  - ix, )
            self[start + ix] = part[len(part) - 1 - ix]
            #print(self, ix,  (ix + moves) % len(part))
        return
        
    def hex(self):
        return hex(self.bits)
    
    def bin(self):
        return bin(self.bits)

class TicTacToe:
    SYMBOLS = ' XO'
    LININDEX = ( 0, 1, 2, 7, 8, 3, 6, 5, 4 )
    CIRINDEX = { (0,0): 0, (0,1):1, (0,2): 2, (1,0):7, (1,1):8, (1,2):3, (2,0):6, (2,1):5, (2,2):4 }
    RCINDEX = ( (0,0), (0, 1), (0, 2), (1, 2), (2, 2), (2,1), (2,0), (1, 0), (1,1) )
    
    def __init__(self, t3board = None):
        bitarray.set_bitwidth(2)
        if t3board == None :
            self.board = bitarray()
        elif isinstance(t3board, TicTacToe) :
            self.board = bitarray(int(t3board.board) )
    
    def __eq__(self, other):
        if not isinstance(other, TicTacToe) :
            return NotImplemented
        return self.signature() == other.signature()

    def __hash__(self):
        return self.signature()
    
    def signature(self):
        mybits = bitarray(self.board)
        sigval = int(mybits)
        for _ in range(4) :
            if int(mybits) < sigval :
                sigval = int(mybits)
            mybits.rotright(0, 8, 2)
        mybits.reverse(1, 8)
        for _ in range(4) :
            if int(mybits) < sigval :
                sigval = int(mybits)
            mybits.rotright(0, 8, 2)
        return sigval
        
    def __str__(self):
        rows = ''
        for row in range(5):
            if (row & 1) == 1 :
                rows += '-+-+-'
            else:
                r = row>>1
                rows += '|'.join([self.SYMBOLS[self.board[self.CIRINDEX[(r,i)]]] for i in range(3)])
            rows += '\n'
        return rows
    
    def __repr__(self):
        return str(self)
        
    def next_turn(self):
        xc = 0
        oc = 0
        for ix in range(9):
            c = self.board[ix]
            if c == 1 :
                xc += 1
            elif c == 2 :
                oc += 1
        if xc > oc :
            return 1
        else:
            return 0
    
    def place(self,row, col):
        if self.board[self.CIRINDEX[row, col]] != 0 :
            return False
        if self.next_turn() == 0 :
            self.board[self.CIRINDEX[row, col]] = 1
        else: 
            self.board[self.CIRINDEX[row, col]] = 2
            #print(self.board[3*row+col])
        return True
    
    def winner(self):
        for s in ( (0, 1, 2), (7, 8, 3), (6, 5, 4), (0, 7, 6), (1, 8, 5), (2, 3, 4), (0, 8, 4), (2, 8, 6) ) :
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
                if wonby != 0 and newt3 not in settled :
                    print(f'won by {wonby}\n{newt3}\n')
                    settled.add( newt3 )
                else:
                    path[-1][1] = ix+1
                    path.append( [newt3, 0] )
                    #print(f'move {(ix//3, ix%3)}\n{newt3}\n')
                    break
        else:
            path.pop()
    return settled            
        
        
if __name__ == '__main__':
    t3 = TicTacToe()
    # t3.place(0,1)
    # t3.place(1,1)
    # t3.place(2,2)
    # print(t3.signature())
    settled = DepthFirstTicTacToe(t3)
    print(len(settled))
    print()
    
    a = list(settled)
    a.sort(key = lambda t3 : int(t3.board))
    for t3 in a:
        print(t3, f'{hex(t3.signature())}\n')