import pygame

pygame.init()
SCREEN = pygame.display.set_mode((900, 900))
WIDTH, HEIGHT = SCREEN.get_size()
SIZE = WIDTH // 3
FONT = pygame.font.SysFont('Comic Sans', SIZE)


class Board:
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self.turn = 'X'
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def show(self) -> None:
        for y in range(3):
            for x in range(3):
                if not self.board[y][x]: continue
                text = FONT.render(self.board[y][x], True, 'white')
                rect = text.get_rect(center=(
                    (x+0.5)*SIZE, (y+0.5)*SIZE
                ))

                SCREEN.blit(text, rect)
    
    def click(self, mx, my):
        x, y = int(mx / SIZE), int(my / SIZE)
        if self.board[y][x]: return

        self.board[y][x] = self.turn
        if self.check_win(): print(f'winner: {self.turn}')
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
        SCREEN.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN: BOARD.click(*event.pos)
        
        BOARD.show()

        for y in range(3):
            pygame.draw.line(SCREEN, 'white', (0, y*SIZE), (WIDTH, y*SIZE))
        for x in range(3):
            pygame.draw.line(SCREEN, 'white', (x*SIZE, 0), (x*SIZE, HEIGHT))

        pygame.display.update()


if __name__ == '__main__':
    main()