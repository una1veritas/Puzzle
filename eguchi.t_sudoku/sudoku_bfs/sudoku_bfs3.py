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

        execution(child)

        print(child, '\n')

        print(len(children))

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

#tech1_solverを実行する関数
def execution(value):
    copy_value = []
    copy_value = copy.deepcopy(value)

    if answer(copy_value):
        return copy_value

    if value == tech1_solver(copy_value):
        return copy_value

    execution(tech1_solver(value))

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

    return value

#行について1つだけ空きマスであればマスを埋める
def tech1_row(value, y, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]

    #各行の空きマスの数をカウントする
    for _x in range (9):
        if value[y][_x] == 0:
            zero_count = zero_count + 1

    #空きマスが1つだけならどの数字が埋められていないかを調べる
    if zero_count == 1:
        for _x in range(9):
            number.remove(value[y][_x])

        #埋められていない数字を空きマスに入れる
        for _x in range(9):
            if value[y][_x] == 0:
                value[y][_x] = number[0]
                return value

    return value

#列について1つだけ空きマスであればマスを埋める
def tech1_column(value, x, i):
    zero_count = 0
    number = [0,1,2,3,4,5,6,7,8,9]

    #各列の空きマスの数をカウントする
    for _y in range (9):
        if value[_y][x] == 0:
            zero_count = zero_count + 1

    #空きマスが1つだけならどの数字が埋められていないかを調べる
    if zero_count == 1:
        for _y in range(9):
            number.remove(value[_y][x])

        #埋められていない数字を空きマスに入れる
        for _y in range(9):
            if value[_y][x] == 0:
                value[_y][x] = number[0]
                return value
    return value

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

#ソルバーを実行する

value = value_from_grid('628914730130257680975836412009683241481572396263149857897465123312798564006321978')
child = []
for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')
print('\n')

child = solver(value)

for _y in range(0, 9):
    for _x in range(0, 9):
        print(child[_y][_x], end = '')
    print('\n')
