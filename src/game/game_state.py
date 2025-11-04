import pygame as pg
from src.game.player import Player

class GameState:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Game State Management Example")
        self.clock = pg.time.Clock()
        self.player = Player()
        self.running = True

    def reset_game(self):
        self.player.reset_position()

    def set_player_speed(self, speed):
        self.player.set_speed(speed)

    def get_player_position(self):
        return self.player.get_position()

    def get_player_velocity(self):
        return self.player.get_velocity()

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.player.handle_input()
            self.player.update()

            self.screen.fill((0, 0, 0))  # Clear screen with black
            self.player.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()