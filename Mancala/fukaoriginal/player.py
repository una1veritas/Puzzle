import random
from abc import ABCMeta, abstractmethod
from typing import Dict, List

from algorithm import search_with_min_max
from board import Board


class Player(metaclass=ABCMeta):
    def __init__(self, player_id: int):
        self.player_id = player_id

    @abstractmethod
    def act(self, board: Board) -> int:
        pass


class RandomPlayer(Player):
    """Choose grid randomly."""

    def act(self, board: Board) -> int:
        candidates: List = list(board.get_players_movable_grids(player_id=self.player_id).keys())
        return random.choice(candidates)


class Human(Player):
    """Grid is chosen by human interactively."""

    def act(self, board: Board) -> int:
        candidates: Dict = board.get_players_movable_grids(player_id=self.player_id)
        while True:
            board.print_board()
            raw_input = input(f"You can choose from {candidates}: ")
            try:
                result = int(raw_input)
            except ValueError:
                print(f"Invalid input {raw_input}. Input should be Integer.")
                continue
            if result not in candidates:
                print(f"Invalid input {result}. Input should be from {list(candidates.keys())}.")
                continue
            return result


class MinMaxPlayer(Player):
    """Choose grid based on min-max algorithm."""

    def act(self, board: Board) -> int:
        if board.players_num > 2:
            raise Exception("When players are more than 3, Min max algorithm takes a lot of time to run.")
        result: Dict[str, int] = search_with_min_max(player_id=self.player_id, board=board)
        print(f"Evaluation: {result['value']}")
        return result["action"]
