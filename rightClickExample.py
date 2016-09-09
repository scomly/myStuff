class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)
                        
        self.buttonVarName.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.buttonVarName.customContextMenuRequested.connect(self.popUp)
        
    def popUp(self, event):
        
        self.menu = QtGui.QMenu()
        deleteAction = self.menu.addAction('Remove')
        deleteAction.triggered.connect(self.RemoveAction)
        self.menu.popup(QtGui.QCursor.pos())            
           
    #def mouseReleaseEvent(self, event):
        #if self.underMouse():     
            
        
    #def contextMenuEvent(self, event):
        #self.menu = QtGui.QMenu(self)
        #deleteAction = QtGui.QAction('Remove', self)
        #deleteAction.triggered.connect(self.RemoveAction)
        #self.menu.addAction(deleteAction)
        #self.menu.popup(QtGui.QCursor.pos())
        
    def RemoveAction(self):
        print "Remove"







##################################################################################

from PySide import QtGui, QtCore

class PopUp(QtGui.QDialog):
    def __init__(self):
        super(PopUp, self).__init__()
        layout1 = QtGui.QVBoxLayout()
        self.setLayout(layout1)
        self.line = QtGui.QLineEdit()
        button1 = QtGui.QPushButton("Set")
        layout1.addWidget(self.line)
        layout1.addWidget(button1)
        button1.clicked.connect(self.setOptions)

        self.text = None

    def setOptions(self):
        self.text = self.line.text()
        self.accept()


class Dialog1(QtGui.QDialog):
    def __init__(self):
        super(Dialog1, self).__init__()

        layout1 = QtGui.QHBoxLayout()
        self.setLayout(layout1)
        button1 = QtGui.QPushButton("Do it")
        button2 = QtGui.QPushButton("Set Options")
        self.label1 = QtGui.QLabel()
        button1.clicked.connect(self.doingit)
        button2.clicked.connect(self.doOptions)
        layout1.addWidget(button1)
        layout1.addWidget(button2)
        layout1.addWidget(self.label1)
        
##########################################################################
        
        button1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button1.customContextMenuRequested.connect(self.popUp)
    
    def popUp(self, event):
        self.menu = QtGui.QMenu()
        deleteAction = QtGui.QAction('Remove', self)
        deleteAction.triggered.connect(self.RemoveAction)
        self.menu.addAction(deleteAction)
        self.menu.popup(QtGui.QCursor.pos())            
           
    #def mouseReleaseEvent(self, event):
        #if self.underMouse():     
            
        
    #def contextMenuEvent(self, event):
        #self.menu = QtGui.QMenu(self)
        #deleteAction = QtGui.QAction('Remove', self)
        #deleteAction.triggered.connect(self.RemoveAction)
        #self.menu.addAction(deleteAction)
        #self.menu.popup(QtGui.QCursor.pos())
        
    def RemoveAction(self):
        print "Remove"
        

    def doOptions(self):
        popup = PopUp()
        def getOptions():
            theOptions = popup.text
            self.label1.setText(theOptions)
        popup.accepted.connect(getOptions)
        popup.show()

    def doingit(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Are you sure you want to DO this???")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        ret = msgBox.exec_()

        if ret == msgBox.Ok:
            print "Ok!"
        if ret == msgBox.Cancel:
            print "Not Ok!"

diag = Dialog1()
diag.show()
