'''
Created on 2026/01/28

@author: sin
'''
import operator

class bitarray:
    
    ''' popcnt '''
    @staticmethod
    def bit1count(intval): 
        BITS_COUNT_TABLE = [ 0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, ]
        cnt = 0
        while intval > 0 :
            cnt += BITS_COUNT_TABLE[intval & 0x0f]
            intval >> 4
            cnt += BITS_COUNT_TABLE[intval & 0x0f]
            intval >> 4
        return cnt
    
    @staticmethod
    def bit_length(val, bwidth):
        counter = 0
        while val > 0 :
            val >>= bwidth
            counter += 1
        return counter

    
    def __init__(self, bitwidth, initlen, initval):
        if isinstance(bitwidth, int) :
            self._uwidth = bitwidth
            self._size = initlen
            self.bits = int(initval)
        else:
            raise NotImplementedError(f'{initval} is invalid initializer.')
    
    def _bitmask(self):
        return (1 << self._uwidth) - 1

    def __int__(self):
        return self.bits
    
    def __len__(self):
        return self._size
    
    def __getitem__(self, index):
        if not isinstance(index, slice):
            ix = operator.index(index)  # accepts int-like objects
            return self._bitmask() & (self.bits >> (self._uwidth * ix))
        
        #raise NotImplementedError('get item with slice is not implemented')
        # slice index -> return same type (copy) for safety
        # slice.indices normalizes start/stop/step and handles negatives/out-of-range
        start, stop, step = index.indices(len(self))
        
        newbits = 0
        for ix in range(start, stop, step) :
            val = self._bitmask() & (self.bits >> (self._uwidth * ix))
            newbits |= (val << (self._uwidth * ix))
        return bitarray(self._uwidth, stop - start, newbits)
    
    def set(self, ix, val):
        if ix >= self._size :
            self._size = ix + 1
        print(ix, val, self._size, f'len = {len(self)}')
        val &= self._bitmask()
        self.bits &= ~(self._bitmask() << (self._uwidth * ix))
        self.bits |= (val << (self._uwidth * ix))
        
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
        print(f'len = {len(self)}')
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
        

        