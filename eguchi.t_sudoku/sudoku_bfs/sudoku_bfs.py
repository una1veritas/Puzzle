import copy

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


#幅優先探索のソルバー
def solver(value):
    children = []
    x = y = i = 0
    child = []
    copy_child = []

    children.append(value)
    
    while len(children) != 0:
        
        #子の中から1つ取り出す
        child = children[0]
        
        if len(children) % 100 == 0 : print(len(children))

        #childが正解ならば終了
        if answer(child) == True:
            return child
        
        #数字を空きマスに入れていく
        for y in range(9):
            for x in range(9):
                if child[y][x] == 0:
                    for i in range(1, 10):
                        if check(child, x, y, i):
                            copy_child = copy.deepcopy(child)
                            copy_child[y][x] = i
                            children.append(copy_child)

 
        #調べた盤面をリストから除外する
        if len(children) != 0:
            del children[0]

#盤面に空きマスが無ければtrueを返す
def answer(value):
    x = y = 0
    zero_count = 0

    for y in range(9):
        for x in range(9):
            if value[y][x] == 0:
                zero_count = zero_count + 1

    if zero_count == 0:
        return True
    else:
        return False

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

def print_sudoku(value):
    for _y in range(0, 9):
        for _x in range(0, 9):
            print(value[_y][_x], end = ' ')
        print('\n')
    print('\n')
#ソルバーを実行する

#value = value_from_grid('628914730130257680975836412009683241481572396263149857897465123312798564006321978')
value = value_from_grid('000503000260080051300000008070000020000702000508030107001604500050020040002050700')
child = []
print_sudoku(value)

child = solver(value)

print_sudoku(child)
