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
