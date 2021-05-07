import pygame
import board

pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("TCP Chess")
clock = pygame.time.Clock()
run = True

board_image = pygame.image.load("images/board.png")
bPawn = pygame.image.load("images/pawn_black.png")
wPawn = pygame.image.load("images/pawn_white.png")
bBishop = pygame.image.load("images/bishop_black.png")
wBishop = pygame.image.load("images/bishop_white.png")
bKnight = pygame.image.load("images/knight_black.png")
wKnight = pygame.image.load("images/knight_white.png")
bRook = pygame.image.load("images/rook_black.png")
wRook = pygame.image.load("images/rook_white.png")
bQueen = pygame.image.load("images/queen_black.png")
wQueen = pygame.image.load("images/queen_white.png")
bKing = pygame.image.load("images/king_black.png")
wKing = pygame.image.load("images/king_white.png")

game = board.Board()
mat = game.convertBoard()
game.printBoard()
print(mat)

mat_test = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'], ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]


def draw_piece(piece, x, y):
    img = pygame.image
    pieces = {
        'P': wPawn,
        'p': bPawn,
        'B': wBishop,
        'b': bBishop,
        'N': wKnight,
        'n': bKnight,
        'R': wRook,
        'r': bRook,
        'Q': wQueen,
        'q': bQueen,
        'K': wKing,
        'k': bKing
    }
    img = pieces.get(piece)
    x = x*100
    y = y*100
    screen.blit(img, (x, y))


def draw_board(matrix):
    screen.blit(board_image, (0, 0))
    for i in range(8):
        for j in range(8):
            if matrix[i][j]:
                piece = matrix[i][j]
                draw_piece(piece, i, j)
    pygame.display.update()

def run_gui():
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_board(mat_test)
        pygame.display.update()
        clock.tick(20)
    pygame.quit()
    quit()

run_gui()