import pygame
import button

class GameBoardUI:
    def __init__(self, game_manager):
        self.manager = game_manager
        self.level = None

        self.game_border = pygame.surface.Surface((486,486))
        self.game_border_rect = self.game_border.get_rect()
        self.game_border_rect.topleft = (97, 93)

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
                        (148 + (x * 96), 144 + (y * 96)), 
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
                (148 + (x * 96), 144 + (y * 96)), 
                (24, 0), 
                (23,23), 
                "assets/number_buttons.png", 
                self.level1_buttons
            )

        elif level == 2:
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small, 
                        (136 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level2_buttons
                    )
                )

        elif level == 3:
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small, 
                        (136 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level3_buttons
                    )
                )

    def setup_load_game(self):
        level = self.manager._level
        if level == 1:
            self.level = "LEVEL_ONE"
            for i in range(25):
                y, x = i // 5, i % 5
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.large, 
                        (148 + (x * 96), 144 + (y * 96)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level1_buttons
                    )
                )
        elif level == 2:
            self.level = "LEVEL_TWO"
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small,
                        (136 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level2_buttons
                    )
                )

        elif level == 3:
            self.level = "LEVEL_THREE"
            for i in range(49):
                y, x = i // 7, i % 7
                val = self.manager._state.grid[y][x]
                sprite_pos = (val * 24, 0)
                self.button_list.append(
                    button.Button(
                        self.small,
                        (136 + (x * 68), 132 + (y * 68)), 
                        sprite_pos, 
                        (23,23), 
                        "assets/number_buttons.png", 
                        self.level3_buttons
                    )
                )

    def undo(self, click_pos: tuple[int, int]):
        if self.manager._state.val <= 2: return
        if self.level == "LEVEL_ONE":
            y, x = self.manager._state.pos
            idx = y * 5 + x
            self.button_list[idx] = button.Button(
                self.large, 
                (148 + (x * 96), 144 + (y * 96)), 
                (0, 0), 
                (23,23), 
                "assets/number_buttons.png", 
                self.level1_buttons
            )
            self.manager._state = self.manager.undo_move()

        elif self.level == "LEVEL_TWO":
            y, x = self.manager._state.pos
            idx = y * 7 + x
            self.button_list[idx] = button.Button(
                self.small, 
                (136 + (x * 68), 132 + (y * 68)),
                (0, 0), 
                (23,23), 
                "assets/number_buttons.png", 
                self.level2_buttons
            )
            self.manager._state = self.manager.undo_move()

        elif self.level == "LEVEL_THREE":
            y, x = self.manager._state.pos
            idx = y * 7 + x
            self.button_list[idx] = button.Button(
                self.small, 
                (136 + (x * 68), 132 + (y * 68)),
                (0, 0), 
                (23,23), 
                "assets/number_buttons.png", 
                self.level3_buttons
            )
            self.manager._state = self.manager.undo_move()

    def hint(self):
        self.manager.solve()
        if self.level == "LEVEL_ONE":
            for item in self.manager._stack:
                y, x = item.pos
                idx = y * len(item.grid) + x
                val = item.grid[y][x]
                sprite_pos = (24 * val, 0)
                self.button_list[idx] = button.Button(
                    self.large, 
                    (148 + (x * 96), 144 + (y * 96)),
                    sprite_pos, 
                    (23,23), 
                    "assets/number_buttons.png", 
                    self.level1_buttons
                )

        elif self.level == "LEVEL_TWO":
            for item in self.manager._stack[1:]:
                y, x = item.pos
                idx = y * len(item.grid) + x
                val = item.grid[y][x]
                sprite_pos = (24 * val, 0)
                self.button_list[idx] = button.Button(
                    self.small, 
                    (136 + (x * 68), 132 + (y * 68)),
                    sprite_pos, 
                    (23,23), 
                    "assets/number_buttons.png", 
                    self.level2_buttons
                )

        elif self.level == "LEVEL_THREE":
            for item in self.manager._stack:
                y, x = item.pos
                idx = y * len(item.grid) + x
                val = item.grid[y][x]
                sprite_pos = (24 * val, 0)
                self.button_list[idx] = button.Button(
                    self.small, 
                    (136 + (x * 68), 132 + (y * 68)),
                    sprite_pos, 
                    (23,23), 
                    "assets/number_buttons.png", 
                    self.level3_buttons
                )
        return False

    def update(self, click_pos: tuple[int, int]):
        if self.level == "LEVEL_ONE":
            for i in range(25):
                if self.button_list[i].update(self.large, click_pos):
                    y, x = i // 5, i % 5
                    if self.manager.make_move((y, x)):
                        val = self.manager._state.val - 1
                        self.button_list[i] = button.Button(
                            self.large, 
                            (148 + (x * 96), 144 + (y * 96)), 
                            (val * 24, 0), 
                            (23,23), 
                            "assets/number_buttons.png", 
                            self.level1_buttons
                        )
                        if self.manager.check_level():
                            self.level = "LEVEL_TWO"
                            self.setup_new_level(2)
                    else:
                        print("Invalid!")

        elif self.level == "LEVEL_TWO":
            for i in range(49):
                if self.button_list[i].update(self.small, click_pos):
                    y, x = i // 7, i % 7
                    if self.manager.make_move((y, x)):
                        val = self.manager._state.val - 1
                        sprite_pos = (val * 24, 0)
                        self.button_list[i] = button.Button(
                            self.small, 
                            (136 + (x * 68), 132 + (y * 68)), 
                            sprite_pos, 
                            (23,23), 
                            "assets/number_buttons.png", 
                            self.level2_buttons
                        )
                        if self.manager.check_level():
                            self.level = "LEVEL_THREE"
                            self.setup_new_level(3)
                    else:
                        print("Invalid!")

        elif self.level == "LEVEL_THREE":
            for i in range(49):
                if self.button_list[i].update(self.small, click_pos):
                    y, x = i // 7, i % 7
                    if self.manager.make_move((y, x)):
                        val = self.manager._state.val - 1
                        sprite_pos = (val * 24, 0)
                        self.button_list[i] = button.Button(
                            self.small, 
                            (136 + (x * 68), 132 + (y * 68)), 
                            sprite_pos, 
                            (23,23), 
                            "assets/number_buttons.png", 
                            self.level3_buttons
                        )
                        if self.manager.check_level():
                            self.level = "COMPLETE"
                            return True
                    else:
                        print("Invalid!")
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