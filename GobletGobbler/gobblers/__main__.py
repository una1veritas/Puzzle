'''
Created on 2026/01/18

@author: sin
'''

class GobletGobblers:
    def __init__(self):
        self.board = [0]*9
        # each cell formed from 6 bit, 
        # 1 in each 2 bits represents existence of either blue one or red one
    
    def __str__(self):
        rows = ''
        for row in range(3):
            sym = self.board[row*3:row*3+3]
            rows += f'{sym[0]:1}|{sym[1]:1}|{sym[2]:1}'
            if row < 2 :
                rows+= '\n'
                rows += '-+-+-'
            rows += '\n'
        return rows
    
if __name__ == '__main__':
    board = GobletGobblers()
    print(board)