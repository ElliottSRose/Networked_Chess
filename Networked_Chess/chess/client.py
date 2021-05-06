import board
import socket
import select
import errno
import sys

HEADER_LENGTH = 10
# IP = socket.gethostname()2
IP = 'localhost'
PORT = 54321

newGame = board.Board()
player = input("Player: ")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((IP, PORT))
clientSocket.setblocking(False)

# Prepare playerName and header and send them
# We need to encode playerName to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
playerName = player.encode('utf-8')
playerHeader = f"{len(playerName):<{HEADER_LENGTH}}".encode('utf-8')
clientSocket.send(playerHeader + playerName)


def parseMessage(message, game=newGame):
    if message[0] == 'G':
        # update board and print
        print(message[1:])
        newGame.move(message[1], int(message[2]), message[3], int(message[4]))
        newGame.printBoard()
    if message[0:3] == "Yes":
        newGame.printBoard()
        print("Type G and move data to send move(Ex: Ge2e4)")
    else:
        print(message)


# while True:
def awaitInput():
    # Wait for user to input a message
    message = input(f'{player} > ')
# If message is not empty - send it
    if message:
        parseMessage(message)
        message = message.encode('utf-8')
        messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        clientSocket.send(messageHeader + message)

while True:
    # awaitInput()
    socket_list = [sys.stdin, clientSocket]

    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(
        socket_list, [], [])

    for sock in read_sockets:
        # incoming message from remote server
        if sock == clientSocket:
            data = sock.recv(1024)
            if not data:
                print('\nDisconnected from server')
                break
            else:
                parseMessage(data.decode('utf-8'))
        else:
            awaitInput()

clientSocket.close()
#     try:
#         while True:
#             playerHeader = clientSocket.recv(HEADER_LENGTH)
#             if not len(playerHeader):
#                 print('Connection closed by the server')
#                 sys.exit()
#             playerLength = int(playerHeader.decode('utf-8').strip())
#             playerName = clientSocket.recv(playerLength).decode('utf-8')
#             messageHeader = clientSocket.recv(1024)
#             messageLength = int(messageHeader.decode('utf-8').strip())
#             print(messageHeader)
#             print(f'{playerName} > {message}')
#     except IOError as e:
#         # If we got different error code - something happened
#         if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
#             print('Reading error: {}'.format(str(e)))
#             sys.exit()
#
#         # We just did not receive anything
#         continue
#
#     except Exception as e:
#         print('Reading error: '.format(str(e)))
#         sys.exit()

# formatting needs
# message type: start, connect, game traffic
#
# 1. message formatting
# 2. connect players
# 3. parse data and make moves
# 4. disconnect after game end
