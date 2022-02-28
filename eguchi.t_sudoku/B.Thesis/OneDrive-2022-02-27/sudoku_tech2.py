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

potential = []
space_potential = []

def solver(value):
    old_value = []

    old_value = copy.deepcopy(value)
    possibility(value)
    for y in range(9):
        for x in range(9):
            if len(potential[9*y+x]) == 1:
                if check(value, x, y, potential[9*y+x][0]) == True:
                    value[y][x] = potential[9*y + x][0]
    potential.clear()
    if value != old_value:
        solver(value)

def possibility(value):
    for y in range(9):
        for x in range(9):
            space_potential = []
            if value[y][x] == 0:
                for i in range(1, 10):
                    if check(value, x, y, i) == True:
                        space_potential.append(i)
                potential.append(space_potential)
            else:
                potential.append(space_potential)
                        
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

value = value_from_grid('001040600000906000300000002040060050900302004030070060700000008000701000004020500')

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


