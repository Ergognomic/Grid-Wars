import pygame

import game_logic as game_logic
import button


class Solo(object):

    def __init__(self, screen: pygame.surface.Surface):
        
        self.screen = screen
        self.solo_buttons = pygame.sprite.Group()
        self.solo_size = pygame.surface.Surface((96, 96))

        self.box = pygame.surface.Surface((486,486))
        self.box_rect = self.box.get_rect()
        self.box_rect.topleft = (397, 93)

        self.button_list: list[button.Button] = []
        self.game = game_logic.LVL_1()

        for i in range(25):
            y = i // 5
            x = i % 5
            if not (y, x) == self.game._state._pos:
                self.button_list.append(button.Button(self.solo_size, (448 + (x * 96), 144 + (y * 96)), (0, 0), (23,23), "assets/empty_buttons.png", self.solo_buttons))
            else:
                self.button_list.append(button.Button(self.solo_size, (448 + (x * 96), 144 + (y * 96)), (0, 0), (23,23), "assets/number_buttons.png", self.solo_buttons))


    def update(self, click_pos: tuple[int, int]):
        
        for i in range(25):
            y = i // 5
            x = i % 5

            if self.button_list[i].update(self.solo_size, click_pos):
                if self.game._take_turn((y, x)):

                    val = self.game._state._val - 2
                    self.button_list[i] = button.Button(self.solo_size, (448 + (x * 96), 144 + (y * 96)), (val * 24, 0), (23,23), "assets/number_buttons.png", self.solo_buttons)

                else: 
                    print("Invalid!")

    def render(self):
        self.box.fill("white")
        self.screen.blit(self.box, self.box_rect)
        self.solo_buttons.draw(self.screen)