import pygame
import sys

import info
import background as bg
import button as bu

import solo_game
import versus_game
import computer_game

solo_txt = "\
    Can you play\n\
    the game by\n\
    yourself?\n\n"

versus_txt = "\
    Play the game\n\
    against the\n\
    computer!\n\n"

robot_txt = "\
    Watch the\n\
    computer play\n\
    the game!\n\n"


class GUIManager():

    def __init__(self, title: str, width: int, height: int) -> None:

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.scale = width / 640
        self.click_pos = (-1,-1)

        self.background = pygame.sprite.Group()
        # self.background = pygame.sprite.LayeredUpdates()
        bg.Background(self.screen, 0, 0, "assets/bg.png", self.background)
        bg.Background(self.screen, 0, 1, "assets/bg.png", self.background)
        bg.Background(self.screen, 1, 0, "assets/bg.png", self.background)
        bg.Background(self.screen, 1, 1, "assets/bg.png", self.background)

        self.menu_buttons = pygame.sprite.Group()
        self.menu_size = pygame.surface.Surface((400, 400))
        self.start_button = bu.Button(self.menu_size, (width/2, 150), (0, 0), (70, 17), "assets/menu_buttons.png", self.menu_buttons)
        self.load_button = bu.Button(self.menu_size, (width/2, 300), (0, 36), (70, 17), "assets/menu_buttons.png", self.menu_buttons)

        self.mode_buttons = pygame.sprite.Group()
        self.mode_size = pygame.surface.Surface((200, 200))
        self.solo_button = bu.Button(self.mode_size, (width/4, 200), (0, 0), (31, 31), "assets/mode_buttons.png", self.mode_buttons)
        self.versus_button = bu.Button(self.mode_size, (width/2, 200), (0, 64), (31, 31), "assets/mode_buttons.png", self.mode_buttons)
        self.robot_button = bu.Button(self.mode_size, (3 * width/4, 200), (0, 128), (31, 31), "assets/mode_buttons.png", self.mode_buttons)

        self.info_bg = pygame.surface.Surface((300, 150))
        self.info_rect = self.info_bg.get_rect()
        self.info_bg.fill("white")

        self.solo_info = info.InfoBox(solo_txt, self.screen, (175, 325), (290, 140), (0xff9f17))
        self.versus_info = info.InfoBox(versus_txt, self.screen, (495, 325), (290, 140), (0xff9f17))
        self.robot_info = info.InfoBox(robot_txt, self.screen, (815, 325), (290, 140), (0xff9f17))

        self.screen_mode = "MAIN_MENU"
        self.game_mode = None
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_pos = pygame.mouse.get_pos()

    def update(self):
        self.background.update()
        if self.screen_mode == "MAIN_MENU":

            if self.start_button.update(self.menu_size, self.click_pos):
                self.screen_mode = "MODE_SELECT"
            if self.load_button.update(self.menu_size, self.click_pos):
                print("load clicked")
        
        elif self.screen_mode == "MODE_SELECT":
            if self.solo_button.update(self.mode_size, self.click_pos):
                self.game_mode = solo_game.Solo(self.screen)
                self.screen_mode = "SOLO_GAME"
                
            if self.versus_button.update(self.mode_size, self.click_pos):
                self.game_mode = versus_game.Versus(self.screen)
                self.screen_mode = "VERSUS_GAME"

            if self.robot_button.update(self.mode_size, self.click_pos):
                self.game_mode = computer_game.Robot(self.screen)
                self.screen_mode = "COMPUTER_GAME"

        elif self.screen_mode == "SOLO_GAME":
            if self.game_mode.update(self.click_pos):
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"
        
        elif self.screen_mode == "VERSUS_GAME":
            if self.game_mode.update(self.click_pos): 
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"

        elif self.screen_mode == "COMPUTER_GAME":
            if self.game_mode.update():
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"


    def render(self):
        self.screen.fill("white")
        self.background.draw(self.screen)

        if self.screen_mode == "MAIN_MENU":
            self.menu_buttons.draw(self.screen)

        elif self.screen_mode == "MODE_SELECT":
            self.mode_buttons.draw(self.screen)

            self.screen.blit(self.info_bg, (170, 320), self.info_rect)
            self.screen.blit(self.info_bg, (490, 320), self.info_rect)
            self.screen.blit(self.info_bg, (810, 320), self.info_rect)

            self.solo_info.render()
            self.versus_info.render()
            self.robot_info.render()

        elif self.screen_mode == "SOLO_GAME":
            self.game_mode.render()
        
        elif self.screen_mode == "VERSUS_GAME":
            self.game_mode.render()

        elif self.screen_mode == "COMPUTER_GAME":
            self.game_mode.render()

        pygame.display.flip()

    def clean(self):
        pygame.quit()
        sys.exit()