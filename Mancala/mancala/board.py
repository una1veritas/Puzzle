import array 

class Board2p:
    NUMBER_OF_PLAYERS : int = 2
    PITS_PER_PLAYER : int = 3
    INITIAL_PIECES_PER_PIT : int = 3
    
    @staticmethod
    def num_of_players() :
        return Board2p.NUMBER_OF_PLAYERS

    @staticmethod
    def pits_per_player(val = None) :
        if val is not None :
            Board2p.PITS_PER_PLAYER = int(val)
        return Board2p.PITS_PER_PLAYER
    
    @staticmethod
    def initial_pieces_in_pit(val = None) : 
        if val != None :
            Board2p.INITIAL_PIECES_PER_PIT = int(val)
        return Board2p.INITIAL_PIECES_PER_PIT
    
    def __init__(self, board2p = None, initial_pieces_in_pit = None, pits_per_player = None):
        if initial_pieces_in_pit != None :
            Board2p.initial_pieces_in_pit(int(initial_pieces_in_pit))
        if pits_per_player != None :
            Board2p.pits_per_player(int(pits_per_player))
        if board2p != None :
            self.board = array.array('B', board2p.board)
        else:
            boardarray = ([Board2p.initial_pieces_in_pit(None)] * Board2p.PITS_PER_PLAYER + [0]) * self.NUMBER_OF_PLAYERS
            boardarray += [0] #player_in_turn
            self.board = array.array('B', boardarray)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        return self.pits_of_player(self.player_in_turn()) == other.pits_of_player(other.player_in_turn()) \
            and self.pits_of_player(self.next_player()) == other.pits_of_player(other.next_player()) 

    def __hash__(self):
        hash_elems = []
        hash_elems.append(hash(self.pits_of_player(self.player_in_turn())))
        hash_elems.append(hash(self.pits_of_player(self.next_player())))
        return hash(tuple(hash_elems))
    
    '''the index of the first pit of player'''
    def _row_begin(self, player_id : int) -> int:
        return (player_id  % Board2p.num_of_players()) * (self.pits_per_player() + 1)
    
    '''the index of the last store of player'''    
    def _row_end(self, player_id : int) -> int:
        return  ((player_id  % self.NUMBER_OF_PLAYERS) + 1) * (self.pits_per_player() + 1)
    
    def _pits_end(self, player_id : int) -> int:
        return self._row_begin(player_id) + self.pits_per_player()
    
    def row_of_player(self, player_id : int) -> tuple:
        return tuple(self.board[self._row_begin(player_id) : self._row_end(player_id)])
    
    def pits_of_player(self, player_id : int) -> tuple:
        return tuple(self.board[self._row_begin(player_id) : self._pits_end(player_id)])
    
    def _index_is_store(self, index : int):
        return (index % (self.pits_per_player() + 1)) == self.pits_per_player()
    
    def player_in_turn(self) : 
        return self.board[-1]
    
    def next_player(self):
        return (self.player_in_turn() + 1) % self.NUMBER_OF_PLAYERS
    
    def switch_turn(self):
        if self.next_player() == 2 :
            raise ValueError(f'next player id == {self.next_player()}')
        self.board[-1] = self.next_player()
    
    '''手を打つ．盤の石を動かし状態を変更、ターン交代なら True '''
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.
        :params
        index: int: which grid to be moved
        :return
        whether you can move again or not.
        """
        
        if not ( 0 <= index < self.pits_per_player() ) :
            raise ValueError(f"Invalid index: {index}. choice of move should be in from 0 to before {self.num_of_pits}")
        
        start_ix = self._row_begin(self.player_in_turn())
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
        
        if self.game_settled_by(self.player_in_turn()) :
            return False

        if not self._index_is_store(index) :
            self.switch_turn()
            return True
        return False

    def possible_moves(self, player_id = None):
        if player_id == None :
            player_id = self.player_in_turn()
        pits = self.pits_of_player(player_id)
        for ix in range(len(pits), 0, -1) :
            if pits[ix - 1] > 0 :
                yield ix - 1

    def game_settled_by(self, player_id):
        #print(self.pit_array(player_id))
        if sum(self.pits_of_player(player_id)) == 0 :
            return True
        return False
    
    def signature(self):
        distribution = [ c for c in self.pits_of_player(self.player_in_turn()) if c > 0] + [ c for c in self.pits_of_player(self.next_player()) if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def in_stores(self):
        total = 0
        for ix in range(self.NUMBER_OF_PLAYERS) :
            total += self.board[ix * (self.pits_per_player() + 1) + self.pits_per_player()]
        return total

    def __str__(self):
        #print(self.board)
        pit_strs = list()
        for player_id in range(self.NUMBER_OF_PLAYERS) :
            t = '[' 
            t += ', '.join([str(i) for i in self.pits_of_player(player_id)])
            t += '; ' + str(self.row_of_player(player_id)[-1])
            t += ']'
            pit_strs.append(t)
        return 'Board2p('+str(self.player_in_turn())+', ' + ','.join(pit_strs)+')'
    
    def __repr__(self):
        return self.__str__()
    