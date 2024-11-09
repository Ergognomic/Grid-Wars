from __future__ import annotations
from copy import deepcopy
import random as rand

#   set to TRUE, if you want the AI to progress
#   the game and not just print out a solution
AI_CAN_PROGRESS = True
class Game:

    _size: int
    _turn: int = 1
    _level: int = 1
    _running: bool = True

    _gamestate_stack: list[type[GameState]] = []
    _lvl2_position_map: dict[int, list[tuple[int, int]]] = {}
    _lvl3_position_map: dict[int, list[tuple[int, int]]] = {}

    def __init__(self, grid_size: int = 5) -> None: 
        Game._size = grid_size

    def play(self) -> None:

        level1 = LVL_1(self._size)
        level2 = LVL_2(self._size + 2)
        level3 = LVL_3(self._size + 2)

        level1.start_level()
        while Game._running:
            match Game._level:
                case 1:
                    level1._take_turn()
                    Game._turn += 1

                    if level1._state._val > Game._size * Game._size:
                        level2.start_level()
                        Game._level += 1
                case 2:
                    level2._take_turn()
                    Game._turn += 1

                    if level2._state._val > Game._size * Game._size:
                        level3.start_level()
                        Game._level += 1
                case 3:
                    level3._take_turn()
                    Game._turn += 1

                    if level3._state._val > Game._size * Game._size:
                        Game._level += 1
                case _:
                    Game._running = False   
        input('You win!')

    def _update_stack(state: type[GameState], input_pos: tuple[int, int], keep_stack: bool = True) -> type[GameState]:
        # Updates the stack with most recent move #
        y, x = input_pos
        new_grid = deepcopy(state._grid)
        new_grid[y][x] = state._val

        new_gamestate = GameState(grid=new_grid, pos=input_pos, val=state._val+1)
        if keep_stack: Game._gamestate_stack.append(new_gamestate)
        return new_gamestate

    def _update_lvl2_dict(state: type[GameState]) -> None:
        # Updates the possible positions in grid for lvl2 grid #
        y, x = state._pos
        s = state._size
        valid_pos: list[tuple[int, int]] = []
        
        # check for diagonals
        if y == x: 
            valid_pos.extend([(0, 0), (s + 1, s + 1)])
        if y == -x + s - 1:
            valid_pos.extend([(s + 1, 0), (0, s + 1)])
        valid_pos.extend([(y + 1, 0), (y + 1, s + 1), (0, x + 1), (s + 1, x + 1)])
        Game._lvl2_position_map[state._val-1] = valid_pos
    
    def _update_lvl3_dict(state: type[GameState]) -> None:
        # Updates the possible positions in grid for lvl3 grid #
        y, x = state._pos
        s = Game._size
        valid_pos: list[tuple[int, int]] = []

        # check for diagonals
        asc_diagonal = [(0, s + 1), (s + 1, 0)]
        desc_diagonal = [(0, 0), (s + 1, s + 1)]

        if (y, x) in desc_diagonal:
            for i in range(1, s + 1):
                valid_pos.append((i, i))
        elif (y, x) in asc_diagonal:
            for i in range(1, s + 1):
                valid_pos.append((s + 1 - i, i))
        elif x == 0 or x == s + 1:  # vertical edges
            for i in range(1, s + 1):
                valid_pos.append((y, i))
        elif y == 0 or y == s + 1:  # horizontal edges
            for i in range(1, s + 1):
                valid_pos.append((i, x))
        Game._lvl3_position_map[state._val-1] = valid_pos

    def _undo() -> type[GameState]:
        # Return to previous gamestate #
        Game._gamestate_stack.pop()
        return Game._gamestate_stack[-1]
    
