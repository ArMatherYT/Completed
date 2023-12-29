import pygame
import random

pygame.init()
SCREEN = pygame.display.set_mode((400, 400))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True
CLOCK = pygame.time.Clock()
FPS = 120

CORNERS = (
    pygame.Vector2(WIDTH/2, 20),
    pygame.Vector2(20, HEIGHT-20),
    pygame.Vector2(WIDTH-20, HEIGHT-20),
)

x = random.randint(-50, 50)
y = random.randint(-50, 50)
CURRENT = pygame.Vector2(x + WIDTH/2, y + HEIGHT/2)
for corner in CORNERS:
    pygame.draw.circle(SCREEN, 'white', corner, 1)

while RUNNING:
    # SCREEN.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    
    pygame.draw.circle(SCREEN, 'white', CURRENT, 1)
    random_corner = random.choice(CORNERS)
    CURRENT = CURRENT.lerp(random_corner, 0.5)

    pygame.display.update()
    CLOCK.tick(FPS)