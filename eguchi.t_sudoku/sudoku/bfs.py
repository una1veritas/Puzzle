
class Sudoku():
    def __init__(self, grid):
        if isinstance(grid, str) :
            grid = [int(d) for d in grid]
        if not isinstance(grid, list) :
            raise TypeError('illegal arguments for constructor.')
        if len(grid) != 81 :
            raise ValueError('list has illegal number of elements '+str(len(grid)))
        self.values = tuple([d for d in grid])            
            
    def __str__(self):
        tmp = ''
        for r in range(9):
            for c in range(9):
                tmp += str(self.at(r, c))
                if c % 3 == 2:
                    tmp += '|'
                else:
                    tmp += ' '
            tmp += '\n'
            if r % 3 == 2 :
                tmp += '-----+-----+-----+\n'
        return tmp
    
    def __hash__(self):
        hashval = 0
        for bval in self.values:
            hashval = hashval*9 + bval
        return hashval
    
    def __eq__(self, another):
        if isinstance(another, Sudoku) :
            for i in range(len(self.values)):
                if self.values[i] != another.values[i] : return False
            return True
        return False 
    
    def at(self, row, col):
        #return self.values[self.index(row, col)]
        return self.values[row*9+col]
    
    def index(self, row, col):
        return row*9+col
    
    def issolved(self):
        return 0 not in self.values
    
    def rowboxes(self, row, col = 0):
        if 0 <= row < 9 and 0 <= col < 9:
            for c in range(9):
                yield (row, c)

    def columnboxes(self, row = 0, col = 0):
        if 0 <= row < 9 and 0 <= col < 9:
            for r in range(9):
                yield (r, col)      
    
    def blockboxes(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            baserow = (row // 3)*3
            basecol = (col // 3)*3
            for r in range(baserow, baserow+3):
                for c in range(basecol, basecol+3):
                    yield (r, c)

    def check(self, row, col, num):
        if num == 0 : return True
        for r,c in self.rowboxes(row):
            if self.at(r,c) == num : return False
        for r,c in self.columnboxes(col=col):
            if self.at(r,c) == num : return False
        for r,c in self.blockboxes(row, col):
            if self.at(r,c) == num : return False
        return True

    def possible(self, row, col):
        if self.at(row,col) != 0 : return set()
        numset = set([1,2,3,4,5,6,7,8,9])
        for r,c in self.rowboxes(row):
            numset.discard(self.at(r,c))
        for r,c in self.columnboxes(col=col):
            numset.discard(self.at(r,c))
        for r,c in self.blockboxes(row, col):
            numset.discard(self.at(r,c))
        return numset
    
    def fillsomebox(self):
        filled = list()
        for r, c in [(r,c) for r in range(9) for c in range(9)]:
            for i in self.possible(r,c):
                #print(r,c,i,self.check(r,c,i))
                filled.append(self.filledwith(r,c,i))
        return filled
    
    def filledwith(self, row, col, num):
        newvalues = list(self.values)
        newvalues[self.index(row, col)] = num
        return Sudoku(newvalues)
        
    def level(self):
        return [box != 0 for box in self.values].count(True)

sudoku = Sudoku('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
print(sudoku)

#print([(r,c) for r, c in sudoku.blockboxes(6,5)])
#solver(value)
frontier = list()
#done = set()
frontier.append(sudoku)
level = 0
solved = None
while solved == None :
    first = frontier.pop(0)
    if first.issolved():
        solved = first
        break
    #done.add(first)
    if first.level() > level :
        level = first.level()
        print('level {}, frontier size = {}, hash = {}'.format(first.level(), len(frontier), hex(hash(first))))
        print(first)
    nextgen = first.fillsomebox()
    frontier.extend(nextgen)

print(solved)
