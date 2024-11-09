import sprite_utils

class Background(sprite_utils.SpriteManager):

    def __init__(self, surface: sprite_utils.pygame.surface.Surface, x_pos: int, y_pos: int, *args):
        super().__init__(*args) # initialize SpriteManager class
        self.image, self.rect = self.scale_img(self.img_path, surface)

        self.x, self.y = x_pos, y_pos
        self.x_steps, self.y_steps = 0, 0

        self.rect.x = self.rect.width * self.x
        self.rect.y = self.rect.height * self.y
    
    def update(self):
        self.rect.move_ip(-1, -1)
        self.x_steps += 1
        self.y_steps += 1

        if self.x_steps >= self.rect.width:
            self.rect.x = self.x * self.rect.width
            self.x_steps = 0
        if self.y_steps >= self.rect.height:
            self.rect.y = self.y * self.rect.height
            self.y_steps = 0