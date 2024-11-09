import random as rand
from copy import deepcopy

class GameState:
    """Represents a single variation of the game board."""

    def __init__(
            self,
            grid: list[list[int]],
            current_pos: tuple[int, int]
    ) -> None:
        self._grid = grid
        self._grid_size = len(grid)
        self._current_pos = current_pos

    def get_valid_tiles(self) -> list[tuple[int, int]]:
        """Finds the current valid tiles within the gamestate."""
        r = self._current_pos[0]
        c = self._current_pos[1]

        valid_tiles: list[tuple[int, int]] = []
        for i in range(max(r - 1, 0), min(r + 2, self._grid_size)):
            for j in range(max(c - 1, 0), min(c + 2, self._grid_size)):
                if (i, j) != self._current_pos and self._grid[i][j] == 0:
                    valid_tiles.append((i, j))
        return valid_tiles
    
    def __str__(self) -> str:
        output = ''
        for row in self._grid:
            for entry in row:
                output += f'{str(entry).zfill(2)} '
            output += '\n'
        return output

class Game:
    """Responsible for managing and running a game."""

    _turn: int = 1
    _level: int = 1
    _is_running: bool = True

    _gamestate_stack: list[GameState] = []

    def __init__(self, grid_size: int = 7) -> None:
        # Only supporting square grids for now
        self._grid_size = grid_size

    def start_game(self) -> None:
        
        level1 = self.Level_1(self._grid_size - 2)
        level2 = self.Level_2(self._grid_size)

        level1.start_game()
        while Game._is_running:
            match Game._level:
                case 1:
                    level1._take_turn()
                    Game._turn += 1

                    if level1._to_place == level1._grid_size * level1._grid_size + 1:
                        level2.start_game(level1._current_gamestate._grid)
                        Game._level += 1
                case 2:
                    level2._take_turn()
                    Game._turn += 1
                case _:
                    Game._is_running = False

        input('You win!')


    class Level_1:
        
        def __init__(self, grid_size: int = 5) -> None:
            self._grid_size = grid_size
            self._to_place = 2

        def start_game(self) -> None:

            starting_grid = [
                [0 for _ in range(self._grid_size)] 
                for _ in range(self._grid_size)
            ]
            ini_r = rand.randint(1, self._grid_size - 1)
            ini_c = rand.randint(1, self._grid_size - 1)
            starting_grid[ini_r][ini_c] = 1
            starting_state = GameState(
                grid=starting_grid,
                current_pos = (ini_r, ini_c)
            )

            self._current_gamestate = starting_state
            Game._gamestate_stack.append(starting_state)

        def _take_turn(self) -> None:
            """Prompts the player for input."""

            print(f'Turn {Game._turn}   Current Position {self._current_gamestate._current_pos}:')
            valid_tiles = self._current_gamestate.get_valid_tiles()

            self._display_gamestate()
            inp_coords = (-2,-2)
            while True:
                try:
                    inp = input(f'Select a valid location (format: row, col | undo: -1,-1 | solve: -2, -2): {valid_tiles}\n')
                    inp_r, inp_c = inp.split(',')
                    inp_coords = (int(inp_r), int(inp_c))

                    if (
                        (inp_coords not in valid_tiles and (inp_coords != (-1,-1) and inp_coords != (-2, -2))) or
                        (inp_coords == (-1, -1) and self._to_place == 2) # Undoing at the start
                    ): raise ValueError
                    else: break
                except:
                    print('Invalid.', end=' ')
                    continue

            if inp_coords == (-1, -1):
                self._undo()
            elif inp_coords == (-2, -2):
                solution = Ai(self._current_gamestate, self._to_place).solve()
                if not solution:
                    print("No Solution.")
                else:
                    print(solution)
                    
                    """vv-Useful if you want the game to end after solving-vv"""
                    self._to_place = self._grid_size * self._grid_size + 1
                    self._current_gamestate = solution
            else:
                new_grid = deepcopy(self._current_gamestate._grid)
                new_grid[inp_coords[0]][inp_coords[1]] = self._to_place
                new_gamestate = GameState(grid=new_grid, current_pos=inp_coords)

                Game._gamestate_stack.append(new_gamestate)
                self._current_gamestate = new_gamestate
                self._to_place += 1

                if self._to_place == self._grid_size * self._grid_size + 1:
                    Game._level += 1

        def _undo(self) -> None:
            """Returns to the last gamestate."""

            Game._gamestate_stack.pop()
            self._current_gamestate = Game._gamestate_stack[-1]
            self._to_place -= 1

        def _display_gamestate(self) -> None:
            """Displays the current state of the game board."""

            print(self._current_gamestate)


    class Level_2:

        def __init__(self, grid_size: int = 7) -> None:
            self._grid_size = grid_size
            self._to_place = 2

        def start_game(self, grid: list[list[int]]) -> None:

            starting_grid = [
                [0 for _ in range(self._grid_size)] 
                for _ in range(self._grid_size)
            ]
            for y in range(1, len(grid) + 1):
                for x in range(1, len(grid) + 1):
                    starting_grid[y][x] = grid[y-1][x-1]

        def _take_turn(self) -> None:

            

        def _undo(self) -> None:
            """Returns to the last gamestate."""

            Game._gamestate_stack.pop()
            self._current_gamestate = Game._gamestate_stack[-1]
            self._to_place -= 1

        def _display_gamestate(self) -> None:
            """Displays the current state of the game board."""

            print(self._current_gamestate)



class Ai:
    def __init__(self, ini_state: type[GameState], turn: int) -> None:
        
        self._ini_state: type[GameState] = ini_state
        self._val = turn

        grid = deepcopy(ini_state._grid)
        self._solution: type[GameState] = GameState(grid=grid, current_pos=ini_state._current_pos)

    def solve(self) -> type[GameState]:
        if self.backtrack(self._ini_state, self._val): 
            return self._solution

    def backtrack(self, state: type[GameState], val: int) -> bool:
        """Backtracking algorithm for solving level 1"""
        
        if val > state._grid_size * state._grid_size: return True
        valid_tiles = state.get_valid_tiles()

        for v in valid_tiles:
            self._solution._grid[v[0]][v[1]] = val
            new_state = GameState(grid=self._solution._grid, current_pos=v)

            if self.backtrack(new_state, val+1): return True
            else: self._solution._grid[v[0]][v[1]] = 0

        return False

if __name__ == '__main__':
    Game().start_game()