import random as rand
from copy import deepcopy

class GameManager(object):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_game(self):
        x = 0

    def save_game(self):
        x = 0

    def start_game(self):
        x = 0

class Game(object):
    
    def __init__(self) -> None:
        self._turn: int = 1
        self._stack: list[type[GameState]] = []

    def _update_stack(self, state: type['GameState'], input_pos: tuple[int, int]) -> type['GameState']:
        # Updates the stack with most recent move #
        y, x = input_pos
        new_grid = deepcopy(state._grid)
        new_grid[y][x] = state._val

        new_gamestate = GameState(grid=new_grid, pos=input_pos, val=state._val+1)
        self._stack.append(new_gamestate)
        return new_gamestate


class LVL_1(Game):

    def __init__(self) -> None:
        super().__init__()

        starting_grid = [[0 for _ in range(5)] for _ in range(5)]
        row, col = rand.randint(1, 5 - 1), rand.randint(1, 5 - 1)
        starting_grid[row][col] = 1

        valid_tiles = self._get_valid_tiles(starting_grid, (row, col))
        starting_state = GameState(starting_grid, (row, col), valid_tiles, 2)

        self._stack.append(starting_state)
        self._state = starting_state

    def _take_turn(self, pos: tuple[int, int]) -> bool:
        valid_tiles = self._state._valid_tiles
        if pos not in valid_tiles:
            return False
        else:
            valid_tiles = self._get_valid_tiles(self._state._grid, pos)
            y, x = pos
            new_grid = deepcopy(self._state._grid)
            new_grid[y][x] = self._state._val

            new_gamestate = GameState(new_grid, pos, valid_tiles, self._state._val+1)
            self._stack.append(new_gamestate)
            self._state = new_gamestate
            return True 
        
    def _get_valid_tiles(self, grid: list[list[int]], pos: tuple[int, int]) -> list[tuple[int, int]]:
        y, x = pos
        valid_tiles: list[tuple[int, int]] = []
        for i in range(max(y-1, 0), min(y+2, 5)):
            for j in range(max(x-1, 0), min(x+2, 5)):
                if (i, j) != pos and grid[i][j] == 0:
                # if (i, j) != self._state._pos and self._state._grid[i][j] == 0:
                    valid_tiles.append((i, j))
        return valid_tiles


class GameState(object):

    def __init__(self, grid: list[list[int]], pos: tuple[int, int], valid_tiles: list[tuple[int, int]], val: int):  
        self._grid = grid
        self._pos = pos

        self._valid_tiles = valid_tiles
        self._val = val