import array

class Board2p:
    NUMBER_OF_PLAYERS : int = 2

    def __init__(
        self,
        init_pieces_per_pit : int = 3,
        pits_per_player : int = 3,
        board_array = None,
        player_in_turn = 0
    ):
        self.initial_pieces = init_pieces_per_pit
        self.num_of_pits = pits_per_player
        row = [self.initial_pieces] * self.num_of_pits + [0]
        if board_array != None :
            self.board = [array.array('B', board_array[0]), array.array('B', board_array[1])]
        else:
            self.board = [array.array('B', row), array.array('B', row)]
        self.player_in_turn = player_in_turn
    
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        if self.num_of_pits != other.num_of_pits :
            return False
        if self.board[self.current_player()][:self.num_of_pits] != other.board[other.current_player()][:other.num_of_pits] :
            return False
        if self.board[self.next_player()][:self.num_of_pits] != other.board[other.next_player()][:other.num_of_pits] :
            return False
        return True

    def __hash__(self):
        hash_elems = list()
        hash_elems.append(self.player_in_turn)
        hash_elems.append(tuple(self.board[self.player_in_turn][:self.num_of_pits]))
        hash_elems.append(tuple(self.board[self.player_in_turn][:self.num_of_pits]))
        return hash(tuple(hash_elems))
    
    def __copy__(self):
        mycopy = Board2p(
            init_pieces_per_pit = self.initial_pieces,
            pits_per_player = self.num_of_pits,
            board_array = self.board,
            player_in_turn = self.player_in_turn
            )
        return mycopy
    
    def index_is_store(self, index : int) -> bool :
        return index == self.num_of_pits
    
    def current_player(self):
        return self.player_in_turn 
    
    def next_player(self):
        return (self.player_in_turn + 1) % self.NUMBER_OF_PLAYERS
    
    def switch_turn(self):
        self.player_in_turn = self.next_player()
    
        '''手を打つ．石を動かさず、勝利の場合 True を返し．そうでない場合 False を返す．エラーチェックしない．'''
    def winning_move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """

        pieces = self.board[self.player_in_turn][index]
        if pieces > 0 and pieces < (self.num_of_pits + 1 - index) + self.num_of_pits + 1 \
        and index == self.num_of_pits - 1 :
            return True
        return False
        
        
    '''手を打つ．石を動かす．勝利の場合 True を返す．そうでない場合，必要ならターンを変えて False を返す．'''
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """
        #print(f'before {self.board}, {self.player_in_turn}, {index}')
        
        if self.index_is_store(index) or index > self.num_of_pits:
            raise ValueError(f"Invalid index: {index}. choice of move should be in range from 0 to before {len(self._pits_of(self.current_player()))}")

        pieces = self.board[self.player_in_turn][index]
        if pieces == 0:
            #print(self, index)
            raise ValueError(f"The pit of player {self.player_in_turn} index={index} has no pieces.")
        self.board[self.player_in_turn][index] = 0
        '''となりの穴からまいていく'''
        player_id = self.player_in_turn
        for _ in range(0, pieces):
            index += 1
            if index > self.num_of_pits :
                player_id = (player_id + 1) % self.NUMBER_OF_PLAYERS
                index = 0
            #print(self, player_id, index)
            self.board[player_id][index] += 1
        
        #print(f'after {self.board}')
        if sum(self.board[self.player_in_turn][:self.num_of_pits]) == 0 :
            return True
        if not self.index_is_store(index) :
            self.switch_turn()
        return False

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.player_in_turn
        for ix, value in enumerate(self.board[player_id][:self.num_of_pits]) :
            #print(f'ix = {ix}, value = {value}')
            if value > 0 :
                yield ix

    def game_won_by(self, player_id):
        #print(self.pit_array(player_id))
        return sum(self.board[player_id][:self.num_of_pits]) == 0
    
    def __str__(self):
        pit_strs = list()
        for player_id in range(self.NUMBER_OF_PLAYERS) :
            t = '[' 
            t += ', '.join([str(i) for i in self.board[player_id][:self.num_of_pits]])
            t += '; ' + ', '.join([str(i) for i in self.board[player_id][self.num_of_pits:]])
            t += ']'
            pit_strs.append(t)
        return 'Board2p('+str(self.player_in_turn)+', ' + ','.join(pit_strs)+')'
    