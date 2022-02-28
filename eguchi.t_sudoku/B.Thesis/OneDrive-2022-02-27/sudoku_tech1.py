import copy
#テクニック1

#テキストを二次元配列に変換する関数
def value_from_grid(grid):
    pos = []
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

def solver(value):
    x = y = 0
    i = 1
    
    for i in range(1, 10):
        for y in range(9):
            solver_row(value, y, i)

    for i in range(1, 10):
        for x in range(9):
            solver_column(value, x, i)
    
    for i in range(1, 10):
        for y in range(9):
            for x in range(9):
                solver_group(value, x, y, i)

    if solver_row(value, y, i) or solver_column(value, x, i) or solver_group(value, x, y, i):
        solver(value)

    return value

def solver_row(value, y, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]
    
    for _x in range (9):
        if value[y][_x] == 0:
            zero_count += 1
            
    if zero_count == 1:
        for _x in range(9):
            if check(value, _x, y, i):
                if value[y][_x] == 0:
                    value[y][_x] = i
                    return True

    return False

def solver_column(value, x, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]
    
    for _y in range (9):
        if value[_y][x] == 0:
            zero_count += 1

    if zero_count == 1:
        for _y in range(9):
            if value[_y][x] == 0:
                if check(value, x, _y, i):
                    value[_y][x] = i
                    return True
    return False

def solver_group(value, x, y, i):
    zero_count = 0
    xbase = (x // 3) * 3
    ybase = (y // 3) * 3

    for _y in range(ybase, ybase + 3):
        for _x in range (xbase, xbase + 3):
            if value[_y][_x] == 0:
                zero_count += 1

    if zero_count == 1:
        for _y in range(ybase, ybase + 3):
            for _x in range (xbase, xbase + 3):
                if value[_y][_x] == 0:
                    if check(value, _x, _y, i):
                        value[_y][_x] = i
                        return True
    return False
            
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

value = value_from_grid('080100000000070016610800000004000702000906000905000400000001028450090000000003040')

for _y in range(0, 9):
    for _x in range(0, 9):
        if _x == 2 or _x == 5:
            print(value[_y][_x], end = '')
            print('|', end = '')
        else:
            print(value[_y][_x], end = '')
    print('\n')
    if _y == 2 or _y == 5:
        print('---+---+---')
print('\n')

solver(value)

for _y in range(0, 9):
    for _x in range(0, 9):
        if _x == 2 or _x == 5:
            print(value[_y][_x], end = '')
            print('|', end = '')
        else:
            print(value[_y][_x], end = '')
    print('\n')
    if _y == 2 or _y == 5:
        print('---+---+---')



