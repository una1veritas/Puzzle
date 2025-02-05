from copy import deepcopy
from typing import Dict

<<<<<<< HEAD:Mancala/mancala/board.py
class Board2players:
    INITIAL_STONES_IN_SOTRE = 0
    NUMBER_OF_PLAYERS: int = 2
    STORES_PER_PLAYER : int = 1
    
=======
INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS = 0


class Board2:
    NUM_OF_PLAYERS: int = 2
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/board.py
    def __init__(
        self,
        init_pieces_per_grid: int = 3,
        grids_per_player: int = 3,
        grids_between_players: int = 1,
        data : list = None
    ):
        self.NUM_OF_PLAYERS = players_num
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
<<<<<<< HEAD:Mancala/mancala/board.py
        self.data = (
            [init_pieces_per_grid] * grids_per_player
            + [self.INITIAL_STONES_IN_SOTRE] * self.STORES_PER_PLAYER
        ) * self.NUMBER_OF_PLAYERS
        self.next_player_id = 0
    
    def __eq__(self, another):
        if not isinstance(another, type(self)) :
            return False
        if self.next_player_id != another.next_player_id :
            return False
        if self.init_pieces_per_grid == another.init_pieces_per_grid \
        and self.grids_per_player == another.grids_per_player :
            for i in range(self.NUMBER_OF_PLAYERS) :
                start_pit = self.get_player_start_index(i)
                for x in range(start_pit, start_pit + self.grids_per_player) :
                    if self.data[x] != another.data[x] :
                        return False
            return True
        return False

    def __hash__(self):
        hashes = [self.next_player_id]
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_pit = self.get_player_start_index(i)
            hashes.append(hash(tuple(self.data[start_pit: start_pit + self.grids_per_player]))) 
        return hash(tuple(hashes))

    def signature(self):
        nums = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_pit = self.get_player_start_index(i)
            nums += self.data[start_pit: start_pit + self.grids_per_player]
        return sorted(nums,reverse=True)[:self.grids_per_player]
    
    def next_player(self):
        return self.next_player_id
    
    def progress_turn(self):
        self.next_player_id = (self.next_player_id + 1) % self.NUMBER_OF_PLAYERS
=======
        self.grids_between_players = grids_between_players
        if data is None :
            self.data = (
                [init_pieces_per_grid] * grids_per_player
                + [INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS] * grids_between_players
            ) * players_num
        else:
            self.data = [i for i in data]
    
#    def __str__(self):
#        return "|".join([str(i) for i in self.data])
    
    def __eq__(self, other):
        return self.NUM_OF_PLAYERS == other.NUM_OF_PLAYERS and \
        self.grids_per_player == other.grids_per_player and \
        self.grids_between_players == other.grids_between_players and \
        self.data == other.data
        
    def __hash__(self):
        mask64 = (1<<64) - 1
        val = 0
        for ix in range(self.NUM_OF_PLAYERS):
            ms5bits = (val >> (64 - 5)) & 0x1f
            val <<= 5 
            val += self.data[ix]
            val ^= ms5bits
            val &= mask64
        return val
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/board.py
        
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.

        :params
        index: int: which grid to be moved

        :return
        whether you can move again or not.
        """
        if index >= len(self.data):
            raise ValueError(f"Invalid index: {index}. index should satisfy index < {len(self.data)}")
        if self._is_grid_between_players(index):
            raise ValueError(f"Invalid index: {index}. The index points grids between players.")

        pieces = self.data[index]

        if pieces == 0:
            raise ValueError(f"The grid with index={index} has no pieces.")

        for i in range(1, pieces + 1):
            index_to_be_incremented = self._add_index(index, i)
            self.data[index_to_be_incremented] += 1

        self.data[index] = 0

        return self._is_grid_between_players(self._add_index(index, pieces))

    def _add_index(self, index, diff):
        return (index + diff) % len(self.data)

    def _is_grid_between_players(self, index: int):
        return index % (self.grids_per_player + self.grids_between_players) >= self.grids_per_player

    def get_players_grids(self, player_id: int) -> Dict[int, int]:
        start_index = self.get_player_start_index(player_id=player_id)
        return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_grids(self) -> Dict[int, int]:
        start_index = self.get_start_index()
        return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_player_start_index(self, player_id: int) -> int:
        return player_id * (self.grids_per_player + self.grids_between_players)

    def get_start_index(self) -> int:
        return self.next_player_id * (self.grids_per_player + self.STORES_PER_PLAYER)

    def get_players_movable_grids(self, player_id: int) -> Dict[int, int]:
        players_grids = self.get_players_grids(player_id=player_id)
        return {key: value for key, value in players_grids.items() if value > 0}

    def get_movable_grids(self) -> Dict[int, int]:
        players_grids = self.get_players_grids(player_id=self.next_player_id)
        return {key: value for key, value in players_grids.items() if value > 0}

    def does_player_win(self, player_id: int) -> bool:
        movable_grids = self.get_players_movable_grids(player_id=player_id)
        return len(movable_grids) == 0

    def does_next_player_win(self) -> bool:
        movable_grids = self.get_players_movable_grids(player_id=self.next_player_id)
        return len(movable_grids) == 0

    def __str__(self):
<<<<<<< HEAD:Mancala/mancala/board.py
        strlist = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            result = '*' if i == self.next_player_id else ' '
            result += '['
            start_pit = self.get_player_start_index(0)
            result += ', '.join([ str(i) for i in self.data[start_pit : start_pit + self.grids_per_player]]) + '; '
            result += ','.join([str(i) for i in self.data[start_pit + self.grids_per_player : \
                                         start_pit + self.grids_per_player + self.STORES_PER_PLAYER]])
            result += ']'
            strlist.append(result)
        return '('+', '.join(strlist)+')'
    
=======
        val = ''
        for i in range(self.NUM_OF_PLAYERS):
            player_start_grid = self.get_player_start_index(i)
            player_last_grid = player_start_grid + self.grids_per_player
            val += str(self.data[player_start_grid : player_last_grid])
            val += str(self.data[player_last_grid : player_last_grid + self.grids_between_players])
        return val
>>>>>>> parent of dc87796 (snap shot):Mancala/fuka/board.py
