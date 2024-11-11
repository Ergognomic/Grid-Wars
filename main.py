import gui_utils

FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

game = gui_utils.GUIManager("GAME", SCREEN_WIDTH, SCREEN_HEIGHT)
clock = gui_utils.pygame.time.Clock()

while game.is_running:

    game.handle_events()
    game.update()
    game.render()

    clock.tick(FPS)
    
game.clean()