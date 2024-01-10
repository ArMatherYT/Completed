import math
from math import sin, cos
import pygame
import random
from random import randint
from pygame.mixer import Sound

pygame.init()
SCREEN = pygame.display.set_mode((400, 400))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True
CLOCK = pygame.time.Clock()
FPS = 60
DT = 0
COLORS = (
    '#ff0000',
    '#ff7f00',
    '#ffff00',
    '#7fff00',
    '#00ff00',
    '#00ff7f',
    '#00ffff',
    '#007fff',
    '#0000ff',
    '#7f00ff',
    '#ff00ff',
    '#ff007f'
)


class Particle:
    def __init__(
        self, x: float, y: float, angle: int
    ):

        angle = math.radians(angle)
        self.x = x
        self.y = y
        self.speed = randint(50, 100)
        self.dx = self.speed*cos(angle)
        self.dy = self.speed*sin(angle)
        self.color = random.choice(COLORS)
    
    def draw(self) -> None:
        x = int(self.x)
        y = int(self.y)
        SCREEN.set_at((x, y), self.color)

    def update(self) -> None:
        self.x += self.dx * DT
        self.y += self.dy * DT


class Rocket:
    sound = Sound('recursos/firework.wav')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.particles = []
        self.speed = randint(100, 400)
        self.max_height = randint(0, 100)
    
    def update(self) -> bool:
        for particle in self.particles:
            particle.update()
        if self.particles: return
        self.y -= self.speed * DT
        if self.y <= self.max_height:
            return self.explode()
        return False
        
    def explode(self) -> True:
        self.particles = [
            Particle(self.x, self.y, i)
            for i in range(360)
        ]
        self.sound.play()
        return True
    
    def draw(self) -> None:
        for particle in self.particles:
            particle.draw()
        if self.particles: return
        pygame.draw.rect(
            SCREEN, 'red',
            (self.x-2, self.y, 4, 10)
        )


class RocketCluster:
    def __init__(self):
        self.rockets = [
            Rocket(
                randint(10, WIDTH-10),
                HEIGHT+100
            )
            for _ in range(5)
        ]
    
    def update(self) -> None:
        for rocket in self.rockets:
            if not rocket.update(): continue
            x = randint(10, WIDTH-10)
            new = Rocket(x, HEIGHT+100)
            self.rockets.append(new)
            if len(self.rockets) > 15:
                self.rockets.pop(0)

    def draw(self) -> None:
        for rocket in self.rockets:
            rocket.draw()


CLUSTER = RocketCluster()

while RUNNING:
    SCREEN.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    
    CLUSTER.update()
    CLUSTER.draw()

    pygame.display.update()
    DT = CLOCK.tick(FPS) / 1000