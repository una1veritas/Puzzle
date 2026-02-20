'''
Created on 2026/01/28

@author: sin
'''
import operator

class bitarray:
    
    def __init__(self, arg1, arg2 = None):
        if isinstance(arg1, bitarray) and arg2 == None:
            #ignore arg2 and arg3
            self.bitwidth = arg1.bitwidth
            self.mask = arg1.mask
            self.bits = arg1.bits
        elif isinstance(arg1, int):
            self.bitwidth = int(arg1)
            self.mask = (1<<self.bitwidth) - 1
            if isinstance(arg2, int) :
                self.bits = arg2
            elif isinstance(arg2, (tuple, list, str)) :
                self.bits = 0
                for i in range(len(arg2)) :
                    self[i] = arg2[i]
        else:
            raise NotImplementedError(f'{arg1} is invalid initializer.')

    def __int__(self) -> int:
        return self.bits
    
    def __len__(self) -> int:
        return (self.bits.bit_length() + self.bitwidth - 1) // self.bitwidth if self.bits else 1
    
    def __eq__(self, other) -> bool:
        if isinstance(other, bitarray) :
            return self.bits == other.bits and self.bitwidth == other.bitwidth
        elif hasattr(other, '__getitem__') and len(self) == len(other) :
            return all([self[i] == other[i] for i in range(len(self))])
        return False
    
    def __hash__(self) -> int:
        return hash(self.bits)

    def __getitem__(self, index):
        if not isinstance(index, slice):
            ix = operator.index(index)  # accepts int-like objects=
            return (self.bits >> (self.bitwidth * ix)) & self.mask
        
        # raise NotImplementedError('get item with slice is not implemented')
        # slice index -> return same type (copy) for safety
        # slice.indices normalizes start/stop/step and handles negatives/out-of-range
        start, stop, step = index.indices(len(self))
        intval = 0
        iy = 0
        for ix in range(start, stop, step) :
            intval |= self[ix] << (iy * self.bitwidth)
            iy += 1
        return bitarray(self.bitwidth, intval)
    
    def __setitem__(self, index, value):
        # validate values before storing        
        # if value.bit_length() > self.bitwidth :
        #     raise ValueError(f'value {value} exceeds limit {(1<<self.bitwidth)-1}.')
        if not isinstance(index, slice):
            ix = operator.index(index)
            #print(index, value)
            if value > self.mask :
                raise ValueError(f'value {value} exceeds limit {self.mask}.')
            windowbits = self.bits & (self.mask << (ix * self.bitwidth))
            self.bits ^= windowbits
            self.bits |= value  << (self.bitwidth * ix)
            return
        # slice assignment
        start, stop, step = index.indices(len(self))
        indices = list(range(start, stop, step))
        vals = list(value)  # materialize the RHS
        if len(vals) != len(indices):
            raise ValueError(f"attempt to assign sequence of size {len(vals)} " \
                             f"to extended slice of size {len(indices)}" \
                             )
        for i, v in zip(indices, vals):
            if v > self.mask :
                raise ValueError(f'value {v} exceeds limit {self.mask}.')
            self[i] = v
        return
        
    class bitarray_iterator:
        def __init__(self, barray):
            self.array = barray
            self.index = 0
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.index < len(self.array) :
                result = self.array[self.index]
                self.index += 1
                return result
            else:
                raise StopIteration            
        
    
    def __iter__(self):
        return self.bitarray_iterator(self)

    
    def __repr__(self):
        return 'bitarray(' + str(self) + ') '
    
    def __str__(self):
        #print(f'len = {len(self)}')
        return '(' + ', '.join([str(e) for e in self]) + ')'
    
    def __bytes__(self):
        seq = b''
        val = self.bits
        for i in range(len(self)-1, -1, -1):
            #print(hex(val))
            seq += bytes([val & 0xff])
            val >>= 8
        return seq
    
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
    bw = 11
    n = 17
    l = [random.randint(0,(1<<bw) - 1) for _ in range(n)]
    print(l)
    ba = bitarray(bw, l)
    print(f'bitarray = {ba}')
    print(f'len = {len(ba)}')
    print(f'by slice 3:-1 {ba[3:-1]}')
    ba[3:7:2] = [18, 22]
    print(ba)
    print(bytes(ba))
    ba = bitarray(bw, l)
    
    for i in range(10000):
        ix = random.randint(0, n - 1)
        iy = (ix + random.randint(0,n)) % n
        t = l[ix]
        l[ix] = l[iy]
        l[iy] = t
        #print(l)
        t = ba[ix]
        ba[ix] = ba[iy]
        ba[iy] = t
        if ba == l :
            pass
        else:
            raise ValueError('differ!!')
    else:
        print('passed!')