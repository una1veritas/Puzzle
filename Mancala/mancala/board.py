from typing import Dict

class Board2players:
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
    
    def __eq__(self, another):
        if not isinstance(another, type(self)) :
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
        hashes = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_pit = self.get_player_start_index(i)
            hashes.append(hash(tuple(self.data[start_pit: start_pit + self.grids_per_player]))) 
        return hash(tuple(hashes))

    
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
        return index % (self.grids_per_player + self.STORES_PER_PLAYER) >= self.grids_per_player

    def get_players_grids(self, player_id: int) -> Dict[int, int]:
        start_index = self.get_player_start_index(player_id=player_id)
        return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_player_start_index(self, player_id: int) -> int:
        return player_id * (self.grids_per_player + self.STORES_PER_PLAYER)

    def get_players_movable_grids(self, player_id: int) -> Dict[int, int]:
        players_grids = self.get_players_grids(player_id=player_id)
        return {key: value for key, value in players_grids.items() if value > 0}

    def does_player_win(self, player_id: int) -> bool:
        movable_grids = self.get_players_movable_grids(player_id=player_id)
        return len(movable_grids) == 0

    def signature(self):
        distribution = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            start_grid_index = i*(self.grids_per_player + self.STORES_PER_PLAYER)
            distribution += [ c for c in self.data[start_grid_index: start_grid_index + self.grids_per_player] if c > 0]
        distribution.sort(reverse=True)
        return distribution

    def __str__(self):
        strlist = list()
        for i in range(self.NUMBER_OF_PLAYERS) :
            result = ''
            start_grid_index = i*(self.grids_per_player + self.STORES_PER_PLAYER)
            result += str(self.data[start_grid_index: start_grid_index + self.grids_per_player])
            result += str(self.data[start_grid_index + self.grids_per_player: start_grid_index + self.grids_per_player + self.STORES_PER_PLAYER])
            # result = '['
            # start_pit = self.get_player_start_index(0)
            # result += ', '.join([ str(i) for i in self.data[start_pit : start_pit + self.grids_per_player]]) + '; '
            # result += ','.join([str(i) for i in self.data[start_pit + self.grids_per_player : \
            #                              start_pit + self.grids_per_player + self.STORES_PER_PLAYER]])
            # result += ']'
            strlist.append(result)
        return '('+', '.join(strlist)+')'
    