import game_utils

FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

game = game_utils.GameManager("GAME", SCREEN_WIDTH, SCREEN_HEIGHT)
clock = game_utils.pygame.time.Clock()

while game.is_running:

    game.handle_events()
    game.update()
    game.render()

    clock.tick(FPS)
    
game.clean()