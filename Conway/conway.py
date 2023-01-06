"""
Conway's game of life is a 1-player game also called cellular automata.
"""

import pygame
import numpy as np

# PYGAME CONFIG
pygame.init()
pygame.display.set_caption("CONWAY'S GAME OF LIFE")
SCREEN = pygame.display.set_mode((1600, 800))
WIDTH, HEIGHT = SCREEN.get_size()
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 30)

# GAME CONFIG
FPS = 10
GRID_WIDTH = 32
GRID_HEIGHT = 16
SQUARE_WIDTH = WIDTH / GRID_WIDTH
SQUARE_HEIGHT = HEIGHT / GRID_HEIGHT

# COLORS
BORN = (0, 255, 0)      #00ff00
ALIVE = (255, 255, 255) #ffffff
DEAD = (255, 0, 0)      #ff0000
VOID = (0, 0, 0)        #000000
GRID = (50, 50, 50)     #323232

# BOARD
class Board:
    """Board class"""
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """Resets the configuration"""
        self.board = np.zeros((GRID_WIDTH, GRID_HEIGHT))
        self.pause = True
        self.show_next = False
    
    def click(self, mx: int, my: int) -> None:
        """Updates the board when clicked"""
        if not self.pause: return
        x = int(mx / SQUARE_WIDTH)
        y = int(my / SQUARE_HEIGHT)
        self.board[x, y] = 0 if self.board[x, y] else 1
    
    def get_neighbours(self, cx: int, cy: int) -> int:
        """Returns how many neightbours are around"""
        neighbours = 0
        for h in [-1, 0, 1]:
            for w in [-1, 0, 1]:
                if w == 0 and h == 0: continue
                x = (cx + w) % GRID_WIDTH
                y = (cy + h) % GRID_HEIGHT
                neighbours += self.board[x, y]
        return int(neighbours)
    
    def update(self) -> None:
        """Manages the logic of the game"""
        if self.pause: return
        new_board = np.zeros((GRID_WIDTH, GRID_HEIGHT))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbours = self.get_neighbours(x, y)
                if neighbours < 2 or neighbours > 3:
                    new_board[x, y] = 0
                elif neighbours == 3 and self.board[x, y] == 0:
                    new_board[x, y] = 1
                else:
                    new_board[x, y] = self.board[x, y]
        self.board = new_board.copy()

    def show(self) -> None:
        """Draws the cells on screen"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = (
                    x * SQUARE_WIDTH, y * SQUARE_HEIGHT,
                    SQUARE_WIDTH, SQUARE_HEIGHT
                )

                current = self.board[x, y]
                neighbours = self.get_neighbours(x, y)
                match self.show_next, current, neighbours:
                    case False, 0, _: color = VOID
                    case False, 1, _: color = ALIVE
                    case True, 0, 3: color = BORN
                    case True, 1, 2|3: color = ALIVE
                    case True, 1, _: color = DEAD
                    case _: color = VOID
                
                pygame.draw.rect(SCREEN, color, rect)
                pygame.draw.rect(SCREEN, GRID, rect, width=1)


def main() -> None:
    """Main loop"""
    global FPS
    BOARD = Board()

    while True:
        # SCREEN REFRESH
        SCREEN.fill('black')

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                BOARD.click(*event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BOARD.pause = not BOARD.pause
                    pygame.display.set_caption(
                        'PAUSE' if BOARD.pause else 'RUNNING'
                    )
                elif event.key == pygame.K_n:
                    BOARD.show_next = not BOARD.show_next
                elif event.key == pygame.K_r:
                    BOARD.reset()
                elif event.key == pygame.K_PLUS and FPS < 60:
                    FPS += 1
                elif event.key == pygame.K_MINUS and FPS > 1:
                    FPS -= 1
        
        # BOARD
        BOARD.update()
        BOARD.show()
        
        # UPDATE THE WINDOW
        fps = FONT.render(str(FPS), True, 'white')
        SCREEN.blit(fps, (0, 0))
        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()