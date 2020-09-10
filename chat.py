import socket
import select

class Socket:
    def __init__(self, addr, port=8888):
        self.addr = addr
        self.port = port

        self.clients = []

        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self):
        self._sock.bind(('0.0.0.0', self.port)) #bind create server
        self._sock.listen()

        while True:
            sock_list = self.clients + [self._sock]
            r_event, _, _ = select.select(sock_list, [], [])

            for sock in r_event:
                if sock == self._sock:
                    # Accept new connections
                    conn = self.accept()
                    self.clients.append(conn)
                else:
                    self.handledata(sock)

    def del_client(self, client):
        self.clients.remove(client)

    def handledata(self, sock):
        data = None
        try:
            data = sock.recv(128)
        except:
            pass
        if not data:
            print('Kicking off a client')
            self.del_client(sock)
            return

        for client in self.clients:
            if client == sock:
                continue
            client.send(data)

    def accept(self):
        (conn, address) = self._sock.accept() #wait connect
        print("connection from " + str(address))
        return conn


    def connect(self):
        raise NotImplementedError

server = Socket('127.0.0.1')
server.listen()
