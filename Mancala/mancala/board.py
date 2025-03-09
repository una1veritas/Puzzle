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
        self.board = list()
        for _ in range(self.NUMBER_OF_PLAYERS) :
            self.board.append([init_pieces_per_grid] * grids_per_player + 
                              [self.INITIAL_STONES_IN_SOTRE] * self.STORES_PER_PLAYER)
        self.player_in_turn = 0
    
    def __eq__(self, another):
        if not isinstance(another, type(self)) :
            return False
        if self.grids_per_player != another.grids_per_player :
            return False
        if self.board[self.current_player()][:self.grids_per_player] + self.board[self.next_turn_player()][:self.grids_per_player] \
        != another.board[another.current_player()][:another.grids_per_player] + another.board[another.next_turn_player()][:another.grids_per_player] :
            return False
        return True

    def __hash__(self):
        hash_codes = list()
        hash_codes.append(hash(tuple(self.board[self.current_player()][:self.grids_per_player])))
        hash_codes.append(hash(tuple(self.board[self.next_turn_player()][:self.grids_per_player])))
        return hash(tuple(hash_codes))
    
    def index_is_store(self, index : int):
        return self.grids_per_player <= index
    
    def current_player(self):
        return self.player_in_turn 
    
    def next_turn_player(self):
        return (self.player_in_turn + 1) % self.NUMBER_OF_PLAYERS
    
    def switch_turn(self):
        self.player_in_turn = self.next_turn_player()
        
    '''手を打つ．石を動かす．勝利の場合 True を返す．そうでない場合，必要ならターンを変えて False を返す．'''
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """
        
        if not ( 0 <= index < self.grids_per_player ) :
            raise ValueError(f"Invalid index: {index}. choice of move should be in from 0 to before {len(self.pit_array(self.player_in_turn))}")

        pieces = self.board[self.player_in_turn][index]
        if pieces == 0:
            print(self, index)
            raise ValueError(f"The pit of player {self.player_in_turn} index={index} has no pieces.")
        
        self.board[self.player_in_turn][index] = 0
        player = self.player_in_turn
        pit_index = index
        #print(self.board, player, pit_index)
        for _ in range(pieces,0,-1):
            '''となりの穴から'''
            pit_index += 1
            self.board[player][pit_index] += 1
            if pit_index == self.grids_per_player :
                pit_index = 0
                player = (player + 1) % self.NUMBER_OF_PLAYERS
            pieces -= 1
            #print(self.board, player, pit_index)
            
        if sum(self.board[self.player_in_turn][:self.grids_per_player]) == 0 :
            return True
        if not self.index_is_store(pit_index) :
                self.player_in_turn = (player + 1) % self.NUMBER_OF_PLAYERS
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
        for ix in range(self.grids_per_player) :
            if self.board[player_id][ix] > 0 :
                yield ix
    
    # def does_player_win(self, player_id: int) -> bool:
    #     movable_grids = self.get_players_movable_grids(player_id=player_id) 
    #     return len(movable_grids) == 0

    def game_won_by(self, player_id):
        #print(self.pit_array(player_id))
        return sum(self.board[player_id][:self.grids_per_player]) == 0
    
    def signature(self):
        distribution = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            distribution += [ c for c in self.board[i][:self.grids_per_player] if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        pit_strs = list()
        for plid in range(self.NUMBER_OF_PLAYERS) :
            result = '[' 
            result += ', '.join([str(i) for i in self.board[plid][:self.grids_per_player]])
            result += '; ' + str(self.board[plid][self.grids_per_player])
            result += ']'
            pit_strs.append(result)
        return 'Board2p('+str(self.player_in_turn)+', ' + ','.join(pit_strs)+')'
    