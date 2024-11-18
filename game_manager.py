import game_logic

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
        self._state = self._stack[-1]

    # def load_game(self, file_path: str):
    #     x = 0

    # def save_game(self, file_path: str):
    #     x = 0

    def _get_level_logic(self, level: int):
        if level == 1: return game_logic.LVL1()
        if level == 2: return game_logic.LVL2()
        if level == 3: return game_logic.LVL3()