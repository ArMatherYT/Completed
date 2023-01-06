import pygame

# PYGAME CONFIGURATION
pygame.init()
SCREEN = pygame.display.set_mode((900, 900))
WIDTH, HEIGHT = SCREEN.get_size()
BIG_FONT = pygame.font.SysFont('Arial', WIDTH//3)
SMALL_FONT = pygame.font.SysFont('Arial', WIDTH//6)
SIZE = WIDTH / 3

# COLORS
BLUE = (3, 78, 101)     #034e65
GREEN = (0, 255, 0)     #00ff00
ORANGE = (255, 127, 0)  #ff7f00

# BOARD CLASS
class Board:
    """Board class"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Resets the board"""
        self.turn = 'X'
        self.winner = None
        self.win_rect = None
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def show(self) -> None:
        """Draws the board on screen"""
        for y in range(3):
            for x in range(3):
                if not self.board[y][x]: continue
                color = ORANGE if self.board[y][x] == 'O' else GREEN
                text = BIG_FONT.render(self.board[y][x], True, color)
                rect = text.get_rect(center=(
                    (x+0.5) * SIZE, (y+0.5) * SIZE
                ))
                SCREEN.blit(text, rect)
        if self.winner: SCREEN.blit(self.winner, self.win_rect)
        
    
    def click(self, mx: int, my: int) -> None:
        """Manages the click on the board"""
        if self.winner: return
        x, y = int(mx/SIZE), int(my/SIZE)
        if self.board[y][x]: return
        self.board[y][x] = self.turn
        if self.check_win():
            self.winner = SMALL_FONT.render(f'Winner: {self.turn}', True, 'white')
            self.win_rect = self.winner.get_rect(centerx=WIDTH/2, centery=HEIGHT/2)
        self.turn = 'X' if self.turn == 'O' else 'O'

    def check_win(self):
        """All the logic to check the winner"""
        # ROWS
        if self.board[0][0] == self.board[0][1] == self.board[0][2] == self.turn:
            return True
        if self.board[1][0] == self.board[1][1] == self.board[1][2] == self.turn:
            return True
        if self.board[2][0] == self.board[2][1] == self.board[2][2] == self.turn:
            return True
        
        # COLUMNS
        if self.board[0][0] == self.board[1][0] == self.board[2][0] == self.turn:
            return True
        if self.board[0][1] == self.board[1][1] == self.board[2][1] == self.turn:
            return True
        if self.board[0][2] == self.board[1][2] == self.board[2][2] == self.turn:
            return True
        
        # DIAGONALS
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.turn:
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.turn:
            return True

        return False


def main() -> None:
    """Main loop"""
    BOARD = Board()

    while True:
        SCREEN.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN: BOARD.click(*event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: BOARD.reset()
        
        # DRAWING BOARD
        for y in range(1, 3):
            pygame.draw.line(SCREEN, 'white', (WIDTH*0.05, y*SIZE), (WIDTH*0.95, y*SIZE), width=3)
        
        for x in range(1, 3):
            pygame.draw.line(SCREEN, 'white', (x*SIZE, HEIGHT*0.05), (x*SIZE, HEIGHT*0.95), width=3)
        
        BOARD.show()

        pygame.display.update()


if __name__ == '__main__':
    main()