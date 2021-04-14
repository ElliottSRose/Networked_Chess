import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4321))
#s.setblocking(False)


class Client:

    def newClient(self):
        while True:
            msg = s.recv(1024)
            print(msg.decode("utf-8"))
            move = input("Please enter move: ")
            s.sendto((bytes(move, "utf-8")), (socket.gethostname(), 4321))

if __name__ == '__main__':
    Client().newClient()
