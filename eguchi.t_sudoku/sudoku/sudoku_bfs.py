
class Sudoku:
    def __init__(self, grid):
    #テキストを二次元配列に変換する関数
    #   def value_from_grid(grid):
        self.value = []
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
            if (count % 9) == 0:
                self.value.append(row)
                row = []

    def children(self):
        #bfsにおけるnode = value
        #最後まで解き終わっていればループ終了
        if answer(self.value):
            return []
        
        #左上から空きマスに数字を1つ入れていく
        print("computing newgen..")
        newgen = []
        for y in range(9):
            for x in range(9):
                if self.value[y][x] == 0:
                    for i in range(1, 9):
                        #数字を入れた盤面をチェックし制約を満たすとき、その盤面を子とする
                        if self.check(x, y, i):
                            self.value[y][x] = i
                            newgen.append(self.value)
                            
        return newgen


    #盤面に空きマスが無ければtrueを返す
    def answer(value):
        for row in range(9):
            for col in range(9):
                print(row, col, value)
                if value[row][col] == 0:
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
    
    def __str__(self):
        tmp = ''
        for r in range(10):
            if r < 9 :
                if r % 3 == 0:
                    for c in range(9):
                        if c % 3 == 0 :
                            tmp += '+-'
                        else:
                            tmp += '--'
                    tmp += '+\n'
                for c in range(10):
                    if c < 9 : 
                        if c % 3 == 0 :
                            tmp += '|'
                        else:
                            tmp += ' '
                        tmp += str(value[r][c])
                    else:
                        tmp += '|'
            else:
                for c in range(9):
                    if c % 3 == 0 :
                        tmp += '+-'
                    else:
                        tmp += '--'
                tmp += '+\n'
            tmp += '\n'
        return tmp


sudoku = Sudoku('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
print(sudoku)

# for _y in range(0, 9):
#     for _x in range(0, 9):
#         print(value[_y][_x], end = '')
#     print('\n')
print('\n')

frontier = [sudoku]
while len(frontier) > 0:
    print(frontier)
    node = frontier.pop(0)
    nextgens = children(node)
    frontier.append(nextgens)
    print(len(frontier))

# for _y in range(0, 9):
#     for _x in range(0, 9):
#         print(value[_y][_x], end = '')
#     print('\n')
print(grid_str(value))

