from copy import deepcopy
from typing import Dict, Tuple, List, Any
import gc, json

from board import Board2players
import pickle

def search_with_min_max(player_id: int, board: Board2players, dp : dict) -> Tuple[int, int]:
    if dp == None :
        dp = {}
    search_with_min_max.original_player_id = player_id
    search_with_min_max.max_signature = [0]

    '''Returns a pair (action, value) where action is the choice as a move, and value is its evaluation '''
    def _evaluate(player_id: int, board: Board2players) -> Tuple[int, int]:
        result = dp.get((board, player_id)) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if result is not None:
            #print(result)
            return result
        candidates = list(board.get_players_movable_grids(player_id=player_id).keys())
        #print('_evaluate', player_id, board, candidates)            
        eval_table = dict()
        if len(candidates) == 0:
            '''no pieces in player_id's grids'''
            eval_table[-1] = 1 if player_id == search_with_min_max.original_player_id else -1
        #result = None
        for action in candidates:
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == search_with_min_max.original_player_id:
                    eval_table[action] = 1
                else:
                    eval_table[action] = -1
                break
            else:
                next_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS
                r = _evaluate(next_player_id, tmp_board)[1]
                eval_table[action] = r + 1 if r > 0 else r - 1
        
        if len(eval_table) == 0 :
            print(board, eval_table, player_id, search_with_min_max.original_player_id)
        if player_id == search_with_min_max.original_player_id:
            best_action = max(eval_table, key=eval_table.get)
        else:
            best_action = min(eval_table, key=eval_table.get)
        result = ( best_action, eval_table[best_action])
        
        sig = board.signature()
        if sig > search_with_min_max.max_signature :
            search_with_min_max.max_signature = sig
            print('signature = ', search_with_min_max.max_signature, ' dp length = ', len(dp))
            gc.collect()
            with open('hint_dp.pkl', mode = 'wb') as file:
                pickle.dump(dp, file)
            # with open('dp_dict.json', mode='w') as file:
            #     json.dump(dp, file)
        #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        if sum(sig) <= 19 :
            dp[(board, player_id)] = result
        return result

    return _evaluate(player_id=player_id, board=board)


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
