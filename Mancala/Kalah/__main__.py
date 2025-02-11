'''
Created on 2025/02/11

@author: sin
'''
from board import Board2players
#すまん二人専用にちょっといじってある

def _get_opponent_pocket_index(board, index: int) -> int:
    """ 対応する敵陣のポケットのインデックスを計算 """
    #player_id = board._get_player_id(index)
    player_id = index // (board.grids_per_player + board.STORES_PER_PLAYER) # grid between players の一人あたりの数のこと
    opponent_id = (player_id + 1) % board.NUMBER_OF_PLAYERS
    print(f'pocket/pid index = {index}, player id = {player_id}, opponent player id = {opponent_id}')
    start_index = board.get_player_start_index(opponent_id)
    
    offset = (board.grids_per_player - 1) - (index % board.grids_per_player)
    '''プレーヤーのグリッド（ポケット）の何番目かは、
    (board.grids_per_player + board.grid_between_player) で余りをとらんといかんのでは？'''
    offset = (board.grids_per_player - 1) - (index % (board.grids_per_player + board.STORES_PER_PLAYER))
    
    return start_index + offset

if __name__ == '__main__':
    board = Board2players(3, 6)
    print(board)
    print('[13][12,11,10, 9, 8, 7]]\n    [ 0, 1, 2, 3, 4, 5][ 6]')
    for ix in range(12) :
        if board._is_grid_between_players(ix) : continue
        associated_index = _get_opponent_pocket_index(board, ix)
        print(associated_index)
        print()