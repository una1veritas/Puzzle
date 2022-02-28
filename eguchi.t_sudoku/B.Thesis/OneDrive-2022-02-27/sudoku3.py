#幅優先探索

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


def solver(value, x = 0, y = 0, i = 1):
    #縦が8より大きいときは解けたときだからTrueを返す.
    if y > 8:
        return True

    #空きマスでないとき
    elif value[y][x] != 0:
        
        #横軸の最後に到達したら下の列に移動する
        if x == 8:
            if solver(value, 0, y+1, i):
                return True
            
        #右端以外のとき右のマスに移動する
        else:
            if solver(value, x+1, y, i):
                return True
    #空きマスのとき
    else:
        for i in range(1, 10):
            if check(value, x, y, i):
                value[y][x] = i
                if x == 8:
                    if solver(value, 0, y+1):
                        return True
                else:
                    if solver(value, x+1, y):
                        return True
        value[y][x] = 0
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

value = value_from_grid('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
solver(value)
for _y in range(0, 9):
    for _x in range(0, 9):
        print(value[_y][_x], end = '')
    print('\n')


