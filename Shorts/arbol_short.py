import math
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((400, 400))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True
TIME = 0
CLOCK = pygame.time.Clock()
FPS = 60

class Branch:
    def __init__(self, length, angle, parent=None):
        self.length = length
        self.angle = angle
        self.color = 'brown' if length > 25 else 'green'
        self.width = 3 if self.color == 'brown' else 1

        if parent:
            self.x0 = parent.x1
            self.y0 = parent.y1
        else:
            self.x0 = WIDTH/2
            self.y0 = HEIGHT

        angle = math.radians(self.angle)
        self.x1 = self.x0 + self.length*math.sin(angle)
        self.y1 = self.y0 - self.length*math.cos(angle)
    
        self.branches = []
        self.grow_factor = 0.75
        self.grow_angle = 20

    def draw(self):
        pygame.draw.line(SCREEN, self.color, (self.x0, self.y0), (self.x1, self.y1), width=self.width)
        for branch in self.branches:
            branch.draw()
    
    def grow(self):
        if self.length < 10: return
        if self.branches:
            for branch in self.branches:
                branch.grow()
        else:
            left = Branch(self.length*self.grow_factor, self.angle-self.grow_angle, self)
            right = Branch(self.length*self.grow_factor, self.angle+self.grow_angle, self)
            self.branches.append(left)
            self.branches.append(right)


ROOT = Branch(100, 0)

i = 0
while RUNNING:
    SCREEN.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    
    ROOT.draw()
    pygame.display.update()
    TIME += CLOCK.tick(FPS)/1000
    i += 4
    if i % FPS == 0:
    	ROOT.grow()