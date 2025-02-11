'''
Created on 2025/02/11

@author: sin
'''
from typing import List, Optional, Type

from game import Game
from board import Board2players
from player import *

import psutil
import os

def consistent_prev_move(board : Board2players, player_id : int, start : int, amount: int):
    if board.data[start] != 0 :
        return False
    placed = [0] * len(board.data)
    for ix in range(start+1, start+amount) :
        placed[ix % len(board.data)] += 1
        print(placed, ix, board.data[ix % len(board.data)])
        if board.is_store(ix) :
            print('yes')
        if board.is_store(ix) or board.data[ix % len(board.data)] >= placed[ix] :
            continue
        return False
    return True
    
if __name__ == '__main__':
    board = Board2players(init_pieces_per_grid = 2, grids_per_player = 3)
    board.data[2] = 0
    print(board)
    print(consistent_prev_move(board, player_id=0, start=2, amount=4))