import pygame
import random
import computer_ui as comp
import game_manager as gm


class Robot(object):
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.manager = gm.GameManager(comp.GameBoardUI)

        self.manager.new_game()
        self.manager.ui.setup_new_game()

        self.start_time = pygame.time.get_ticks()

    def update(self):
        cooldown = random.randint(500, 2000)
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= cooldown:
            self.start_time = current_time
            if self.manager.ui.update(): return True
        return False

    def render(self):
        self.manager.ui.render(self.screen)