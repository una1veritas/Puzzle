'''
Created on 2025/11/06

@author: sin
'''
import random 

class Towers :
    def __init__(self, maxval: int = 5, seed: int | None = None):
        self.towers = [[] for _ in range(3)]
        if seed is not None:
            random.seed(seed)
        self.towers[0] = [i for i in range(1, maxval+1)].copy()
        random.shuffle(self.towers[0])
        return
    
    def __str__(self):
        buf = "Towers(\n"
        for ea in self.towers:
            buf += str(ea)
            buf += "\n"
        buf += ") "
        return buf
    
    def move_top(self, src, dst):
        top = self.towers[src - 1].pop(-1)
        self.towers[dst - 1].append(top)
    
    def completed(self):
        nonemptycount = 0
        for t in self.towers: 
            if len(t) > 0 :
                nonemptycount += 1
            for ix in range(1, len(t)):
                if not (t[ix - 1] > t[ix]) :
                    return False
        return nonemptycount == 1
    
if __name__ == '__main__':
    tws = Towers()
    while True:
        print(tws)
        opr = input('? ')
        try:
            oprs = opr.split(' ')
            fromix = int(oprs[0])
            toix = int(oprs[1])
            if fromix <= 0 or fromix > len(tws.towers) :
                raise ValueError('too big or small')
            if toix <= 0 or toix > len(tws.towers) :
                raise ValueError('too big or small')
        except ValueError:
            print('seems operation is illegal. quit.')
            break
        tws.move_top(fromix, toix)
        if tws.completed() :
            print('Congraturation!!')
            break
        