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

def negotiateMessage(clientSocket, message, playerList):
    # This function takes our recieved messages, and parses the first letter to identify the traffic type
    if message[0] == "S":

        for player in playerList:

            message = "Available: " + str(player["name"]) + "\n"

            message = message.encode('utf-8')

            clientSocket.send(message)

        clientSocket.send("Type C and opponent name to challenge(Ex: CJames to play James).".encode("utf-8"))

    elif message[0] == "C":
        # get name of opponent
        opponent = message[1:]
        # find opponents index
        opponentIndex = next((i for i, item in enumerate(playerList) if item["name"] == opponent), None)
        # set opponent's opponent
        playerList[opponentIndex]['Opp_IP'] = clientSocket
        # find player's index
        playerIndex = next((i for i, item in enumerate(playerList) if item["IP"] == clientSocket), None)
        # set player's opponent
        playerList[playerIndex]['Opp_IP'] = playerList[opponentIndex]['IP']
        # Send request message to opponent to start game and start by default
        playerList[opponentIndex]['IP'].send("Play a game? Type Yes or No".encode('utf-8'))
    # if no, disconnect players
    if message[0] =='G':

        playerIndex = next((i for i, item in enumerate(playerList) if item["IP"] == clientSocket), None)

        playerList[playerIndex]['Opp_IP'].send(message.encode('utf-8'))


def receiveMessage(clientSocket):

    try:
        messageHeader = clientSocket.recv(HEADER_LENGTH)

        if not len(messageHeader):
            return False
        messageLength = int(messageHeader.decode('utf-8').strip())

        return {'header': messageLength, 'data': clientSocket.recv(messageLength)}

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

            playerList.append({"name": user['data'].decode('utf-8'), "IP": clientSocket, "Opp_IP": "null"})

            clientSocket.send("You've been added to the waiting queue. Type S to see available players".encode("utf-8"))

        else:

            message = receiveMessage(notifiedSocket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notifiedSocket]['data'].decode('utf-8')))

                socketsList.remove(notifiedSocket)

                del clients[notifiedSocket]

                continue

            user = clients[notifiedSocket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            negotiateMessage(notifiedSocket, message['data'].decode("utf-8"), playerList)
    #         for clientSocket in clients:
    #             if clientSocket != notifiedSocket:
    #                 clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])
    #
    # for notifiedSocket in exceptionSockets:
    #
    #     socketsList.remove(notifiedSocket)
    #     del clients[notifiedSocket]

