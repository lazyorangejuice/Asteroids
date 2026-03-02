from circleshape import CircleShape
from constants import *
import pygame
from logger import log_event
import random

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ASTEROID_1_IMAGE = pygame.image.load("asteroid 2 sprite 2.png").convert_alpha()
ASTEROID_2_IMAGE = pygame.image.load("asteroid sprite 2.png").convert_alpha()

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius 
        SCALED_SPRITE_1 = pygame.transform.scale(ASTEROID_1_IMAGE, (self.radius , self.radius))
        SCALED_SPRITE_2 = pygame.transform.scale(ASTEROID_2_IMAGE, (self.radius , self.radius))
        sprite_list = [SCALED_SPRITE_1,SCALED_SPRITE_2]
        print (random.choice(sprite_list))
        self.image = random.choice(sprite_list)
        self.rect = self.position 
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20,50)
            ast_vec = self.velocity.rotate(angle)
            ast_vec2 =  self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = ast_vec * 1.8
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = ast_vec2 * 1.8