class LVL_1:

    def __init__(self, grid_size: int = 5) -> None:
        self._size = grid_size

    def start_level(self) -> None:
        starting_grid = [[0 for _ in range(self._size)] for _ in range(self._size)]
        initial_row, initial_col = rand.randint(1, self._size - 1), rand.randint(1, self._size - 1)
        starting_grid[initial_row][initial_col] = 1

        starting_state = GameState(grid=starting_grid, pos=(initial_row, initial_col), val=2)
        Game._gamestate_stack.append(starting_state)
        self._state = starting_state
        
    def _take_turn(self) -> None:
        # Prompts the player for input #
        print(f'Turn {Game._turn} | Current Value {self._state._val} | Current Position {self._state._pos}:')
        self._display_gamestate()
        
        valid_tiles = self._get_valid_tiles(self._state)
        input_pos = (-2, -2)
        while True:
            try: 
                inp = input(f'Select a valid location (format: row, col | undo: -1,-1 | solve: -2, -2): {valid_tiles}\n')
                if inp == 'q':
                    Game._running = False
                    return
                
                inp_r, inp_c = inp.split(',')
                input_pos = (int(inp_r), int(inp_c))
                if (
                    (input_pos not in valid_tiles and (input_pos != (-1,-1) and input_pos != (-2, -2))) or
                    (input_pos == (-1, -1) and self._state._val == 2) # Undoing at the start
                ): raise ValueError
                else: break
            except:
                print('Invalid.', end=' ')
                continue
        
        if input_pos == (-1, -1): 
            self._state = Game._undo()

        elif input_pos == (-2, -2):
            solution = AI(state=self._state, level=self, keep_stack=AI_CAN_PROGRESS).solve_level()
            print(solution) if solution else print("No Solution.")
            if AI_CAN_PROGRESS: self._state = solution

        else:
            self._state = Game._update_stack(self._state, input_pos)
            Game._update_lvl2_dict(self._state)

    def _display_gamestate(self) -> None:
        # Displays the current state of the game board #
        print(self._state)

    def _get_valid_tiles(self, state: type[GameState]) -> list[tuple[int, int]]:
        # Finds the valid tiles for the given state in LVL_1 #
        y, x = state._pos
        valid_tiles: list[tuple[int, int]] = []
        for i in range(max(y - 1, 0), min(y + 2, self._size)):
            for j in range(max(x - 1, 0), min(x + 2, self._size)):
                if (i, j) != state._pos and state._grid[i][j] == 0: 
                    valid_tiles.append((i, j))
        return valid_tiles

class LVL_2:
    
    def __init__(self, grid_size: int = 7) -> None:
        self._size = grid_size

    def start_level(self) -> None:
        starting_grid = [[0 for _ in range(self._size)] for _ in range(self._size)] 
        prev_grid = Game._gamestate_stack[-1]._grid

        for r in range(self._size - 2):
            for c in range(self._size - 2):
                starting_grid[r+1][c+1] = prev_grid[r][c]
        
        starting_state = GameState(grid=starting_grid, pos=(-1,-1), val=2)
        Game._gamestate_stack.append(starting_state)
        self._state = starting_state

    def _take_turn(self) -> None:
        # Prompts the player for input #
        print(f'Turn {Game._turn} | Current Value {self._state._val}')
        self._display_gamestate()

        valid_tiles = self._get_valid_tiles(self._state)
        input_pos = (-2, -2)
        while True:
            try: 
                inp = input(f'Select a valid location (format: row, col | undo: -1,-1 | solve: -2, -2): {valid_tiles}\n')
                if inp == 'q':
                    Game._running = False
                    return
                
                inp_r, inp_c = inp.split(',')
                input_pos = (int(inp_r), int(inp_c))
                if (
                    (input_pos not in valid_tiles and (input_pos != (-1,-1) and input_pos != (-2, -2))) or
                    (input_pos == (-1, -1) and self._state._val == 2) # Undoing at the start
                ): raise ValueError
                else: break
            except:
                print('Invalid.', end=' ')
                continue

        if input_pos == (-1, -1): 
            self._state = Game._undo()

        elif input_pos == (-2, -2):
            solution = AI(self._state, level=self, keep_stack=AI_CAN_PROGRESS).solve_level()
            print(solution) if solution else print("No Solution.")
            if AI_CAN_PROGRESS: self._state = solution

        else:
            self._state = Game._update_stack(self._state, input_pos)
            Game._update_lvl3_dict(self._state)

    def _display_gamestate(self) -> None:
        # Displays the current state of the game board #
        print(self._state)

    def _get_valid_tiles(self, state: type[GameState]) -> list[tuple[int, int]]:
        # Finds the valid tiles for the given state in LVL_2 #
        valid_tiles: list[tuple[int, int]] = []
        for y, x in Game._lvl2_position_map[state._val]:
            if not state._grid[y][x]:
                valid_tiles.append((y,x))
        return valid_tiles

