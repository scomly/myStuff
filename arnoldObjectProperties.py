from PySide import QtGui
from PySide import QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken
import yaml
import os
import lighting.arnold.settings

####### Load Arnold #######
lighting.arnold.settings.initPlugin()

########################################################################
############################### GUI ####################################
########################################################################

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    
class ObjectProperty(QtGui.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(ObjectProperty, self).__init__(parent)
                
        self.setWindowTitle("Add Object Property Attributes")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed    
    
        ########### Checkbox Label List #####################################
                
        self.renderStats = ["Primary Visibility", "Cast Shadows", "Recieve Shadows", "Visible in Relfections", "Visible in Refractions"]
        self.aiStats = ["Self Shadows", "Opaque", "Visible in Diffuse", "Visible in Glossy", "Matte", "Trace Sets"]
        self.subD = ["Subdiv Type", "Subdiv Iterations"]
        self.disp = ["Disp Height", "Disp Padding", "Disp Zero Value", "Auto Bump"]
      
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
        
        #################### Which Kind Checkboxes ##################################
        
        #whichKindLabelLayout = QtGui.QHBoxLayout() # layout for label
        #layout.addLayout(whichKindLabelLayout)
        
        #whatKindLabel = QtGui.QLabel("Which Objects")
        #layout.addWidget(whatKindLabel)
        #font = QtGui.QFont()
        #font.setBold(True)
        #font.setPointSize(12)
        #whatKindLabel.setFont(font)
        #whatKindLabel.setMaximumWidth(200)
        #whatKindLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        WhichGeoLayout = QtGui.QHBoxLayout() # layout for frames
        layout.addLayout(WhichGeoLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)
        
        self.whichOne = QtGui.QSpacerItem(100,0)
        WhichGeoLayout.layout().addSpacerItem(self.whichOne)
        
        self.geoButton = QtGui.QCheckBox('Geometry')
        WhichGeoLayout.addWidget(self.geoButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.geoButton.setFont(font)
        self.geoButton.setChecked(True)
        
        self.procPullButton = QtGui.QCheckBox('Procedural Pulldown')
        WhichGeoLayout.addWidget(self.procPullButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.procPullButton.setFont(font)
        self.procPullButton.setChecked(False)
        
        self.procCheckboxButton = QtGui.QCheckBox('Procedural Checkbox')
        WhichGeoLayout.addWidget(self.procCheckboxButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.procCheckboxButton.setFont(font)
        self.procCheckboxButton.setChecked(False)
        
        self.whichTwo = QtGui.QSpacerItem(100,0)
        WhichGeoLayout.layout().addSpacerItem(self.whichTwo)
        
        ################## Layout for frames ########################################
        
        self.whichThree = QtGui.QSpacerItem(0,10)
        layout.layout().addSpacerItem(self.whichThree)
               
        framesHorizLayout = QtGui.QHBoxLayout() # layout for frames
        layout.addLayout(framesHorizLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)
        
        ########### Catch All Checkboxes Here #######################################
        
        self.renderStatsButtonList = []
        self.aiStatsButtonList = []
        self.subDButtonList = []
        self.dispButtonList = []
        
        self.outputText = []
             

        #################### Render Stats Frame #####################################
        
        self.rStats_frame = QtGui.QFrame()
        self.rStats_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.rStats_frame)
        
        self.rStats_frame.setLayout(QtGui.QVBoxLayout())
              
        self.rStats_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        self.rStats_frame.setMinimumHeight(200)
                
        self.rStatsframeLabelVarName = QtGui.QLabel('Render Stats')
        self.rStatsframeLabelVarName.setToolTip("Click to toggle row")
        self.rStats_frame.layout().addWidget(self.rStatsframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.rStatsframeLabelVarName.setFont(font)
        self.rStatsframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.rStatsframeLabelVarName.mouseReleaseEvent = self.rStatsToggle
        
            ##### Widgets #####         
        
        self.primVisButton = QtGui.QCheckBox('Primary Visibility')
        self.renderStatsButtonList.append(self.primVisButton)
        self.rStats_frame.layout().addWidget(self.primVisButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.primVisButton.setFont(font)
        self.primVisButton.setChecked(True)
                
        self.castShadButton = QtGui.QCheckBox('Cast Shadows')
        self.renderStatsButtonList.append(self.castShadButton)
        self.rStats_frame.layout().addWidget(self.castShadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.castShadButton.setFont(font)
        self.castShadButton.setChecked(True)
        
        self.recShadButton = QtGui.QCheckBox('Recieve Shadows')
        self.renderStatsButtonList.append(self.recShadButton)
        self.rStats_frame.layout().addWidget(self.recShadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.recShadButton.setFont(font)
        self.recShadButton.setChecked(True)   
        
        self.visReflButton = QtGui.QCheckBox('Visible in Reflections')
        self.renderStatsButtonList.append(self.visReflButton)
        self.rStats_frame.layout().addWidget(self.visReflButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visReflButton.setFont(font)
        self.visReflButton.setChecked(True)
        
        self.visRefrButton = QtGui.QCheckBox('Visible in Refractions')
        self.renderStatsButtonList.append(self.visRefrButton)
        self.rStats_frame.layout().addWidget(self.visRefrButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visRefrButton.setFont(font)
        self.visRefrButton.setChecked(True)
        
        self.spacer1 = QtGui.QSpacerItem(0,39)
        self.rStats_frame.layout().addSpacerItem(self.spacer1)
        
        self.rStatsSetButton = QtGui.QPushButton("Add")
        self.rStatsSetButton.setToolTip("Adds renders attributes to selected set")
        self.rStats_frame.layout().addWidget(self.rStatsSetButton)
        self.rStatsSetButton.clicked.connect(self.checkRenderStats) ## clicked
        
        self.rStatsRemoveButton = QtGui.QPushButton("Remove")
        self.rStatsRemoveButton.setToolTip("Removes renders attributes to selected set")
        self.rStats_frame.layout().addWidget(self.rStatsRemoveButton)
        self.rStatsRemoveButton.clicked.connect(self.deleteRenderStats) ## clicked
              
        #################### Ai Render State Frame ##############################################
        
        self.aiStats_frame = QtGui.QFrame()
        self.aiStats_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.aiStats_frame)
        
        self.aiStats_frame.setLayout(QtGui.QVBoxLayout())
        self.aiStats_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.aiStatsframeLabelVarName = QtGui.QLabel('Ai Render Stats')
        self.aiStatsframeLabelVarName.setToolTip("Click to toggle row")
        self.aiStats_frame.layout().addWidget(self.aiStatsframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.aiStatsframeLabelVarName.setFont(font)
        self.aiStatsframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.aiStatsframeLabelVarName.mouseReleaseEvent = self.aiToggle

        ######## Checkboxes ########
        
        self.selfShadButton = QtGui.QCheckBox('Self Shadows')
        self.aiStatsButtonList.append(self.selfShadButton)
        self.aiStats_frame.layout().addWidget(self.selfShadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selfShadButton.setFont(font)
        self.selfShadButton.setChecked(False)
        
        self.opaqueButton = QtGui.QCheckBox('Opaque')
        self.aiStatsButtonList.append(self.opaqueButton)
        self.aiStats_frame.layout().addWidget(self.opaqueButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.opaqueButton.setFont(font)
        self.opaqueButton.setChecked(False)
        
        self.visDiffButton = QtGui.QCheckBox('Visible in Diffuse')
        self.aiStatsButtonList.append(self.visDiffButton)
        self.aiStats_frame.layout().addWidget(self.visDiffButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visDiffButton.setFont(font)
        self.visDiffButton.setChecked(False)
        
        self.visGlossButton = QtGui.QCheckBox('Visible in Glossy')
        self.aiStatsButtonList.append(self.visGlossButton)
        self.aiStats_frame.layout().addWidget(self.visGlossButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visGlossButton.setFont(font)
        self.visGlossButton.setChecked(False)
        
        self.matteButton = QtGui.QCheckBox('Matte')
        self.aiStatsButtonList.append(self.matteButton)
        self.aiStats_frame.layout().addWidget(self.matteButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.matteButton.setFont(font)
        self.matteButton.setChecked(False)
        
        self.traceSetButton = QtGui.QCheckBox('Trace Sets')
        self.aiStatsButtonList.append(self.traceSetButton)
        self.aiStats_frame.layout().addWidget(self.traceSetButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.traceSetButton.setFont(font)
        self.traceSetButton.setChecked(False)
        
        self.spacer2 = QtGui.QSpacerItem(0,18)
        self.aiStats_frame.layout().addSpacerItem(self.spacer2)
        
        self.aiStatsSetButton = QtGui.QPushButton("Add")
        self.aiStatsSetButton.setToolTip("Adds renders attributes to selected set")
        self.aiStats_frame.layout().addWidget(self.aiStatsSetButton)
        self.aiStatsSetButton.clicked.connect(self.checkAiRenderStats) ## clicked
        
        self.aiStatsRemoveButton = QtGui.QPushButton("Remove")
        self.aiStatsRemoveButton.setToolTip("Removes renders attributes to selected set")
        self.aiStats_frame.layout().addWidget(self.aiStatsRemoveButton)
        self.aiStatsRemoveButton.clicked.connect(self.deleteAiRenderStats) ## clicked

        #################### SubD Frame ##############################################
        
        self.subD_frame = QtGui.QFrame()
        self.subD_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.subD_frame)
        
        self.subD_frame.setLayout(QtGui.QVBoxLayout())
        self.subD_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.subDframeLabelVarName = QtGui.QLabel('SubD')
        self.subDframeLabelVarName.setToolTip("Click to toggle row")
        self.subD_frame.layout().addWidget(self.subDframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.subDframeLabelVarName.setFont(font)
        self.subDframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.subDframeLabelVarName.mouseReleaseEvent = self.subDToggle
        
        self.subTypeButton = QtGui.QCheckBox('Subdiv Type')
        self.subDButtonList.append(self.subTypeButton)
        self.subD_frame.layout().addWidget(self.subTypeButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.subTypeButton.setFont(font)
        self.subTypeButton.setChecked(False)
        
        self.subIterButton = QtGui.QCheckBox('Subdiv Iterations')
        self.subDButtonList.append(self.subIterButton)
        self.subD_frame.layout().addWidget(self.subIterButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.subIterButton.setFont(font)
        self.subIterButton.setChecked(False)
        
        self.spacer3 = QtGui.QSpacerItem(0,102)
        self.subD_frame.layout().addSpacerItem(self.spacer3)
        
        self.subDSetButton = QtGui.QPushButton("Add")
        self.subDSetButton.setToolTip("Adds renders attributes to selected set")
        self.subD_frame.layout().addWidget(self.subDSetButton)
        self.subDSetButton.clicked.connect(self.checkSubD) ## clicked

        self.subDRemoveButton = QtGui.QPushButton("Remove")
        self.subDRemoveButton.setToolTip("Removes renders attributes to selected set")
        self.subD_frame.layout().addWidget(self.subDRemoveButton)
        self.subDRemoveButton.clicked.connect(self.deleteSubD) ## clicked
              
        #################### Disp Frame ##############################################
               
        self.disp_frame = QtGui.QFrame()
        self.disp_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.disp_frame)
        
        self.disp_frame.setLayout(QtGui.QVBoxLayout())
        self.disp_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.dispframeLabelVarName = QtGui.QLabel('Displace')
        self.dispframeLabelVarName.setToolTip("Click to toggle row")
        
        self.disp_frame.layout().addWidget(self.dispframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.dispframeLabelVarName.setFont(font)
        self.dispframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.dispframeLabelVarName.mouseReleaseEvent = self.dispToggle

        self.dispHeightButton = QtGui.QCheckBox('Disp Height(Not in Proc)')
        self.dispButtonList.append(self.dispHeightButton)
        self.disp_frame.layout().addWidget(self.dispHeightButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispHeightButton.setFont(font)
        self.dispHeightButton.setChecked(False)        

        self.dispPadButton = QtGui.QCheckBox('Disp Padding')
        self.dispButtonList.append(self.dispPadButton)
        self.disp_frame.layout().addWidget(self.dispPadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispPadButton.setFont(font)
        self.dispPadButton.setChecked(False) 

        self.dispZeroButton = QtGui.QCheckBox('Disp Zero Value')
        self.dispButtonList.append(self.dispZeroButton)
        self.disp_frame.layout().addWidget(self.dispZeroButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispZeroButton.setFont(font)
        self.dispZeroButton.setChecked(False) 

        self.autoBumpButton = QtGui.QCheckBox('Auto Bump')
        self.dispButtonList.append(self.autoBumpButton)
        self.disp_frame.layout().addWidget(self.autoBumpButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autoBumpButton.setFont(font)
        self.autoBumpButton.setChecked(False)
                
        self.spacer4 = QtGui.QSpacerItem(0,60)
        self.disp_frame.layout().addSpacerItem(self.spacer4)
        
        self.dispSetButton = QtGui.QPushButton("Add")
        self.dispSetButton.setToolTip("Adds renders attributes to selected set")
        self.disp_frame.layout().addWidget(self.dispSetButton)
        self.dispSetButton.clicked.connect(self.checkDisp) ## clicked

        self.dispRemoveButton = QtGui.QPushButton("Remove")
        self.dispRemoveButton.setToolTip("Removes renders attributes to selected set")
        self.disp_frame.layout().addWidget(self.dispRemoveButton)
        self.dispRemoveButton.clicked.connect(self.deleteDisp) ## clicked

        ########### Set Name Box ################
        
        lineEditHorizLayout = QtGui.QHBoxLayout() # layout for set creation
        layout.addLayout(lineEditHorizLayout)
        lineEditHorizLayout.layout().setAlignment(QtCore.Qt.AlignLeft)
        lineEditHorizLayout.layout().setContentsMargins(200,5,5,5)        
        self.createSet_label = QtGui.QLabel('Set Name')
        setLabelFont = QtGui.QFont()
        setLabelFont.setBold(True)
        setLabelFont.setPointSize(10)
        self.createSet_label.setFont(setLabelFont)
        lineEditHorizLayout.addWidget(self.createSet_label)
        self.createSet_label.setMaximumWidth(70)                      
        self.createSet_lineEdit = LineEdit()
        self.createSet_lineEdit.setMaximumWidth(200)
        lineEditHorizLayout.addWidget(self.createSet_lineEdit)
        self.createSet_lineEdit.setPlaceholderText("Name the set here")
               
        ########### Create Button ################
        
        createLayout = QtGui.QVBoxLayout() # layout for set creation button
        layout.addLayout(createLayout)
        createLayout.layout().setAlignment(QtCore.Qt.AlignCenter)
        createLayout.layout().setContentsMargins(5,5,5,5) 
        self.createButton = QtGui.QPushButton("Create")
        self.createButton.setToolTip("Clicking Create will create a set with the above attributes and the seletced geometry. Please name the set before clicking Create")
        createLayout.layout().addWidget(self.createButton)
        self.createButton.setMinimumHeight(50)
        self.createButton.setMinimumWidth(400)
        self.createButton.clicked.connect(self.createSet) ## clicked
        
        ########### Edit Sets Buttons ################
        
        spacer = QtGui.QSpacerItem(175,10)
        layout.addSpacerItem(spacer)
        
        editSetsLabelLayout = QtGui.QHBoxLayout() # layout for label
        layout.addLayout(editSetsLabelLayout)
        
        editSetsLabel = QtGui.QLabel("Edit Sets")
        editSetsLabelLayout.addWidget(editSetsLabel)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        editSetsLabel.setFont(font)
        editSetsLabel.setMaximumWidth(100)
        editSetsLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        editSetsButtonsLayout = QtGui.QHBoxLayout() # layout for buttons
        layout.addLayout(editSetsButtonsLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)
        
        self.addToSetButton = QtGui.QPushButton("Add")
        self.addToSetButton.setToolTip("To add objects or to nest sets select the objects or sets you want to add first then select the set you want to add them too last.")
        editSetsButtonsLayout.layout().addWidget(self.addToSetButton)
        self.addToSetButton.setMinimumHeight(50)
        self.addToSetButton.setMinimumWidth(150)

        self.addToSetButton.clicked.connect(self.addSetMembers) ## clicked
        
        self.removeToSetButton = QtGui.QPushButton("Remove")
        self.removeToSetButton.setToolTip("To remove objects from a set select the objects you want to remove first then the set you want to remove them from last.")
        editSetsButtonsLayout.layout().addWidget(self.removeToSetButton)
        self.removeToSetButton.setMinimumHeight(50)
        self.removeToSetButton.setMinimumWidth(150)
        self.removeToSetButton.clicked.connect(self.removeSetMembers) ## clicked        

        ########### Output Window #################
        
        self.outWindow = QtGui.QTextEdit()
        self.outWindow.setReadOnly(True)
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(275)
        self.outWindow.setText("Docs -- http://redmine.mill.co.uk/projects/millla/wiki/ArnoldObjectProperties")
        
        #######################################################################################        
                
        self.setLayout(layout)
        
###############################################################################################
    
  ######### Add Attributes ##########################
  
    def checkRenderStats(self):
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []       

        getSelect = cmds.ls(sl=True)[0]
      
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ########## Geo ########################################            
            if self.geoButton.isChecked()==True:          
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('primaryVisibility',node=theSet,ex=True) == False: 
                        addPrimaryVis = cmds.addAttr(ln='primaryVisibility',at='bool',dv=1)
                        self.outputText.append('Created Primary Visibility attribute')                    
                    else:
                        self.outputText.append("<font color=yellow>Primary Visibllity Already Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('castsShadows',node=theSet,ex=True) == False: 
                        addCastShad = cmds.addAttr(ln='castsShadows',at='bool',dv=1)
                        self.outputText.append('Created Cast Shadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Cast Shadows Already Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('recieveShadows',node=theSet,ex=True) == False: 
                        addReceiveShad = cmds.addAttr(ln='recieveShadows',at='bool',dv=1)
                        self.outputText.append('Created Recieve Shadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Recieve Shadows Already Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('visibleInReflections',node=theSet,ex=True) == False: 
                        addVisInKr = cmds.addAttr(ln='visibleInReflections',at='bool',dv=1)
                        self.outputText.append('Created Visible in Reflections attribute')
                    else:
                        self.outputText.append("<font color=yellow>Visible in Reflections Already Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('visibleInRefractions',node=theSet,ex=True) == False: 
                        addVisInKt = cmds.addAttr(ln='visibleInRefractions',at='bool',dv=1)
                        self.outputText.append('Created Visible in Refraction attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Refractions Already Exists<font/><br>")
           
           ############ Procedural Pulldown #######################
            if self.procPullButton.isChecked()==True:                                
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__primary',node=theSet,ex=True) == False: 
                        addPrimaryVis = cmds.addAttr(ln='attrai__all__vis__primary',at='bool',dv=1)
                        self.outputText.append('Created Primary Visibility attribute for procedural pulldown')                    
                    else:
                        self.outputText.append("<font color=yellow>Primary Visibllity Already Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__shadow',node=theSet,ex=True) == False: 
                        addCastShad = cmds.addAttr(ln='attrai__all__vis__shadow',at='bool',dv=1)
                        self.outputText.append('Created Cast Shadows attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>Cast Shadows Already Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__receive_shadows',node=theSet,ex=True) == False: 
                        addReceiveShad = cmds.addAttr(ln='attrai__all__shape__receive_shadows',at='bool',dv=1)
                        self.outputText.append('Created Recieve Shadows attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>Recieve Shadows Already Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__reflection',node=theSet,ex=True) == False: 
                        addVisInKr = cmds.addAttr(ln='attrai__all__vis__reflection',at='bool',dv=1)
                        self.outputText.append('Created Visible in Reflections attribute for procedural pulldown')
                    else:
                        self.outputText.append("<font color=yellow>Visible in Reflections Already Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__refraction',node=theSet,ex=True) == False: 
                        addVisInKt = cmds.addAttr(ln='attrai__all__vis__refraction',at='bool',dv=1)
                        self.outputText.append('Created Visible in Refraction attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Refractions Already Exists<font/><br>")                    

           ############ Procedural Checkbox #######################           
            if self.procCheckboxButton.isChecked()==True:                                
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__primary',node=theSet,ex=True) == False: 
                        addPrimaryVis = cmds.addAttr(ln='attrai__vis__primary',at='bool',dv=1)
                        self.outputText.append('Created Primary Visibility attribute for procedural checkbox')                    
                    else:
                        self.outputText.append("<font color=yellow>Primary Visibllity Already Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__shadow',node=theSet,ex=True) == False: 
                        addCastShad = cmds.addAttr(ln='attrai__vis__shadow',at='bool',dv=1)
                        self.outputText.append('Created Cast Shadows attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>Cast Shadows Already Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__receive_shadows',node=theSet,ex=True) == False: 
                        addReceiveShad = cmds.addAttr(ln='attrai__shape__receive_shadows',at='bool',dv=1)
                        self.outputText.append('Created Recieve Shadows attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>Recieve Shadows Already Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__reflection',node=theSet,ex=True) == False: 
                        addVisInKr = cmds.addAttr(ln='attrai__vis__reflection',at='bool',dv=1)
                        self.outputText.append('Created Visible in Reflections attribute for procedural checkbox')
                    else:
                        self.outputText.append("<font color=yellow>Visible in Reflections Already Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__refraction',node=theSet,ex=True) == False: 
                        addVisInKt = cmds.addAttr(ln='attrai__vis__refraction',at='bool',dv=1)
                        self.outputText.append('Created Visible in Refraction attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Refractions Already Exists<font/><br>")                                                 
        else:
            self.outputText.append("<font color=yellow>Select a Set to Add Attributes<font/>")
            
        self.getOutputText()

    def checkAiRenderStats(self):        
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ############## Geo #############################
            if self.geoButton.isChecked()==True:           
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('aiSelfShadows',node=theSet,ex=True) == False: 
                        addAiSelfShad = cmds.addAttr(ln='aiSelfShadows',at='bool',dv=1)
                        self.outputText.append('Created aiSelfShadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Self Shadows Already Exists<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('aiOpaque',node=theSet,ex=True) == False: 
                        addOpaque = cmds.addAttr(ln='aiOpaque',at='bool',dv=1)
                        self.outputText.append('Created aiOpaque attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiOpaque Already Exists<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('aiVisibleInDiffuse',node=theSet,ex=True) == False: 
                        addVisInKd = cmds.addAttr(ln='aiVisibleInDiffuse',at='bool',dv=1)
                        self.outputText.append('Created Visible in Diffuse attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Diffuse Already Exists<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('aiVisibleInGlossy',node=theSet,ex=True) == False: 
                        addVisInGlossy = cmds.addAttr(ln='aiVisibleInGlossy',at='bool',dv=1)
                        self.outputText.append('Created Visible in Glossy attribute') 
                    else:
                        print self.outputText.append("<font color=yellow>Visible in Glossy Already Exists<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('aiMatte',node=theSet,ex=True) == False: 
                        addMatte = cmds.addAttr(ln='aiMatte',at='bool',dv=0)
                        self.outputText.append('Created aiMatte attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Matte Already Exists<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('aiTraceSets',node=theSet,ex=True) == False: 
                        addAiTraceSets = cmds.addAttr(ln='aiTraceSets',dt='string')
                        self.outputText.append('Created Trace Sets attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Trace Sets Already Exists<font/><br>")
                    
            ############ Procedural Pulldown ###########################
            if self.procPullButton.isChecked()==True:             
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__self_shadows',node=theSet,ex=True) == False: 
                        addAiSelfShad = cmds.addAttr(ln='attrai__all__shape__self_shadows',at='bool',dv=1)
                        self.outputText.append('Created aiSelfShadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Self Shadows Already Exists for procedural pulldown<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__opaque',node=theSet,ex=True) == False: 
                        addOpaque = cmds.addAttr(ln='attrai__all__shape__opaque',at='bool',dv=1)
                        self.outputText.append('Created aiOpaque attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiOpaque Already Exists for procedural pulldown<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__diffuse',node=theSet,ex=True) == False: 
                        addVisInKd = cmds.addAttr(ln='attrai__all__vis__diffuse',at='bool',dv=1)
                        self.outputText.append('Created Visible in Diffuse attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Diffuse Already Exists for procedural pulldown<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__glossy',node=theSet,ex=True) == False: 
                        addVisInGlossy = cmds.addAttr(ln='attrai__all__vis__glossy',at='bool',dv=1)
                        self.outputText.append('Created Visible in Glossy attribute') 
                    else:
                        print self.outputText.append("<font color=yellow>Visible in Glossy Already Exists for procedural pulldown<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__matte',node=theSet,ex=True) == False: 
                        addMatte = cmds.addAttr(ln='attrai__shape__matte',at='bool',dv=0)
                        self.outputText.append('Created aiMatte attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Matte Already Exists for procedural pulldown<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__trace_sets',node=theSet,ex=True) == False: 
                        addAiTraceSets = cmds.addAttr(ln='attrai__shape__trace_sets',dt='string')
                        self.outputText.append('Created Trace Sets attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Trace Sets Already Exists for procedural pulldown<font/><br>")
            
            ############ Procedural Checkbox ###########################            
            if self.procCheckboxButton.isChecked()==True:             
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__self_shadows',node=theSet,ex=True) == False: 
                        addAiSelfShad = cmds.addAttr(ln='attrai__shape__self_shadows',at='bool',dv=1)
                        self.outputText.append('Created aiSelfShadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Self Shadows Already Exists for procedural checkbox<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__opaque',node=theSet,ex=True) == False: 
                        addOpaque = cmds.addAttr(ln='attrai__shape__opaque',at='bool',dv=1)
                        self.outputText.append('Created aiOpaque attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiOpaque Already Exists for procedural checkbox<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__diffuse',node=theSet,ex=True) == False: 
                        addVisInKd = cmds.addAttr(ln='attrai__vis__diffuse',at='bool',dv=1)
                        self.outputText.append('Created Visible in Diffuse attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Visible in Diffuse Already Exists for procedural checkbox<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__glossy',node=theSet,ex=True) == False: 
                        addVisInGlossy = cmds.addAttr(ln='attrai__vis__glossy',at='bool',dv=1)
                        self.outputText.append('Created Visible in Glossy attribute') 
                    else:
                        print self.outputText.append("<font color=yellow>Visible in Glossy Already Exists for procedural checkbox<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__matte',node=theSet,ex=True) == False: 
                        addMatte = cmds.addAttr(ln='attrai__shape__matte',at='bool',dv=0)
                        self.outputText.append('Created aiMatte attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Matte Already Exists for procedural checkbox<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__trace_sets',node=theSet,ex=True) == False: 
                        addAiTraceSets = cmds.addAttr(ln='attrai__shape__trace_sets',dt='string')
                        self.outputText.append('Created Trace Sets attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Trace Sets Already Exists for procedural checkbox<font/><br>")                    
        else:
            self.outputText.append("<font color=yellow>Select a Set to Add Attributes<font/>")
            
        self.getOutputText()

    def checkSubD(self):               
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect  
            
            ########### GEO ######################################
            if self.geoButton.isChecked()==True:        
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('aiSubdivType',node=theSet,ex=True) == False: 
                        addSubdivType = cmds.addAttr(ln='aiSubdivType',at='enum', enumName='none:catclark:linear')
                        self.outputText.append('Created aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Type Already Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('aiSubdivIterations',node=theSet,ex=True) == False: 
                        addSubdivIterations = cmds.addAttr(ln='aiSubdivIterations',at='byte')
                        self.outputText.append('Created aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Iterations Already Exists<font/><br>")
                    
            ########## Proc Pulldown ############################
            if self.procPullButton.isChecked()==True:
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_type',node=theSet,ex=True) == False: 
                        addSubdivType = cmds.addAttr(ln='attrai__polymesh__subdiv_type',at='enum', enumName='none:catclark:linear')
                        self.outputText.append('Created aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Type Already Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_iterations',node=theSet,ex=True) == False: 
                        addSubdivIterations = cmds.addAttr(ln='attrai__polymesh__subdiv_iterations',at='byte')
                        self.outputText.append('Created aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Iterations Already Exists<font/><br>")  
            
            ########## Proc Checkbox ############################
            if self.procCheckboxButton.isChecked()==True:
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_type',node=theSet,ex=True) == False: 
                        addSubdivType = cmds.addAttr(ln='attrai__polymesh__subdiv_type',at='enum', enumName='none:catclark:linear')
                        self.outputText.append('Created aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Type Already Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_iterations',node=theSet,ex=True) == False: 
                        addSubdivIterations = cmds.addAttr(ln='attrai__polymesh__subdiv_iterations',at='byte')
                        self.outputText.append('Created aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>aiSubdiv Iterations Already Exists<font/><br>")                    
        else:
            self.outputText.append("<font color=yellow>Select a Set to Add Attributes<font/><br>")
            
        self.getOutputText()
            
    def checkDisp(self):        
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ############## GEO ###############################################
            if self.geoButton.isChecked()==True:                      
                if self.dispHeightButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == False: 
                        addDispHeight = cmds.addAttr(ln='aiDispHeight',at='float')
                        self.outputText.append('Created Displacement Height attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispPadding',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='aiDispPadding',at='float')
                        self.outputText.append('Created Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispZeroValue',node=theSet,ex=True) == False:
                        addScalarZeroValue = cmds.addAttr(ln='aiDispZeroValue',at='float')
                        self.outputText.append('Created Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispAutobump',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='aiDispAutobump',at='bool',dv=0)
                        self.outputText.append('Created Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>AutoBump Already Exists<font/>")
                    
            ############ Proc Pulldown #################################
            if self.procPullButton.isChecked()==True:
                #if self.dispHeightButton.isChecked()==True:
                    #if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == False: 
                        #addDispHeight = cmds.addAttr(ln='aiDispHeight',at='float')
                        #self.outputText.append('Created Displacement Height attribute') 
                    #else:
                        #self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__min_disp_padding',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='attrai__min_disp_padding',at='float')
                        self.outputText.append('Created Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__use_default_disp_zero_value',node=theSet,ex=True) == False:
                        addScalarZeroValue = cmds.addAttr(ln='attrai__use_default_disp_zero_value',at='float')
                        self.outputText.append('Created Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__override_autobump',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='attrai__override_autobump',at='bool',dv=0)
                        self.outputText.append('Created Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>AutoBump Already Exists<font/>")
                    
            ############ Proc Checkbox #################################
            if self.procCheckboxButton.isChecked()==True:
                #if self.dispHeightButton.isChecked()==True:
                    #if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == False: 
                        #addDispHeight = cmds.addAttr(ln='aiDispHeight',at='float')
                        #self.outputText.append('Created Displacement Height attribute') 
                    #else:
                        #self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__min_disp_padding',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='attrai__min_disp_padding',at='float')
                        self.outputText.append('Created Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__use_default_disp_zero_value',node=theSet,ex=True) == False:
                        addScalarZeroValue = cmds.addAttr(ln='attrai__use_default_disp_zero_value',at='float')
                        self.outputText.append('Created Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__override_autobump',node=theSet,ex=True) == False: 
                        addBoundsPad = cmds.addAttr(ln='attrai__override_autobump',at='bool',dv=0)
                        self.outputText.append('Created Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>AutoBump Already Exists<font/>")  
               
        else:
            self.outputText.append("<font color=yellow>Select a Set to Add Attributes<font/>")
        
        self.getOutputText()    
            
  ######### Remove Attributes ##########################
  
    def deleteRenderStats(self):
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []       

        getSelect = cmds.ls(sl=True)[0]
      
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ############## GEO ########################################
            if self.geoButton.isChecked()==True:           
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('primaryVisibility',node=theSet,ex=True) == True: 
                        addPrimaryVis = cmds.deleteAttr('%s.primaryVisibility' % theSet)
                        self.outputText.append('Removed Primary Visibility attribute')                    
                    else:
                        self.outputText.append("<font color=yellow>No Primary Visibllity Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('castsShadows',node=theSet,ex=True) == True: 
                        addCastShad = cmds.deleteAttr('%s.castsShadows' % theSet)
                        self.outputText.append('Removed Cast Shadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Cast Shadows Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('recieveShadows',node=theSet,ex=True) == True: 
                        addReceiveShad = cmds.deleteAttr('%s.recieveShadows' % theSet)
                        self.outputText.append('Removed Recieve Shadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Recieve Shadows Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('visibleInReflections',node=theSet,ex=True) == True: 
                        addVisInKr = cmds.deleteAttr('%s.visibleInReflections' % theSet)
                        self.outputText.append('Removed Visible in Reflections attribute')
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Reflections Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('visibleInRefractions',node=theSet,ex=True) == True: 
                        addVisInKt = cmds.deleteAttr('%s.visibleInRefractions'% theSet)
                        self.outputText.append('Removed Visible in Refraction attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Refractions Exists<font/><br>")
                        
            ############## Procedural Pulldown ########################################
            if self.procPullButton.isChecked()==True:           
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__primary',node=theSet,ex=True) == True: 
                        addPrimaryVis = cmds.deleteAttr('%s.attrai__all__vis__primary' % theSet)
                        self.outputText.append('Removed Primary Visibility attribute for procedural pulldown')                    
                    else:
                        self.outputText.append("<font color=yellow>No Primary Visibllity Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__shadow',node=theSet,ex=True) == True: 
                        addCastShad = cmds.deleteAttr('%s.attrai__all__vis__shadow' % theSet)
                        self.outputText.append('Removed Cast Shadows attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Cast Shadows Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__receive_shadows',node=theSet,ex=True) == True: 
                        addReceiveShad = cmds.deleteAttr('%s.attrai__all__shape__receive_shadows' % theSet)
                        self.outputText.append('Removed Recieve Shadows attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Recieve Shadows Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__reflection',node=theSet,ex=True) == True: 
                        addVisInKr = cmds.deleteAttr('%s.attrai__all__vis__reflection' % theSet)
                        self.outputText.append('Removed Visible in Reflections attribute for procedural pulldown')
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Reflections Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__refraction',node=theSet,ex=True) == True: 
                        addVisInKt = cmds.deleteAttr('%s.attrai__all__vis__refraction'% theSet)
                        self.outputText.append('Removed Visible in Refraction attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Refractions Exists<font/><br>")
                        
            ############## Procedural Checkbox ########################################
            if self.procCheckboxButton.isChecked()==True:           
                if self.primVisButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__primary',node=theSet,ex=True) == True: 
                        addPrimaryVis = cmds.deleteAttr('%s.attrai__vis__primary' % theSet)
                        self.outputText.append('Removed Primary Visibility attribute for procedural checkbox')                    
                    else:
                        self.outputText.append("<font color=yellow>No Primary Visibllity Exists<font/><br>")            
                if self.castShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__shadow',node=theSet,ex=True) == True: 
                        addCastShad = cmds.deleteAttr('%s.attrai__vis__shadow' % theSet)
                        self.outputText.append('Removed Cast Shadows attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Cast Shadows Exists<font/><br>")
                if self.recShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__receive_shadows',node=theSet,ex=True) == True: 
                        addReceiveShad = cmds.deleteAttr('%s.attrai__shape__receive_shadows' % theSet)
                        self.outputText.append('Removed Recieve Shadows attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Recieve Shadows Exists<font/><br>")
                if self.visReflButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__reflection',node=theSet,ex=True) == True: 
                        addVisInKr = cmds.deleteAttr('%s.attrai__vis__reflection' % theSet)
                        self.outputText.append('Removed Visible in Reflections attribute for procedural checkbox')
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Reflections Exists<font/><br>")
                if self.visRefrButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__refraction',node=theSet,ex=True) == True: 
                        addVisInKt = cmds.deleteAttr('%s.attrai__vis__refraction'% theSet)
                        self.outputText.append('Removed Visible in Refraction attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Refractions Exists<font/><br>")                
                        
        else:
            self.outputText.append("<font color=yellow>Select a Set to Remove Attributes<font/>")
            
        self.getOutputText()

    def deleteAiRenderStats(self):        
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
        ############## GEO #####################################    
            if self.geoButton.isChecked()==True:           
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('aiSelfShadows',node=theSet,ex=True) == True: 
                        addAiSelfShad = cmds.deleteAttr('%s.aiSelfShadows' % theSet)
                        self.outputText.append('Removed aiSelfShadows attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Self Shadows Exists<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('aiOpaque',node=theSet,ex=True) == True: 
                        addOpaque = cmds.deleteAttr('%s.aiOpaque' % theSet)
                        self.outputText.append('Removed aiOpaque attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiOpaque Exists<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('aiVisibleInDiffuse',node=theSet,ex=True) == True: 
                        addVisInKd = cmds.deleteAttr('%s.aiVisibleInDiffuse' % theSet)
                        self.outputText.append('Removed Visible in Diffuse attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Diffuse Exists<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('aiVisibleInGlossy',node=theSet,ex=True) == True: 
                        addVisInGlossy = cmds.deleteAttr('%s.aiVisibleInGlossy' % theSet)
                        self.outputText.append('Removed Visible in Glossy attribute') 
                    else:
                        print self.outputText.append("<font color=yellow>No Visible in Glossy Exists<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('aiMatte',node=theSet,ex=True) == True:
                        addMatte = cmds.deleteAttr('%s.aiMatte' % theSet)
                        self.outputText.append('Removed aiMatte attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Matte Exists<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('aiTraceSets',node=theSet,ex=True) == True: 
                        addAiTraceSets = cmds.deleteAttr('%s.aiTraceSets' % theSet)
                        self.outputText.append('Removed Trace Sets attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No Trace Sets Exists<font/><br>")
                        
            ############## Procedural Pulldown #####################################    
            if self.procPullButton.isChecked()==True:           
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__self_shadows',node=theSet,ex=True) == True: 
                        addAiSelfShad = cmds.deleteAttr('%s.attrai__all__shape__self_shadows' % theSet)
                        self.outputText.append('Removed aiSelfShadows attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Self Shadows Exists<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__shape__opaque',node=theSet,ex=True) == True: 
                        addOpaque = cmds.deleteAttr('%s.attrai__all__shape__opaque' % theSet)
                        self.outputText.append('Removed aiOpaque attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No aiOpaque Exists<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__diffuse',node=theSet,ex=True) == True: 
                        addVisInKd = cmds.deleteAttr('%s.attrai__all__vis__diffuse' % theSet)
                        self.outputText.append('Removed Visible in Diffuse attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Diffuse Exists<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__all__vis__glossy',node=theSet,ex=True) == True: 
                        addVisInGlossy = cmds.deleteAttr('%s.attrai__all__vis__glossy' % theSet)
                        self.outputText.append('Removed Visible in Glossy attribute for procedural pulldown') 
                    else:
                        print self.outputText.append("<font color=yellow>No Visible in Glossy Exists<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__matte',node=theSet,ex=True) == True:
                        addMatte = cmds.deleteAttr('%s.attrai__shape__matte' % theSet)
                        self.outputText.append('Removed aiMatte attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Matte Exists<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__trace_sets',node=theSet,ex=True) == True: 
                        addAiTraceSets = cmds.deleteAttr('%s.attrai__shape__trace_sets' % theSet)
                        self.outputText.append('Removed Trace Sets attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No Trace Sets Exists<font/><br>") 
                        
            ############## Procedural Checkbox #####################################    
            if self.procCheckboxButton.isChecked()==True:           
                if self.selfShadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__self_shadows',node=theSet,ex=True) == True: 
                        addAiSelfShad = cmds.deleteAttr('%s.attrai__shape__self_shadows' % theSet)
                        self.outputText.append('Removed aiSelfShadows attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Self Shadows Exists<font/><br>")            
                if self.opaqueButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__opaque',node=theSet,ex=True) == True: 
                        addOpaque = cmds.deleteAttr('%s.attrai__shape__opaque' % theSet)
                        self.outputText.append('Removed aiOpaque attribute for procedural pulldown') 
                    else:
                        self.outputText.append("<font color=yellow>No aiOpaque Exists<font/><br>")
                if self.visDiffButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__diffuse',node=theSet,ex=True) == True: 
                        addVisInKd = cmds.deleteAttr('%s.attrai__vis__diffuse' % theSet)
                        self.outputText.append('Removed Visible in Diffuse attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Visible in Diffuse Exists<font/><br>")
                if self.visGlossButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__vis__glossy',node=theSet,ex=True) == True: 
                        addVisInGlossy = cmds.deleteAttr('%s.attrai__vis__glossy' % theSet)
                        self.outputText.append('Removed Visible in Glossy attribute for procedural checkbox') 
                    else:
                        print self.outputText.append("<font color=yellow>No Visible in Glossy Exists<font/><br>")
                if self.matteButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__matte',node=theSet,ex=True) == True:
                        addMatte = cmds.deleteAttr('%s.attrai__shape__matte' % theSet)
                        self.outputText.append('Removed aiMatte attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>Matte Already Exists<font/><br>")
                if self.traceSetButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__shape__trace_sets',node=theSet,ex=True) == True: 
                        addAiTraceSets = cmds.deleteAttr('%s.attrai__shape__trace_sets' % theSet)
                        self.outputText.append('Removed Trace Sets attribute for procedural checkbox') 
                    else:
                        self.outputText.append("<font color=yellow>No Trace Sets Exists<font/><br>")                                       
        else:
            self.outputText.append("<font color=yellow>Select a Set to Remove Attributes<font/>")
            
        self.getOutputText()

    def deleteSubD(self):               
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ################## GEO ######################################  
            if self.geoButton.isChecked()==True:         
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('aiSubdivType',node=theSet,ex=True) == True: 
                        addSubdivType = cmds.deleteAttr('%s.aiSubdivType' % theSet)
                        self.outputText.append('Removed aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Type Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('aiSubdivIterations',node=theSet,ex=True) == True: 
                        addSubdivIterations = cmds.deleteAttr('%s.aiSubdivIterations' % theSet)
                        self.outputText.append('Removed aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Iterations Exists<font/><br>")
                    
            ################ Procedural Pulldown ################################
            if self.procPullButton.isChecked()==True:
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_type',node=theSet,ex=True) == True: 
                        addSubdivType = cmds.deleteAttr('%s.attrai__polymesh__subdiv_type' % theSet)
                        self.outputText.append('Removed aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Type Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_iterations',node=theSet,ex=True) == True: 
                        addSubdivIterations = cmds.deleteAttr('%s.attrai__polymesh__subdiv_iterations' % theSet)
                        self.outputText.append('Removed aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Iterations Exists<font/><br>")
                    
           ################ Procedural Checkbox ################################
            if self.procCheckboxButton.isChecked()==True:
                if self.subTypeButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_type',node=theSet,ex=True) == True: 
                        addSubdivType = cmds.deleteAttr('%s.attrai__polymesh__subdiv_type' % theSet)
                        self.outputText.append('Removed aiSubdiv Type attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Type Exists<font/><br>")            
                if self.subIterButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__polymesh__subdiv_iterations',node=theSet,ex=True) == True: 
                        addSubdivIterations = cmds.deleteAttr('%s.attrai__polymesh__subdiv_iterations' % theSet)
                        self.outputText.append('Removed aiSubdiv Iterations attribute') 
                    else:
                        self.outputText.append("<font color=yellow>No aiSubdiv Iterations Exists<font/><br>")                                 
        else:
            self.outputText.append("<font color=yellow>Select a Set to Remove Attributes<font/><br>")
            
        self.getOutputText()
            
    def deleteDisp(self):        
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []   
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect
            
            ############ GEO ##############################
            if self.geoButton.isChecked()==True:                        
                if self.dispHeightButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == True: 
                        addDispHeight = cmds.deleteAttr('%s.aiDispHeight' % theSet)
                        self.outputText.append('Removed Displacement Height attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispPadding',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.aiDispPadding' % theSet)
                        self.outputText.append('Removed Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispZeroValue',node=theSet,ex=True) == True: 
                        addScalarZeroValue = cmds.deleteAttr('%s.aiDispZeroValue' % theSet)
                        self.outputText.append('Removed Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('aiDispAutobump',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.aiDispAutobump' % theSet)
                        self.outputText.append('Removed Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>No AutoBump Exists<font/>")
                    
            ############### Procedural Pulldown ##############################
            if self.procPullButton.isChecked()==True:            
                #if self.dispHeightButton.isChecked()==True:
                    #if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == True: 
                        #addDispHeight = cmds.deleteAttr('%s.aiDispHeight' % theSet)
                        #self.outputText.append('Removed Displacement Height attribute') 
                    #else:
                        #self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__min_disp_padding',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.attrai__min_disp_padding' % theSet)
                        self.outputText.append('Removed Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__use_default_disp_zero_value',node=theSet,ex=True) == True: 
                        addScalarZeroValue = cmds.deleteAttr('%s.attrai__use_default_disp_zero_value' % theSet)
                        self.outputText.append('Removed Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__override_autobump',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.attrai__override_autobump' % theSet)
                        self.outputText.append('Removed Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>No AutoBump Exists<font/>")            
            
            ############### Procedural Checkbox ##############################
            if self.procCheckboxButton.isChecked()==True:            
                #if self.dispHeightButton.isChecked()==True:
                    #if cmds.attributeQuery('aiDispHeight',node=theSet,ex=True) == True: 
                        #addDispHeight = cmds.deleteAttr('%s.aiDispHeight' % theSet)
                        #self.outputText.append('Removed Displacement Height attribute') 
                    #else:
                        #self.outputText.append("<font color=yellow>Displacement Height Already Exists<font/><br>")            
                if self.dispPadButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__min_disp_padding',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.attrai__min_disp_padding' % theSet)
                        self.outputText.append('Removed Displacement Padding attribute') 
                    else:
                        self.outputText.append("<font color=yellow>Displacement Padding Already Exists<font/><br>")
                if self.dispZeroButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__use_default_disp_zero_value',node=theSet,ex=True) == True: 
                        addScalarZeroValue = cmds.deleteAttr('%s.attrai__use_default_disp_zero_value' % theSet)
                        self.outputText.append('Removed Displacement Zero Value attribute')
                    else:
                        self.outputText.append("<font color=yellow>Disp Zero Already Exists<font/><br>")
                if self.autoBumpButton.isChecked()==True:
                    if cmds.attributeQuery('attrai__override_autobump',node=theSet,ex=True) == True: 
                        addBoundsPad = cmds.deleteAttr('%s.attrai__override_autobump' % theSet)
                        self.outputText.append('Removed Disp Auto Bump attribute')                     
                    else:
                        self.outputText.append("<font color=yellow>No AutoBump Exists<font/>")                                              
        else:
            self.outputText.append("<font color=yellow>Select a Set to Remove Attributes<font/>")
        
        self.getOutputText()
                        
    def getOutputText(self):
        conformOutput = '\n'.join(self.outputText) ## reformats output list for things not using font tags
        outputTextWindow = self.outWindow.setText(conformOutput) ## prints output in output box
        
    def combineAllChecks(self):
        self.checkRenderStats()
        self.checkAiRenderStats()
        self.checkSubD()
        self.checkDisp()

    def createSet(self):
        getExistingText = self.outWindow.toPlainText()
        setName = self.createSet_lineEdit.text()
        geoOrigSelection = cmds.ls(sl=True)
    
        #### Convert any shape selections for transforms ####
        selectConvert = []
        
        for x in geoOrigSelection:
            print x
            if cmds.nodeType(x)!='transform':
                findTransform = cmds.listRelatives(x, parent=True)[0]
                selectConvert.append(findTransform)
            else:
                selectConvert.append(x)
                
        cmds.select(selectConvert)
                
        if len(selectConvert) > 0:
            if len(setName) > 0:
                if not cmds.objExists(setName):
                    createSet = cmds.sets(name=setName)
                    cmds.select(createSet,r=True,ne=True)
                    self.combineAllChecks()
                else:
                    if len(getExistingText) > 0:
                        print "five"
                        self.outputText = []  
                    self.outputText.append("<font color=yellow>A SET WITH THAT NAME ALREADY EXISTS<font/>")
            else:
                if len(getExistingText) > 0:
                    self.outputText = []  
                self.outputText.append("<font color=yellow>PLEASE NAME THE SET<font/>")
        else:
            if len(getExistingText) > 0:
                self.outputText = []  
            self.outputText.append("<font color=yellow>PLEASE SELECT GEOMETRY FOR THE SET<font/>")
         
        self.getOutputText()
        
        
##################### Edit Existing Sets ######################

    def removeSetMembers(self):
        getSelect = cmds.ls(sl=True)        
        objectSet = []
        geo = []    
        if cmds.objectType(getSelect[-1]) != 'objectSet':
            print 'select the geometry first then the set you want to remove from last'
        else:
            objectSet = getSelect[-1]
            del getSelect[-1]
            geo = getSelect    
            for x in geo:
                #print x
                cmds.sets(x,rm=objectSet)
                    
    def addSetMembers(self):
        getSelect = cmds.ls(sl=True)        
        objectSet = []
        geo = []    
        if cmds.objectType(getSelect[-1]) != 'objectSet':
            print 'select the geometry first then the set you want to add too'
        else:
            objectSet = getSelect[-1]
            del getSelect[-1]
            geo = getSelect    
            for x in geo:
                #print x
                cmds.sets(x,add=objectSet)
               
######################### Row Toggles #########################

    def rStatsToggle(self, event):
        flipRow(self.renderStatsButtonList)

    def aiToggle(self, event):
        flipRow(self.aiStatsButtonList)
        
    def subDToggle(self, event):
        flipRow(self.subDButtonList)
        
    def dispToggle(self, event):
        flipRow(self.dispButtonList)        
       
def flipRow(whichList):
    if whichList[0].isChecked() == False:
        for x in whichList:
            x.setChecked(True)
    else:
        for x in whichList:
            x.setChecked(False)
            
#####################################################################

class LineEdit(QtGui.QLineEdit):
    """Custom QLineEdit."""
    def keyPressEvent(self, event):
        """Override key press event."""
        key = event.key()
        if key == QtCore.Qt.Key_Control or key == QtCore.Qt.Key_Shift:
            pass
        else:
            super(LineEdit, self).keyPressEvent(event)

def launchUI():
    global obPropUtil
    
    # will try and close the ui if it exists
    try: obPropUtil.close()
    except: pass
    
    obPropUtil = ObjectProperty()
    obPropUtil.show()
    obPropUtil.raise_()   
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()
