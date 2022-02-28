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

def technique(value):
    old_value = []

    old_value = value

    tech1_solver(value)
    tech2_solver(value)

    if value != old_value:
        technique(value)
        

#行,列,グループについてtech1を使う関数
def tech1_solver(value):
    x = y = 0
    i = 1

    for i in range(1, 10):
        for y in range(9):
            tech1_row(value, y, i)

    for i in range(1, 10):
        for x in range(9):
            tech1_column(value, x, i)
    
    for i in range(1, 10):
        for y in range(9):
            for x in range(9):
                tech1_group(value, x, y, i)

    if tech1_row(value, y, i) or tech1_column(value, x, i) or tech1_group(value, x, y, i):
        tech1_solver(value)

    return value

#行について1つだけ空きマスであればマスを埋める
def tech1_row(value, y, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]

    #各行の空きマスの数をカウントする
    for _x in range (9):
        if value[y][_x] == 0:
            zero_count = zero_count + 1

    if zero_count == 1:
        for _x in range(9):
            if check(value, _x, y, i):
                if value[y][_x] == 0:
                    value[y][_x] = i
                    return True

    return False

#列について1つだけ空きマスであればマスを埋める
def tech1_column(value, x, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]

    #各列の空きマスの数をカウントする
    for _y in range (9):
        if value[_y][x] == 0:
            zero_count = zero_count + 1

    if zero_count == 1:
        for _y in range(9):
            if check(value, x, _y, i):
                if value[_y][x] == 0:
                    value[_y][x] = i
                    return True
    return False

#グループについて1つだけ空きマスであればマスを埋める
def tech1_group(value, x, y, i):
    zero_count = 0
    xbase = (x // 3) * 3
    ybase = (y // 3) * 3
    
    #各グループの空きマスの数をカウントする
    for _y in range(ybase, ybase + 3):
        for _x in range (xbase, xbase + 3):
            if value[_y][_x] == 0:
                zero_count = zero_count + 1

    #空きマスが1つだけなら制約を満たすよう数字を入れる                
    if zero_count == 1:
        for _y in range(ybase, ybase + 3):
            for _x in range (xbase, xbase + 3):
                if check(value, _x, _y, i):
                    if value[_y][_x] == 0:
                        value[_y][_x] = i
                        return True
    return False




potential = []
space_potential = []

def tech2_solver(value):
    old_value = []

    old_value = copy.deepcopy(value)
    
    tech2_possibility(value)
    for y in range(9):
        for x in range(9):
            if len(potential[9*y+x]) == 1:
                value[y][x] = potential[9*y + x][0]

    potential.clear()
    if value != old_value:
        tech2_solver(value)

    return value

def tech2_possibility(value):
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




#ソルバーを実行する
value = value_from_grid('080100000000070016610800000004000702000906000905000400000001028450090000000003040')
child = []
for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')
print('\n')

child = technique(value)

for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')
