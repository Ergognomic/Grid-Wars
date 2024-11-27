import pygame

import help
import button
import solo_ui as solo
import game_manager as gm

class Solo(object):
    def __init__(self, screen: pygame.surface.Surface, file_name: str = ""):
        self.screen = screen
        self.manager = gm.GameManager(solo.GameBoardUI)

        if file_name == "":
            self.manager.new_game()
            self.manager.ui.setup_new_game()
        else:
            self.manager.load_game(file_name)
            self.manager.ui.setup_load_game()


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
        if self.help_opened:
            if self.text_box.update(self.solo_size, click_pos):
                self.help_opened = False

        # HELP BUTTON
        elif self.help_button.update(self.solo_size, click_pos):
            self.help_opened = True

        # SAVE BUTTON
        elif self.save_button.update(self.solo_size, click_pos):
            self.manager.save_game("solo_save.json")
        
        # UNDO BUTTON
        elif self.undo_button.update(self.solo_size, click_pos, active=self.manager._state.val > 2):
            self.manager.ui.undo(click_pos)
        
        # HINT BUTTON
        elif self.hint_button.update(self.solo_size, click_pos):
            if self.manager.ui.hint(): 
                return True  # Game Completed!!

        # GAME BOARD
        if self.manager.ui.update(click_pos): 
            return True   # Game Completed!!
        return False

    def render(self):
        if self.help_opened:
            self.text_box.render()
            return
    
        # MISC BUTTONS
        self.menu_border.fill("white")
        self.screen.blit(self.menu_border, self.menu_border_rect)
        self.misc_buttons.draw(self.screen)

        # GAME BOARD
        self.manager.ui.render(self.screen)        