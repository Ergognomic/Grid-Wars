import text_utils

class InfoBox(text_utils.Text):
    def __init__(self, txt: str, *args):
        super().__init__(*args)
        self.info = txt
        self.load_message((10, 10))

    def load_message(self, pos: tuple[int, int]):
        self.text_box.fill(self.color)
        x, y = pos
        
        for word in self.info.split('\n'):
            rect = text_utils.pygame.rect.Rect((x, y), self.rect.size)
            self.font.render_to(self.text_box, rect, word, (255,255,255))
            y += 45
        
    def render(self):
        self.screen.blit(self.text_box, self.rect)
