import socket
import select


class Server:
    FOR_READ = list()
    FOR_WRITE = list()

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 7897

    BUFFER = {}
    CLIENTS = []

    srv_sock = None
    R, W, ERR = list(), list(), list()
    client, address = None, None
    message, data = "", ""

    def plug(self):
        self.srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv_sock.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.srv_sock.listen(10)
        self.srv_sock.setblocking(False)
        self.FOR_READ.append(self.srv_sock)

    def add_client(self, r):
        self.client, self.address = self.srv_sock.accept()
        self.client.setblocking(False)
        self.FOR_READ.append(self.client)
        self.CLIENTS.append(self.client)

    def close_client(self, r):
        self.FOR_READ.remove(r)
        self.CLIENTS.remove(r)

    def read(self, list_r):
        for r in list_r:
            if r is self.srv_sock:
                self.add_client(r)
            else:
                self.data = r.recv(2048)
                self.data = self.data.decode("utf-8")
                if "disconnected" in self.data:
                    self.close_client(r)
            self.BUFFER[r.fileno()] = self.data
            self.FOR_WRITE.append(r)

    def write(self, list_w):
        for w in list_w:
            self.data = self.BUFFER[w.fileno()]
            for client in self.CLIENTS:
                if client != w:
                    client.send(self.data.encode("utf-8"))

    def processes(self):
        while True:
            self.R, self.W, self.ERR = select.select(self.FOR_READ, self.FOR_WRITE, self.FOR_READ)
            self.FOR_WRITE = list()
            self.read(self.R)
            self.write(self.W)
