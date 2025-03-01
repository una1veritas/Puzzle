from copy import deepcopy
from typing import Dict, Tuple, List, Any
import gc, json

from board import Board2p

def search_with_min_max(player_id: int, board: Board2p, dp : dict) -> Tuple[int, int]:
    if dp == None :
        search_with_min_max.dp = {}
    search_with_min_max.original_player_id = player_id
    search_with_min_max.max_to_go = 0
    search_with_min_max.max_sig = []
    
    '''Returns a pair (action, value) where action is the choice as a move, and value is its evaluation '''
    def _evaluate(board: Board2p) -> Tuple[int, int, int]:
        result = dp.get(board) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if result is not None:
            #print(result)
            return result
        candidates = [i for i in board.possible_moves()]
        #print(board, candidates)
        for action in candidates:
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            
            if tmp_board.won_by_player() :
                if tmp_board.next_move_player() == search_with_min_max.original_player_id :
                    result = (action, 1, 0)
                    #print('original')
                else:
                    result = (action, 0, 0)
                    #print('opponent')
                break
            else:
                r = _evaluate(tmp_board)
                if result == None :
                    result = (action, r[1], r[2] + 1) # action の move をした結果数手先でおきた結果
                else:
                    if board.next_move_player() == search_with_min_max.original_player_id: 
                        if r[1] > result[1] or (r[1] == result[1] and r[2] + 1 < result[2]) :
                            result = (action, r[1], r[2] + 1)
                    else:
                        if r[1] < result[1] or (r[1] == result[1] and r[2] + 1 > result[2]):
                            result = (action, r[1], r[2] + 1)
        to_go = result[2]
        sig = board.signature()
        if to_go > search_with_min_max.max_to_go or sig > search_with_min_max.max_sig :
            if sig > search_with_min_max.max_sig :
                search_with_min_max.max_sig = sig
            if to_go > search_with_min_max.max_to_go :
                search_with_min_max.max_to_go = to_go
            print(f'max to over = {search_with_min_max.max_to_go}, dp size = {len(dp)}, signature = {search_with_min_max.max_sig}')
            print(f"key {str(board)} and value {result}.")
            print()
            gc.collect()
        dp[board] = result
        return result

    r = _evaluate(board=board)
    return (r[0], r[1])


if __name__ == "__main__":
    board = Board2p(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
