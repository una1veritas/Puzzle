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
        self.players = [player_class(player_id=i) for i, player_class in enumerate(player_classes)]
        self.initial_pieces = init_pieces_per_grid
        self.nuber_of_pits = grids_per_player
        self.grids_between_players = grids_between_players
        self.max_turns = max_turns
        self.board = Board2p(
            init_pieces_per_grid=init_pieces_per_grid,
            grids_per_player=grids_per_player,
        )
    
    def number_of_players(self):
        return len(self.players)
    
    def run(self) -> Optional[int]:
        hint_dp = dict()
        turn_n = 1
        while True:
            print(f"Turn {turn_n}")
            print(f"Player {self.board.current_player()}")
            current_player_id = self.board.current_player()
            while self.board.current_player() == current_player_id :
                print(self.board)
                player = self.players[current_player_id]
                index = player.act(self.board) if not isinstance(player, MinMaxPlayer) else player.act(self.board, hint_dp)
                #print(f"Took action {index}")
                mem_usa = get_memory_usage()
                #print(f'memory usage {mem_usa/10245/1024:.2f}Mb.')
                # if index == -1 :
                #     break
                #print("before move", self.board)                
                game_finished = self.board.move(index=index)
                #print("after move", self.board)
                if game_finished:
                    break
                print()
            if game_finished :
                print()
                print(f"Player {self.board.current_player()} wins!")
                print(self.board)
                print()
                return self.board.current_player()
            
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
                grids_per_player=6
                )
    winner = game.run()
    swatch_stop = time.time()
    print(datetime.now())
    print(f"winner: {winner}")
    print(swatch_stop - swatch_start)
