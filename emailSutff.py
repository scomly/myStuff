import os, sys, functools

try:
    import dloMethodUtils
    import dloPyQtUtil
except:
    import dloTools.dloMethodUtils as dloMethodUtils
    import dloTools.dloPyQtUtil as dloPyQtUtil

reload(dloMethodUtils)
reload(dloPyQtUtil)

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

try: import tdShotgun.tdShotgunUtils as mShotgunUtils
except: pass

def shotgungGetTaskList(): 
    steps = []
    
    try:
        dloPyQtUtil.dloQtWaiCursor(1)
        shotgunSteps = mShotgunUtils.buildStepNameFilter()
        dloPyQtUtil.dloQtWaiCursor(0)
        
        for i in range(len(shotgunSteps)): steps.append(shotgunSteps[i]['code'])
        steps = list(set(steps))
        steps.sort()
    
    except: dloPyQtUtil.dloQtWaiCursor(0)

    return steps

########################################################
#### MAIN UI
########################################################
class dloEmailUI(QDialog):
    def __init__(self, parent=None):
        super(dloEmailUI, self).__init__(parent)
        self.setStyleSheet('Background: rgb(80,80,80); color: rgb(200,200,200)')
        self.setWindowTitle("Email UI")
        
        configName = "%s_emailUIConfig" %dloMethodUtils.dloGetCurrentShow()
        
        UIWinPos = dloPyQtUtil.dloQtConfigGetLastWinPos(configName)
        self.setGeometry(int(UIWinPos[0]), int(UIWinPos[1]), 700, 600)
        
        self.boldFont = QFont()
        self.boldFont.setPointSize(int(10))
        self.boldFont.setWeight(75)

        self.font = QFont()
        self.font.setPointSize(int(10))
        
        self.fixedWidthFont = QFont("Courier", 10)
        self.fixedWidthFont.setPointSize(int(10))
        self.fixedWidthFont.setWeight(75)
        self.fixedWidthFont.setFixedPitch(1)
        
        #predefined vars
        self.preCommand = ""
        self.postCommand = ""
        self.objList = []
        self.currentShow = dloMethodUtils.dloGetCurrentShow()
        self.currentSeq = dloMethodUtils.dloGetCurrentSeq()
        self.currentShot = dloMethodUtils.dloGetCurrentShot()
        
        #main layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        self.setLayout(mainLayout)
        
        #subject section
        hbox = QHBoxLayout()
        mainLayout.addLayout(hbox)
        
        label = QLabel('   Subject:')
        label.setMinimumSize(QSize(70, 20))
        label.setFont(self.boldFont)
        hbox.addWidget(label)
        
        self.subjectLineEdit = QLineEdit()
        self.subjectLineEdit.setFont(self.font)
        self.subjectLineEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.subjectLineEdit.setStyleSheet('Background:rgb(20,20,20);border-style:outset;border-radius:8px;min-height:1.7em;border-width:2px;border-color:rgb(100,100,100)')
        hbox.addWidget(self.subjectLineEdit)
        
        #to section
        hbox = QHBoxLayout()
        mainLayout.addLayout(hbox)
        
        label = QLabel('   To:')
        label.setMinimumSize(QSize(70, 20))
        label.setFont(self.boldFont)
        hbox.addWidget(label)
        
        self.toLineEdit = QLineEdit()
        self.toLineEdit.setFont(self.font)
        self.toLineEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.toLineEdit.setStyleSheet('Background:rgb(20,20,20);border-style:outset;border-radius:8px;min-height:1.7em;border-width:2px;border-color:rgb(100,100,100)')
        hbox.addWidget(self.toLineEdit)
        
        #cc section
        hbox = QHBoxLayout()
        mainLayout.addLayout(hbox)
        
        label = QLabel('   Cc:')
        label.setMinimumSize(QSize(70, 20))
        label.setFont(self.boldFont)
        hbox.addWidget(label)
        
        self.ccLineEdit = QLineEdit()
        self.ccLineEdit.setFont(self.font)
        self.ccLineEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.ccLineEdit.setStyleSheet('Background:rgb(20,20,20);border-style:outset;border-radius:8px;min-height:1.7em;border-width:2px;border-color:rgb(100,100,100)')
        hbox.addWidget(self.ccLineEdit)
        
        #divider
        divider = QFrame()
        divider.setFrameStyle(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        mainLayout.addWidget(divider)
        
        #message header, shotgun task, add task, copy recipient
        hbox = QHBoxLayout()
        mainLayout.addLayout(hbox)
        
        label = QLabel('   Message:')
        label.setMinimumSize(QSize(70, 20))
        label.setFont(self.boldFont)
        hbox.addWidget(label)
        
        #spacer
        spacerSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox.addItem(spacerSpacer)

        #task combobox
        self.taskComboBox = QComboBox()
        self.taskComboBox.setFont(self.font)
        self.taskComboBox.setMinimumHeight(25)
        self.taskComboBox.setStyleSheet('Background:rgb(20,20,20)')
        hbox.addWidget(self.taskComboBox)
        
        tasks = shotgungGetTaskList()
        self.taskComboBox.addItems(tasks)
        
        #add task button
        addTaskButton = QPushButton('Add Task')
        addTaskButton.setFont(self.font)
        addTaskButton.setStyleSheet('border-style:outset;border-radius:5px;border-width:2px;border-color:rgb(5,5,20);\
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 rgb(60,60,140), stop: 1 rgb(10,10,40))')
        addTaskButton.setMinimumHeight(25)
        addTaskButton.setMinimumWidth(100)
        addTaskButton.setDefault(0)
        addTaskButton.setAutoDefault(0)
        addTaskButton.clicked.connect(self.addTaskEmail)
        hbox.addWidget(addTaskButton)
        
        #copy recipient button
        copyRecipientButton = QPushButton('Copy Recipient')
        copyRecipientButton.setFont(self.font)
        copyRecipientButton.setStyleSheet('border-style:outset;border-radius:5px;border-width:2px;border-color:rgb(5,5,20);\
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 rgb(60,100,60), stop: 1 rgb(20,30,20))')
        copyRecipientButton.setMinimumHeight(25)
        copyRecipientButton.setMinimumWidth(120)
        copyRecipientButton.setDefault(0)
        copyRecipientButton.setAutoDefault(0)
        copyRecipientButton.clicked.connect(self.copyRecipient)
        hbox.addWidget(copyRecipientButton)
        
        #message text field
        self.messageTextEdit = QTextEdit()
        self.messageTextEdit.setFont(self.font)
        self.messageTextEdit.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.messageTextEdit.setStyleSheet('Background:rgb(20,20,20);border-style:none')
        self.messageTextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        mainLayout.addWidget(self.messageTextEdit)

        #send button
        hbox = QHBoxLayout()
        mainLayout.addLayout(hbox)
        
        sendButton = QPushButton('Send Email')
        sendButton.setFont(self.boldFont)
        sendButton.setStyleSheet('border-style:outset;border-radius:5px;border-width:2px;border-color:rgb(5,5,20);\
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 rgb(40,40,40), stop: 1 rgb(0,0,0))')
        sendButton.setMinimumHeight(30)
        sendButton.setMinimumWidth(120)
        sendButton.setDefault(0)
        sendButton.setAutoDefault(0)
        sendButton.clicked.connect(functools.partial(self.sendMail))
        hbox.addWidget(sendButton)
    
    def addTaskEmail(self):
        import tdShotgun.tdShotgunAssignments as mShotgunAssignments
        
        task = str(self.taskComboBox.currentText())
        currentList = str(self.toLineEdit.text())
        
        try:
            print "Getting shotgun artist assignment for: %s %s %s" %(self.currentShow, self.currentShot, task)
            
            dloPyQtUtil.dloQtWaiCursor(1)
            emailList = mShotgunAssignments.getArtistEmailList(job=self.currentShow, shots=[self.currentShot], steps=[task])
            dloPyQtUtil.dloQtWaiCursor(0)
            
            if len(emailList):
                emailArtists = ",".join([each.replace("@methodstudios.com", "") for each in emailList])
                
                if len(currentList): currentList += "," + emailArtists
                else: currentList += emailArtists
                
                self.toLineEdit.setText(currentList)
        except:
            dloPyQtUtil.dloQtWaiCursor(0)
            QMessageBox.question(self, "Warning", "No artists found for task %s under %s" %(task, self.currentShot), QMessageBox.Ok)
    
    def copyRecipient(self):
        to = str(self.toLineEdit.text())
        cc = str(self.ccLineEdit.text())
        body = str(self.messageTextEdit.toPlainText())
            
        users = to.replace(" ", "").split(",")
        users.extend(cc.replace(" ", "").split(","))
        users = [user + "@methodstudios.com" for user in users if len(user)]
        
        userString = ", ".join(users)
        
        os.popen('/tools/td/release/bin/xsel -b', 'wb').write(userString)
        msg = "\nCopied:\n\n%s\n\nto buffer, hit Ctrl-V to paste..." %("\n".join(userString.replace(" ", "").split(",")))
        QMessageBox.question(self, 'Confirm', msg, QMessageBox.Ok)
        
    def sendMail(self):
        #pre command
        preCommand = self.preCommand
        
        if len(preCommand): 
            print preCommand
            exec(preCommand)
            
        subject = str(self.subjectLineEdit.text())
        to = str(self.toLineEdit.text())
        cc = str(self.ccLineEdit.text())
        body = str(self.messageTextEdit.toPlainText())
            
        users = to.replace(" ", "").split(",")
        users.extend(cc.replace(" ", "").split(","))
        users = [user + "@methodstudios.com" for user in users if len(user)]
        
        users = list(set(users))
        
        emailCmd = "Subject: %s\n" %subject
        emailCmd += "To: %s\n" %(", ".join(users))
        emailCmd += "Message:\n\n%s" %body
        
        print emailCmd
        
        if os.name == "posix":
            import mEmail
            mEmail.sendMail(users, "[%s]" %subject, body)       
        
        #post command
        postCommand = self.postCommand
        
        if len(postCommand): 
            print postCommand
            exec(postCommand)

        self.close()
          
    def closeEvent(self,event):
        lastPos = self.pos()
        lastWidth = self.width()
        lastHeight = self.height()
        
        configName = "%s_emailUIConfig" %dloMethodUtils.dloGetCurrentShow()
        
        if os.name == "nt": dloPyQtUtil.dloQtStoreConfig('UIWinPos', (lastPos.x()+8, lastPos.y()+30), configName)
        else: dloPyQtUtil.dloQtStoreConfig('UIWinPos', (lastPos.x()+4, lastPos.y()+25), configName)   
        
        #dloPyQtUtil.dloQtStoreConfig('lastWidth', lastWidth, configName)
        
def launchEmailUI():
    global isMaya, emailUI
                
    isMaya = dloPyQtUtil.dloIsMaya()
    
    try: emailUI.close()
    except: pass
        
    if isMaya: 
        app = dloPyQtUtil.dloGetMayaMainWindow()
        emailUI = dloEmailUI(app)
    else: 
        app = QApplication(sys.argv)
        emailUI = dloEmailUI()

    emailUI.show()

    if not isMaya: sys.exit(app.exec_())
    
########################################################
#### MAIN EXEC
########################################################
if __name__ == "__main__":
    launchEmailUI()

