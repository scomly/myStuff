from PySide import QtGui
from PySide import QtCore
import maya.OpenMayaUI as mui
import shiboken
import maya.cmds as cmds

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    

class UtilityToolBoxUI(QtGui.QDialog):
    
    def __init__(self, parent=getMayaWindow()):
        super(UtilityToolBoxUI, self).__init__(parent)
        
        self.setWindowTitle("Utility Toolbox")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed
        
        self.createLayout() # runs def createLayout
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        self.setMinimumHeight(500)
        self.setMinimumWidth(750)
        
        ########### catch all checkboxes here ################
        self.cbButtonList = {}
        
        #################### top frame ##############################################
        
        self.top_frame = QtGui.QFrame()
        self.top_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.top_frame)
        
        self.top_frame.setLayout(QtGui.QHBoxLayout())
        
        FrameLabel("mask_label", "LightMtls", self.top_frame)
        
        topList = ["Red", "Green", "Blue", "White", "Black"]
        
        for x in topList:
            cb = UtilCreateCheckBox(x, x, self.top_frame)
            self.cbButtonList[x] = cb
        
        ####################### middle top frame #################################
        
        self.middleTop_frame = QtGui.QFrame()
        self.middleTop_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleTop_frame)
        
        self.middleTop_frame.setLayout(QtGui.QHBoxLayout())
        
        FrameLabel("RE_label", "RenderElem", self.middleTop_frame)
        
        middleTopList = ["Shadow", "Contact_Shadow", "Fresnel", "Reflection_Occ"]
        
        for x in middleTopList:
            cb = UtilCreateCheckBox(x, x, self.middleTop_frame)
            self.cbButtonList[x] = cb
            
        ##########################  middle frame ##########################################
        
        self.middleBot_frame = QtGui.QFrame()
        self.middleBot_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleBot_frame)
        
        self.middleBot_frame.setLayout(QtGui.QHBoxLayout())
        
        FrameLabel("Shader_label", "Shaders", self.middleBot_frame)
        
        middleBotList = ["Shadow_Catcher", "Plate_Projection", "Reflection_Catcher"]
        
        for x in middleBotList:
            cb = UtilCreateCheckBox(x, x, self.middleBot_frame)
            self.cbButtonList[x] = cb
       
              
        ############################ bottom frame ##########################################
        
        self.bottom_frame = QtGui.QFrame()
        self.bottom_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.bottom_frame)

        self.bottom_frame.setLayout(QtGui.QHBoxLayout())
        
        FrameLabel("Util_label", "Utilities", self.bottom_frame)
        
        bottomList = ["Ref_Spheres"]
        
        
               
        for x in bottomList:
            cb = UtilCreateCheckBox(x, x, self.bottom_frame)
            self.cbButtonList[x] = cb
            
            
                    
        ######################### Un/Check All buttons ##################################################
        
        allCheckLayout = QtGui.QHBoxLayout()
        layout.addLayout(allCheckLayout)
        
        self.checkAll_button = QtGui.QPushButton("Check All")
        allCheckLayout.layout().addWidget(self.checkAll_button)
        self.checkAll_button.clicked.connect(self.checkAllFunction)
        
        
        self.checkNone_button = QtGui.QPushButton("Check None")
        allCheckLayout.layout().addWidget(self.checkNone_button)
        self.checkNone_button.clicked.connect(self.checkNoneFunction)
                       
        
        ####################### Import button #####################################################
        
        self.import_button = QtGui.QPushButton("Import")
        layout.addWidget(self.import_button)
        self.import_button.setMinimumHeight(50)
        
        self.import_button.clicked.connect(self.importButtonFunction)
                
        #################################################################################################
        
        self.setLayout(layout) # add main layout itself to this dialog
        
        
    def importButtonFunction(self):
        for x,y in self.cbButtonList.items():
        
            print x,y
                
       
    def checkAllFunction(self):
        print "Check All"
        
    def checkNoneFunction(self):
        print "Check None"



class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        #self.buttonVarName = buttonVarName
        # buttonVarName = the button creation variable name
        #self.buttonLabelName = buttonLabelName
        # buttonLabelName = the label next to the button
        #self.frame = frame
        # frame = which frame it will land in
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)

        
class FrameLabel(object):
    def __init__(self, frameLabelVarName, frameLabelName, frame):
        
        self.frameLabelVarName = frameLabelVarName
        # frameLabelVarName = the frame creation variable name
        self.frameLabelName = frameLabelName
        # frameLabelName = the name of the label on the frame
        self.frame = frame
        # frame = which frame it will land in
        
        frameLabelVarName = QtGui.QLabel(frameLabelName)
        frame.layout().addWidget(frameLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        frameLabelVarName.setFont(font)

        
        
if __name__ == "__main__":
    
    # will try and close the ui if it exists
    try:
        ui.close()
    except:
        pass
        
    ui = UtilityToolBoxUI()
    ui.show()





















    
