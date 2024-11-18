import pygame
import pygame.freetype

class Text(object):

    def __init__(self, surface: pygame.surface.Surface, screen_pos: tuple[int, int], size: tuple[int, int], bg_color: int):
        self.screen = surface
        self.color = bg_color

        self.text_box = pygame.surface.Surface(size)
        self.rect = self.text_box.get_rect()
        self.rect.topleft = screen_pos

        self.font = pygame.freetype.Font('assets/fonts/BitendDEMO.otf', 30)
