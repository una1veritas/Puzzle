from typing import List, Optional, Type

from board import Board2p
from player import Player

import psutil
import os


class Game:
    def __init__(
        self,
        player_classes: List[Type[Player]],
        init_pieces_per_pit: int = 3,
        pits_per_player: int = 4,
        max_turns: int = 255,
    ):
        if not len(player_classes) > 1:
            raise ValueError("Players should be more than 2.")
        self.players = [player_class(player_id=i) for i, player_class in enumerate(player_classes)]
        self.initial_pieces = init_pieces_per_pit
        self.nuber_of_pits = pits_per_player
        self.max_turns = max_turns
        self.board = Board2p(
            init_pieces_per_pit=init_pieces_per_pit,
            pits_per_player=pits_per_player,
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
                ans = input("Shall we continue? (yes/no) ")
                if 'yes' in ans :
                    self.max_turns *= 2
                else:
                    print("Draw...")
                    return


if __name__ == "__main__":
    from player import Human, MinMaxPlayer, RandomPlayer
    import time
    from datetime import datetime
    
    print(datetime.now())
    swatch_start = time.time()
    game = Game(player_classes=[MinMaxPlayer, MinMaxPlayer], \
                pits_per_player = 6, \
                init_pieces_per_pit = 2, \
                )
    winner = game.run()
    swatch_stop = time.time()
    print(datetime.now())
    print(f"winner: {winner}")
    print(swatch_stop - swatch_start)
