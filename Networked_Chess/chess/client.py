import socket
import select
import errno

HEADER_LENGTH = 10
# IP = socket.gethostname()
IP = 'localhost'
PORT = 54321


player = input("Player: ")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((IP, PORT))
clientSocket.setblocking(False)

# Prepare playerName and header and send them
# We need to encode playerName to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
playerName = player.encode('utf-8')
playerHeader = f"{len(playerName):<{HEADER_LENGTH}}".encode('utf-8')
clientSocket.send(playerHeader + playerName)

while True:

    # Wait for user to input a message
    message = input(f'{player} > ')

    # If message is not empty - send it
    if message:
    
        message = message.encode('utf-8')
        messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        clientSocket.send(messageHeader + message)

    try:
        while True:

            playerHeader = clientSocket.recv(HEADER_LENGTH)

            if not len(playerHeader):
                print('Connection closed by the server')
                sys.exit()

            playerLength = int(playerHeader.decode('utf-8').strip())

            playerName = clientSocket.recv(playerLength).decode('utf-8')

            messageHeader = clientSocket.recv(HEADER_LENGTH)
            messageLength = int(messageHeader.decode('utf-8').strip())
            message = clientSocket.recv(messageLength).decode('utf-8')

            # Print message
            print(f'{playerName} > {message}')

    except IOError as e:
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()