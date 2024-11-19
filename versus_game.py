import pygame
import random

import help
import button

import versus_player_ui as player
import versus_computer_ui as robot
import game_manager as gm

class Versus(object):
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.player_manager = gm.GameManager(player.GameBoardUI)
        self.computer_manager = gm.GameManager(robot.GameBoardUI)

        self.player_manager.new_game()
        self.player_manager.ui.setup_new_game()

        self.computer_manager.new_game()
        self.computer_manager._stack = self.player_manager._stack
        self.computer_manager._state = self.player_manager._state
        self.computer_manager.ui.setup_new_game()

        self.start_time = pygame.time.get_ticks()

        self.help_opened = True
        self.text_box = help.HelpBox(self.screen, (140, 50), (1000, 620), (0xff9f17))

        self.large = pygame.surface.Surface((96, 96))
        self.menu_border = pygame.surface.Surface((102, 400))
        self.menu_border_rect = self.menu_border.get_rect()
        self.menu_border_rect.topleft = (589, 93)

        self.misc_buttons = pygame.sprite.Group()
        self.help_button = button.Button(self.large, (640, 144), (24, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.save_button = button.Button(self.large, (640, 243), (144, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.undo_button = button.Button(self.large, (640, 342), (0, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)
        self.hint_button = button.Button(self.large, (640, 441), (48, 0), (23,23), "assets/misc_buttons.png", self.misc_buttons)

    def update(self, click_pos: tuple[int, int]):
        if self.help_opened:
            if self.text_box.update(self.large, click_pos):
                self.help_opened = False

        # HELP BUTTON
        elif self.help_button.update(self.large, click_pos):
            self.help_opened = True

        # SAVE BUTTON
        elif self.save_button.update(self.large, click_pos):
            print("save")
        
        # UNDO BUTTON
        elif self.undo_button.update(self.large, click_pos, active=self.player_manager._state.val > 2):
            self.player_manager.ui.undo(click_pos)
        
        # HINT BUTTON
        elif self.hint_button.update(self.large, click_pos):
            if self.player_manager.ui.hint(): 
                return True  # Game Completed!!

        # PLAYER BOARD
        if self.player_manager.ui.update(click_pos):
            print("Player Wins!")
            return True  # Game Completed!!
        
        cooldown = random.randint(1000, 5000)
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= cooldown:
            self.start_time = current_time
            if self.computer_manager.ui.update(): 
                print("Computer Wins!")
                return True

        return False

    def render(self):
        if self.help_opened:
            self.text_box.render()
            return
        
        # MISC BUTTONS
        self.menu_border.fill("white")
        self.screen.blit(self.menu_border, self.menu_border_rect)
        self.misc_buttons.draw(self.screen)

        # PLAYER BOARD
        self.player_manager.ui.render(self.screen)

        # COMPUTER BOARD
        self.computer_manager.ui.render(self.screen)
