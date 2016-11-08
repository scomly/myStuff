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
        
        framesHorizLayout = QtGui.QHBoxLayout() # layout for frames
        layout.addLayout(framesHorizLayout)
        layout.setAlignment(QtCore.Qt.AlignTop)
        
        ########### Catch All Checkboxes Here ################
        
        self.renderStatsButtonList = []
        self.aiStatsButtonList = []
        self.subDButtonList = []
        self.dispButtonList = []
        
        self.outputText = []

        #################### Render Stats Frame ##############################################
        
        self.rStats_frame = QtGui.QFrame()
        self.rStats_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.rStats_frame)
        
        self.rStats_frame.setLayout(QtGui.QVBoxLayout())
              
        self.rStats_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        self.rStats_frame.setMinimumHeight(200)
                
        self.rStatsframeLabelVarName = QtGui.QLabel('Render Stats')
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
        self.rStats_frame.layout().addWidget(self.rStatsSetButton)
        self.rStatsSetButton.clicked.connect(self.checkRenderStats) ## clicked
              
        #################### Ai Render State Frame ##############################################
        
        self.aiStats_frame = QtGui.QFrame()
        self.aiStats_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.aiStats_frame)
        
        self.aiStats_frame.setLayout(QtGui.QVBoxLayout())
        self.aiStats_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.aiStatsframeLabelVarName = QtGui.QLabel('Ai Render Stats')
        self.aiStats_frame.layout().addWidget(self.aiStatsframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.aiStatsframeLabelVarName.setFont(font)
        self.aiStatsframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.aiStatsframeLabelVarName.mouseReleaseEvent = self.aiToggle

            ##### Checkboxes #####
        
        self.selfShadButton = QtGui.QCheckBox('Self Shadows')
        self.aiStatsButtonList.append(self.selfShadButton)
        self.aiStats_frame.layout().addWidget(self.selfShadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selfShadButton.setFont(font)
        self.selfShadButton.setChecked(True)
        
        self.opaqueButton = QtGui.QCheckBox('Opaque')
        self.aiStatsButtonList.append(self.opaqueButton)
        self.aiStats_frame.layout().addWidget(self.opaqueButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.opaqueButton.setFont(font)
        self.opaqueButton.setChecked(True)
        
        self.visDiffButton = QtGui.QCheckBox('Visible in Diffuse')
        self.aiStatsButtonList.append(self.visDiffButton)
        self.aiStats_frame.layout().addWidget(self.visDiffButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visDiffButton.setFont(font)
        self.visDiffButton.setChecked(True)
        
        self.visGlossButton = QtGui.QCheckBox('Visible in Glossy')
        self.aiStatsButtonList.append(self.visGlossButton)
        self.aiStats_frame.layout().addWidget(self.visGlossButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.visGlossButton.setFont(font)
        self.visGlossButton.setChecked(True)
        
        self.matteButton = QtGui.QCheckBox('Matte')
        self.aiStatsButtonList.append(self.matteButton)
        self.aiStats_frame.layout().addWidget(self.matteButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.matteButton.setFont(font)
        self.matteButton.setChecked(True)
        
        self.traceSetButton = QtGui.QCheckBox('Trace Sets')
        self.aiStatsButtonList.append(self.traceSetButton)
        self.aiStats_frame.layout().addWidget(self.traceSetButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.traceSetButton.setFont(font)
        self.traceSetButton.setChecked(True)
        
        self.spacer2 = QtGui.QSpacerItem(0,18)
        self.aiStats_frame.layout().addSpacerItem(self.spacer2)
        
        self.aiStatsSetButton = QtGui.QPushButton("Add")
        self.aiStats_frame.layout().addWidget(self.aiStatsSetButton)
        self.aiStatsSetButton.clicked.connect(self.checkAiRenderStats) ## clicked

        #################### SubD Frame ##############################################
        
        self.subD_frame = QtGui.QFrame()
        self.subD_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.subD_frame)
        
        self.subD_frame.setLayout(QtGui.QVBoxLayout())
        self.subD_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.subDframeLabelVarName = QtGui.QLabel('SubD')
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
        self.subTypeButton.setChecked(True)
        
        self.subIterButton = QtGui.QCheckBox('Subdiv Iterations')
        self.subDButtonList.append(self.subIterButton)
        self.subD_frame.layout().addWidget(self.subIterButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.subIterButton.setFont(font)
        self.subIterButton.setChecked(True)
        
        self.spacer3 = QtGui.QSpacerItem(0,102)
        self.subD_frame.layout().addSpacerItem(self.spacer3)
        
        self.subDSetButton = QtGui.QPushButton("Add")
        self.subD_frame.layout().addWidget(self.subDSetButton)
        self.subDSetButton.clicked.connect(self.checkSubD) ## clicked
              
        #################### Disp Frame ##############################################
               
        self.disp_frame = QtGui.QFrame()
        self.disp_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        framesHorizLayout.addWidget(self.disp_frame)
        
        self.disp_frame.setLayout(QtGui.QVBoxLayout())
        self.disp_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        
        self.dispframeLabelVarName = QtGui.QLabel('Displace')
        
        self.disp_frame.layout().addWidget(self.dispframeLabelVarName)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.dispframeLabelVarName.setFont(font)
        self.dispframeLabelVarName.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        self.dispframeLabelVarName.mouseReleaseEvent = self.dispToggle

        self.dispHeightButton = QtGui.QCheckBox('Disp Height')
        self.dispButtonList.append(self.dispHeightButton)
        self.disp_frame.layout().addWidget(self.dispHeightButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispHeightButton.setFont(font)
        self.dispHeightButton.setChecked(True)        

        self.dispPadButton = QtGui.QCheckBox('Disp Padding')
        self.dispButtonList.append(self.dispPadButton)
        self.disp_frame.layout().addWidget(self.dispPadButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispPadButton.setFont(font)
        self.dispPadButton.setChecked(True) 

        self.dispZeroButton = QtGui.QCheckBox('Disp Zero Value')
        self.dispButtonList.append(self.dispZeroButton)
        self.disp_frame.layout().addWidget(self.dispZeroButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dispZeroButton.setFont(font)
        self.dispZeroButton.setChecked(True) 

        self.autoBumpButton = QtGui.QCheckBox('Auto Bump')
        self.dispButtonList.append(self.autoBumpButton)
        self.disp_frame.layout().addWidget(self.autoBumpButton)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autoBumpButton.setFont(font)
        self.autoBumpButton.setChecked(True)
                
        self.spacer4 = QtGui.QSpacerItem(0,60)
        self.disp_frame.layout().addSpacerItem(self.spacer4)
        
        self.dispSetButton = QtGui.QPushButton("Add")
        self.disp_frame.layout().addWidget(self.dispSetButton)
        self.dispSetButton.clicked.connect(self.checkDisp) ## clicked

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
        self.createSet_lineEdit = QtGui.QLineEdit()
        self.createSet_lineEdit.setMaximumWidth(200)
        lineEditHorizLayout.addWidget(self.createSet_lineEdit)
        self.createSet_lineEdit.setPlaceholderText("Name the set here")
               
        ########### Create Button ################
        
        createLayout = QtGui.QVBoxLayout() # layout for set creation button
        layout.addLayout(createLayout)
        createLayout.layout().setAlignment(QtCore.Qt.AlignCenter)
        createLayout.layout().setContentsMargins(5,5,5,5) 
        self.createButton = QtGui.QPushButton("Create")
        createLayout.layout().addWidget(self.createButton)
        self.createButton.setMinimumHeight(50)
        self.createButton.setMinimumWidth(400)
        self.createButton.clicked.connect(self.createSet) ## clicked

        ########### Output Window #################
        
        self.outWindow = QtGui.QTextEdit()
        self.outWindow.setReadOnly(True)
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(275)
        
        ################################################################################################        
                
        self.setLayout(layout)
        
################################################################################################
    
  ######### Check if checked ##########################
  
    def checkRenderStats(self):
        getExistingText = self.outWindow.toPlainText()
        if len(getExistingText) > 0:
            self.outputText = []       
        getSelect = cmds.ls(sl=True)[0]
        if cmds.objectType(getSelect, isType='objectSet') == True:
            theSet = getSelect            
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
                    self.outputText.append("<font color=yellow>Casts Shadows Already Exists<font/><br>")
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
                    addMatte = cmds.addAttr(ln='aiMatte',at='bool',dv=1)
                    self.outputText.append('Created aiMatte attribute') 
                else:
                    self.outputText.append("<font color=yellow>Matte Already Exists<font/>")
            if self.traceSetButton.isChecked()==True:
                if cmds.attributeQuery('aiTraceSets',node=theSet,ex=True) == False: 
                    addAiTraceSets = cmds.addAttr(ln='aiTraceSets',at='bool',dv=1)
                    self.outputText.append('Created Trace Sets attribute') 
                else:
                    self.outputText.append("<font color=yellow>Trace Sets Already Exists<font/><br>")
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
                    addBoundsPad = cmds.addAttr(ln='aiDispAutobump',at='bool',dv=1)
                    self.outputText.append('Created Disp Auto Bump attribute')                     
                else:
                    self.outputText.append("<font color=yellow>AutoBump Already Exists<font/>")   
        else:
            self.outputText.append("<font color=yellow>Select a Set to Add Attributes<font/>")
        
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
        geoSelection = cmds.ls(sl=True)
        if cmds.objectType(geoSelection, isType='objectSet') == False:
            if len(geoSelection) > 0:
                if len(setName) > 0:
                    if not cmds.objExists(setName):
                        createSet = cmds.sets(name=setName)
                        cmds.select(createSet,r=True,ne=True)
                        self.combineAllChecks()
                    else:
                        if len(getExistingText) > 0:
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
        else:
            if len(getExistingText) > 0:
                self.outputText = []  
            self.outputText.append("<font color=yellow>YOU HAVE A SET SELECTED. PLEASE SELECT GEOMETRY OR GROUPS.<font/>")
            
        self.getOutputText()
            

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
