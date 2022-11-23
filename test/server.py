import uuid
from PyQt5 import QtCore, QtNetwork
import os

class ServerManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ServerManager, self).__init__(parent)
        self._server = QtNetwork.QTcpServer(self)
        self._server.newConnection.connect(self.on_newConnection)
        self._clients = {}

    def launch(self, address=QtNetwork.QHostAddress.Any, port=9999):
        return self._server.listen(QtNetwork.QHostAddress(address), port)

    
    def on_newConnection(self):
        print("NEW")
        socket = self._server.nextPendingConnection()
        socket.readyRead.connect(self.on_readyRead)
        if socket not in self._clients:
            self._clients[socket] = uuid.uuid4()

    
    def on_readyRead(self):



        # receive 4096 bytes each time
        #BUFFER_SIZE = 4096
        #received = client_socket.recv(BUFFER_SIZE).decode()
        filename = 'Seq_received.txt'
        with open(filename, "wb") as f:            
            socket = self.sender()
            bytes_read = socket.readAll()
            # read 1024 bytes from the socket (receive)
            #bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                print("Nothing more received")
            # write to the file the bytes we just received
            f.write(bytes_read)


        #socket = self.sender()
        #resp = socket.readAll()
        #resp = str(resp, encoding='utf-8')
        #code = self._clients[socket]
        #print("From[{}]- message: {}".format(code, resp))
        resp = 'file Received!'
        msg_resp = "Server: " + str(resp)
        msg_resp = bytes(msg_resp, 'utf-8')
        socket.write(msg_resp)

if __name__ == '__main__':
    import sys
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtCore.QCoreApplication(sys.argv)

    address = '127.0.0.1'
    port = 9000
    server = ServerManager()
    if not server.launch(address, port):
        sys.exit(-1)
    sys.exit(app.exec_())


