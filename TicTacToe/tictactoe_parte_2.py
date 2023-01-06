import pygame

pygame.init()
SCREEN = pygame.display.set_mode((900, 900))
WIDTH, HEIGHT = SCREEN.get_size()
SIZE = WIDTH // 3
BIG_FONT = pygame.font.SysFont('Arial', SIZE)
SMALL_FONT = pygame.font.SysFont('Arial', SIZE//2)

# COLORS
BLUE = (3, 78, 101)     #034e65
GREEN = (0, 255, 0)     #00ff00
ORANGE = (255, 127, 0)  #ff7f00


class Board:
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self.turn = 'X'
        self.winner = None
        self.win_rect = None
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def show(self) -> None:
        for y in range(3):
            for x in range(3):
                if not self.board[y][x]: continue
                color = ORANGE if self.board[y][x] == 'X' else GREEN
                text = BIG_FONT.render(self.board[y][x], True, color)
                rect = text.get_rect(center=(
                    (x+0.5)*SIZE, (y+0.5)*SIZE
                ))

                SCREEN.blit(text, rect)
        
        if self.winner:
            message = f'{self.winner} WINS!'
            winner = SMALL_FONT.render(message, True, 'white')
            win_rect = winner.get_rect(center=(WIDTH/2, HEIGHT/2))
            SCREEN.blit(winner, win_rect)
    
    def click(self, mx, my):
        if self.winner: return
        x, y = int(mx / SIZE), int(my / SIZE)
        if self.board[y][x]: return

        self.board[y][x] = self.turn
        if self.check_win(): self.winner = self.turn
        self.turn = 'X' if self.turn == 'O' else 'O'
    
    def check_win(self):
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
        
        # DIAGONAL
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.turn:
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.turn:
            return True
        
        return False


def main() -> None:

    BOARD = Board()

    while True:
        SCREEN.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN: BOARD.click(*event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BOARD.reset()
        
        BOARD.show()

        for y in range(1, 3):
            pygame.draw.line(
                SCREEN, 'white',
                (SIZE*0.05, y*SIZE), (WIDTH-SIZE*0.05, y*SIZE),
                width=3
            )
        for x in range(1, 3):
            pygame.draw.line(
                SCREEN, 'white',
                (x*SIZE, SIZE*0.05), (x*SIZE, HEIGHT-SIZE*0.05),
                width=3
            )

        pygame.display.update()


if __name__ == '__main__':
    main()