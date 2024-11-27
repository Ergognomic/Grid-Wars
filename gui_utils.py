import pygame
import sys
import json

import tkinter
import tkinter.filedialog

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
        
        self.title_size = pygame.surface.Surface((800, 600))
        self.title = bu.Button(self.title_size, (width/2, 100), (0, 90), (89, 17), "assets/menu_buttons.png", self.menu_buttons)

        self.menu_size = pygame.surface.Surface((400, 400))
        self.start_button = bu.Button(self.menu_size, (width/2, 300), (0, 0), (70, 17), "assets/menu_buttons.png", self.menu_buttons)
        self.load_button = bu.Button(self.menu_size, (width/2, 450), (0, 36), (70, 17), "assets/menu_buttons.png", self.menu_buttons)

        self.mode_buttons = pygame.sprite.Group()
        self.mode_size = pygame.surface.Surface((200, 200))
        self.solo_button = bu.Button(self.mode_size, (width/4, 200), (0, 0), (31, 31), "assets/mode_buttons.png", self.mode_buttons)
        self.versus_button = bu.Button(self.mode_size, (width/2, 200), (0, 64), (31, 31), "assets/mode_buttons.png", self.mode_buttons)
        self.robot_button = bu.Button(self.mode_size, (3 * width/4, 200), (0, 128), (31, 31), "assets/mode_buttons.png", self.mode_buttons)

        self.back_buttons = pygame.sprite.Group()
        self.back_size = pygame.surface.Surface((96,96))
        self.back_button = bu.Button(self.back_size, (50, 50), (120, 0), (23, 23), "assets/misc_buttons.png", self.back_buttons)

        self.info_bg = pygame.surface.Surface((300, 150))
        self.info_rect = self.info_bg.get_rect()
        self.info_bg.fill("white")

        self.solo_info = info.InfoBox(solo_txt, self.screen, (175, 325), (290, 140), (0xff9f17))
        self.versus_info = info.InfoBox(versus_txt, self.screen, (495, 325), (290, 140), (0xff9f17))
        self.robot_info = info.InfoBox(robot_txt, self.screen, (815, 325), (290, 140), (0xff9f17))

        self.screen_mode = "MAIN_MENU"
        self.game_mode = None
        self.is_running = True
        self.file_name = ""

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
                self.start_button.clicked = True

            if self.load_button.update(self.menu_size, self.click_pos):
                self.load_button.clicked = True
                file_ui = tkinter.Tk()
                file_ui.withdraw()
                full_path = tkinter.filedialog.askopenfilename(parent=file_ui, initialdir='./saves')
                file_ui.destroy()
                
                if "/saves" not in full_path:
                    self.file_name = ""
                else:
                    relative_path = full_path.split("/saves", 1)[-1]
                    self.file_name = "./saves" + relative_path

                    if relative_path == "/solo_save.json":
                        self.game_mode = solo_game.Solo(self.screen, self.file_name)
                        self.screen_mode = "SOLO_GAME"

                    elif relative_path == "/vs_save.json":
                        self.game_mode = versus_game.Versus(self.screen, self.file_name)
                        self.screen_mode = "VERSUS_GAME"

                    elif relative_path == "/computer_save.json":
                        self.game_mode = computer_game.Robot(self.screen, self.file_name)
                        self.screen_mode = "COMPUTER_GAME"
        
        elif self.screen_mode == "MODE_SELECT":
            
            if self.back_button.update(self.back_size, self.click_pos):
                self.screen_mode = "MAIN_MENU"
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True

                self.start_button.clicked = True
                self.load_button.clicked = True

            if self.solo_button.update(self.mode_size, self.click_pos):
                self.game_mode = solo_game.Solo(self.screen, self.file_name)
                self.screen_mode = "SOLO_GAME"

            if self.versus_button.update(self.mode_size, self.click_pos):
                self.game_mode = versus_game.Versus(self.screen, self.file_name)
                self.screen_mode = "VERSUS_GAME"
                
            if self.robot_button.update(self.mode_size, self.click_pos):
                self.game_mode = computer_game.Robot(self.screen, self.file_name)
                self.screen_mode = "COMPUTER_GAME"

        elif self.screen_mode == "SOLO_GAME":
            if self.back_button.update(self.back_size, self.click_pos):
                self.screen_mode = "MAIN_MENU"
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True
                
                self.start_button.clicked = True
                self.load_button.clicked = True

                self.file_name = ""

            if self.game_mode.update(self.click_pos):
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"
                
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True
                
                self.start_button.clicked = True
                self.load_button.clicked = True

                self.file_name = ""

        elif self.screen_mode == "VERSUS_GAME":
            if self.back_button.update(self.back_size, self.click_pos):
                self.screen_mode = "MAIN_MENU"
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True

                self.start_button.clicked = True
                self.load_button.clicked = True

                self.file_name = ""
            
            if self.game_mode.update(self.click_pos): 
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"
                
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True
                
                self.start_button.clicked = True
                self.load_button.clicked = True        
                
                self.file_name = ""                

        elif self.screen_mode == "COMPUTER_GAME":
            if self.back_button.update(self.back_size, self.click_pos):
                self.screen_mode = "MAIN_MENU"
                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True
                
                self.start_button.clicked = True
                self.load_button.clicked = True            
                
                self.file_name = ""
            
            if self.game_mode.update():
                self.game_mode = None
                self.screen_mode = "MAIN_MENU"

                self.back_button.clicked = True
                self.solo_button.clicked = True
                self.versus_button.clicked = True
                self.robot_button.clicked = True

                self.start_button.clicked = True
                self.load_button.clicked = True

                self.file_name = ""  

    def render(self):
        self.screen.fill("white")
        self.background.draw(self.screen)

        if self.screen_mode != "MAIN_MENU":
            self.back_buttons.draw(self.screen)

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
            self.back_buttons.draw(self.screen)
            self.game_mode.render()
        
        elif self.screen_mode == "VERSUS_GAME":
            self.game_mode.render()

        elif self.screen_mode == "COMPUTER_GAME":
            self.game_mode.render()

        pygame.display.flip()

    def clean(self):
        pygame.quit()
        sys.exit()