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



from PySide import QtGui, QtCore

class Dialog1(QtGui.QDialog):
    def __init__(self):
        super(Dialog1, self).__init__()

        layout1 = QtGui.QHBoxLayout()
        self.setLayout(layout1)
        button1 = QtGui.QPushButton("Do it")
        button1.clicked.connect(self.doingit)
        layout1.addWidget(button1)

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

import sys
from PySide import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        
        layout2 = QtGui.QVBoxLayout() # main layout
        #self.setMinimumHeight(650)
        #self.setMinimumWidth(750)
        #layout2.setSpacing(0)

        self.setLayout(layout2)
        sureLayout = QtGui.QHBoxLayout()
        layout2.addLayout(sureLayout)
        
        #spacer = QtGui.QSpacerItem(175,0)
        #sureLayout.addSpacerItem(spacer)
        
        sureLabel = QtGui.QLabel("You sure hoe?")
        sureLayout.addWidget(sureLabel)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        sureLabel.setFont(font)
        sureLabel.setMaximumWidth(100)
              

        

        
        #spacer2 = QtGui.QSpacerItem(15,0)
        #radioLayout.addSpacerItem(spacer2)
        
        sureButtonLayout = QtGui.QHBoxLayout()
        layout2.addLayout(sureButtonLayout)
        
        yesButton = QtGui.QPushButton("Yes")
        yesButton.setMaximumWidth(200)
        sureButtonLayout.addWidget(yesButton)
        yesButton.clicked.connect(self.yesDialog) ## clicked
        
        #spacer3 = QtGui.QSpacerItem(150,0)
        #sureButtonLayout.addSpacerItem(spacer3)    
        noButton = QtGui.QPushButton("Yes")
        noButton.setMaximumWidth(200)
        sureButtonLayout.addWidget(noButton)
        noButton.clicked.connect(self.noDialog) ## clicked

        
        #self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()
        
    def yesDialog(self):
        print "yes"
        
    def noDialog(self):
        print "no"
        

    
def launchUI():
    global Example
    
    # will try and close the ui if it exists
    try: Example.close()
    except: pass
    
    Example = Example()
    Example.show()    
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()
