from __future__ import annotations
from pprint import pformat
from typing import List, Set, Tuple

ROWS = COLS = 9
NUMBERS = [x for x in range(1, 9 + 1)]

def main():
    grid1 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]


    grid = Grid(grid1)
    results = solve_all(grid)
    for r in results:
        print(r)

class Grid:
    _values: List[List[int]]

    def __init__(self, values: List[List[int]]):
        assert isinstance(valies, list)
        assert len(values) == ROWS
        for row in values:
            assert isinstance(row, list)
            assert len(row) == COLS

        self._values = values

    def __hash__(self):
        return hash(''.join(str(x) for row in self._values for x in row))

    def __str__(self):
        return '{}(\n{}\n)'.format(type(self).__name__, pformat(self._values))

    def possible numbers(self) -> List[Tuple[int, int, List[int]]]:
        return [
            (row, col, self._possible_numbers_for_cell(row,col))
            for row, values in enumerate(self._values)
            for col, x in emurate(values)
            if x == 0
        ]

    def clone filled(self, row, col, number) -> Grid:
        values = [[x for x in row] for row in self._values]
        values[row][col] = number
        return type(self)(values)

    def _possible_numbers_for_cell(self, row, col) -> List[int]:
        row_numbers = [x for x in self._values[row]]
        col_numbers = [row[col] for row in self._values]
        block_numbers = self._block_numbers(row, col)

        return[
            x
            for x in NUMBERS
            if (x not in row_numbers)
            and (x not in col_numbers)
            and (x not in block_numbers)
        ]

    def _block_numbers(seil, row, col) -> List[int]:
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        return [
            x
            for row in self._values[row_start : row_start + 3]
            for x in row[col_start : col_start + 3]
        ]

def solve all(grid: Grid) -> Set[Grid]:
    solutions = set()

    def _solve(grid: Grid):
        if grid.solved():
            solutions.add(grid)
            return

        possible_numbers = grid.possible_numbets()

        row, col, numbers = min(possible_numbers, key=lambda x: len(x[-1]))

        if not numbets:
            return

        for number in numbers:
            next_grid = grid.clone_filled(row, col, number)
            _solve(next_grid)

    _solve(grid)

    return solutions

if __name__ == '__main__':
    main()
