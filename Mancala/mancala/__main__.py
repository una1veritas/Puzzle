from typing import List, Optional, Type

from board import Board2p
from player import Player

import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss  # in bytes


class Game:
    def __init__(
        self,
        player_classes: List[Type[Player]],
        init_pieces_per_grid: int = 3,
        grids_per_player: int = 4,
        grids_between_players: int = 1,
        max_turns: int = 100,
    ):
        if not len(player_classes) > 1:
            raise ValueError("Players should be more than 2.")
        players = [player_class(player_id=i) for i, player_class in enumerate(player_classes)]
        players_num = len(players)
        self.players_num = players_num
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
        self.grids_between_players = grids_between_players
        self.max_turns = max_turns
        self.board = Board2p(
            init_pieces_per_grid=init_pieces_per_grid,
            grids_per_player=grids_per_player,
        )
        self.players = players

    def run(self) -> Optional[int]:
        hint_dp = dict()
        turn_n = 1
        while True:
            print(f"Turn {turn_n}")
            for player in self.players:
                print(self.board)
                print(f"Player {player.player_id}")
                while True:
                    if self.board.game_won_by(player.player_id):
                        print(f"Player {player.player_id} wins!")
                        print(self.board)
                        return player.player_id
                    
                    index = player.act(self.board) if not isinstance(player, MinMaxPlayer) else player.act(self.board, hint_dp)
                    print(f"Action {index}")
                    mem_usa = get_memory_usage()
                    print(f'memory usage {mem_usa/10245/1024:.2f}Mb.')
                    if index == -1 :
                        break
                    game_finished = self.board.move(index=index)
                    if game_finished:
                        break

                if game_finished :
                    # for key, val in hint_dp.items():
                    #     print(key, val)
                    print(f"Player {self.board.current_player()} wins!")
                    print(self.board)
                    return self.board.current_player()
                print()
            turn_n += 1
            if turn_n >= self.max_turns:
                print("Draw...")
                return


if __name__ == "__main__":
    from player import Human, MinMaxPlayer, RandomPlayer
    import time
    from datetime import datetime
    
    print(datetime.now())
    swatch_start = time.time()
    game = Game(player_classes=[MinMaxPlayer, MinMaxPlayer], \
                init_pieces_per_grid=2, \
                grids_per_player=3
                )
    winner = game.run()
    swatch_stop = time.time()
    print(datetime.now())
    print(f"winner: {winner}")
    print(swatch_stop - swatch_start)
