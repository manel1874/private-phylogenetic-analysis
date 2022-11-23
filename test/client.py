from PyQt5 import QtCore, QtNetwork
import os

class ClientManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ClientManager, self).__init__(parent)
        self._socket = QtNetwork.QTcpSocket(self)
        self._socket.stateChanged.connect(self.on_stateChanged)
        self._socket.readyRead.connect(self.on_readyRead)
        self._timer = QtCore.QTimer(self, interval=1000)
        self._timer.timeout.connect(self.sendMessage)

    def launch(self, address=QtNetwork.QHostAddress.Any, port=9999):
        print(address)
        print(port)
        return self._socket.connectToHost(QtNetwork.QHostAddress(address), port)

    
    def on_stateChanged(self, state):
        if state == QtNetwork.QAbstractSocket.ConnectedState:
            self._timer.start()
            print("connected")
        elif state == QtNetwork.QAbstractSocket.UnconnectedState:
            print("disconnected")
            QtCore.QCoreApplication.quit()

    
    def sendMessage(self):
        if self._socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            
            filename = 'Sequence_0.txt'
            filesize = os.path.getsize(filename)
            print(filesize)
            #filesize =bytes(filesize, 'utf-8')
            #self._socket.write(filesize) 

            #s.send(f"{filesize}".encode())
            # start sending the file
            with open(filename, "rb") as f:
                # read the bytes from the file
                bytes_read = f.read()#BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    print("File transmitting is done")
                # we use sendall to assure transimission in 
                # busy networks
                self._socket.write(bytes_read) 
                print("Sending chunck...")
            
            
            
            #msg = QtCore.QDateTime.currentDateTime().toString()
            #msg =bytes(msg, 'utf-8')
            #self._socket.write(msg) 

    
    def on_readyRead(self):
        print("Response: ", self._socket.readAll())

if __name__ == '__main__':
    import sys
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtCore.QCoreApplication(sys.argv)
    address = '127.0.0.1'
    port = 9000
    server = ClientManager()
    server.launch(address, port)
    sys.exit(app.exec_())







