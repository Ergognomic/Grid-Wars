import pygame
import button

from collections import deque

class RobotBoardUI:
    def __init__(self, game_manager):
        self.manager = game_manager
        self.level = None
        self._stack = None

        self.game_border = pygame.surface.Surface((486,486))
        self.game_border_rect = self.game_border.get_rect()
        self.game_border_rect.topleft = (697, 93)

        self.large = pygame.surface.Surface((96,96))
        self.small = pygame.surface.Surface((68,68))

        self.button_list: list[button.Button] = []
        self.level1_buttons = pygame.sprite.Group()
        self.level2_buttons = pygame.sprite.Group()
        self.level3_buttons = pygame.sprite.Group()

    def setup_new_game(self):
        self.level = "LEVEL_ONE"
        self.setup_new_level(1)

    def setup_new_level(self, level):
        self.button_list.clear()
        if level == 1:
            for i in range(25):
                y, x = i // 5, i % 5
                self.button_list.append(
                    button.Button(
                        self.large, 
                        (748 + (x * 96), 144 + (y * 96)), 
                        (0, 0), 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level1_buttons
                    )
                )
            y, x = self.manager._state.pos
            idx = y * 5 + x
            self.button_list[idx] = button.Button(
                self.large, 
                (748 + (x * 96), 144 + (y * 96)), 
                (24, 0), 
                (23,23), 
                "assets/number_buttons.png", 
                self.level1_buttons
            )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack)

        elif level == 2:
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small, 
                        (736 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level2_buttons
                    )
                )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack[1:])

        elif level == 3:
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small, 
                        (736 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level3_buttons
                    )
                )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack)

    def setup_load_game(self):
        level = self.manager._level
        if level == 1:
            self.button_list.clear()
            self.level = "LEVEL_ONE"
            for i in range(25):
                y, x = i // 5, i % 5
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.large, 
                        (748 + (x * 96), 144 + (y * 96)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level1_buttons
                    )
                )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack)

        elif level == 2:
            self.button_list.clear()
            self.level = "LEVEL_TWO"
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small,
                        (736 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level2_buttons
                    )
                )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack)

        elif level == 3:
            self.button_list.clear()
            self.level = "LEVEL_THREE"
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small,
                        (736 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level3_buttons
                    )
                )
            self.manager.solve(False)
            self._stack = deque(self.manager._stack)

    def update(self):
        move = self._stack.popleft()
        y, x = move.pos
        idx = y * len(move.grid) + x
        val = move.grid[y][x]
        sprite_pos = (24 * val, 0)
        
        self.manager._state = move
        if self.level == "LEVEL_ONE":
            button_size = self.large
            self.button_list[idx] = button.Button(
                button_size, 
                (748 + (x * button_size.get_width()), 144 + (y * button_size.get_height())),
                sprite_pos, 
                (23,23), 
                "assets/number_buttons.png", 
                self.level1_buttons
            )
            if self.manager.check_level():
                self.level = "LEVEL_TWO"
                self.setup_new_level(2)

        elif self.level == "LEVEL_TWO":
            button_size = self.small
            self.button_list[idx] = button.Button(
                button_size, 
                (736 + (x * button_size.get_width()), 132 + (y * button_size.get_height())),
                sprite_pos, 
                (23,23), 
                "assets/number_buttons.png", 
                self.level2_buttons
            )
            if self.manager.check_level():
                self.level = "LEVEL_THREE"
                self.setup_new_level(3)

        elif self.level == "LEVEL_THREE":
            button_size = self.small
            self.button_list[idx] = button.Button(
                button_size, 
                (736 + (x * button_size.get_width()), 132 + (y * button_size.get_height())),
                sprite_pos, 
                (23,23), 
                "assets/number_buttons.png", 
                self.level3_buttons
            )
            if self.manager.check_level():
                self.level = "COMPLETE"
                return True
            
        return False
    

    def render(self, surface: pygame.surface.Surface):
        self.game_border.fill("white")
        surface.blit(self.game_border, self.game_border_rect)

        if self.level == "LEVEL_ONE":
            self.level1_buttons.draw(surface)
        elif self.level == "LEVEL_TWO":
            self.level2_buttons.draw(surface)
        elif self.level == "LEVEL_THREE":
            self.level3_buttons.draw(surface)
