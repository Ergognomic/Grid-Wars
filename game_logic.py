from abc import ABC, abstractmethod
from dataclasses import dataclass
from copy import deepcopy
import random

class GameLogic(ABC):
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def take_turn(self):
        pass
    
    @abstractmethod
    def fill_map(self):
        pass

    @abstractmethod
    def _get_valid_tiles(self):
        pass

class LVL1(GameLogic):
    def initialize(self):
        starting_grid = [[0 for _ in range(5)] for _ in range(5)]
        row, col = random.randint(1, 5 - 1), random.randint(1, 5 - 1)
        starting_grid[row][col] = 1

        valid_tiles = self._get_valid_tiles(starting_grid, (row, col))
        starting_state = GameState(starting_grid, (row, col), valid_tiles, 2)
        return starting_state

    def take_turn(self, state: 'GameState', pos: tuple[int, int]):
        y, x = pos
        tiles = self._get_valid_tiles(state.grid, pos)
        new_grid = deepcopy(state.grid)
        new_grid[y][x] = state.val
        return GameState(new_grid, pos, tiles, state.val+1)

    def fill_map(self):
        pass

    def _get_valid_tiles(self, grid: list[list[int]], pos: tuple[int, int], *args) -> list[tuple[int, int]]:
        y, x = pos
        valid_tiles: list[tuple[int, int]] = []
        for i in range(max(y-1, 0), min(y+2, 5)):
            for j in range(max(x-1, 0), min(x+2, 5)):
                if (i, j) != pos and grid[i][j] == 0:
                    valid_tiles.append((i, j))
        return valid_tiles

class LVL2(GameLogic):
    def initialize(self, prev_grid: list[list[int]]):
        self.pos_map: dict[int, list[tuple[int, int]]] = {}
        starting_grid = [[0 for _ in range(7)] for _ in range(7)]
        for row in range(5):
            for col in range(5):
                val = prev_grid[row][col]
                starting_grid[row+1][col+1] = val
                self.fill_map((row,col), val)

        valid_tiles = self._get_valid_tiles(starting_grid, (-1,-1), 2)
        starting_state = GameState(starting_grid, (-1, -1), valid_tiles, 2)
        return starting_state
    
    def take_turn(self, state: 'GameState', pos: tuple[int, int]):
        y, x = pos
        if state.val < 25:
            tiles = self._get_valid_tiles(state.grid, pos, state.val + 1)
        else:
            tiles = self._get_valid_tiles(state.grid, pos, state.val)
        new_grid = deepcopy(state.grid)
        new_grid[y][x] = state.val
        return GameState(new_grid, pos, tiles, state.val + 1)

    def fill_map(self, pos: tuple[int, int], val: int):
        y, x = pos
        valid_pos: list[tuple[int, int]] = []
        # check for diagonals
        if y == x:
            valid_pos.extend([(0,0), (6,6)])
        if y == -x + 4:
            valid_pos.extend([(6,0), (0,6)])
        valid_pos.extend([(y + 1, 0), (y + 1, 6), (0, x + 1), (6, x + 1)])
        self.pos_map[val] = valid_pos

    def _get_valid_tiles(self, grid: list[list[int]], pos: tuple[int, int], val: int) -> list[tuple[int, int]]:
        valid_tiles: list[tuple[int, int]] = []
        for r, c in self.pos_map[val]:
            if (r, c) != pos and grid[r][c] == 0:
                valid_tiles.append((r, c))
        return valid_tiles

class LVL3(GameLogic):
    def initialize(self, prev_grid: list[list[int]]):
        self.pos_map: dict[int, list[tuple[int, int]]] = {}
        starting_grid = [[0 for _ in range(7)] for _ in range(7)]
        for row in range(7):
            for col in range(7):
                if prev_grid[row][col] == 1:
                    starting_row, starting_col = row, col
                    starting_grid[row][col] = prev_grid[row][col]

                elif row in {0, 6} or col in {0, 6}:
                    val = prev_grid[row][col]
                    starting_grid[row][col] = val
                    self.fill_map((row, col), val)
        
        valid_tiles = self._get_valid_tiles(starting_grid, (starting_row, starting_col), 2)
        starting_state = GameState(starting_grid, (starting_row, starting_col), valid_tiles, 2)
        return starting_state
    
    def take_turn(self, state: 'GameState', pos: tuple[int, int]):
        y, x = pos
        if state.val < 25:
            tiles = self._get_valid_tiles(state.grid, pos, state.val + 1)
        else:
            tiles = self._get_valid_tiles(state.grid, pos, state.val)
        new_grid = deepcopy(state.grid)
        new_grid[y][x] = state.val
        return GameState(new_grid, pos, tiles, state.val + 1)

    def fill_map(self, pos: tuple[int, int], val: int):
        y, x = pos
        valid_pos: list[tuple[int, int]] = []

        # check diagonals
        asc_diagonal = [(0,6), (6,0)]
        desc_diagonal = [(0,0), (6,6)]
        if (y, x) in desc_diagonal:
            for i in range(1, 6):
                valid_pos.append((i,i))
        elif (y, x) in asc_diagonal:
            for i in range(1, 6):
                valid_pos.append((6-i, i))
        # vertical edges
        elif x == 0 or x == 6:
            for i in range(1, 6):
                valid_pos.append((y, i))
        # horizontal edges
        elif y == 0 or y == 6:
            for i in range(1, 6):
                valid_pos.append((i, x))
        self.pos_map[val] = valid_pos
    
    def _get_valid_tiles(self, grid: list[list[int]], pos: tuple[int, int], val: int) -> list[tuple[int, int]]:
        prev_y, prev_x = pos
        valid_tiles: list[tuple[int, int]] = []
        directions = [(-1,0), (1,0), (0,-1), (0,1),     # Horizontal/Vertical
                      (-1,-1), (-1,1), (1,-1), (1,1)]   # Diagonal
        for y, x in self.pos_map[val]:
            if (y, x) != pos and grid[y][x] == 0:
                for dy, dx in directions:
                    if (y == prev_y + dy) and (x == prev_x + dx):
                        valid_tiles.append((y, x))
        return valid_tiles

@dataclass(frozen=True)
class GameState:
    grid: list[list[int]]
    pos: tuple[int, int]
    valid_tiles: list[tuple[int, int]]
    val: int