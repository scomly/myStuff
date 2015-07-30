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
        
        ############ Save Preset ##########################
        
        radioLayout = QtGui.QHBoxLayout()
        layout.addLayout(radioLayout)
        
        spacer = QtGui.QSpacerItem(150,0)
        radioLayout.addSpacerItem(spacer)
        
        radioLabel = QtGui.QLabel("Save Preset")
        radioLayout.addWidget(radioLabel)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        radioLabel.setFont(font)
        radioLabel.setMaximumWidth(100)
              
        radioGroup = QtGui.QButtonGroup()
       
        self.showRadio = QtGui.QRadioButton("Show")
        self.showRadio.setMaximumWidth(50)
        self.showRadio.setMinimumWidth(50)
        self.showRadio.setChecked(True)
        radioGroup.addButton(self.showRadio)
        
        self.seqRadio = QtGui.QRadioButton("Seq")
        self.seqRadio.setMaximumWidth(50)
        self.seqRadio.setMinimumWidth(50)
        radioGroup.addButton(self.seqRadio)
        
        self.shotRadio = QtGui.QRadioButton("Shot")
        self.shotRadio.setMaximumWidth(50)
        self.shotRadio.setMinimumWidth(50)        
        radioGroup.addButton(self.shotRadio)
        
        radioLayout.addWidget(self.showRadio)
        radioLayout.addWidget(self.seqRadio)
        radioLayout.addWidget(self.shotRadio)
        
        spacer2 = QtGui.QSpacerItem(20,0)
        radioLayout.addSpacerItem(spacer2)
        
        saveButton = QtGui.QPushButton("Save")
        saveButton.setMaximumWidth(50)
        radioLayout.addWidget(saveButton)
        saveButton.clicked.connect(self.savePreset)
                
        loadButton = QtGui.QPushButton("Load")
        loadButton.setMaximumWidth(50)
        radioLayout.addWidget(loadButton)
        loadButton.clicked.connect(self.loadPreset)
        
        spacer3 = QtGui.QSpacerItem(125,0)
        radioLayout.addSpacerItem(spacer3)
        
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
        
        self.import_button.clicked.connect(self.importButtonFunction)
                
        ####################### Output Window ####################################################
        
        self.outWindow = QtGui.QTextEdit()
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(250)
        
        ############################################################################################
                
        self.setLayout(layout) # add main layout itself to this dialog
        
    ################### Save/Load Preset Functions ##########################    
        
    def savePreset(self):
        for x,y in self.cbButtonList.iteritems():
            if y.isChecked() == True:
                cbState = True
            else:
                cbState = False
            self.getState[x] = cbState
            
        if self.showRadio.isChecked() == True:
            with open('/Users/scomly/Desktop/yaml/show/test.yml', 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))
        elif self.seqRadio.isChecked() == True:
            with open('/Users/scomly/Desktop/yaml/seq/test.yml', 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))
        elif self.shotRadio.isChecked() == True:
            with open('/Users/scomly/Desktop/yaml/shot/test.yml', 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))
            
    def loadPreset(self):
        if self.showRadio.isChecked() == True:
            infile = open('/Users/scomly/Desktop/yaml/show/test.yml')
        elif self.seqRadio.isChecked() == True:
            infile = open('/Users/scomly/Desktop/yaml/seq/test.yml')
        elif self.shotRadio.isChecked() == True:
            infile = open('/Users/scomly/Desktop/yaml/shot/test.yml')
  
        inSettings = yaml.load(infile)
        infile.close()

        for x in self.cbButtonList:
            if x in inSettings.keys():
                if inSettings[x]:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Checked)' % (x))
                else:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Unchecked)' % (x))
          
    def importButtonFunction(self):
        
        cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
        if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
            cmds.loadPlugin('vrayformaya', qt=True)
            
        output = []
        warningSphere = []
        warningPlate = []
        
        shotCam = 'shotcam1:shot_camera'   
                 
        for x,y in self.cbButtonList.iteritems():
            
            if x == "Red" and y.isChecked() == True:
                CreateRGBLightMaterials('RED',1,0,0)
                output.append("Created Red VRay Light Material")
                
            if x == "Green" and y.isChecked() == True:
                CreateRGBLightMaterials('GREEN',0,1,0)
                output.append("Created Green VRay Light Material")
                              
            if x == "Blue" and y.isChecked() == True:
                CreateRGBLightMaterials('BLUE',0,0,1)
                output.append("Created Blue VRay Light Material")
                
            if x == "White" and y.isChecked() == True:
                CreateRGBLightMaterials('WHITE',1,1,1)
                output.append("Created White VRay Light Material")
                                
            if x == "Black" and y.isChecked() == True:
                CreateRGBLightMaterials('BLACK',0,0,0)
                output.append("Created Black VRay Light Material")
                
            if x == "Shadow" and y.isChecked() == True:
                CreateRenderElements('shadow')
                output.append("Created Matte Shadow Render Element")
                
            if x == "Contact_Shadow" and y.isChecked() == True:
                CreateCatchers('contact_shadow')
                CreateRenderElements('contactShadow')
                output.append("Created Contact Shadow Render Element")
                output.append("Created Conatct Shadow VRay Dirt Texture")
                                
            if x == "Reflection_Occ" and y.isChecked() == True:
                CreateCatchers('reflection')
                CreateRenderElements('refl_occ')
                output.append("Created Reflection Occlusion VRay Dirt Texture")
                output.append("Created Refleection Occlusion Render Element")               
                                                      
            if x == "Fresnel" and y.isChecked() == True:
                CreateRenderElements('fresnel')
                output.append("Created VRay Frensel Utility")
                output.append("Created Fresnel Render Element")
                        
            if x == "Shadow_Catcher" and y.isChecked() == True:
                CreateCatchers('shadow')
                output.append("Created Shadow Catcher Vray Mtl")
                
            if x == "Plate_Projection" and y.isChecked() == True:
                PlateProject()
                output.append("Created Plate Projection Shader")
                if not cmds.objExists(shotCam): 
                   warningPlate.append("Could not link plate projection node to shotcam. Shotcam does not exist.")
          
            if x == "Reflection_Catcher" and y.isChecked() == True:
                CreateCatchers('reflection')
                output.append("Created Reflection Catcher Vray Mtl")
                 
            if x == "Ref_Spheres" and y.isChecked() == True:
                CreateRefSphere()
                output.append("Created Reference Spheres and Color Chart")
                if not cmds.objExists(shotCam): 
                   warningSphere.append("Could not position and constrain to shotcam. Shotcam does not exist.")
        
        conformOutput = '\n'.join(output) ## reformats output list
        conformSphereWarn = '\n'.join(warningSphere) ## reformats output list
        conformPlateWarn = '\n'.join(warningPlate) ## reformats output list
                
        warningSphereOut = "<font color=red>" + conformSphereWarn + "</font>" ## turn that string red
        warningPlateOut = "<font color=red>" + conformPlateWarn + "</font>" ## turn that string red
        
        self.outWindow.setText(conformOutput) ## prints output in output box
        self.outWindow.append(warningSphereOut) ## prints warnings in output box 
        self.outWindow.append(warningPlateOut) ## prints warnings in output box         

    ############# Un/Check All Functions ######################
    
    def checkAllFunction(self): ## Check all Button
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(True)
        
    def checkNoneFunction(self): ## Check None Button
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(False)
                
    ############## Toggle each line Functions ###################################
        
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
