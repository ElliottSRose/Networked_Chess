import random
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

def flipCoin():
    side = [1, 0]
    return random.choice(side)

def negotiateMessage(clientSocket, message, playerList):
    # This function takes our recieved messages, and parses the first letter to identify the traffic type
    playerIndex = next((i for i, item in enumerate(playerList) if item["IP"] == clientSocket), None)
    if message[0] == "S":

        clientSocket.send("Players waiting for an opponent:\n".encode("utf-8"))

        for player in playerList:

            if player["Available"] == "yes":

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
        # set player's opponent
        playerList[playerIndex]['Opp_IP'] = playerList[opponentIndex]['IP']
        # Send request message to opponent to start game and start by default
        playerList[opponentIndex]['IP'].send("Play a game? Type Yes or No".encode('utf-8'))

    elif message[0:4] == 'Yes':

        result = flipCoin()

        if result == 1:

            playerList[playerIndex]['Opp_IP'].send("You've won the coin toss, your move".encode('utf-8'))
            playerList[playerIndex]['IP'].send("You've lost the coin toss, your opponent moves first".encode('utf-8'))

        else:
            playerList[playerIndex]['IP'].send("You've won the coin toss, your move".encode('utf-8'))
            playerList[playerIndex]['Opp_IP'].send("You've lost the coin toss, your opponent moves first".encode('utf-8'))

        playerList[playerIndex]['Available'] = 'no'
        opponentIndex = next((i for i, item in enumerate(playerList) if item["IP"] == playerList[playerIndex]['Opp_IP']), None)
        playerList[opponentIndex]['Available'] = 'no'

    elif message[0:4] == "exit":
        del playerList[playerIndex]

    else:
        playerList[playerIndex]['Opp_IP'].send(message.encode("utf-8"))


def receiveMessage(clientSocket):

    try:
        messageHeader = clientSocket.recv(HEADER_LENGTH)

        if not len(messageHeader):
            return False
        messageLength = int(messageHeader.decode('utf-8').strip())

        return {'header': messageLength, 'data': clientSocket.recv(messageLength)}

    except:

        return False

def threaded_game_session(p1, p2, srvr):
    p1Socket = p1[0]
    p2Socket = p2[0]
    #print("thread started")
    p1Socket.send(bytes("Welcome player1, you have the fist move", "utf-8"))
    p2Socket.send(bytes("Welcome player2, player1 has the first move", "utf-8"))

    while True:

        break

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

            playerList.append({"name": user['data'].decode('utf-8'), "IP": clientSocket, "Opp_IP": "null", "Available":"yes"})

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