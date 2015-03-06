import socket
from PyQt4 import QtCore

       

class Client(QtCore.QThread):
    def __init__(self, interface):
        QtCore.QThread.__init__(self)
        self.cmd = True
        self.interface = interface
        self.connect(self.interface, QtCore.SIGNAL('stopThread'), self.stop)
    
    def connectToServ(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.settimeout(0.2) #socket non bloquante
    
    def setCmd(self, cmd):
        self.cmd = cmd
    
    def stop(self):
        self.cmd = False
    
    def msgToServ(self, msg):
        self.socket.sendall(msg)
    
    def emitMsg (self, text):
        self.emit(QtCore.SIGNAL('msgFromServ'), text)
    
    def run(self):
        while self.cmd:
            try: #au cas où le settimeout provoque une exception
                data = self.socket.recv(1024)
                None
                if data :
                    # print(data)
                    self.emitMsg(data)
            except: None
        self.socket.close()
        self.emit(QtCore.SIGNAL('endOfThread'))
