from typing import Dict
from numpy import ix_
from pickle import TRUE, FALSE

class Board2p:
    INITIAL_STONES_IN_STORE : int = 0
    NUMBER_OF_PLAYERS : int = 2
    STORES_PER_PLAYER : int = 1

    def __init__(
        self,
        init_pieces_per_grid : int = 3,
        grids_per_player : int = 3
    ):
        self.initial_pieces = init_pieces_per_grid
        self.num_of_pits = grids_per_player
        self.board = tuple(([init_pieces_per_grid] * self.num_of_pits + 
                            [self.INITIAL_STONES_IN_STORE] * self.STORES_PER_PLAYER)* self.NUMBER_OF_PLAYERS)
        self.player_in_turn = 0
    
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        if self.num_of_pits != other.num_of_pits :
            return False
        if self._pits_of_current() + self._pits_of_next() != other._pits_of_current() + other._pits_of_next() :
            return False
        return True

    def __hash__(self):
        hash_codes = list()
        hash_codes.append(hash(tuple(self._pits_of_current())))
        hash_codes.append(hash(tuple(self._pits_of_next())))
        return hash(tuple(hash_codes))
    
    '''the index of the first pit of player'''
    def start_index(self, player_id : int) -> int:
        return (player_id % self.NUMBER_OF_PLAYERS) * (self.num_of_pits + self.STORES_PER_PLAYER)
    
    '''the index of the last store of player'''    
    def end_index(self, player_id : int) -> int:
        return (player_id % self.NUMBER_OF_PLAYERS) * (self.num_of_pits + self.STORES_PER_PLAYER) + (self.num_of_pits + self.STORES_PER_PLAYER)
    
    def _pits_of(self, player_id : int) -> list:
        return self.board[self.start_index(player_id) : self.start_index(player_id) + self.num_of_pits]

    def _stores_of(self, player_id : int) -> list:
        return self.board[self.start_index(player_id) + self.num_of_pits : self.end_index(player_id)]

    def _pits_of_current(self) -> list:
        return self.board[self.current_player()][:self.num_of_pits]
    
    def _pits_of_next(self) -> list:
        return self.board[self.next_turn_player()][:self.num_of_pits]
    
    def current_player(self):
        return self.player_in_turn 
    
    def next_turn_player(self):
        return (self.player_in_turn + 1) % self.NUMBER_OF_PLAYERS
    
    def switch_turn(self):
        self.player_in_turn = self.next_turn_player()
    
        '''手を打つ．石を動かさず、勝利の場合 True を返し．そうでない場合 False を返す．エラーチェックしない．'''
    def winning_move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """

        remain = (self.num_of_pits + self.STORES_PER_PLAYER) - (index % (self.num_of_pits + self.STORES_PER_PLAYER))
        if remain > self.STORES_PER_PLAYER:
            return False        
        pieces = self.board[self.player_in_turn][index]
        if pieces == 0 :
            return False
        if pieces - self.STORES_PER_PLAYER > self.num_of_pits + self.STORES_PER_PLAYER :
            return False
        return sum(self._pits_of_current()) == pieces
        
    '''手を打つ．石を動かす．勝利の場合 True を返す．そうでない場合，必要ならターンを変えて False を返す．'''
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """
        
        if not ( 0 <= index < self.num_of_pits ) :
            raise ValueError(f"Invalid index: {index}. choice of move should be in from 0 to before {len(self.pit_array(self.player_in_turn))}")

        pieces = self.board[self.player_in_turn][index]
        if pieces == 0:
            print(self, index)
            raise ValueError(f"The pit of player {self.player_in_turn} index={index} has no pieces.")
        new_board = list(self.board)
        position = [self.player_in_turn, index]
        new_board[position[0]][position[1]] = 0
        '''となりの穴から'''
        for _ in range(0, pieces):
            pit_index += 1
            if pit_index >= self.num_of_pits + self.STORES_PER_PLAYER :
                player = (player + 1) % self.NUMBER_OF_PLAYERS
                pit_index %= self.num_of_pits + self.STORES_PER_PLAYER
            self.board[player][pit_index] += 1
        
        #print(self.board, pit_index, self.num_of_pits)
        
        if sum(self._pits_of(self.player_in_turn)) == 0 :
            return True
        if pit_index < self.num_of_pits :
            self.switch_turn()
        return False

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.current_player()
        for ix in range(self.num_of_pits) :
            if self.board[player_id][ix] > 0 :
                yield ix

    def game_won_by(self, player_id):
        #print(self.pit_array(player_id))
        return sum(self._pits_of(player_id)) == 0
    
    def signature(self):
        distribution = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            distribution += [ c for c in self._pits_of(i) if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        print(self.board)
        pit_strs = list()
        for player_id in range(self.NUMBER_OF_PLAYERS) :
            t = '[' 
            t += ', '.join([str(i) for i in self._pits_of(player_id)])
            t += '; ' + ', '.join([str(i) for i in self._stores_of(plid)])
            t += ']'
            pit_strs.append(t)
        return 'Board2p('+str(self.player_in_turn)+', ' + ','.join(pit_strs)+')'
    