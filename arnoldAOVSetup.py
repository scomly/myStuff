from PySide import QtGui
from PySide import QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken
import yaml
import os

########################################################################
############################### GUI ####################################
########################################################################

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    
class AOVSetUI(QtGui.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(AOVSetUI, self).__init__(parent)
        
        self.setWindowTitle("Set AOVs")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed
        
        ########### Stashbox #####################################

        self.layerOverridesDictionary = {}
        #self.incomingLayerOverridesValuesDictoinary = {}
        #self.renderLayersFrames = {}
        #self.renderLayerButtons = {}
        self.defaultRenderLayerState = {}
                
        self.stashFramesCreateButton = {}
        self.stashRenderButtons = {}
        self.stashRenderButtonsPerFrame = {}
        self.stashButtonsTwoFrame = {}
      
        #############################################################################

        self.createLayout() # runs function below
    
    ################################################################################    
    ##################### Layout Creation ##########################################    
    ################################################################################
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        #self.setMinimumHeight(650)
        #self.setMinimumWidth(750)
        layout.setSpacing(0)

        self.framesHorizLayout = QtGui.QHBoxLayout() # layout for frames
        layout.addLayout(self.framesHorizLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)
               
        ##### Run Functions #####
        self.getRenderLayers()
        self.getAllAOVS()
        
        ######## Create Frames ########       
        for x in self.getRenderLayers:
            #print x
            self.incomingLayerOverridesValuesDictionary = {}
            self.renderLayersFrames = {}
            cbList = []
            
            self.frameVarName = (x + 'frame')
            self.frameLabelVarName = (x + 'labelVarName')
            self.frameLabelName = x
            frameCreate = Frame(self.framesHorizLayout, self.frameVarName, self.frameLabelVarName, self.frameLabelName)

            self.renderLayersFrames[self.frameLabelName] = frameCreate.frameVarName           
            self.setDefaultRenderState()
          
            #### Saving which Frame is which Object #####
            #self.stashFrames[self.frameVarName] = frameCreate.frameVarName
           
            ####### Create Checkboxes #########
            for aov in self.getAOVs:
                                
                self.renderLayerButtons = {}
                self.makeColor = {}

                aovSplit = aov.split('aiAOV_')[1]                
                buttonVarName = (self.frameVarName + aovSplit + 'checkbox')                
                createButtons = UtilCreateCheckBox(buttonVarName, aovSplit, frameCreate.frameVarName)
                self.renderLayerButtons[aovSplit] = createButtons.buttonVarName
                
                #### Link Button Labels to Button IDs ####
                self.stashRenderButtons[buttonVarName] = createButtons.buttonVarName
                #print self.stashRenderButtons

                cbList.append(buttonVarName)
                              
                #### Change the Aov State Dictoinary Per Render Layer (Not Default Render Layer) #####                
                if x != "defaultRenderLayer":
                    self.getConnections = cmds.listConnections('%s.enabled' % aov, plugs=True)
                    if self.getConnections > 0:
                        for connection in self.getConnections:    
                            attr_component_list = connection.split(".")    
                            if attr_component_list[0] == x:
                                attr = ".".join(attr_component_list[0:-1])
                                getNewOverrideValue = cmds.getAttr("%s.value" % attr)    
                                if getNewOverrideValue == 1.0:
                                    getNewOverrideValue = True
                                else:
                                    getNewOverrideValue = False
                                               
                                self.defaultRenderLayerState[aovSplit] = getNewOverrideValue
                                self.makeColor[aovSplit] = "color: orange"
                             
                #### Load checkbox state from scene #######
                for node in self.renderLayerButtons:
                    setChecked = self.defaultRenderLayerState[node]
                    self.renderLayerButtons[node].setChecked(setChecked)
                    
                    #### Make overrides orange ####
                    if node in self.makeColor:
                        setColor = self.makeColor[node]
                        self.renderLayerButtons[node].setStyleSheet(setColor)
                        
            self.spacer1 = QtGui.QSpacerItem(0,50)
            frameCreate.frameVarName.layout().addSpacerItem(self.spacer1)
                        
            ####### Create Set Button #######
            self.setButtonVarName = (x + 'setButton')
            createSetButton = UtilCreateSetButton(self.setButtonVarName,frameCreate.frameVarName, self.printButtonStatus)
            #print createSetButton.setButtonVarName
            
            ###### Link Set Button in Frame to Frame/RenderLayer #######
            self.stashFramesCreateButton[createSetButton.setButtonVarName] = x
            #print self.stashFramesCreateButton
            
            ###### Link Buttons in Frame to Frame Create Set Button #######
            self.stashRenderButtonsPerFrame[createSetButton.setButtonVarName] = cbList
            #print self.stashRenderButtonsPerFrame
            
            #### Link Buttons to Frame they live in ####
            self.stashButtonsTwoFrame[frameCreate.frameLabelVarName] = cbList
            #print self.stashButtonsTwoFrame
            

            

    #################################################################################

        self.setLayout(layout) # add main layout itself to this dialog
        
    #################################################################################


    #################################################################################
    ################## FUNUCTIONS ###################################################
    #################################################################################
    
    def getRenderLayers(self):
        self.getRenderLayers = cmds.ls(type='renderLayer')
        
    def setDefaultRenderState(self):
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) != "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
        for node in self.getAOVs:
            self.getInitState = cmds.getAttr("%s.enabled" % node)
            node = node.split('aiAOV_')[1]
            self.defaultRenderLayerState[node] = self.getInitState
        
    def getAllAOVS(self):
        self.getAOVs = cmds.ls(type='aiAOV')
                            
    def printButtonStatus(self):
        splitName = []
        addName = []
        sender = []       
        sender = self.sender()        
        newKeys = self.stashRenderButtonsPerFrame[sender]
        for x in newKeys:
            splitName = x.split('frame')[1]
            splitName = splitName.split('checkbox')[0]
            addName = ('aiAOV_%s.enabled' % splitName)            
            if self.stashFramesCreateButton[sender] == "defaultRenderLayer":
                if self.stashRenderButtons[x].isChecked() == True:               
                    cmds.setAttr(addName, 1)
                else:
                    cmds.setAttr(addName, 0)                    
            else:                
                if self.stashRenderButtons[x].isChecked()==True and cmds.getAttr(addName) == 0:  
                    self.checkStatusSet(layer=self.stashFramesCreateButton[sender],value=1,attr=addName)            
                    self.stashRenderButtons[x].setStyleSheet("color: orange")
                if self.stashRenderButtons[x].isChecked()==False and cmds.getAttr(addName) == 1:
                    self.checkStatusSet(layer=self.stashFramesCreateButton[sender],value=0,attr=addName)                    
                    self.stashRenderButtons[x].setStyleSheet("color: orange")                                     
        if self.stashFramesCreateButton[sender] == "defaultRenderLayer":                
            launchUI()
            
    def checkStatusSet(self,layer=None,value=None,attr=None):
        cmds.editRenderLayerAdjustment(attr,layer=layer)
        connection_list = cmds.listConnections(attr, plugs=True)
        if connection_list is not None:
            for connection in connection_list:
                attr_component_list = connection.split(".")
                if attr_component_list[0] == layer:
                    attr = ".".join(attr_component_list[0:-1])
                    cmds.setAttr("%s.value" % attr, value)
                    
