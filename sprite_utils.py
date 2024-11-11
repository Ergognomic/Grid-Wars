import pygame

class SpriteManager(pygame.sprite.Sprite):

    def __init__(self, img_path: str, *args):
        super().__init__(*args) # initialize Sprite class
        self.img_path = img_path

    # load single-image from path
    def load_img(self, img_path: str) -> tuple[pygame.surface.Surface, pygame.Rect]:
        image = pygame.image.load(img_path)
        rect = image.get_rect()
        return image, rect

    # scale single image from path
    def scale_img(self, img_path: str, surface: pygame.surface.Surface, scale: int = 1) -> tuple[pygame.surface.Surface, pygame.Rect]:
        image, rect = self.load_img(img_path)
        image_w, image_h = image.get_size()
        surface_w, surface_h = surface.get_size()

        ratio = (surface_w / image_w) / scale
        new_size = (round(image_w * ratio), round(image_h * ratio))
        image = pygame.transform.scale(image, new_size)
        rect = image.get_rect()
        return image, rect

    # load sprite image from spritesheet
    def load_sprite(self, spritesheet: pygame.surface.Surface, pos: tuple[int, int], size: tuple[int, int]):
        image = pygame.Surface.subsurface(spritesheet, pos, size)
        rect = image.get_rect()
        return image, rect

    # scale sprite image from spritesheet
    def scale_sprite(self, spritesheet: pygame.surface.Surface, surface: pygame.surface.Surface, scale: int = 1, *args) ->  tuple[pygame.surface.Surface, pygame.Rect]:
        image, rect = self.load_sprite(spritesheet, *args)
        image_w, image_h = image.get_size()
        surface_w, surface_h = surface.get_size()

        ratio = (surface_w / image_w) / scale
        new_size = (round(image_w * ratio), round(image_h * ratio))
        image = pygame.transform.scale(image, new_size)
        rect = image.get_rect()
        return image, rect