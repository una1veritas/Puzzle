from copy import deepcopy
from typing import Dict, Tuple, List, Any
import gc, json
import psutil, os

from board import Board2p

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss  # in bytes

def search_with_min_max(player_id: int, board: Board2p, dp : dict) -> Tuple[int, int]:
    # if player_id != board.current_player() :
    #     raise ValueError('Error!')
    if dp == None :
        search_with_min_max.dp = {}
    search_with_min_max.original_player_id = board.current_player() #player_id
    search_with_min_max.max_to_go = 0
    search_with_min_max.max_sig = []
    
    '''Returns a pair (action, value) where action is the choice as a move, and value is its evaluation '''
    def _evaluate(board: Board2p) -> Tuple[int, int, int]:
        #print('_evaluate', board)
        result = dp.get(board) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if result is not None:
            return result
        for a_move in board.possible_moves():
            tmp_board = deepcopy(board)
            won_by_current = tmp_board.move(a_move)
            #print(f'move = {a_move}, tmp board = {tmp_board}')
            if won_by_current :
                #print('won by current')
                if tmp_board.current_player() == search_with_min_max.original_player_id :
                    result = (a_move, 1, 0)
                else:
                    result = (a_move, 0, 0)
                break
            r = _evaluate(tmp_board)
            #print(f'r = {r}')
            if result == None :
                '''a_move という手を打った move の結果その r[2] 手先でおきた勝敗'''
                result = (a_move, r[1], r[2] + 1) 
            else:
                if board.current_player() == search_with_min_max.original_player_id:
                    if r[1] > result[1] or (r[1] == 1 and r[2] + 1 < result[2]) or (r[1] == 0 and r[2] + 1 > result[2]) :
                        result = (a_move, r[1], r[2] + 1)
                else:
                    if r[1] < result[1] or (r[1] == 1 and r[2] + 1 > result[2]) or (r[1] == 0 and r[2] + 1 < result[2]) :
                        result = (a_move, r[1], r[2] + 1)
        #print(f'board = {board} result = {result}')
        to_go = result[2]
        sig = board.signature()
        if to_go > search_with_min_max.max_to_go or sig > search_with_min_max.max_sig :
            if sig > search_with_min_max.max_sig :
                search_with_min_max.max_sig = sig
            if to_go > search_with_min_max.max_to_go :
                search_with_min_max.max_to_go = to_go
            print(f'max to over = {search_with_min_max.max_to_go}, dp size = {len(dp)}, signature = {search_with_min_max.max_sig}')
            print(f"key {str(board)} and value {result}.")
            mem_usa = get_memory_usage()
            print(f'memory usage {mem_usa/10245/1024:.2f}Mb.')
            print()
            gc.collect()
        dp[board] = result
        return result

    r = _evaluate(board=board)
    return (r[0], r[1])


if __name__ == "__main__":
    board = Board2p(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
