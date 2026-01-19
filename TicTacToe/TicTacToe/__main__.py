'''
Created on 2025/04/16

@author: sin
'''
class TicTacToe:
    def __init__(self, board = None):
        if board == None :
            self.board = [0] * 9
            self.nextturn = 0 # first X player
        else:
            self.board = list()
            count_X = 0 
            count_O = 0
            for cell in board:
                self.board.append(cell)
                if self.board[-1] == 1 or self.board[-1] == 'X' :
                    self.board[-1] = 1
                    count_X += 1
                elif self.board[-1] == 2 or self.board[-1] == 'X' :
                    self.board = 'O'
                    count_O += 1
            if count_X == count_O :
                self.nextturn = 0
            else:
                self.nextturn = 1
    
    def __str__(self):
        rows = ''
        for row in range(3):
            sym = ['X' if cell == 1 else ('O' if cell == 2 else ' ') for cell in self.board[row*3:row*3+3]]
            rows += f'{sym[0]:1}|{sym[1]:1}|{sym[2]:1}'
            if row < 2 :
                rows+= '\n'
                rows += '-+-+-'
            rows += '\n'
        return rows
    
    def place(self,row, col):
        if self.nextturn == 0 :
            self.board[3*row+col] = 1
        else: 
            self.board[3*row+col] = 2
        self.nextturn = (self.nextturn + 1) % 2
    
        
    
def DepthFirstTicTacToe(ttt):
        for ix in range(len(ttt)):
            if ttt.board[ix] == 0 :
                if ttt.nextturn == 1 :
                    nextboard = TicTacToe(ttt.board)
                    nextboard[ix] = 'X'
                    
if __name__ == '__main__':
    ttt = TicTacToe()
    print(ttt)
    ttt.place(0,2)
    print(ttt)