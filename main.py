import pygame
from sys import exit
from pygame.locals import *
from pathlib import Path
from os import path
import random
import math
import numpy
import settings


pygame.init()
clock = pygame.time.Clock()
walls = pygame.sprite.Group()

def get_file(filePath): return path.join(Path(__file__).parent, filePath)

class Player:
    def __init__(self, position, size):
        self.rect = pygame.Rect(position, size)
        self.speed = 10
        self.trail = []

    def update(self, keys):
        pygame.draw.rect(settings.SCREEN, (200,200,200), self.rect)
        for area, pos in enumerate(self.trail, 1):
            size = ((area*(self.rect.width/len(self.trail))), area*(self.rect.height/len(self.trail)))
            rect = pygame.Rect((pos[0]-(size[0]/2), pos[1]-(size[0]/2)), size)
            pygame.draw.rect(settings.SCREEN, (200,200,200), rect)

        self.velocity = pygame.Vector2((0,0))
        
        if keys[K_w]: self.velocity.y += -self.speed
        if keys[K_a]: self.velocity.x += -self.speed
        if keys[K_s]: self.velocity.y += self.speed
        if keys[K_d]: self.velocity.x += self.speed

        if self.velocity.magnitude() > 0:
            self.velocity.scale_to_length(self.speed)
            self.trail.append(self.rect.center)
        
        self.rect.move_ip(self.velocity)
        if len(self.trail) > 5: self.trail.pop(0)

        self.neutralise_collision()


    def neutralise_collision(self):
        ''' Returns an opposition vector to any colliding objects '''
        for collideable in walls:
            if self.rect.colliderect(collideable):
                collisionDir = self.compare_position(collideable)
                setattr(getattr(self, "rect"), self.return_flipped(collisionDir), getattr(getattr(collideable, "rect"), collisionDir))

    def compare_position(self, collideable):
        ''' Returns the direction self is of object as a vector '''
        selfCentre = self.rect.center
        rectCentre = collideable.rect.center

        relativeDir = {"x": rectCentre[0] - selfCentre[0], "y": rectCentre[1] - selfCentre[1]}

        if abs(relativeDir["x"]) > abs(relativeDir["y"]):
            if numpy.sign(relativeDir["x"]) == -1: return "right"
            else: return "left"

        if abs(relativeDir["x"]) < abs(relativeDir["y"]):
            if numpy.sign(relativeDir["y"]) == -1: return "bottom"
            else: return "top"

        elif abs(relativeDir["x"]) == abs(relativeDir["y"]):
            if numpy.sign(relativeDir["x"]) == -1 and numpy.sign(relativeDir["y"]) == 1: return "topright"
            if numpy.sign(relativeDir["x"]) == -1 and numpy.sign(relativeDir["y"]) == -1: return "bottomright"
            if numpy.sign(relativeDir["x"]) == 1 and numpy.sign(relativeDir["y"]) == -1: return "bottomleft"
            if numpy.sign(relativeDir["x"]) == 1 and numpy.sign(relativeDir["y"]) == 1: return "topleft"

    def return_flipped(self, dir):
        if dir == "top": return "bottom"
        if dir == "topright": return "bottomleft"
        if dir == "right": return "left"
        if dir == "bottomright": return "topleft"
        if dir == "bottom": return "top"
        if dir == "bottomleft": return "topright"
        if dir == "left": return "right"
        if dir == "topleft": return "bottomright"


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size, group):
        super().__init__(group)
        self.rect = pygame.Rect(pos, size)

    def update(self):
        pygame.draw.rect(settings.SCREEN, (35,35,35), self.rect)

def run():
    player = Player(position=(50,50), size=(50,50))
    
    def randWall():
        randPos = (random.randint(settings.RESOLUTION[0] / 4, settings.RESOLUTION[0] - settings.RESOLUTION[0] / 4),
                   random.randint(settings.RESOLUTION[1] / 4, settings.RESOLUTION[1] - settings.RESOLUTION[1] / 4))
        size = (50,50)
        return Wall(randPos, size, walls)

    gameWalls = [randWall() for _ in range(5)]

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        settings.SCREEN.fill((51, 51, 51))
        source = pygame.mouse.get_pos()
        inputs = pygame.key.get_pressed()

        player.update(inputs)
        walls.update()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run()