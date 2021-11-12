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

def execution(value):
    copy_value = []
    copy_value = copy.deepcopy(value)

    if answer(copy_value):
        return copy_value

    if value == solver(copy_value):
        return copy_value

    execution(solver(value))

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

    return value

def solver_row(value, y, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]
    
    for _x in range (9):
        if value[y][_x] == 0:
            zero_count += 1
            
    if zero_count == 1:
        for _x in range(9):
            number.remove(value[y][_x])

        for _x in range(9):
            if value[y][_x] == 0:
                value[y][_x] = number[0]
                return value

    return value

def solver_column(value, x, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]
    
    for _y in range (9):
        if value[_y][x] == 0:
            zero_count += 1

    if zero_count == 1:
        for _y in range(9):
            number.remove(value[_y][x])
        
        for _y in range(9):
            if value[_y][x] == 0:
                value[_y][x] = number[0]
                return value
    return value

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
                if check(value, _x, _y, i):
                    value[_y][_x] = i
                    return value
    return value
            
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

value = value_from_grid('600014730130257600975836412009683201480072396263149057897460023312798564000320978')

for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')

print('\n')

execution(value)

for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')


