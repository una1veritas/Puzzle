from copy import deepcopy
from typing import Dict, Tuple

import gc
from board import Board2players
import threading

def search_with_min_max(player_id: int, board: Board2players) -> Tuple[str, int]:
    dp = {}
    ''' key : (Board2players, player_id (int) ), value: [(action(str), minmax(int)), reffered(int)] '''
    original_player_id = player_id
    search_with_min_max.max_signature = [0] #関数内の静的変数の宣言と初期化
    
    def _evaluate(player_id : int, board : Board2players, result : list) -> None:
        result.clear()
        board.next_player_id = player_id
        value = dp.get(board, None) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if value is not None:
            #value[1] += 1
            result += value
            return

        candidates = board.get_players_movable_grids(player_id=player_id)
        eval_tables = {}
        threads = []
        return_values = {}
        for action in candidates.keys():
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == original_player_id:
                    result += [action, 1]
                else:
                    result += [action, -1]
                break

            new_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS
            if not act_again : tmp_board.progress_turn()
            #result_pair = []
            #_evaluate(new_player_id, tmp_board, result_pair)
            return_values[action] = []
            a_thread = threading.Thread(target=_evaluate, args=(new_player_id, tmp_board, return_values[action]) )
            threads.append(a_thread)
            a_thread.start()
            # eval_tables[action] = result_pair[0]
        
        for a_thread in threads:
            a_thread.join()
        
        for key, val in return_values.items():
            eval_tables[key] = val[0]
            
        if len(result) == 0 :
            if player_id == original_player_id:
                best_action = max(eval_tables, key=eval_tables.get)
            else:
                best_action = min(eval_tables, key=eval_tables.get)

            result += [best_action, eval_tables[best_action]]

        #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        #dp[board] = result
        board_signature = board.signature()
        if board_signature < [15]:
            dp[(board, player_id)] = result
        if board_signature > search_with_min_max.max_signature :
            search_with_min_max.max_signature = board_signature
            print(f'max signature = {search_with_min_max.max_signature}, dp length = {len(dp)}.\n', end='')
            lowrefkeys = [ key for key, value in dp.items() if value[1] <= 1]
            for key in lowrefkeys:
                del dp[key]
            gc.collect()
        return 

    # return _evaluate(player_id=player_id, board=board)
    return_val = []
    _evaluate(player_id=player_id, board=board, result = return_val)
    return tuple(return_val)


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
