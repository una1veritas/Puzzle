from copy import deepcopy
from typing import Dict, Tuple, List, Any
import gc, json

from board import Board2players
import pickle

def search_with_min_max(player_id: int, board: Board2players, dp : dict) -> Tuple[int, int]:
    if dp == None :
        dp = {}
    search_with_min_max.original_player_id = player_id
    search_with_min_max.max_to_over = 0

    '''Returns a pair (action, value) where action is the choice as a move, and value is its evaluation '''
    def _evaluate(player_id: int, board: Board2players) -> Tuple[int, int]:
        result = dp.get((board, player_id)) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if result is not None:
            #print(result)
            return result
        
        candidates = [i for i in board.possible_moves(player_id)]
        for action in candidates:
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            
            if tmp_board.does_player_win(player_id=player_id) :
                if player_id == search_with_min_max.original_player_id :
                    result = (action, 1)
                else:
                    result = (action, -1)
                break
            else:
                next_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS
                if result == None :
                    result = _evaluate(next_player_id, tmp_board)
                else:
                    r = _evaluate(next_player_id, tmp_board)
                    if player_id == search_with_min_max.original_player_id: 
                        if r[1] > result[1] :
                            result = r
                    else:
                        if r[1] < result[1] :
                            result = r
        if board.data[result[0]] == 0 :
            print(board, result)
            for k, v in dp.items():
                print(str(k[0]),str(k[1]),v)
            raise ValueError('empty pit chosen.')
        to_go = result[1]
        if to_go > search_with_min_max.max_to_over :
            search_with_min_max.max_to_over = to_go
            print('max to over = ', search_with_min_max.max_to_over, ' dp length = ', len(dp))
            print(f"adding key {str(board)}, {player_id} and value {result}.")
            # with open('hint_dp.pkl', mode = 'wb') as file:
            #     pickle.dump(dp, file)
            # with open('dp_dict.json', mode='w') as file:
            #     json.dump(dp, file)
            #gc.collect()
        if to_go > 0 :
            dp[(board, player_id)] = result
        # #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        return result

    return _evaluate(player_id=player_id, board=board)


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
