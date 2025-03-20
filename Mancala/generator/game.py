'''
Created on 2025/02/11

@author: sin
'''

from typing import List, Optional, Type
from player import Player

class Game:
    def __init__(
        self,
        player_classes: List[Type[Player]],
        init_pieces_in_pit: int = 3,
        grids_per_player: int = 4,
        grids_between_players: int = 1,
        max_turns: int = 100,
    ):
        if not len(player_classes) > 1:
            raise ValueError("Players should be more than 2.")
        players = [player_class(player_id=i) for i, player_class in enumerate(player_classes)]
        players_num = len(players)
        self.players_num = players_num
        self.initial_pieces = init_pieces_in_pit
        self.nuber_of_pits = grids_per_player
        self.grids_between_players = grids_between_players
        self.max_turns = max_turns
        self.board = Board2p(
            init_pieces_in_pit=init_pieces_in_pit,
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
                    index = player.act(self.board) if not isinstance(player, MinMaxPlayer) else player.act(self.board, hint_dp)
                    print(f"Action {index}")
                    mem_usa = get_memory_usage()
                    print(f'memory usage {mem_usa/10245/1024:.2f}Mb.')
                    if index == -1 :
                        break
                    act_again = self.board.move(index=index)
                    if not act_again:
                        break

                if self.board.does_player_win(player.player_id):
                    print(f"Player {player.player_id} wins!")
                    print(self.board)
                    return player.player_id
                print()
            turn_n += 1
            if turn_n >= self.max_turns:
                print("Draw...")
                return
