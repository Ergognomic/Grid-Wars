import game_logic
import json

class GameManager:
    def __init__(self, ui_class):
        self.ui = ui_class(self)
        self._level = None
        self._logic = None
        self._state = None
        self._turn = None
        
        self._stack: list[game_logic.GameState] = []

    def new_game(self):
        self._level = 1
        self._logic = self._get_level_logic(self._level)
        self._state = self._logic.initialize()
        self._turn = 1
        self._stack.append(self._state)

    def load_game(self, file_path: str):
        with open(file_path, 'r') as file:
            game_data = json.load(file)
            self._level = game_data['level']
            self._logic = self._get_level_logic(self._level)
            self._stack = [game_logic.GameState.from_json(state) for state in game_data['stack']]
            self._state = self._stack[-1]
            self._turn = game_data['turn']
    
    def make_move(self, pos: tuple[int, int]):
        if pos not in self._state.valid_tiles: return False
        self._state = self._logic.take_turn(self._state, pos)
        self._stack.append(self._state)
        return True

    def check_level(self):
        if self._state.val <= 25: return False
        self._level += 1
        if self._level > 3: return True

        self._logic = self._get_level_logic(self._level)
        prev_grid = self._stack[-1].grid
        self._stack.clear()

        self._state = self._logic.initialize(prev_grid)
        self._stack.append(self._state)
        return True

    def undo_move(self):
        self._stack.pop()
        return self._stack[-1]

    def save_game(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.to_dict(), file)

    def _get_level_logic(self, level: int):
        if level == 1: return game_logic.LVL1()
        if level == 2: return game_logic.LVL2()
        if level == 3: return game_logic.LVL3()

    def solve(self, hint: bool = True):
        if self.backtrack(self._stack[-1]):
            if hint: self._stack.pop()
            self._state = self._stack[-1]
            return True
        
    def backtrack(self, state: game_logic.GameState):
        if state.val > 25: return True
        for tile in state.valid_tiles:
            y, x = tile
            if state.val == 25:
                new_valid_tiles = self._logic._get_valid_tiles(state.grid, (y, x), state.val)
            else:
                new_valid_tiles = self._logic._get_valid_tiles(state.grid, (y, x), state.val + 1)
            new_grid = game_logic.deepcopy(state.grid)
            new_grid[y][x] = state.val
            state = game_logic.GameState(new_grid, tile, new_valid_tiles, state.val + 1)
            self._stack.append(state)
            
            if self.backtrack(state): return True
            else: state = self.undo_move()
        return False
    
    def to_dict(self) -> dict:
        return {
            'level': self._level,
            'turn': self._turn,
            'stack': [state.to_dict() for state in self._stack]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())