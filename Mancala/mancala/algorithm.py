from copy import deepcopy
from typing import Dict, Tuple

from board import Board2players
import gc

def search_with_min_max(player_id: int, board: Board2players) -> Tuple[str, int]:
    dp = {}
    ''' key : (Board2players, player_id (int) ), value: [(action(str), minmax(int)), reffered(int)] '''
    original_player_id = player_id
    search_with_min_max.max_signature = [0] #関数内の静的変数の宣言と初期化

    def _evaluate(player_id: int, board: Board2players) -> Tuple[str, int]:
        value = dp.get((board, player_id), None) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if value is not None:
            value[1] += 1
            return value[0]

        candidates = board.get_players_movable_grids(player_id=player_id)
        eval_tables = {}
        result = None
        for action in candidates.keys():
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == original_player_id:
                    result : Tuple[str, int] = (action, 1)
                else:
                    result : Tuple[str, int] = (action, -1)
                break

            new_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS

            eval_tables[action] = _evaluate(player_id=new_player_id, board=tmp_board)[1]

        if result is None:
            if player_id == original_player_id:
                best_action = max(eval_tables, key=eval_tables.get)
            else:
                best_action = min(eval_tables, key=eval_tables.get)

            result : Tuple[str, int] = (best_action, eval_tables[best_action])

        #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        board_signature = board.signature()
        if board_signature < [12]:
            dp[(board, player_id)] = [result, 1]
        if board_signature > search_with_min_max.max_signature :
            search_with_min_max.max_signature = board_signature
            print('max signature = ', search_with_min_max.max_signature, ' dp length = ', len(dp))
            lowrefkeys = [ key for key, value in dp.items() if value[1] <= 2]
            for key in lowrefkeys:
                del dp[key]
            gc.collect()
        return result

    return _evaluate(player_id=player_id, board=board)


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
