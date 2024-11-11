import sprite_utils

class Button(sprite_utils.SpriteManager):

    def __init__(self, surface: sprite_utils.pygame.surface.Surface, screen_pos: tuple[int, int], sprite_pos: tuple[int, int], size: tuple[int, int], *args):
        super().__init__(*args) # initialize SpriteManager class
        self.spritesheet, self.rect = self.load_img(self.img_path)
        self.image, self.rect = self.scale_sprite(self.spritesheet, surface, 1, sprite_pos, size)
        
        self.screen_pos = screen_pos
        self.sprite_pos, self.sprite_size = sprite_pos, size
        self.rect.center = self.screen_pos

        self.clicked = True

    def update(self, surface: sprite_utils.pygame.surface.Surface, click_pos: tuple[int, int]):
        action = False
        mouse_pos = sprite_utils.pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            x, y = self.sprite_pos
            w, h = self.sprite_size
            self.image, self.rect = self.scale_sprite(self.spritesheet, surface, 1, (x, y + h + 1), (w, h))
            self.rect.center = self.screen_pos
            
            
            if self.rect.collidepoint(click_pos) and sprite_utils.pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        else:
            self.image, self.rect = self.scale_sprite(self.spritesheet, surface, 1, self.sprite_pos, self.sprite_size)
            self.rect.center = self.screen_pos

        if sprite_utils.pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action
