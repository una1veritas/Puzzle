'''
Created on 2025/02/11

@author: sin
'''
from board import Board2players

def _get_opponent_pocket_index(self, index: int) -> int:
    """ 対応する敵陣のポケットのインデックスを計算 """
    player_id = self._get_player_id(index)
    opponent_id = (player_id + 1) % self.players_num
    
    start_index = self.get_player_start_index(opponent_id)
    
    offset = (self.grids_per_player - 1) - (index % self.grids_per_player)
    return start_index + offset

if __name__ == '__main__':
    pass