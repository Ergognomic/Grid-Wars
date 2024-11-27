import text_utils
import button


txt1 = "Welcome to GRID WARS!\n\
This is the HELP Page, you can open this page at any time by\n\
pressing the `H` button on the screen or on your keyboard.\n\
Press the `<` button in-game to return to the main menu\n\
or press the `ESC` key on your keyboard to quit to desktop.\n\n\
HOW TO PLAY\n\
    Every new game starts at Level 1.\n\
    Complete a level to advance automatically to the next.\n\
    The ultimate goal is to successfully fill in numbers 2\n\
    through 25 according to the rules of each level.\n"

txt2 = "LEVEL 1: The Inner Grid\n\
In this level, you'll play on a 5x5 grid with the number 1\n\
already placed randomly by the game. Fill numbers 2\n\
to 25 one at a time in ascending order.\n\n\
RULES FOR PLACING NUMBERS\n\
    - The number must be placed into an empty cell.\n\
    - The cell must be adjacent to the previous\n\
      number`s cell.\n"

txt3 = "LEVEL 2: The Outer Ring\n\
In this level a 7x7 grid appears, keeping the inner 5x5\n\
grid intact with all the numbers from Level 1. Now you\n\
must fill numbers 2 to 25 into the outer ring of the 7x7 grid.\n\n\
RULES FOR PLACING NUMBERS\n\
    - The number must be placed into an empty cell.\n\
    - Match one of the following from the number`s inner grid position.\n\
            1)   Be on the same row or column as the inner position.\n\
            2)  Be on the matching corner if the inner position\n\
                is one of the longest diagonals.\n"

txt4 = "LEVEL 3: Return to the Inner Grid\n\
In this level the system clears all numbers from the inner 5x5\n\
grid except for the 1, while the outer ring numbers from level 2\n\
remain. Fill numbers 2 to 25 into the inner grid, following the\n\
rules from level 1 with some additional constraints.\n\n\
RULES FOR PLACING NUMBERS\n\
    - Cell must be adjacent to the previous number.\n\
    - Cell must be on the same row or column as the matching\n\
      number in the outer-ring OR on a diagonal where the number\n\
            exists at one corner.\n"

txt5 = "**Dead Ends and Undos**\n\
    Even if the rules are followed, sometimes a dead-end\n\
    may occur which means that there are no valid tiles\n\
    available for the next number. If this occurs players\n\
    can undo turns one at a time, starting from the most\n\
    recent, to resolve a dead-end.\n\
    There is, however, one case where players cannot\n\
    perform an undo:\n\
        -   Players cannot undo at the beginning of a level\n\
            (i.e. players cannot undo into a previous level)."

txt6 = "**Hints**\n\
    For players who are stuck or need help, clicking on the\n\
    light-bulb icon will use a hint. This will give players some\n\
    help on the current level.\n\n\
**Saving**\n\
    Clicking on the `S` icon will allows players to save their game\n\
    for later. Saved games can be loaded from the main menu."

class HelpBox(text_utils.Text):

    def __init__(self, *args):
        super().__init__(*args)
        
        self.button_size = text_utils.pygame.surface.Surface((96, 96))
        self.close_button = button.Button(self.button_size, (1090,100), (72,0), (23,23), "assets/misc_buttons.png")
        self.left_button = button.Button(self.button_size, (190,620), (120,0), (23,23), "assets/misc_buttons.png")
        self.right_button = button.Button(self.button_size, (1090,620), (96,0), (23,23), "assets/misc_buttons.png")

        self.pages: list[str] = []
        self.page_num = 0

        self.pages.append(txt1)
        self.pages.append(txt2)
        self.pages.append(txt3)
        self.pages.append(txt4)
        self.pages.append(txt5)
        self.pages.append(txt6)
        self.load_page(self.page_num)

    def load_page(self, page_num: int):
        self.load_messages(self.pages[page_num], (10, 10))

    def load_messages(self, txt: str, pos: tuple[int, int]):
        
        self.text_box.fill(self.color)
        x, y = pos

        rect = text_utils.pygame.rect.Rect((x, y), self.rect.size)
        self.font.render_to(self.text_box, rect, "Help Menu", (255,255,255))
        y += 75
        
        for word in txt.split('\n'):
            rect = text_utils.pygame.rect.Rect((x, y), self.rect.size)
            self.font.render_to(self.text_box, rect, word, (255,255,255))
            y += 45

    def update(self, *args):
        action = False
        if self.close_button.update(*args):
            action = True
        elif self.left_button.update(*args):
            if self.page_num > 0:
                self.page_num -= 1
                self.load_page(self.page_num)
        elif self.right_button.update(*args):
            if self.page_num < len(self.pages) - 1:
                self.page_num += 1
                self.load_page(self.page_num)
        return action
        
    def render(self):
        self.screen.blit(self.text_box, self.rect)
        if self.page_num > 0:
            self.left_button.draw(self.screen)
        if self.page_num < len(self.pages) - 1:
            self.right_button.draw(self.screen)

        self.close_button.draw(self.screen)
        