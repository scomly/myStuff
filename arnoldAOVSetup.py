from PySide import QtGui
from PySide import QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken

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
        self.stashReverseRenderButtons = {}
        self.stashRenderButtonsPerFrame = {}
        self.stashButtonsTwoFrame = {}
        self.stashToggleButton = {}
        self.stashOverrides = []
      
        #############################################################################

        self.createLayout() # runs function below
        
    
    ################################################################################    
    ##################### Layout Creation ##########################################    
    ################################################################################
        

    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        #self.setMinimumHeight(700)
        #self.setMinimumWidth(1000)
        layout.layout().setContentsMargins(0,0,0,0)
        layout.layout().setSpacing(0)
        
        
        scroll_area = QtGui.QScrollArea(self)
        scroll_area_content = QtGui.QFrame(self)
        
        scroll_area_content.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        scroll_area.setWidget(scroll_area_content)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)       

        self.framesHorizLayout = QtGui.QHBoxLayout(scroll_area_content) # layout for frames
        self.framesHorizLayout.layout().setContentsMargins(0,0,0,0)
        self.framesHorizLayout.layout().setSpacing(0)
        
        
        
     
        
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
                createButtons = UtilCreateCheckBox(buttonVarName, aovSplit, frameCreate.frameVarName, self.returnSignal)
                self.renderLayerButtons[aovSplit] = createButtons.buttonVarName
                
                #### Link Button Labels to Button IDs ####
                self.stashRenderButtons[buttonVarName] = createButtons.buttonVarName
                #print self.stashRenderButtons
                
                #### Reverse Button IDs to Labels ######
                self.stashReverseRenderButtons[createButtons.buttonVarName] = buttonVarName
                
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
                        self.stashOverrides.append(self.renderLayerButtons[node])
                        setColor = self.makeColor[node]
                        self.renderLayerButtons[node].setStyleSheet(setColor)
                        
            self.spacer1 = QtGui.QSpacerItem(0,50)
            frameCreate.frameVarName.layout().addSpacerItem(self.spacer1)
            
            ####### Create Toggle Button #####
            self.setToggleVarName = (x + 'Toggle')
            createToggleButton = UtilCreateToggleButton(self.setToggleVarName,frameCreate.frameVarName, self.toggleFunc)
                        
            ####### Create Set Button #######
            self.setButtonVarName = (x + 'setButton')
            createSetButton = UtilCreateSetButton(self.setButtonVarName,frameCreate.frameVarName, self.setButtonStatus)
            
            ###### Link Set Button in Frame to Frame/RenderLayer #######
            self.stashFramesCreateButton[createSetButton.setButtonVarName] = x
            #print self.stashFramesCreateButton
            
            ###### Link Buttons in Frame to Frame Create Set Button #######
            self.stashRenderButtonsPerFrame[createSetButton.setButtonVarName] = cbList
            #print self.stashRenderButtonsPerFrame
            
            #### Link Buttons to Frame they live in ####
            self.stashButtonsTwoFrame[frameCreate.frameVarName] = cbList
            #print self.stashButtonsTwoFrame
            
            #### Link Toggle Button to Set Button in same Frame ####
            self.stashToggleButton[createToggleButton.setToggleVarName] = frameCreate.frameVarName
            #print self.stashToggleButton
            
            self.spacer2 = QtGui.QSpacerItem(0,100)
            self.framesHorizLayout.layout().addSpacerItem(self.spacer2)

    #################################################################################

        self.setLayout(layout) # add main layout itself to this dialog
        getSize = scroll_area_content.sizeHint()
        getSize.setWidth(min(2000, getSize.width()))
        getSize.setHeight(min(1000, getSize.height()))
        self.resize(getSize)
        
    #################################################################################


    #################################################################################
    ################## FUNUCTIONS ###################################################
    #################################################################################
    
    def getRenderLayers(self):
        self.getRenderLayers = cmds.ls(type='renderLayer')
        ### to make sure default render layer is first in the list ####
        self.getRenderLayers.remove('defaultRenderLayer')
        self.getRenderLayers.insert(0,'defaultRenderLayer')
        
    def setDefaultRenderState(self):
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) != "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
        for node in self.getAOVs:
            nodeSplit = []
            self.getInitState = cmds.getAttr("%s.enabled" % node)
            nodeSplit = node.split('aiAOV_')[1]
            self.defaultRenderLayerState[nodeSplit] = self.getInitState
        
    def getAllAOVS(self):
        self.getAOVs = cmds.ls(type='aiAOV')
                            
    def setButtonStatus(self):
        splitName = []
        addName = []
        sender = []
        newX = []
        newXTwo = []
        newY = []
        newYTwo = []     
        sender = self.sender()        
        newKeys = self.stashRenderButtonsPerFrame[sender]
        #print newKeys
        for x in newKeys:
            #print x#
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
                    self.stashOverrides.append(self.stashRenderButtons[x])  ### problem is here I think


                if self.stashRenderButtons[x].isChecked()==False and cmds.getAttr(addName) == 1:
                    self.checkStatusSet(layer=self.stashFramesCreateButton[sender],value=0,attr=addName)                    
                    self.stashRenderButtons[x].setStyleSheet("color: orange")

                    
                if self.stashRenderButtons[x].isChecked()==True and cmds.getAttr(addName) == 1:  
                    cmds.editRenderLayerAdjustment(addName, layer=self.stashFramesCreateButton[sender], remove=True)        
                    self.stashRenderButtons[x].setStyleSheet("color: active")

                if self.stashRenderButtons[x].isChecked()==False and cmds.getAttr(addName) == 0:
                    cmds.editRenderLayerAdjustment(addName, layer=self.stashFramesCreateButton[sender], remove=True)        
                    self.stashRenderButtons[x].setStyleSheet("color: active")
                    

                    
                    

                                                      
        if self.stashFramesCreateButton[sender] == "defaultRenderLayer":
            #print self.stashOverrides
            test = {}
            newX = []
            newXTwo = []
            newY = []
            newYTwo = []
            #setChecked = []
            for x in self.stashRenderButtons:
                y = self.stashRenderButtons[x]
                if y not in self.stashOverrides:
                    self.setDefaultRenderState()
                    newX = x.split('frame')[1]
                    newXTwo = newX.split('checkbox')[0]
                    setChecked = self.defaultRenderLayerState[newXTwo]
                    self.stashRenderButtons[x].setChecked(setChecked)

          
    def checkStatusSet(self,layer=None,value=None,attr=None):
        cmds.editRenderLayerAdjustment(attr,layer=layer)
        connection_list = cmds.listConnections(attr, plugs=True)
        if connection_list is not None:
            for connection in connection_list:
                attr_component_list = connection.split(".")
                if attr_component_list[0] == layer:
                    attr = ".".join(attr_component_list[0:-1])
                    cmds.setAttr("%s.value" % attr, value)
                                        
    def toggleFunc(self):
        getFlip = []
        getButtons = []
        toggleSend = self.sender()
        getFrameFlip = self.stashToggleButton[toggleSend]
        getButtons = self.stashButtonsTwoFrame[getFrameFlip]
        getOne = self.stashRenderButtons[getButtons[0]]
        if getOne.isChecked() == False:            
            for x in getButtons:
                self.stashRenderButtons[x].setChecked(True)
        else:
            for x in getButtons:
                self.stashRenderButtons[x].setChecked(False)
        
        
    def returnSignal(self):
        splitName = []
        addName = []
        sender = []       
        sender = self.sender()
        removeItem = self.stashReverseRenderButtons[sender]
        splitItem = removeItem.split('frame')[1]
        splitItemTwo = splitItem.split('checkbox')[0]
        addAttribute = ('aiAOV_%s.enabled' % splitItemTwo)
        self.layer = removeItem.split('frame')[0]
        getConnections = cmds.listConnections(addAttribute, plugs=True)
        if getConnections > 0:
            for connection in getConnections:    
                attr_component_list = connection.split(".") 
                if attr_component_list[0] == self.layer:    
                    self.getSender =  self.sender()
                    self.menu = QtGui.QMenu()
                    deleteAction = QtGui.QAction('Remove Override', self)
                    deleteAction.triggered.connect(self.removeOverride)
                    self.menu.addAction(deleteAction)
                    self.menu.popup(QtGui.QCursor.pos())
        
        
    def removeOverride(self):
        #splitName = []
        #addName = []
        #sender = []       
        sender = self.getSender
        removeItem = self.stashReverseRenderButtons[sender]
        splitItem = removeItem.split('frame')[1]
        splitItem = splitItem.split('checkbox')[0]
        addAttribute = ('aiAOV_%s.enabled' % splitItem)
        cmds.editRenderLayerAdjustment(addAttribute, layer=self.layer, remove=True)
        getDefaultState = cmds.getAttr(addAttribute)
        if sender in self.stashOverrides:
            self.stashOverrides.remove(sender)
        #print sender
        if getDefaultState == 1:
            sender.setChecked(True)          
            sender.setStyleSheet("color: active")
        else:
            sender.setChecked(False)          
            sender.setStyleSheet("color: active")            

        
                    
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
        self.frameVarName.setMinimumHeight(100)
        #self.frameVarName.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)               
        self.frameLabelVarName = QtGui.QLabel(frameLabelName)
        self.frameVarName.layout().addWidget(self.frameLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.frameLabelVarName.setFont(font)
            
################## Create Checkbox Class ########################################
            
class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame, rmbFunc):
        
        self.buttonVarName = buttonVarName
        self.frame = frame        
        self.rmbFunc = rmbFunc
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        self.frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)
        
        self.buttonVarName.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.buttonVarName.customContextMenuRequested.connect(self.rmbFunc)
        
################## Create Toggle Class ########################################

class UtilCreateToggleButton(object):
    def __init__(self, setToggleVarName, frame, toggleFunc):
        
        self.setToggleVarName = setToggleVarName
        self.frame = frame
        self.toggleFunc = toggleFunc
        
        self.setToggleVarName = QtGui.QPushButton('TOGGLE ROW')
        self.frame.layout().addWidget(self.setToggleVarName)
        self.setToggleVarName.setMinimumHeight(25)                
        self.setToggleVarName.setMinimumWidth(200)
            
        self.setToggleVarName.clicked.connect(self.toggleFunc) ## clicked
        
################## Create Set Button Class ########################################
            
class UtilCreateSetButton(object):
    def __init__(self, setButtonVarName, frame, setFunc):
        
        self.setButtonVarName = setButtonVarName
        self.frame = frame
        self.setFunc = setFunc
        
        self.setButtonVarName = QtGui.QPushButton('SET')
        self.frame.layout().addWidget(self.setButtonVarName)
        self.setButtonVarName.setMinimumHeight(50)                
        self.setButtonVarName.setMinimumWidth(200)
            
        self.setButtonVarName.clicked.connect(self.setFunc) ## clicked

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
