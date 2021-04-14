import socket
import selectors


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4321))
sel = selectors.DefaultSelector()
#s.setblocking(False)

# below is the function to set the number of clients that can access the
# server. python documentation can provide us info on how to use it to
# create a queue of clients and pair into games.
s.listen(6)

class Server:

    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established !")
        clientsocket.send(bytes("welcome to the server", "utf-8"))

if __name__ == '__main__':
    Server()