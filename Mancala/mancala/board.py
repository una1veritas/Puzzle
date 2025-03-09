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
        self.board = [
            [init_pieces_per_grid] * grids_per_player + [self.INITIAL_STONES_IN_SOTRE] * self.STORES_PER_PLAYER 
            ]* self.NUMBER_OF_PLAYERS
        self.player_in_turn = 0
    
    def __eq__(self, another):
        if not isinstance(another, type(self)) :
            return False
        if self.grids_per_player != another.grids_per_player :
            return False
        if self.pit_array(self.current_player()) + self.pit_array(self.next_turn_player()) \
        != another.pit_array(another.current_player()) + another.pit_array(another.next_turn_player()) :
            return False
        return True

    def __hash__(self):
        hash_codes = list()
        hash_codes.append(hash(tuple(self.pit_array(self.current_player()))))
        hash_codes.append(hash(tuple(self.pit_array(self.next_turn_player()))))
        return hash(tuple(hash_codes))
    
    def pit_array(self, player_id : int):
        return self.board[player_id][:self.grids_per_player]
    
    def store(self, player_id : int):
        return self.board[player_id][self.grids_per_player:]
    
    def current_player(self):
        return self.player_in_turn 
    
    def next_turn_player(self):
        return (self.player_in_turn + 1) % self.NUMBER_OF_PLAYERS
    
    def pit_number(self, player_id : int, pit_or_store_index : int):
        return player_id * (self.grids_per_player + self.STORES_PER_PLAYER) + pit_or_store_index 

    def pit_position(self, index : int):
        player_id = index // (self.grids_per_player + self.STORES_PER_PLAYER)
        pit_or_store_index = index % (self.grids_per_player + self.STORES_PER_PLAYER)
        return (player_id, pit_or_store_index) 
        
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.

        :params
        index: int: which grid to be moved

        :return
        whether you can move again or not.
        """
        if index < 0 or index >= len(self.pit_array(self.player_in_turn)) :
            raise ValueError(f"Invalid index: {index}. choice of move should be in from 0 to before {len(self.pit_array(self.player_in_turn))}")

        pieces = self.pit_array(self.player_in_turn)[index]

        if pieces == 0:
            print(self, index)
            raise ValueError(f"The pit of player {self.player_in_turn} index={index} has no pieces.")
        
        self.pit_array(self.player_in_turn)[index] = 0
        start_index = self.pit_number(self.player_in_turn, index)
        last_pos = self.pit_position(start_index)
        for i in range(start_index + 1, start_index + pieces + 1):
            last_pos = self.pit_position(i)
            self.board[last_pos[0]][last_pos[1]] += 1
            
        if last_pos[1] >= self.grids_per_player :
            return True
        else:
            return False 

    # def _add_index(self, index, diff):
    #     return (index + diff) % len(self.data)

    # def _is_grid_between_players(self, index: int):
    #     return index % (self.grids_per_player + self.STORES_PER_PLAYER) >= self.grids_per_player

    # def get_players_grids(self, player_id: int) -> Dict[int, int]:
    #     start_index = self.get_player_start_index(player_id=player_id)
    #     return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    # def get_player_start_index(self, player_id: int) -> int:
    #     return player_id * (self.grids_per_player + self.STORES_PER_PLAYER)

    # def get_players_movable_grids(self, player_id: int) -> Dict[int, int]:
    #     players_grids = self.get_players_grids(player_id=player_id)
    #     return {key: value for key, value in players_grids.items() if value > 0}

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.current_player()
        for ix in range(len(self.pit_array(player_id))) :
            if self.pit_array(player_id)[ix] > 0 :
                yield ix
    
    # def does_player_win(self, player_id: int) -> bool:
    #     movable_grids = self.get_players_movable_grids(player_id=player_id) 
    #     return len(movable_grids) == 0

    def won_by_player(self, player_id):
        #print(self.pit_array(player_id))
        return sum(self.pit_array(player_id)) == 0
    
    def signature(self):
        distribution = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_grid_index = i*(self.grids_per_player + self.STORES_PER_PLAYER)
            distribution += [ c for c in self.data[start_grid_index: start_grid_index + self.grids_per_player] if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        result = ''
        result += str(self.board[0][:self.grids_per_player])
        result += str(self.board[0][self.grids_per_player:])
        result += ', '
        result += str(self.board[1][:self.grids_per_player])
        result += str(self.board[1][self.grids_per_player:])
        return 'Board2p('+str(self.player_in_turn)+' ' + result+')'
    