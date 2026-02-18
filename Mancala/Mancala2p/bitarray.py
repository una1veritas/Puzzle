'''
Created on 2026/01/28

@author: sin
'''
import operator

class bitarray:
    
    def __init__(self, arg1, arg2 = None, arg3 = None):
        if isinstance(arg1, bitarray) :
            #ignore arg2 and arg3
            self.bitwidth = arg1.bitwidth
            self.bits = arg1.bits
        elif isinstance(arg1, int) :
            self.bitwidth = int(arg1)
            if isinstance(arg2, int) :
                self.bits = arg2
            elif isinstance(arg2, (tuple, list, str)) :
                self.bits = 0
                for i in range(len(arg2)) :
                    self[i] = arg2[i]
        else:
            raise NotImplementedError(f'{arg1} is invalid initializer.')
    
    ''' popcnt '''
    @staticmethod
    def bit_count(intval): 
        return self.bits.bit_count()

    def _mask(self):
        return (1 << self.bitwidth) - 1

    def __int__(self):
        return self.bits
    
    def __len__(self):
        return self.bits.bit_length() // self.bitwidth + \
            (1 if self.bits.bit_length() % self.bitwidth > 0 else 0)
    
    def __eq__(self, other):
        if isinstance(other, bitarray) :
            return self.bits == other.bits and self.bitwidth == other.bitwidth
        return False
    
    def __hash__(self):
        return hash(self.bits)

    def __getitem__(self, index):
        if not isinstance(index, slice):
            ix = operator.index(index)  # accepts int-like objects=
            return (self.bits >> (self.bitwidth * ix)) & self._mask()
        
        raise NotImplementedError('get item with slice is not implemented')
        # slice index -> return same type (copy) for safety
        # slice.indices normalizes start/stop/step and handles negatives/out-of-range
        # start, stop, step = index.indices(len(self))
        # newarray = bitarray(self.bitwidth, stop - start, 0)
        # nix = 0
        # for ix in range(start, stop, step) :
        #     newarray[nix] = self.get(ix)
        # return newarray
    
    def __setitem__(self, index, value):
        # validate values before storing        
        # if value.bit_length() > self.bitwidth :
        #     raise ValueError(f'value {value} exceeds limit {(1<<self.bitwidth)-1}.')
        if value > self._mask() :
            raise ValueError(f'value {value} exceeds limit {self._mask()}.')
        if not isinstance(index, slice):
            ix = operator.index(index)
            #print(index, value)
            windowed = self.bits & (self._mask() << (ix * self.bitwidth))
            self.bits ^= windowed
            self.bits |= value  << (self.bitwidth * ix)
            if self.bits == 0 :
                print(ix, value, windowed)
        else:
            raise NotImplementedError('set item with slice is not implemented')
        # slice assignment
        # start, stop, step = index.indices(len(self))
        # indices = list(range(start, stop, step))
        # vals = list(value)  # materialize the RHS
        # if len(vals) != len(indices):
        #     raise ValueError(
        #         f"attempt to assign sequence of size {len(vals)} "
        #         f"to extended slice of size {len(indices)}"
        #     )
        # for i, v in zip(indices, vals):
        #     self.set(i, v)
        # return
    
    def __repr__(self):
        return 'bitarray(' + str(self) + ') '
    
    def __bin__(self):
        return bin(self.bits)
    
    def __str__(self):
        #print(f'len = {len(self)}')
        return str([self[i] for i in range(len(self))])

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
    

if __name__ == "__main__":
    import random
    l = [random.randint(0,511) for _ in range(20)]
    print(l)
    ba = bitarray(9, l)
    print('bitarray =', ba)
    
    for i in range(10000):
        ix = random.randint(0,20 - 1)
        iy = (ix + random.randint(0,20)) % 20
        t = l[ix]
        l[ix] = l[iy]
        l[iy] = t
        t = ba[ix]
        ba[ix] = ba[iy]
        ba[iy] = t
        if all([ba[i] == l[i] for i in range(20)]) :
            pass
        else:
            raise ValueError('differ!!')
    else:
        print('passed!')