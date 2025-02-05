<<<<<<< HEAD:Mancala/mancala/algorithm.py
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
=======
from typing import Dict

from board import Board


def search_with_min_max(player_id: int, board: Board) -> Dict[str, int]:
    dp = list()
    for id in range(board.NUM_OF_PLAYERS):
        dp.append(dict())
        
    original_player_id = player_id

    def _evaluate(player_id: int, board: Board) -> Dict[str, int]:
        value = dp[player_id].get(board)
        #print("dp size = {}, {}".format(len(dp[0]), len(dp[1])))
        #print("hash = " + str(hash(board)))
        #print(str(board) + f", {player_id}")
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/algorithm.py
        if value is not None:
            #value[1] += 1
            result += value
            return

        candidates = board.get_players_movable_grids(player_id=player_id)
        eval_tables = {}
        threads = []
        return_values = {}
        for action in candidates.keys():
            tmp_board = Board(board.NUM_OF_PLAYERS, \
                              board.init_pieces_per_grid, 
                              board.grids_per_player, \
                              board.grids_between_players,
                              board.data)
            act_again = tmp_board.move(action)
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == original_player_id:
                    result += [action, 1]
                else:
                    result += [action, -1]
                break

<<<<<<< HEAD:Mancala/mancala/algorithm.py
            if act_again :
                new_player_id = player_id 
            else:
                new_player_id = (player_id + 1) % board.NUMBER_OF_PLAYERS
                tmp_board.progress_turn()
            if tmp_board.next_player() != new_player_id :
                print('player id does not match.')
            try: 
                return_values[action] = []
                a_thread = threading.Thread(target=_evaluate, args=(new_player_id, tmp_board, return_values[action]) )
                threads.append(a_thread)
                a_thread.start()
            except Exception as e:
                print(f'Thread exception: {e}' )
                if a_thread in threads :
                    a_thread.stop()
                _evaluate(new_player_id, tmp_board, return_values[action])
        
        for a_thread in threads:
            a_thread.join()
        
        for key, val in return_values.items():
            eval_tables[key] = val
            
        if len(result) == 0 :
=======
            new_player_id = player_id if act_again else (player_id + 1) % board.NUM_OF_PLAYERS

            eval_tables[action] = _evaluate(player_id=new_player_id, board=tmp_board)["value"]

        if result is None:
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/algorithm.py
            if player_id == original_player_id:
                best_action = max(eval_tables, key=eval_tables.get)
            else:
                best_action = min(eval_tables, key=eval_tables.get)

            result += [best_action, eval_tables[best_action]]

<<<<<<< HEAD:Mancala/mancala/algorithm.py
        #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        #dp[board] = result
        board_signature = board.signature()
        if [1, 1, 1, 1, 1] < board_signature < [16, 1]:
            dp[board] = result
        if board_signature > search_with_min_max.max_signature :
            search_with_min_max.max_signature = max(board_signature, search_with_min_max.max_signature )
            print(f'max signature = {search_with_min_max.max_signature}, dp length = {len(dp)}.\n', end='')
            # lowrefkeys = [ key for key, value in dp.items() if value[1] <= 2]
            # for key in lowrefkeys:
            #     del dp[key]
            # gc.collect()
        return 
=======
        dp[player_id][board] = result
        return result
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/algorithm.py

    # return _evaluate(player_id=player_id, board=board)
    return_val = []
    _evaluate(player_id=player_id, board=board, result = return_val)
    return tuple(return_val)


if __name__ == "__main__":
    board = Board(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
