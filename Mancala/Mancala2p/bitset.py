'''
Created on 2026/02/11

@author: sin
'''

class BitSet:
    '''
    classdocs
    '''


    def __init__(self, params = None):
        '''
        Constructor
        '''
        self.value = 0
        if hasattr(params,'__iter__') :
            for each in params :
                val = int(each)
                if val < 0 :
                    raise ValueError(f'BitSet does not accept negative value {each}')
                self.value |= 1<<val
        elif isinstance(params, int) :
            self.value = params
        elif params != None :
            try:
                self.value = int(params)
            except :
                raise ValueError(f'{params} cannot interpreted as int.')
        return
    
    def __int__(self) -> int:
        return self.value
    
    def __bool__(self) -> bool:
        return bool(self.value)
    
    def __len__(self) -> int:
        # the number of 1 elements
        return self.value.bit_count()

    def bit_length(self) -> int:
        # the number of 1 elements
        return self.value.bit_length()
    
    def add(self, elem: int) -> None:
        if not isinstance(elem, int) or elem < 0 :
            raise TypeError("Element must be a non-neggative integer")
        self.value |= (1 << elem)
    
    #this raises error if elem is abcent.
    def remove(self, elem: int) -> None:
        if not isinstance(elem, int) or elem < 0 :
            raise TypeError("Element must be a non-neggative integer")
        if elem not in self:
            raise ValueError(f"{elem} not in bitset")
        self.value &= ((1<<self.value.bit_length()) - 1) ^ (1 << elem)
    
    def discard(self, elem: int) -> None:
        if not isinstance(elem, int) or elem < 0:
            return
        self.value &= ((1<<self.value.bit_length()) - 1) ^ (1 << elem)

    def __contains__(self, elem: int) -> bool:
        return bool(self.value & (1 << elem))
    
    def __iter__(self):
        self._iter_pos = 0
        return self
    
    def __next__(self):
        while self._iter_pos < self.bitlength() :
            if bool(self.value & (1 << self._iter_pos)) :
                retval = self._iter_pos
                self._iter_pos += 1
                return retval
            self._iter_pos += 1
        raise StopIteration
    
    def __list__(self):
        bits = f'{self.value:b}'
        return [(1<<bpos) for bpos in range(len(bits)) if bits[bpos] == '1']
    
    def __repr__(self) -> str:
        return f'BitSet({str(self)})'
    
    def __str__(self):
        outstr = '{'
        pos = 0
        val = self.value
        while True :
            if bool(val & 1) :
                outstr += str(pos)
                if (val>>1) > 0 :
                    outstr += ', '
                else:
                    break
            pos += 1
            val >>= 1
        return outstr + '} '
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, BitSet):
            return False
        return self.value == other.value
    
    def __or__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        return BitSet(self.value | other.value)
    
    def __and__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        return BitSet(self.value & other.value)
    
    def __xor__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        return BitSet(self.value ^ other.value)
    
    def __sub__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        return BitSet(self.value & ~other.value)
    
    def __ior__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        self.value |= other.value
        return self
    
    def __iand__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        self.value &= other.value
        return self
    
    def __ixor__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        self.value ^= other.value
        return self
    
    def __isub__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        self.value &= ~other.value
        return self
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def copy(self):
        return BitSet(self.value)
    
    def clear(self) -> None:
        self.value = 0

if __name__ == "__main__":
    bset = BitSet({0, 3, 8})
    print(bset)
    bset2 = BitSet({7,88})
    bset |= bset2
    print(bset)
    bset.discard(7)
    print(bset)
    