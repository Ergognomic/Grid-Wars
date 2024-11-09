import pygame
import sys

import background as bg
import button as bu
class GameManager():

    def __init__(self, title: str, width: int, height: int) -> None:

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.background = pygame.sprite.LayeredUpdates()
        bg.Background(self.screen, 0, 0, "assets/bg.png", -10, self.background)
        bg.Background(self.screen, 0, 1, "assets/bg.png", -10, self.background)
        bg.Background(self.screen, 1, 0, "assets/bg.png", -10, self.background)
        bg.Background(self.screen, 1, 1, "assets/bg.png", -10, self.background)
        
        self.menu_buttons = pygame.sprite.LayeredUpdates()
        bu.Button(self.screen, (320, 150), (0, 0), (70, 17), "assets/menu_buttons.png", 0, self.menu_buttons)
        bu.Button(self.screen, (320, 250), (0, 36), (70, 17), "assets/menu_buttons.png", 0, self.menu_buttons)
        
        
        self.is_main_menu = True
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.is_running = False

    def update(self):
        self.background.update()
        if self.is_main_menu:
            for button in self.menu_buttons:
                if button.update(self.screen):
                    self.is_main_menu = False
        
        # self.menu_buttons.update(self.screen)


    def render(self):
        self.screen.fill("black")
        self.background.draw(self.screen)

        if self.is_main_menu:
            self.menu_buttons.draw(self.screen)

        pygame.display.flip()

    def clean(self):
        pygame.quit()
        sys.exit()