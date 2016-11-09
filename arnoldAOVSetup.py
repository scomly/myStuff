# -*- coding: utf-8 -*-
Need to get them set per layer not every layer the same


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
    
class UtilityToolBoxUI(QtGui.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(UtilityToolBoxUI, self).__init__(parent)
        
        self.setWindowTitle("Utility Toolbox")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed
        
        ########### Stashbox #####################################

        layerOverridesDictionary = {}
        self.incomingLayerOverridesValuesDictoinary = {}
        self.renderLayersFrames = {}
        self.renderLayerButtons = {}
      
        #############################################################################

        self.createLayout() # runs function below
    
    ################################################################################    
    ##################### Layout Creation ##########################################    
    ################################################################################
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        self.setMinimumHeight(650)
        self.setMinimumWidth(750)
        layout.setSpacing(0)

        self.framesHorizLayout = QtGui.QHBoxLayout() # layout for frames
        layout.addLayout(self.framesHorizLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.getRenderLayers()
        
        
        ######## Create Frames ########        
        for x in getRenderLayers:
            frameVarName = (x + 'frame')
            frameLabelVarName = (x + 'labelVarName')
            frameLabelName = x
            frameCreate = Frame(self.framesHorizLayout, frameVarName, frameLabelVarName, frameLabelName)
            self.renderLayersFrames[frameLabelName] = frameCreate.frameVarName
            #print self.renderLayersFrames
            
            ##### Get Existing Overrides ######
            getConnections = cmds.listConnections('%s.adjustments' % x, destination=False, source=True, plugs=True)           
            for node in getConnections:
                getValue = cmds.getAttr(node)                
                node = node.split('aiAOV_')[1]
                node = node.split('.enabled')[0]
                self.incomingLayerOverridesValuesDictoinary[node] = getValue
            #print self.incomingLayerOverridesValuesDictoinary
            
            self.getAllAOVS()            
            
            ####### Create Checkboxes #########
            for aov in self.getAOVs:
                aov = aov.split('aiAOV_')[1]          
                buttonVarName = (aov + 'checkbox')                
                createButtons = UtilCreateCheckBox(buttonVarName, aov, frameCreate.frameVarName)
                self.renderLayerButtons[aov] = createButtons.buttonVarName
                
                #### Load checkbox state from scene #######
                for x in self.renderLayerButtons:
                    if x in self.incomingLayerOverridesValuesDictoinary.keys():
                        setChecked = self.incomingLayerOverridesValuesDictoinary[x]
                        self.renderLayerButtons[x].setChecked(setChecked)

    #################################################################################

        self.setLayout(layout) # add main layout itself to this dialog
        
    #################################################################################


    #################################################################################
    ################## FUNUCTIONS ###################################################
    #################################################################################

    
    def getRenderLayers(self):
        getRenderLayers = cmds.ls(type='renderLayer')
        
    def getAllAOVS(self):
        self.getAOVs = cmds.ls(type='aiAOV')
                
    def getOVR_perLayer(self):
        for x in getRenderLayers:
            getConnections = cmds.listConnections('%s.adjustments' % x, destination=False, source=True, plugs=True)
            layerOverridesDictionary[x] = getConnections


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
        self.frameVarName.setMinimumHeight(500)
               
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
        self.frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)

########################################################################################

def launchUI():
    global vrayToolBoxUtil
    
    # will try and close the ui if it exists
    try: vrayToolBoxUtil.close()
    except: pass
    
    vrayToolBoxUtil = UtilityToolBoxUI()
    vrayToolBoxUtil.show()
    vrayToolBoxUtil.raise_()   
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()



