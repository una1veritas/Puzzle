#テキストを二次元配列に変換する関数
def value_from_grid(grid):
    value = []
    num = "123456789"
    chars = [c for c in grid if c in num or c in '0.']
    assert len(chars) == 81
    #入力文字列をint型にする
    grid_int = map(lambda x: int(x) if x != "." else 0, chars)

    count = 0
    row = []

    #入力文字列を9*9に分割する
    for i in grid_int:
        row.append(i)
        count += 1
        if count % 9 == 0:
            value.append(row)
            row = []
    return value

child = []
x = 0
y = 0
i = 0

def solver(value):
    
    #bfsにおけるnode = value
    #最後まで解き終わっていればループ終了
    if answer(value):
        return True
    
    #左上から空きマスに数字を1つ入れていく
    for y in range(9):
        for x in range(9):
            if value[y][x] == 0:
                for i in range(1, 9):
                    #数字を入れた盤面をチェックし制約を満たすとき、その盤面を子とする
                    if check(value, x, y, i):
                        value[y][x] = i
                        child.append(value)
                        
    #子が空でないとき先頭の子を取り出し、それをnodeとして再帰する
    if len(child) != 0:
        solver(child.pop(0))


#盤面に空きマスが無ければtrueを返す
def answer(value):
    x = y = 0

    for y in range(9):
        for x in range(9):
            if value[y][x] == 0:
                return False
    return True

#行,列,グループに対して制約を満たすかチェック
def check(value, x, y, i):
    if row(value, y, i) and column(value, x, i) and block(value, x, y, i):
        return True
    return False

#y行に対して制約を満たすかチェック
def row(value, y, i):
    return all(True if i != value[y][_x] else False for _x in range(9))

#x列に対して制約を満たすかチェック
def column(value, x, i):
    return all(True if i != value[_y][x] else False for _y in range(9))

#グループに対して制約を満たすかチェック
def block(value, x, y, i):
    #所属するブロックの一番左上のマスの座標を求める
    xbase = (x // 3) * 3
    ybase = (y // 3) * 3

    #求めた座標のx,y軸を+3した範囲でチェックするとブロック内でのチェックが出来る
    return all(True if i != value[_y][_x] else False
            for _y in range(ybase, ybase + 3)
                for _x in range(xbase, xbase + 3))

class Sudoku():
    def __init__(self, grid):
        if isinstance(grid, str) :
            if len(grid) != 81 :
                raise ValueError('digit string has illegal length '+str(len(grid)))
            self.values = [int(d) if d.isdigit() else int('0') for d in grid]
            return
        elif isinstance(grid, list) :
            if len(grid) == 81 :
                self.values = [int(d) for d in grid]
                return
            elif len(grid) == 9 :
                self.values = list()
                for r in grid:
                    if len(r) != 9 :
                        raise ValueError('nested list has illegal number of elements '+str(len(r)))
                    self.values += r
                return
            raise ValueError('list has illegal number of elements '+str(len(grid)))
        else:
            raise ValueError('illegal arguments for constructor.')
            
            
    def __str__(self):
        tmp = ''
        for r in range(9):
            for c in range(9):
                tmp += str(self.values[r*9+c])
                if c % 3 == 2:
                    tmp += '|'
                else:
                    tmp += ' '
            tmp += '\n'
            if r % 3 == 2 :
                tmp += '-----+-----+-----+\n'
        return tmp
    
    def issolved(self):
        return 0 not in self.values
    
#    def children(self):
        

sudoku = Sudoku('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
print(sudoku)

print(sudoku.issolved())

#solver(value)
frontier = list()
frontier.append(sudoku)
while any([not s.issolved() for s in frontier]):
    print(frontier)
    break


