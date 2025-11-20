import pygame as pg
from src.game.board import Board
from src.game.game_state import GameState
from src.UI.hud import HUD
from src.UI.renderer import Renderer
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from src.utils.assets import init_assets

WINDOW_SIZE = (TILE_SIZE * BOARD_WIDTH, TILE_SIZE * BOARD_HEIGHT)


def run_game():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("ChessGame-py")
    clock = pg.time.Clock()

    board = Board()
    game_state = GameState(board)  

    # UI
    renderer = Renderer(board)
    hud = HUD(board)
    running = True
    try:
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                else:
                    game_state.handle_event(event)
                    hud.handle_event(event)
           
            screen.fill((30, 30, 30))  
            renderer.draw_board(screen, board)  
            hud.draw(screen)                    

            pg.display.flip()
            clock.tick(60)

    finally:
        pg.quit()


if __name__ == "__main__":
    run_game()

