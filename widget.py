# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from client import *
import os

HOST = '127.0.0.1'    
PORT = 50007 

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self, *args): 
        QtGui.QWidget.__init__(self, *args) 
        self.setObjectName(_fromUtf8("Form"))
        self.path = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1])+os.sep
        self.setStyleSheet(open(self.path+'style.css', 'r').read())
        self.BUTTON_IMAGE = self.path+'close.png'
        self.move(100,100)
        self.offset = QtCore.QPoint(100,100)
        self.okToMove = False
        self.client = Client(HOST, PORT, self)
        self.connected = False
        self.name = b'NoName'
        
        self.affich = b'<br><br><div style="font-size: 22px;"><center>Client Chat ver 0.1</center></div><br>'
        self.setupUi()
        
        self.connect(self.client, QtCore.SIGNAL('msgFromServ'), self.affichMsg)
        self.connect(self.client, QtCore.SIGNAL('endOfThread'), self.quit)
        
    def setupUi(self):
        self.addGrid()
        self.addCloseButton()
        self.beforeConnect()
        
        #on rend la fenêtre transparente :
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def beforeConnect(self):
        #création de la sous-fenêtre de login
        self.frame = QtGui.QFrame(self)
        self.frame.setObjectName(_fromUtf8("frame01"))
        self.frame.setFixedSize(300,120)
        self.grille.addWidget(self.frame, 1, 18)
        self.grilleOnFrame = QtGui.QGridLayout()
        self.frame.setLayout(self.grilleOnFrame)
        self.label1 = QtGui.QLabel('Login', self)
        self.label1.setObjectName(_fromUtf8("labelName"))
        self.grilleOnFrame.addWidget(self.label1, 0, 0)
        self.lineName = QtGui.QLineEdit(self)
        self.lineName.setObjectName(_fromUtf8("saisieName"))
        self.grilleOnFrame.addWidget(self.lineName, 0, 1)
        self.label2 = QtGui.QLabel('Password', self)
        self.label2.setObjectName(_fromUtf8("labelPwd"))
        self.grilleOnFrame.addWidget(self.label2, 1, 0)
        self.linePwd = QtGui.QLineEdit(self)
        self.linePwd.setObjectName(_fromUtf8("saisiePwd"))
        self.grilleOnFrame.addWidget(self.linePwd, 1, 1)
        self.connect(self.lineName, QtCore.SIGNAL('returnPressed()'), self.setName)
        self.connect(self.linePwd, QtCore.SIGNAL('returnPressed()'), self.setName)
        self.frame.mousePressEvent = self.mousePressEventOnText 
        self.frame.mouseReleaseEvent = self.MouseButtonReleaseEventOnText
        self.frame.mouseMoveEvent = self.mouseMoveEventOnText

    def afterConnect(self):
        self.resize(300, 600)
        self.grille.itemAt(1).widget().deleteLater() #on efface self.frame
        self.client.connectToServ()
        self.client.start()
        self.connected = True
        self.addTextEdit()
        self.addLineEdit()
    
    def addGrid(self):
        # crée un plan (layout) et y colle deux boutons
        # le plan est ensuite coller sur le widget central
        self.grille = QtGui.QGridLayout()
        self.setLayout(self.grille)

    def addTextEdit(self):
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setHtml(self.affich.decode('utf-8'))
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 300, 600))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.grille.addWidget(self.textEdit, 1, 0, 1, 20)
        #redirection l'événement "click" de souris vers notre méthode
        self.textEdit.mousePressEvent = self.mousePressEventOnText 
        self.textEdit.mouseReleaseEvent = self.MouseButtonReleaseEventOnText
        #même chose pour le mouvement de souris
        self.textEdit.mouseMoveEvent = self.mouseMoveEventOnText
    
    def addLineEdit(self):
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setObjectName(_fromUtf8("saisie"))
        self.connect(self.lineEdit, QtCore.SIGNAL('returnPressed()'), self.onPresseEnterOnlineEdit)
        self.grille.addWidget(self.lineEdit, 2, 0, 2, 20)
    
    def addCloseButton(self):
        self.ImageButton = ExtendedQLabel(self)
        self.ImageButton.resize(10, 10)
        self.ImageButton.move(0, 160)
        self.ImageButton.setPixmap(QtGui.QPixmap(self.BUTTON_IMAGE).scaled(self.ImageButton.size(), QtCore.Qt.KeepAspectRatio))
        self.connect(self.ImageButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.grille.addWidget(self.ImageButton, 0, 19) 
    
    # --------------------  Mouvement de la fenêtre ---------------------------
    def MouseButtonReleaseEventOnText(self, event):
        self.okToMove = False
    
    def mousePressEventOnText(self, event):
        self.offset = event.pos()
        self.okToMove = True
    
    def mouseMoveEventOnText(self, event):
        #permet de modifier la position de la fenêtre
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        if self.okToMove == True:
            self.move(x-x_w, y-y_w)
    # --------------------  FIN Mouvement fenêtre ---------------------------
    
    def affichMsg(self, msg):
        self.affich += msg+b'<br>'
        self.textEdit.setHtml(self.affich.decode('utf-8'))
        
    def onPresseEnterOnlineEdit(self):
        msg = self.name + self.lineEdit.text().encode('utf-8')
        self.client.msgToServ(msg)
        self.lineEdit.setText('')
    
    def buttonClicked(self):
        if not self.connected : 
            QtCore.QCoreApplication.instance().quit()
        self.emit(QtCore.SIGNAL('stopThread'))
    
    def quit(self):
        QtCore.QCoreApplication.instance().quit()
    
    def setName(self):
        self.name = self.lineName.text().encode('utf-8') + b' : '
        self.afterConnect()

class ExtendedQLabel(QtGui.QLabel):
    #permet de rendre un Qlabel cliquable
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
    
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))