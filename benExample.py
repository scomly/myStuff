from PySide import QtGui, QtCore

class CheckBox(QtGui.QCheckBox):
    def __init__(self, name):
        super(CheckBox, self).__init__()

        self.setText(name)

class Dialog(QtGui.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.widgetList = {}
        list = ["one", "two", "three"]
        for itemName in list:
            itemWidget = CheckBox(itemName)
            layout.addWidget(itemWidget)
            self.widgetList[itemName]=itemWidget

        printButton = QtGui.QPushButton("Print")
        layout.addWidget(printButton)

        printButton.clicked.connect(self.printResults)

    def printResults(self):
        for name, widget in self.widgetList.iteritems():
            if widget.isChecked():
                print name, "Is Checked"

diag = Dialog()
diag.show()

def doOption1():
    print "Doing Option1"

def doOption2():
    print "Doing Option2"

class MyCheckBox(QtGui.QCheckBox):
    def __init__(self, parent, name):
        super(MyCheckBox, self).__init__(parent)
        self.setParent(parent)
        self.setFont(QtGui.QFont("Arial"))
        self.setText(name)

class MyDialog(QtGui.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        goButton = QtGui.QPushButton("Go")
        layout.addWidget(goButton)
        goButton.clicked.connect(self.runOptionFunctions)

        self.allOptionsDict = {}
        optionDict = { "option1": doOption1, "options2": doOption2 }

        for option, optionFunction in optionDict.iteritems():
            checkBox = MyCheckBox(self, option)
            layout.addWidget(checkBox)
            valueDict = { "widget": checkBox, "func": optionFunction }
            self.allOptionsDict[option] = valueDict

    def runOptionFunctions(self):
        for option, value in self.allOptionsDict.iteritems():
            widget = value["widget"]
            function = value["func"]
            if widget.isChecked():
                function()

diag = MyDialog()
diag.show()




