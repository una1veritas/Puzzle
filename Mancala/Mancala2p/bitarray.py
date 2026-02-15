'''
Created on 2026/01/28

@author: sin
'''
import operator

class bitarray:
    
    def __init__(self, arg1, arg2 = None, arg3 = None):
        if isinstance(arg1, bitarray) :
            #ignore arg2 and arg3
            self._uwidth = arg1._uwidth
            self._size = arg1._size
            self.bits = arg1.bits
        elif isinstance(arg2, int) and isinstance(arg3, int) :
            #arg2 as uwidth, arg3 as length
            self._uwidth = arg2
            self._size = arg3
            self.bits = int(arg1)
        elif isinstance(arg1, int) and isinstance(arg2, (tuple, list)) :
            self._uwidth = arg1
            self._size = len(arg2)
            self.bits = 0
            for i in range(len(arg2)) :
                self.set(i, arg2[i] & ((1<<self._uwidth) - 1) )
        else:
            raise NotImplementedError(f'{arg1} is invalid initializer.')
    
    ''' popcnt '''
    @staticmethod
    def bit_count(intval): 
        return self.bits.bit_count()

    def _bitmask(self):
        return (1 << self._uwidth) - 1

    def __int__(self):
        return self.bits
    
    def __len__(self):
        return self._size
    
    def __eq__(self, other):
        if isinstance(other, bitarray) :
            return self._size == other._size and self._uwidth == other._uwidth \
                and self.bits == other.bits
        return False
    
    def __hash__(self):
        return hash(self.bits)
    
    def get(self, ix):
        return self._bitmask() & (self.bits >> (self._uwidth * ix))
    
    def __getitem__(self, index):
        if not isinstance(index, slice):
            ix = operator.index(index)  # accepts int-like objects
            if ix >= 0 :
                return self.get(ix)
            else:
                return self.get(len(self) + ix)
        #raise NotImplementedError('get item with slice is not implemented')
        # slice index -> return same type (copy) for safety
        # slice.indices normalizes start/stop/step and handles negatives/out-of-range
        start, stop, step = index.indices(len(self))
        newarray = bitarray(self._uwidth, stop - start, 0)
        nix = 0
        for ix in range(start, stop, step) :
            newarray[nix] = self.get(ix)
        return newarray
    
    def set(self, ix, val):
        if ix >= self._size :
            self._size = ix + 1
        #print(ix, val, self._size, f'len = {len(self)}')
        val &= self._bitmask()
        self.bits &= ~(self._bitmask() << (self._uwidth * ix))
        self.bits |= (val << (self._uwidth * ix))
        
    def __setitem__(self, index, value):
        # validate values before storing
        if not isinstance(index, slice):
            ix = operator.index(index)
            if ix >= 0 :
                self.set(ix, value)
                return
            else:
                self.set(len(self) + ix, value)
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
        return 'bitarray(' + str(self) + ') '
    
    def __bin__(self):
        return bin(self.bits)
    
    def __str__(self):
        #print(f'len = {len(self)}')
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
        

        