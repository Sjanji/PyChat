from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
class Window(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args) 
        self.setLayout(QVBoxLayout()) 
        self.layout().addWidget(QLabel("<font color='red' size='200'>This is the text</font>")) 
        # let the whole window be a glass 
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.addButton()
        # from ctypes import windll, c_int, byref 
        # windll.dwmapi.DwmExtendFrameIntoClientArea(c_int(self.winId()), byref(c_int(-1)))
        self.move(50, 50)
    
    def mousePressEvent(self, event): 
        self.repaint()
    
    def addButton(self):
        self.quitBouton = QPushButton("Quit")
        self.layout().addWidget(self.quitBouton)
        self.quitBouton.clicked.connect(self.buttonClicked)
    
    def buttonClicked(self):
        QCoreApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec_())
    
#python3 testTransparent.py