from constants import *
from circleshape import CircleShape
from shot import Shot
import pygame
from path_finder import resource_path

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPRITE_IMAGE = pygame.image.load(resource_path("assets/player sprite 2.png")).convert_alpha()
SCALED_SPRITE = pygame.transform.scale(SPRITE_IMAGE, (PLAYER_RADIUS * 4, PLAYER_RADIUS * 4))
ogrotated_image = pygame.transform.rotate(SCALED_SPRITE, 135)

class Player(CircleShape):
    def __init__(self, x, y,):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.image = ogrotated_image
        self.rect = self.position
        
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        rotated_image = pygame.transform.rotate(ogrotated_image, -self.rotation)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.position)
    
    def update(self, dt):
        self.cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed
        self.rect = self.image.get_rect(center=self.position)
    
    def shoot(self):
        if self.cooldown > 0:
            return
        else:
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        bullet = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        bullet.draw(screen)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
