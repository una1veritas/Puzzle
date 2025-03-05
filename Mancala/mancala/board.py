from typing import Dict
from numpy import ix_
from pickle import TRUE

class Board2p:
    INITIAL_STONES_IN_SOTRE = 0
    NUMBER_OF_PLAYERS: int = 2
    STORES_PER_PLAYER : int = 1

    def __init__(
        self,
        init_pieces_per_grid : int = 3,
        grids_per_player : int = 3
    ):
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
        self.data = (
            [init_pieces_per_grid] * grids_per_player
            + [self.INITIAL_STONES_IN_SOTRE] * self.STORES_PER_PLAYER
        ) * self.NUMBER_OF_PLAYERS
        self.next_move_player_id = 0
    
    def __eq__(self, another):
        if not isinstance(another, type(self)) :
            return False
        if self.grids_per_player != another.grids_per_player :
            return False
        if self.players_pit_array(self.next_move_player()) + self.players_pit_array(self.previous_move_player()) \
        != another.players_pit_array(another.next_move_player()) + another.players_pit_array(another.previous_move_player()) :
            return False
        return True

    def __hash__(self):
        hash_codes = list()
        hash_codes.append(hash(tuple(self.players_pit_array(self.next_move_player()))))
        hash_codes.append(hash(tuple(self.players_pit_array(self.previous_move_player()))))
        return hash(tuple(hash_codes))
    
    def players_pit_array(self, player_id : int):
        start_ix = self.get_player_start_index(player_id)
        return self.data[start_ix : start_ix + self.grids_per_player]
    
    def next_move_player(self):
        return self.next_move_player_id 
    
    def previous_move_player(self):
        return (self.next_move_player_id + 1) % self.NUMBER_OF_PLAYERS
    
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.

        :params
        index: int: which grid to be moved

        :return
        whether you can move again or not.
        """
        if index < self.get_player_start_index(self.next_move_player_id) \
        or index >= self.get_player_start_index(self.next_move_player_id) + self.grids_per_player :
            raise ValueError(f"Invalid index: {index}. index should satisfy index < {len(self.data)}")
        if self._is_grid_between_players(index):
            raise ValueError(f"Invalid index: {index}. The index points grids between players.")

        pieces = self.data[index]

        if pieces == 0:
            print(self, index)
            raise ValueError(f"The grid with index={index} has no pieces.")
        
        self.data[index] = 0
        last_placed = index
        for i in range(1, pieces + 1):
            last_placed = (index + i) % len(self.data)
            self.data[last_placed] += 1
            
        if self._is_grid_between_players(last_placed) :
            return True
        else:
            self.next_move_player_id += 1
            self.next_move_player_id %= self.NUMBER_OF_PLAYERS
            return False 

    def _add_index(self, index, diff):
        return (index + diff) % len(self.data)

    def _is_grid_between_players(self, index: int):
        return index % (self.grids_per_player + self.STORES_PER_PLAYER) >= self.grids_per_player

    # def get_players_grids(self, player_id: int) -> Dict[int, int]:
    #     start_index = self.get_player_start_index(player_id=player_id)
    #     return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_player_start_index(self, player_id: int) -> int:
        return player_id * (self.grids_per_player + self.STORES_PER_PLAYER)

    # def get_players_movable_grids(self, player_id: int) -> Dict[int, int]:
    #     players_grids = self.get_players_grids(player_id=player_id)
    #     return {key: value for key, value in players_grids.items() if value > 0}

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.next_move_player()
        start_ix = self.get_player_start_index(player_id)
        end_ix = start_ix + self.grids_per_player
        for ix in range(start_ix, end_ix) :
            if self.data[ix] > 0 :
                yield ix
    
    # def does_player_win(self, player_id: int) -> bool:
    #     movable_grids = self.get_players_movable_grids(player_id=player_id) 
    #     return len(movable_grids) == 0

    def won_by_player(self, player_id):
        return sum(self.players_pit_array(player_id)) == 0
    
    def signature(self):
        distribution = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_grid_index = i*(self.grids_per_player + self.STORES_PER_PLAYER)
            distribution += [ c for c in self.data[start_grid_index: start_grid_index + self.grids_per_player] if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        result = ''
        result += str(self.data[: self.grids_per_player])
        result += str(self.data[self.grids_per_player: self.grids_per_player + self.STORES_PER_PLAYER])
        result += ', '
        result += str(self.data[self.grids_per_player + self.STORES_PER_PLAYER: self.grids_per_player + self.STORES_PER_PLAYER + self.grids_per_player])
        result += str(self.data[self.grids_per_player + self.STORES_PER_PLAYER + self.grids_per_player : ])
        return 'Board2p('+str(self.next_move_player_id)+' ' + result+')'
    