################# Create Frame Class ###########################################
        
class Frame(object):
    def __init__(self, parentLayout, frameVarName, frameLabelVarName, frameLabelName):
        
        self.frameLabelName = frameLabelName
        self.frameVarname = frameVarName      
        self.parentLayout = parentLayout
                        
        self.frameVarName = QtGui.QFrame()
        self.frameVarName.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        self.parentLayout.addWidget(self.frameVarName)        
        self.frameVarName.setLayout(QtGui.QVBoxLayout())              
        self.frameVarName.layout().setAlignment(QtCore.Qt.AlignTop)
        #self.frameVarName.setMinimumHeight(500)               
        self.frameLabelVarName = QtGui.QLabel(frameLabelName)
        self.frameVarName.layout().addWidget(self.frameLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.frameLabelVarName.setFont(font)
            
################## Create Checkbox Class ########################################
            
class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        self.buttonVarName = buttonVarName
        self.frame = frame
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        #self.buttonVarName.setStyleSheet("color: white")
        self.frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)
        
################## Create Set Button Class ########################################
            
class UtilCreateSetButton(object):
    def __init__(self, setButtonVarName, frame, printFunc):
        
        self.setButtonVarName = setButtonVarName
        self.frame = frame
        self.printFunc = printFunc
        
        self.setButtonVarName = QtGui.QPushButton('SET')
        self.frame.layout().addWidget(self.setButtonVarName)
        self.setButtonVarName.setMinimumHeight(50)                
        self.setButtonVarName.setMinimumWidth(200)
            
        self.setButtonVarName.clicked.connect(self.printFunc) ## clicked

########################################################################################

def launchUI():
    global AOVSet
    
    # will try and close the ui if it exists
    try: AOVSet.close()
    except: pass
    
    AOVSet = AOVSetUI()
    AOVSet.show()
    AOVSet.raise_()
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()
