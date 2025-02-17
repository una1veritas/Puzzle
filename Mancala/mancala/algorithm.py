from copy import deepcopy
from typing import Dict, Tuple, List, Any
import gc, json

from board import Board2players
import pickle

def search_with_min_max(player_id: int, board: Board2players, dp : dict) -> Tuple[int, int]:
    if dp == None :
        search_with_min_max.dp = {}
    search_with_min_max.original_player_id = player_id
    search_with_min_max.max_to_go = 0
    search_with_min_max.max_sig = []
    

    '''Returns a pair (action, value) where action is the choice as a move, and value is its evaluation '''
    def _evaluate(player_id: int, board: Board2players) -> Tuple[int, int, int]:
        result = dp.get((board, player_id)) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if result is not None:
            #print(result)
            return result
        candidates = [i for i in board.possible_moves(player_id)]
        #print(board, player_id, candidates)
        for action in candidates:
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            
            if tmp_board.does_player_win(player_id=player_id) :
                if player_id == search_with_min_max.original_player_id :
                    result = (action, 1, 0)
                    #print('original')
                else:
                    result = (action, 0, 0)
                    #print('opponent')
                break
            else:
                next_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS
                r = _evaluate(next_player_id, tmp_board)
                if result == None :
                    result = (action, r[1], r[2] + 1) # action の move をした結果数手先でおきた結果
                else:
                    if player_id == search_with_min_max.original_player_id: 
                        if r[1] > result[1] or (r[1] == result[1] and r[2] + 1 < result[2]) :
                            result = (action, r[1], r[2] + 1)
                        #if result[2] == 1 : break
                    else:
                        if r[1] < result[1] or (r[1] == result[1] and r[2] + 1 < result[2]):
                            result = (action, r[1], r[2] + 1)
                        #if result[2] == 0 : break
        # if board.data[result[0]] == 0 :
        #     for k, v in dp.items():
        #         print("dict: ", str(k[0]),str(k[1]),v)
        #     raise ValueError('empty pit chosen.')
        
        to_go = result[2]
        sig = board.signature()
        if to_go > search_with_min_max.max_to_go or sig > search_with_min_max.max_sig :
            if sig > search_with_min_max.max_sig :
                search_with_min_max.max_sig = sig
            if to_go > search_with_min_max.max_to_go :
                search_with_min_max.max_to_go = to_go
            print(f'max to over = {search_with_min_max.max_to_go}, dp size = {len(dp)}, signature = {search_with_min_max.max_sig}')
            print(f"key {str(board)}, {player_id} and value {result}.")
            # with open('hint_dp.pkl', mode = 'wb') as file:
            #     pickle.dump(dp, file)
            # with open('dp_dict.json', mode='w') as file:
            #     json.dump(dp, file)
            gc.collect()
        if to_go >= 5 :
            dp[(board, player_id)] = result
        # #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        return result

    r = _evaluate(player_id=player_id, board=board)
    return (r[0], r[1])


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
