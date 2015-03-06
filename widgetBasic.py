# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys

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
        self.setStyleSheet(open('style.css', 'r').read())
        self.BUTTON_IMAGE = 'close.png'
        self.move(100,100)
        self.offset = QtCore.QPoint(100,100)
        self.okToMove = False
        self.affich = b'<br><br><div><center>Test d\'un texte en <i>html</i></center></div><br>'
        self.name = b'No name : '
        self.setupUi()
        
        
    def setupUi(self):
        self.resize(300, 600)
        self.addGrid()
        self.closeButton()
        self.afterConnect()
        #on rend la fenêtre transparente :
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def afterConnect(self):
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
    
    def retranslateUi(self):
        self.setWindowTitle(_translate("Form", "Form", None))
        
    def onPresseEnterOnlineEdit(self):
        self.affich += self.name + self.lineEdit.text().encode('utf-8')+b'<br>'
        self.textEdit.setHtml(self.affich.decode('utf-8'))
        self.lineEdit.setText(u'')
    
    def buttonClicked(self): 
        QtCore.QCoreApplication.instance().quit()
    
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
    
    def closeButton(self):
        self.ImageButton = ExtendedQLabel(self)
        self.ImageButton.resize(10, 10)
        self.ImageButton.move(0, 160)
        self.ImageButton.setPixmap(QtGui.QPixmap(self.BUTTON_IMAGE).scaled(self.ImageButton.size(), QtCore.Qt.KeepAspectRatio))
        self.connect(self.ImageButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.grille.addWidget(self.ImageButton, 0, 19)


class ExtendedQLabel(QtGui.QLabel):
    #permet de rendre un Qlabel cliquable
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
    
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

def main(args):
    app = QtGui.QApplication(sys.argv)
    window = Ui_Form()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
