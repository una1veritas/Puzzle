from typing import Dict

INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS = 0


class Board2players:
    def __init__(
        self,
        NUMBER_OF_PLAYERS: int = 2,
        init_pieces_per_grid: int = 3, #それぞれの枠に入った玉の数（初期配置）
        grids_per_player: int = 3, #枠の数
        STORES_PER_PLAYER: int = 1,
    ):
        self.NUM_OF_PLAYERS = NUMBER_OF_PLAYERS
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
        self.grids_between_players = STORES_PER_PLAYER
        self.data = (
            [init_pieces_per_grid] * grids_per_player
            + [INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS] * STORES_PER_PLAYER
        ) * NUMBER_OF_PLAYERS

    # プレイヤー間のグリッドのピース数を取得
    def get_pieces_in_between_grids(self, player_id: int) -> int:
        start_index = self.get_player_start_index(player_id=player_id) + self.grids_per_player
        end_index = start_index + self.grids_between_players
        return sum(self.data[start_index:end_index])

    # 勝敗条件を判定
    def does_player_win(self, player_id: int) -> bool:
        opponent_id = (player_id + 1) % self.NUM_OF_PLAYERS
        player_grids_empty = all(v == 0 for v in self.get_players_grids(player_id).values())
        opponent_grids_empty = all(v == 0 for v in self.get_players_grids(opponent_id).values())

        if player_grids_empty or opponent_grids_empty:
            player_between_pieces = self.get_pieces_in_between_grids(player_id)
            opponent_between_pieces = self.get_pieces_in_between_grids(opponent_id)
            return player_between_pieces > opponent_between_pieces

        return False

    def move(self, index: int) -> bool: #指定した index のグリッドからピースを動かす。グリッドに置かれたピースの数に応じて、次のグリッドにピースを1つずつ分配s。
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

        #現在のプレイヤーのグリッド範囲を取得
        player_id = index // (self.grids_per_player + self.grids_between_players)
        start_index = self.get_player_start_index(player_id)
        end_index = start_index + self.grids_per_player

        pieces = self.data[index]

        if pieces == 0:
            raise ValueError(f"The grid with index={index} has no pieces.")
        
        self.data[index] = 0

        for i in range(1, pieces + 1):
            index_to_be_incremented = self._add_index(index, i)

        # 分配先が次の条件のいずれかを満たす場合のみ加算
        # 1. 自分のグリッド範囲内
        # 2. 他のプレイヤーのグリッド範囲
        # 3. 自分のgrids_between_players
            if (
                start_index <= index_to_be_incremented < end_index  # 自分のグリッド範囲内
                or (not self._is_grid_between_players(index_to_be_incremented))  # グリッド間でない他プレイヤーのグリッド
                or (self._is_grid_between_players(index_to_be_incremented) and player_id == index_to_be_incremented // (self.grids_per_player + self.grids_between_players))  # 自分のgrids_between_players
                #or index_to_be_incremented == index  # 選んだグリッドにも分配
            ):

                self.data[index_to_be_incremented] += 1

        #self.data[index] = 0

        return self._is_grid_between_players(self._add_index(index, pieces))

    def _add_index(self, index, diff):
        return (index + diff) % len(self.data)

    def _is_grid_between_players(self, index: int):
        return index % (self.grids_per_player + self.grids_between_players) >= self.grids_per_player

    def get_players_grids(self, player_id: int) -> Dict[int, int]: #特定のプレイヤーのグリッドと、そのグリッドに置かれているピースの数を取得
        start_index = self.get_player_start_index(player_id=player_id)
        return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_player_start_index(self, player_id: int) -> int: #指定したプレイヤーの最初のグリッドのインデックスを取得
        return player_id * (self.grids_per_player + self.grids_between_players)

    def get_players_movable_grids(self, player_id: int) -> Dict[int, int]: #指定したプレイヤーが動かせるグリッド（ピースが1つ以上あるグリッド）を返す
        players_grids = self.get_players_grids(player_id=player_id)
        return {key: value for key, value in players_grids.items() if value > 0}

    def does_player_win(self, player_id: int) -> bool:
        movable_grids = self.get_players_movable_grids(player_id=player_id)
        return len(movable_grids) == 0

    def print_board(self):
        for i in range(self.NUM_OF_PLAYERS):
            player_start_grid = self.get_player_start_index(i)
            player_last_grid = player_start_grid + self.grids_per_player
            print(self.data[player_start_grid:player_last_grid])
            print(self.data[player_last_grid : player_last_grid + self.grids_between_players])
