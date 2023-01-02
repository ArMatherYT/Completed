"""
SNAKE GAME WITH PYGAME MODULE AND OOP.
PART 1: BASIC ENGINE
BY ARMANDO CHAPARRO 01/01/2023
"""

from random import randint
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1000, 1000))
WIDTH, HEIGHT = SCREEN.get_size()
CLOCK = pygame.time.Clock()

# SETTING TITLE
pygame.display.set_caption('Snake By Armando Chaparro')

# GAME CONFIGURATION
GRID_WIDTH = GRID_HEIGHT = 15
SQUARE_WIDTH = WIDTH // GRID_WIDTH
SQUARE_HEIGHT = HEIGHT // GRID_HEIGHT
FPS = 10

# COLORS
GREEN = pygame.Vector3(145, 190, 72)        #91be48
LIGHT_GREEN = pygame.Vector3(171, 214, 81)  #abd651
DARK_BLUE = pygame.Vector3(0, 0, 255)       #0000ff
LIGHT_BLUE = pygame.Vector3(74, 125, 250)   #4a7dfa
RED = pygame.Vector3(255, 0, 0)             #ff0000
YELLOW = pygame.Vector3(255, 255, 0)        #ffff00


class Food:
    """Food class"""
    def __init__(self):
        self.respawn()

    def respawn(self) -> None:
        """Manages the position and the food rect for collision"""
        x, y = randint(0, GRID_WIDTH - 1), randint(0, GRID_WIDTH - 1)
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(
            x * SQUARE_WIDTH, y * SQUARE_HEIGHT,
            SQUARE_WIDTH, SQUARE_HEIGHT
        )

    def show(self) -> None:
        """Draws the food on screen"""
        pygame.draw.rect(SCREEN, RED, self.rect)
        pygame.draw.rect(SCREEN, LIGHT_GREEN, self.rect, width=1)

    def collide(self, pos: pygame.Vector2) -> bool:
        """Checks if the given position is the same as the food"""
        return self.pos == pos


class Snake:
    """Snake class"""
    def __init__(self):

        self.left = pygame.Vector2(-1, 0)
        self.right = pygame.Vector2(1, 0)
        self.up = pygame.Vector2(0, -1)
        self.down = pygame.Vector2(0, 1)
        self.dir = self.left

        self.respawn()

    def respawn(self) -> None:
        """Manages the Snake pieces and direction"""
        self.pieces = [pygame.Vector2(10, 10)]
        self.dir = self.left
    
    def show(self) -> None:
        """Draws the Snake on screen piece by piece"""
        for (x, y) in self.pieces:
            rect = (x * SQUARE_WIDTH, y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
            pygame.draw.rect(SCREEN, DARK_BLUE, rect)
            pygame.draw.rect(SCREEN, LIGHT_GREEN, rect, width=1)
    
    def update(self) -> None:
        """Updates the Snake's pieces and checks for collision or food"""
        self.pieces.insert(0, self.pieces[0] + self.dir)
        self.pieces.pop(-1)

        self.check_food()
        self.check_collision()
    
    def check_collision(self) -> None:
        """Respawns if the Snake collides with itself or it's out of bounds"""
        if any([
            self.pieces[0].x < 0, self.pieces[0].x == GRID_WIDTH,
            self.pieces[0].y < 0, self.pieces[0].y == GRID_HEIGHT,
            self.pieces.count(self.pieces[0]) != 1
        ]):
            self.respawn()
    
    def check_food(self) -> None:
        """Updates the food and the snake if the Snake collides with food"""
        if FOOD.collide(self.pieces[0]):
            FOOD.respawn()
            self.pieces.insert(0, self.pieces[0] + self.dir)

    def keydown(self, key: int) -> None:
        """Manages the direction based on the key"""
        if key == pygame.K_LEFT and self.dir != self.right:
            self.dir = self.left
        elif key == pygame.K_RIGHT and self.dir != self.left:
            self.dir = self.right
        elif key == pygame.K_DOWN and self.dir != self.up:
            self.dir = self.down
        elif key == pygame.K_UP and self.dir != self.down:
            self.dir = self.up


def main() -> None:
    """Main loop"""
    while True:
        SCREEN.fill(LIGHT_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                SNAKE.keydown(event.key)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                index = x + y * GRID_WIDTH
                if index % 2:
                    continue
                rect = (x * SQUARE_WIDTH, y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
                pygame.draw.rect(SCREEN, GREEN, rect)

        SNAKE.update()
        SNAKE.show()
        FOOD.show()

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    SNAKE = Snake()
    FOOD = Food()
    main()
