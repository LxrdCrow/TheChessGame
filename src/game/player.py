import pygame as pg

class Player:
    def __init__(self, color: str):
        self.position = pg.Vector2(100, 100)
        self.velocity = pg.Vector2(0, 0)
        self.speed = 5
        self.size = pg.Vector2(50, 50)
        self.color = color  
        self.captured_pieces = []

    def handle_input(self):
        keys = pg.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
        if keys[pg.K_UP]:
            self.velocity.y = -self.speed
        if keys[pg.K_DOWN]:
            self.velocity.y = self.speed

    
    def update(self):
        self.position += self.velocity
        self.position.x = max(0, min(self.position.x, 800 - self.size.x))
        self.position.y = max(0, min(self.position.y, 600 - self.size.y))

    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (*self.position, *self.size))
        
    
    def get_rect(self):
        return pg.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    
    def reset_position(self):
        self.position = pg.Vector2(100, 100)

    def set_speed(self, new_speed):
        self.speed = new_speed

    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return self.velocity
    
    