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
        if value is not None:
            return value

        candidates = board.get_players_movable_grids(player_id=player_id)
        eval_tables = {}
        result = None
        for action in candidates.keys():
            tmp_board = Board(board.NUM_OF_PLAYERS, \
                              board.init_pieces_per_grid, 
                              board.grids_per_player, \
                              board.grids_between_players,
                              board.data)
            act_again = tmp_board.move(action)
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == original_player_id:
                    result = {"action": action, "value": 1}
                else:
                    result = {"action": action, "value": -1}
                break

            new_player_id = player_id if act_again else (player_id + 1) % board.NUM_OF_PLAYERS

            eval_tables[action] = _evaluate(player_id=new_player_id, board=tmp_board)["value"]

        if result is None:
            if player_id == original_player_id:
                best_action = max(eval_tables, key=eval_tables.get)
            else:
                best_action = min(eval_tables, key=eval_tables.get)

            result = {"action": best_action, "value": eval_tables[best_action]}

        dp[player_id][board] = result
        return result

    return _evaluate(player_id=player_id, board=board)


if __name__ == "__main__":
    board = Board(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
