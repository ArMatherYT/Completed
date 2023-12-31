import math
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((400, 400))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True
CLOCK = pygame.time.Clock()
FPS = 60
SPEED = 0.5
TIME = 0

N = 100
FACTOR = 2
RADIUS = 175

while RUNNING:
    SCREEN.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    for n in range(N):
        start_angle = 2*math.pi*n/N 
        end_index = (FACTOR*n)%N
        end_angle = 2*math.pi*(end_index)/N

        x0 = WIDTH/2 + RADIUS*math.cos(start_angle)
        y0 = HEIGHT/2 + RADIUS*math.sin(start_angle)
        x1 = WIDTH/2 + RADIUS*math.cos(end_angle)
        y1 = HEIGHT/2 + RADIUS*math.sin(end_angle)

        pygame.draw.circle(SCREEN, 'white', (x0, y0), 2)
        pygame.draw.circle(SCREEN, 'white', (x1, y1), 2)
        pygame.draw.line(SCREEN, 'white', (x0, y0), (x1, y1))

    pygame.display.update()
    TIME = SPEED*CLOCK.tick(FPS)/1000
    FACTOR += TIME