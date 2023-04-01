from Lamps.lamp import Lamp
import socket
import select
from time import sleep
class SocketLamp(Lamp):

    def __init__(self, ip):
        self.socket = socket.socket()
        self.socket.settimeout(2)
        self.socket.connect((ip, 80))


    def off(self):

        self.socket.sendall("0".encode())

    def on(self):
        print(self.socket.getsockname())
        self.socket.sendall("1".encode())

if __name__ == '__main__':
    # socket = socket.socket()
    # socket.connect(("192.168.1.103", 80))
    # socket.send("1".encode())

    import select
    import socket

    ip = '192.168.1.103'
    port = 80

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, port))

    conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10)

    while True:
        try:
            ready_to_read, ready_to_write, in_error = \
                select.select([conn, ], [conn, ], [], 5)
        except select.error:
            conn.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
            conn.close()
            # connection error event here, maybe reconnect
            print('connection error')
            break
        if len(ready_to_read) > 0:
            recv = conn.recv(2048)
            # do stuff with received data
            print(f'received: {recv}')
        if len(ready_to_write) > 0:
            conn.send("1".encode())
            # connection established, send some stuff
            print("ready to writre")
        sleep(1)