class LVL_3:

    def __init__(self, grid_size: int = 7) -> None:
        self._size = grid_size
    
    def start_level(self) -> None:
        starting_grid = [[0 for _ in range(self._size)] for _ in range(self._size)]
        prev_grid = Game._gamestate_stack[-1]._grid

        starting_r, starting_c = (-1, -1)
        for r in range(self._size):
            for c in range(self._size):
                
                if prev_grid[r][c] == 1:
                    starting_r, starting_c = r, c
                    starting_grid[r][c] = prev_grid[r][c]
                
                elif r in {0, self._size-1} or c in {0, self._size-1}:
                    starting_grid[r][c] = prev_grid[r][c]

        starting_state = GameState(grid=starting_grid, pos=(starting_r, starting_c), val=2)
        Game._gamestate_stack.append(starting_state)
        self._state = starting_state

    def _take_turn(self) -> None:
        # Prompts the player for input #
        print(f'Turn {Game._turn} | Current Value {self._state._val} | Current Position {self._state._pos}')
        self._display_gamestate()

        valid_tiles = self._get_valid_tiles(self._state)
        input_pos = (-2, -2)
        while True:
            try: 
                inp = input(f'Select a valid location (format: row, col | undo: -1,-1 | solve: -2, -2): {valid_tiles}\n')
                if inp == 'q':
                    Game._running = False
                    return
                
                inp_r, inp_c = inp.split(',')
                input_pos = (int(inp_r), int(inp_c))
                if (
                    (input_pos not in valid_tiles and (input_pos != (-1,-1) and input_pos != (-2, -2))) or
                    (input_pos == (-1, -1) and self._state._val == 2) # Undoing at the start
                ): raise ValueError
                else: break
            except:
                print('Invalid.', end=' ')
                continue
        
        if input_pos == (-1, -1): 
            self._state = Game._undo()

        elif input_pos == (-2, -2):
            solution = AI(state=self._state, level=self, keep_stack=AI_CAN_PROGRESS).solve_level()
            print(solution) if solution else print("No Solution.")
            if AI_CAN_PROGRESS: self._state = solution
        
        else:
            self._state = Game._update_stack(self._state, input_pos)

    def _display_gamestate(self) -> None:
        # Displays the current state of the game board #
        print(self._state)

    def _get_valid_tiles(self, state: type[GameState]) -> list[tuple[int, int]]:
        # Finds the valid tiles for the given state in the LVL_3 #
        prev_y, prev_x = state._pos
        valid_tiles: list[tuple[int, int]] = []

        directions = [(-1,0), (1,0), (0,-1), (0,1),     # Horizontal/Vertical
                      (-1,-1), (-1,1), (1,-1), (1,1)]   # Diagonal
        
        for y, x in Game._lvl3_position_map[state._val]:
            if not state._grid[y][x]:
                for dy, dx in directions:
                    if (y == prev_y + dy) and (x == prev_x + dx):
                        valid_tiles.append((y,x))
        return valid_tiles

class AI:

    def __init__(self, state: type[GameState], level, keep_stack: bool = False) -> None:
        self._solution: type[GameState] = state
        self._level: type[self] = level
        self._keep_stack: bool = keep_stack

    def solve_level(self) -> type[GameState] | None:
        if self._backtrack(self._solution):
            return self._solution

    def _backtrack(self, state: type[GameState]) -> bool:
        # Backtracking algorithm for solving levels #
        if state._val > Game._size * Game._size: 
            self._solution = deepcopy(state)
            return True

        valid_tiles = self._level._get_valid_tiles(state)
        for tile in valid_tiles:
            new_state = Game._update_stack(state=deepcopy(state), input_pos=tile, keep_stack=self._keep_stack)

            if self._keep_stack and isinstance(self._level, LVL_1): 
                Game._update_lvl2_dict(state=new_state)
            elif self._keep_stack and isinstance(self._level, LVL_2):
                Game._update_lvl3_dict(state=new_state)

            if self._backtrack(state=new_state): 
                return True
            else:
                # if AI_CAN_PROGRESS is True, then the gamestate_stack
                # needs to be popped (undone) for each dead-end in the game
                if self._keep_stack: 
                    Game._undo()
        return False

class GameState:

    def __init__(self, grid: list[list[int]], pos: tuple[int, int], val: int = None) -> None:
        self._grid = grid
        self._size = len(grid)
        self._pos = pos
        self._val = val

    def __str__(self) -> str:
        output = ''
        for row in self._grid:
            for entry in row:
                output += f'{str(entry).zfill(2)} '
            output += '\n'
        return output

if __name__ == '__main__':
    Game().play()
