from PyQt4 import QtGui 
from PyQt4 import QtCore 
import sys

import widget

def main(args):
    app = QtGui.QApplication(sys.argv)
    window = widget.Ui_Form()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)



#python3 main.py