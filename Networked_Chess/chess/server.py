import socket
import selectors
import select

HEADER_LENGTH = 10

# IP = socket.gethostname()
IP = 'localhost'
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen()
socketsList = [s]
clients = {}
playerList = []

def negotiateMessage(clientSocket, message):
    if message == "Start":
        clientSocket.send()

def receiveMessage(clientSocket):

    try:
        messageHeader = clientSocket.recv(HEADER_LENGTH)

        if not len(messageHeader):
            return False
        messageLength = int(messageHeader.decode('utf-8').strip())

        return {'header': messageHeader, 'data': clientSocket.recv(messageLength)}

    except:

        return False

while True:

    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)

    # Iterate over notified sockets
    for notifiedSocket in readSockets:
        if notifiedSocket == s:

            clientSocket, client_address = s.accept()

            user = receiveMessage(clientSocket)

            if user is False:
                continue
            socketsList.append(clientSocket)


            clients[clientSocket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

            playerList.append({"name": user['data'].decode('utf-8'), "IP": client_address})

            for player in playerList:
                message = "Available Players:\n Player: " + str(player["name"]) + "\n"
                message = message.encode('utf-8')
            # messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            # clientSocket.send(messageHeader + message)
                clientSocket.send(message)
        else:

            message = receiveMessage(notifiedSocket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notifiedSocket]['data'].decode('utf-8')))

                socketsList.remove(notifiedSocket)

                del clients[notifiedSocket]

                continue

            user = clients[notifiedSocket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            # clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])
            negotiateMessage(clientSocket, message)
            for clientSocket in clients:

                if clientSocket != notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notifiedSocket in exceptionSockets:

        socketsList.remove(notifiedSocket)
        del clients[notifiedSocket]

