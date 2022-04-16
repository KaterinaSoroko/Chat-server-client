import socket


class Client:
    HOST = '127.0.0.1'
    PORT = 7897
    cl_sock = None
    message, data = "", ""

    def __init__(self):
        self.name = input("Введите ваше имя: ")
        print('Для выхода из чата наберите: `q`.')

    def connected(self):
        self.cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cl_sock.connect((self.HOST, self.PORT))
        self.message = "New client: {}\n".format(self.name)
        self.cl_sock.sendall(self.message.encode('utf-8'))

    def read(self):
        self.message = input('Ваше сообщение >>> ')
        if self.message != "":
            if self.message.lower() == 'q':
                self.message = "{} disconnected\n".format(self.name)
                self.cl_sock.sendall(self.message.encode('utf-8'))
                return True
            else:
                message = "{} wrote: {}\n".format(self.name, self.message)
                self.cl_sock.sendall(message.encode('utf-8'))

    def write(self):
        self.data = self.cl_sock.recv(2048)
        print(self.data.decode('utf-8'))

    def processes(self):
        while True:
            if self.read():
                break
            self.write()

    def disconnected(self):
        self.cl_sock.close()
