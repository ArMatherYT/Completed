"""
SNAKE GAME WITH PYGAME MODULE AND OOP.
PART 2: STYLE
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


def color_lerp(a: pygame.Vector3, b: pygame.Vector3, t: float) -> pygame.Vector3:
    """Returns an interpolated color based on t value"""
    return a + (b - a) * t


class Food:
    """Food class"""
    def __init__(self):

        self.time = 0
        self.delta_time = 1
        self.anim_time = 4
        self.color = RED

        self.respawn()

    def respawn(self) -> None:
        """Manages the position and the food rect for collision"""
        x, y = randint(0, GRID_WIDTH - 1), randint(0, GRID_WIDTH - 1)
        self.pos = pygame.Vector2(x, y)
        if self.pos not in SNAKE.pieces:
            self.rect = pygame.Rect(
                x * SQUARE_WIDTH, y * SQUARE_HEIGHT,
                SQUARE_WIDTH, SQUARE_HEIGHT
            )
        else: self.respawn()

    def update(self) -> None:
        """Updates the color of the food based on time"""
        if self.time < 0 or self.time > self.anim_time:
            self.delta_time *= -1
        self.time += self.delta_time
        self.color = color_lerp(RED, YELLOW, max(0, self.time) / 10)

    def show(self) -> None:
        """Draws the food on screen"""
        pygame.draw.rect(SCREEN, self.color, self.rect)

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
        for i, (x, y) in enumerate(reversed(self.pieces)):
            porcent = i / len(self.pieces)
            color = color_lerp(DARK_BLUE, LIGHT_BLUE, porcent)
            rect = (x * SQUARE_WIDTH, y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
            pygame.draw.rect(SCREEN, color, rect)

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
        FOOD.update()
        SNAKE.show()
        FOOD.show()

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    SNAKE = Snake()
    FOOD = Food()
    main()
