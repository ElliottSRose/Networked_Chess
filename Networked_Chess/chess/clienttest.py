import board
import socket
import errno
import sys
import re
import pygame

HEADER_LENGTH = 10
IP = 'localhost'
PORT = 54321
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP, PORT))
clientSocket.setblocking(False)
newGame = board.Board()

pygame.init()
screen_width = 1100
screen_height = 800
background_color = (0, 0, 0)
text_color = (109, 247, 246)
font = pygame.font.SysFont("helvetica", 20)
font2 = pygame.font.SysFont("helvetica", 14)
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(background_color)
pygame.display.set_caption("TCP Chess")
clock = pygame.time.Clock()
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
textfield = ["Enter your name", '']
text = ''
side = ''

def letter_match(strg, search=re.compile(r'[^a-h]').search):
    return not bool(search(strg))


def number_match(strg, search=re.compile(r'[^1-8]').search):
    return not bool(search(strg))


def validateMove(message):
    return letter_match(message[1]) and number_match(message[2]) and letter_match(message[3]) and number_match(
        message[4])


def parseMessage(message, game=newGame):
    valid = True
    if message[0] == 'G':
        if validateMove(message):
            # update board and print
            add_wrapped_text(message[1:])
            newGame.move(message[1], int(message[2]), message[3], int(message[4]))
            if not (newGame.K.alive):
                print("Black Wins")
                add_wrapped_text("Black Wins")
            elif not (newGame.k.alive):
                add_wrapped_text("White Wins")
                print("White Wins")
        else:
            print("Invalid move")
            add_wrapped_text("Invalid move")
            valid = False
    elif message[7:10] == "won":
        add_wrapped_text(message)
        add_wrapped_text("Your color is White")
        add_wrapped_text("Type G and move data to send move(Ex: Ge2e4)")
    else:
        add_wrapped_text(message)
        print(message)
    return valid


def send_input(messageOutput):
    if parseMessage(messageOutput):
        messageOutput = messageOutput.encode('utf-8')
        messageHeader = f"{len(messageOutput):<{HEADER_LENGTH}}".encode('utf-8')
        clientSocket.send(messageHeader + messageOutput)


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
    x = x * 100
    y = y * 100
    screen.blit(img, (x, y))


def draw_board(matrix):
    screen.fill((0, 0, 0))
    screen.blit(board_image, (0, 0))
    for i in range(8):
        for j in range(8):
            if matrix[i][j]:
                piece = matrix[i][j]
                draw_piece(piece, j, i)
    txt_surface = font.render(text, True, text_color)
    screen.blit(txt_surface, (820, 770))
    draw_textfield(textfield)
    pygame.display.update()


def add_wrapped_text(intext):
    if len(intext) > 38:
        while len(intext) > 38:
            textfield.append(intext[0:38] + '-')
            intext = intext[38:]
    textfield.append(intext)
    textfield.append('')


def draw_textfield(textfield):
    x = 820
    y = 20
    while len(textfield) > 40:
        textfield.pop(0)
    for i in textfield:
        line = font2.render(i, True, text_color)
        screen.blit(line, (x, y))
        y += 16


def run():
    global text
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clientSocket.close()
                print('\nDisconnected from server')
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text:
                        send_input(text)
                        #add_wrapped_text(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_DELETE:
                    text = text[:-1]
                else:
                    text += event.unicode
        draw_board(newGame.convertBoard())
        pygame.display.update()
        clock.tick(20)

        try:
            while True:
                data = clientSocket.recv(1024)
                if data:
                    parseMessage(data.decode('utf-8'))
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            # We just did not receive anything
            continue
        except KeyboardInterrupt:
            continue
        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()

    clientSocket.close()
    print('\nDisconnected from server')

run()

