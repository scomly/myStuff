from PySide import QtGui
from PySide import QtCore
import maya.OpenMayaUI as mui
import shiboken
import maya.cmds as cmds

import yaml

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    

class UtilityToolBoxUI(QtGui.QDialog):
    

    
    def __init__(self, parent=getMayaWindow()):
        super(UtilityToolBoxUI, self).__init__(parent)
        
        self.setWindowTitle("Utility Toolbox")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed
                
        self.topList = ["Red", "Green", "Blue", "White", "Black"]
        self.middleTopList = ["Shadow", "Contact_Shadow", "Fresnel", "Reflection_Occ"]
        self.middleBotList = ["Shadow_Catcher", "Plate_Projection", "Reflection_Catcher"]
        self.bottomList = ["Ref_Spheres"]

        self.createLayout() # runs def createLayout
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        self.setMinimumHeight(650)
        self.setMinimumWidth(750)
        layout.setSpacing(0)
        
        ########### catch all checkboxes here ################
        self.cbButtonList = {}
        self.getState = {}
        
        #################################################################
        
        radioLayout = QtGui.QHBoxLayout()
        layout.addLayout(radioLayout)
        
        spacer = QtGui.QSpacerItem(275,0)
        radioLayout.addSpacerItem(spacer)
        
        radioGroup = QtGui.QButtonGroup()
       
        showRadio = QtGui.QRadioButton("Show")
        showRadio.setMaximumWidth(50)
        showRadio.setMinimumWidth(50)
        showRadio.setChecked(True)
        radioGroup.addButton(showRadio)
        seqRadio = QtGui.QRadioButton("Seq")
        seqRadio.setMaximumWidth(50)
        seqRadio.setMinimumWidth(50)
        radioGroup.addButton(seqRadio)
        shotRadio = QtGui.QRadioButton("Shot")
        shotRadio.setMaximumWidth(50)
        shotRadio.setMinimumWidth(50)        
        radioGroup.addButton(shotRadio)
        
        radioLayout.addWidget(showRadio)
        radioLayout.addWidget(seqRadio)
        radioLayout.addWidget(shotRadio)
        
        spacer2 = QtGui.QSpacerItem(250,0)
        radioLayout.addSpacerItem(spacer2)
        
        #################### top frame ##############################################
        
        self.top_frame = QtGui.QFrame()
        self.top_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.top_frame)
        
        self.top_frame.setLayout(QtGui.QHBoxLayout())
        
        tl = FrameLabel("mask_label", "LightMtls", self.top_frame)
        
        tl.frameLabelVarName.mouseReleaseEvent = self.topToggle
        
       
        self.topListCheckBox = {}
        
        for x in self.topList:
            cb = UtilCreateCheckBox(x, x, self.top_frame)
            self.topListCheckBox[x] = cb.buttonVarName
            setattr(self, x, cb)
            
        self.cbButtonList.update(self.topListCheckBox)
        
        ####################### middle top frame #################################
        self.middleTop_frame = QtGui.QFrame()
        self.middleTop_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleTop_frame)
        
        self.middleTop_frame.setLayout(QtGui.QHBoxLayout())
        
        mtl = FrameLabel("RE_label", "RenderElem", self.middleTop_frame)
        
        mtl.frameLabelVarName.mouseReleaseEvent = self.midTopToggle
        
        
        self.midTopListCheckBox = {}
        
        for x in self.middleTopList:
            cb = UtilCreateCheckBox(x, x, self.middleTop_frame)
            self.midTopListCheckBox[x] = cb.buttonVarName
            setattr(self, x, cb)
            
        self.cbButtonList.update(self.midTopListCheckBox)
            
        ##########################  middle bottom frame ##########################################
        
        self.middleBot_frame = QtGui.QFrame()
        self.middleBot_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.middleBot_frame)
        
        self.middleBot_frame.setLayout(QtGui.QHBoxLayout())
        
        mbl = FrameLabel("Shader_label", "Shaders", self.middleBot_frame)
        
        mbl.frameLabelVarName.mouseReleaseEvent = self.midBotToggle

        self.midBotListCheckBox = {}
        
        for x in self.middleBotList:
            cb = UtilCreateCheckBox(x, x, self.middleBot_frame) 
            self.midBotListCheckBox[x] = cb.buttonVarName
            setattr(self, x, cb)
            
            
                       
        self.cbButtonList.update(self.midBotListCheckBox)
        ############################ bottom frame ##########################################
        
        self.bottom_frame = QtGui.QFrame()
        self.bottom_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout.addWidget(self.bottom_frame)

        self.bottom_frame.setLayout(QtGui.QHBoxLayout())
        
        bl = FrameLabel("Util_label", "Utilities", self.bottom_frame)
        
        bl.frameLabelVarName.mouseReleaseEvent = self.bottomToggle
                
        self.bottomListCheckBox = {}
               
        for x in self.bottomList:
            cb = UtilCreateCheckBox(x, x, self.bottom_frame)
            self.bottomListCheckBox[x] = cb.buttonVarName
            setattr(self, x, cb)
            
            
        self.cbButtonList.update(self.bottomListCheckBox)     
                    
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
        
        #self.import_button.clicked.connect(self.importButtonFunction)
                
        ####################### Output Window ####################################################
        
        self.outWindow = QtGui.QTextEdit()
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(250)
        
        ############################################################################################
        
        
        self.setLayout(layout) # add main layout itself to this dialog
        
        
        
    def checkAllFunction(self): ## Check all Button
        
        for x,y in self.cbButtonList.iteritems():
            
            if y.isChecked() == True:
                cbState = True
            else:
                cbState = False
            self.getState[x] = cbState
                    
        with open('/home/scomly/python/test_yaml/test.yml', 'w') as outfile:
            outfile.write(yaml.dump(self.getState, default_flow_style=False))

        
    def checkNoneFunction(self): ## Check None Button
    
        infile = open('/home/scomly/python/test_yaml/test.yml')
        inSettings = yaml.load(infile)
        infile.close()

        for x in self.cbButtonList:
            if x in inSettings.keys():
                if inSettings[x]:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Checked)' % (x))
                else:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Unchecked)' % (x))
                
                

        
    def topToggle(self, event): ## Top list CB toggle
        flipRow(self.topListCheckBox)        

    def midTopToggle(self, event): ## midTop list CB toggle
        flipRow(self.midTopListCheckBox) 
        
    def midBotToggle(self, event): ## midBot list CB toggle
        flipRow(self.midBotListCheckBox)  

    def bottomToggle(self, event): ## Bottom list CB toggle
        flipRow(self.bottomListCheckBox)
        
def flipRow(whichList): ## toggle row of checkboxes if you click on the label
    if whichList.values()[0].isChecked() == True:
        for x,y in whichList.iteritems():
            y.setChecked(False)
    else:
        for x,y in whichList.iteritems():
            y.setChecked(True)  

class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)
        

        
class FrameLabel(object):
    def __init__(self, frameLabelVarName, frameLabelName, frame):
        
        self.frameLabelName = frameLabelName
        self.frame = frame
        
        self.frameLabelVarName = QtGui.QLabel(frameLabelName)
        frame.layout().addWidget(self.frameLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.frameLabelVarName.setFont(font)               
        
        
if __name__ == "__main__":
    
    # will try and close the ui if it exists
    try:
        ui.close()
    except:
        pass
        
    ui = UtilityToolBoxUI()
    ui.show()        
        
        
