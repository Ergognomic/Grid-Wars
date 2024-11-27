from abc import ABC, abstractmethod
from dataclasses import dataclass
from copy import deepcopy
import random
import json

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
    
    @abstractmethod
    def _initialize_load_game(self):
        pass

class LVL1(GameLogic):
    def initialize(self, y: int = None, x: int = None):
        starting_grid = [[0 for _ in range(5)] for _ in range(5)]

        if y != None and x != None:
            row, col = y, x
        else:
            chance = random.randint(1, 8)
            match chance:
                case 1: 
                    row, col = 0, 0
                case 2:
                    row, col = 1, 1
                case 3:
                    row, col = 0, 4
                case 4:
                    row, col = 3, 2
                case 5:
                    row, col = 4, 3
                case 6:
                    row, col = 4, 4
                case 7:
                    row, col = 2, 1
                case 8:
                    row, col = 1, 0

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

    def _initialize_load_game(self, grid: list[int, int]):
        pass

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

    def _initialize_load_game(self, grid: list[int, int]):
        self.pos_map: dict[int, list[tuple[int, int]]] = {}
        for row in range(5):
            for col in range(5):
                val = grid[row+1][col+1]
                self.fill_map((row,col), val)

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

    def _initialize_load_game(self, grid: list[int, int]):
        self.pos_map: dict[int, list[tuple[int, int]]] = {}
        for row in range(7):
            for col in range(7):
                if row in {0, 6} or col in {0, 6}:
                    val = grid[row][col]
                    self.fill_map((row, col), val)

@dataclass(frozen=True)
class GameState:
    grid: list[list[int]]
    pos: tuple[int, int]
    valid_tiles: list[tuple[int, int]]
    val: int

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    @staticmethod
    def from_json(json_str: str) -> 'GameState':
        data = json.loads(json_str)
        return GameState(data['grid'], tuple(data['pos']), [tuple(t) for t in data['valid_tiles']], data['val'])

    def to_dict(self) -> dict:
        return self.__dict__
    