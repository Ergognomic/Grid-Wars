import pygame

import help
import button
import solo_ui as solo
import game_manager as gm

class Solo(object):

    def __init__(self, screen: pygame.surface.Surface):
        
        self.screen = screen
        self.manager = gm.GameManager(solo.GameBoardUI)

        self.manager.new_game()
        self.manager.ui.setup_new_game()

        self.help_opened = True
        self.text_box = help.HelpBox(self.screen, (140, 50), (1000, 620), (0xff9f17))
        
        self.solo_size = pygame.surface.Surface((96, 96))
        self.menu_border = pygame.surface.Surface((102, 400))
        self.menu_border_rect = self.menu_border.get_rect()
        self.menu_border_rect.topleft = (935, 93)

        self.misc_buttons = pygame.sprite.Group()
        self.help_button = button.Button(self.solo_size, (986, 144), (24, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.save_button = button.Button(self.solo_size, (986, 243), (144, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.undo_button = button.Button(self.solo_size, (986, 342), (0, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.hint_button = button.Button(self.solo_size, (986, 441), (48, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)

    def update(self, click_pos: tuple[int, int]):
        if not self.help_opened:
            # MISC BUTTONS
            if self.help_button.update(self.solo_size, click_pos):
                self.help_opened = True
            elif self.save_button.update(self.solo_size, click_pos):
                print("save")
            elif self.undo_button.update(self.solo_size, click_pos):
                self.manager.ui.undo(click_pos)
            elif self.hint_button.update(self.solo_size, click_pos):
                print("hint")
            # GAME BOARD
            if self.manager.ui.update(click_pos):
                return True
        else:
            if self.text_box.update(self.solo_size, click_pos):
                self.help_opened = False
        return False

    def render(self):
        if not self.help_opened:
            # MISC BUTTONS
            self.menu_border.fill("white")
            self.screen.blit(self.menu_border, self.menu_border_rect)
            self.misc_buttons.draw(self.screen)
            # GAME BOARD
            self.manager.ui.render(self.screen)
        else:
            self.text_box.render()

        