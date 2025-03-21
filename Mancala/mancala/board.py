
class Board2p:
    NUMBER_OF_PLAYERS : int = 2

    def __init__(
        self,
        pits_per_player : int = 3,
        init_pieces_per_pit : int = 3,
    ):
        self.num_of_pits = pits_per_player
        self.board = ([init_pieces_per_pit] * self.num_of_pits + [0]) * self.NUMBER_OF_PLAYERS
        self.player_in_turn = 0
    
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        if self.num_of_pits != other.num_of_pits :
            return False
        if self.current_player() != other.current_player() :
            return False
        if self.pits_of_player(self.current_player()) != other.pits_of_player(other.current_player()) :
            return False
        if self.pits_of_player(self.next_player()) != other.pits_of_player(other.next_player()) :
            return False
        return True

    def __hash__(self):
        hash_elems = [self.player_in_turn]
        hash_elems.append(hash(self.pits_of_player(self.current_player())))
        hash_elems.append(hash(self.pits_of_player(self.next_player())))
        return hash(tuple(hash_elems))
    
    '''the index of the first pit of player'''
    def _row_begin(self, player_id : int) -> int:
        return (player_id  % self.NUMBER_OF_PLAYERS) * (self.num_of_pits + 1)
    
    '''the index of the last store of player'''    
    def _row_end(self, player_id : int) -> int:
        return  ((player_id  % self.NUMBER_OF_PLAYERS) + 1) * (self.num_of_pits + 1)
    
    def _pits_end(self, player_id : int) -> int:
        return self._row_begin(player_id) + self.num_of_pits
    
    def row_of_player(self, player_id : int) -> tuple:
        return tuple(self.board[self._row_begin(player_id) : self._row_end(player_id)])
    
    def pits_of_player(self, player_id : int) -> tuple:
        return tuple(self.board[self._row_begin(player_id) : self._pits_end(player_id)])
    
    def _index_is_store(self, index : int):
        return (index % (self.num_of_pits + 1)) == self.num_of_pits
    
    def current_player(self):
        return self.player_in_turn 
    
    def next_player(self):
        return (self.player_in_turn + 1) % self.NUMBER_OF_PLAYERS
    
    def switch_turn(self):
        self.player_in_turn = self.next_player()
    
        '''手を打つ．石を動かさず、勝利の場合 True を返し．そうでない場合 False を返す．エラーチェックしない．'''
    # def winning_move(self, index: int) -> bool:
    #     """Move the pieces which are in the grid of the given index.
    #     :params
    #     index: int: which grid to be moved
    #     :return
    #     whether you can move again or not.
    #     """
    #
    #     remain = (self.num_of_pits + self.STORES_PER_PLAYER) - (index % (self.num_of_pits + self.STORES_PER_PLAYER))
    #     if remain > self.STORES_PER_PLAYER:
    #         return False        
    #     pieces = self.board[self.player_in_turn][index]
    #     if pieces == 0 :
    #         return False
    #     if pieces - self.STORES_PER_PLAYER > self.num_of_pits + self.STORES_PER_PLAYER :
    #         return False
    #     return sum(self._pits_of_current()) == pieces
        
    '''手を打つ．石を動かす．勝利の場合 True を返す．そうでない場合，必要ならターンを変えて False を返す．'''
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """
        
        if not ( 0 <= index < self.num_of_pits ) :
            raise ValueError(f"Invalid index: {index}. choice of move should be in from 0 to before {self.num_of_pits}")
        
        start_ix = self._row_begin(self.player_in_turn)
        pieces = self.board[start_ix + index]
        if pieces == 0:
            print(self, index)
            raise ValueError(f"The pit of player {self.player_in_turn} index={index} has no pieces.")
        self.board[start_ix + index] = 0
        '''となりの穴から'''
        index += start_ix
        for _ in range(0, pieces):
            index = (index + 1) % len(self.board)
            self.board[index] += 1
        
        #print(self.board[start_ix : start_ix + self.num_of_pits])
        if sum(self.board[start_ix : start_ix + self.num_of_pits]) == 0 :
            return True
        if not self._index_is_store(index) :
            self.switch_turn()
        return False

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.current_player()
        pits = self.pits_of_player(player_id)
        for ix in range(len(pits)) :
            if pits[ix] > 0 :
                yield ix

    def game_won_by(self, player_id):
        #print(self.pit_array(player_id))
        return sum(self._pits_of(player_id)) == 0
    
    def signature(self):
        distribution = [ c for c in self.row_of_player(self.current_player())[:-1] if c > 0] + [ c for c in self.row_of_player(self.current_player())[:-1] if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        #print(self.board)
        pit_strs = list()
        for player_id in range(self.NUMBER_OF_PLAYERS) :
            t = '[' 
            t += ', '.join([str(i) for i in self.row_of_player(player_id)][:-1])
            t += '; ' + str(self.row_of_player(player_id)[-1])
            t += ']'
            pit_strs.append(t)
        return 'Board2p('+str(self.player_in_turn)+', ' + ','.join(pit_strs)+')'
    