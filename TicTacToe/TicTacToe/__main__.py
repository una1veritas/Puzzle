'''
Created on 2025/04/16

@author: sin
'''
class TicTacToe:
    def __init__(self, board = None):
        if board == None :
            self.board = [' '] * 9
        else:
            self.board = board[:9]
    
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
    
    def place(self,row, col, symbol = 'X'):
        self.board[3*row+col] = symbol
        
if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.place(0,2,'X')
    print(ttt)