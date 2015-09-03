from mVray import vrayFrameBuffers as vfb
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
        
        ########### Checkbox Label List #####################################
                
        self.topList = ["Red", "Green", "Blue", "White", "Black"]
        self.middleTopList = ["Shadow", "Contact_Shadow", "Fresnel", "Reflection_Occ"]
        self.middleBotList = ["Shadow_Catcher", "Plate_Projection", "Reflection_Catcher"]
        self.bottomList = ["Ref_Spheres"]
      
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
        
        ########### Catch All Checkboxes Here ################
        
        self.cbButtonList = {}
        self.getState = {}
        
        ############ Save/Load Preset ##########################
        
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
        saveButton.clicked.connect(self.savePreset) ## clicked
                
        loadButton = QtGui.QPushButton("Load")
        loadButton.setMaximumWidth(50)
        radioLayout.addWidget(loadButton)
        loadButton.clicked.connect(self.loadPreset) ## clicked
        
        spacer3 = QtGui.QSpacerItem(125,0)
        radioLayout.addSpacerItem(spacer3)
        
        #################### Top Frame ##############################################
        
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
        
        ####################### Middle Top Frame #################################
        
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
            
        ##########################  Middle Bottom Frame ##########################################
        
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
        
        ############################ Bottom Frame ##########################################
        
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
        self.checkAll_button.clicked.connect(self.checkAllFunction) ## clicked
        
        self.checkNone_button = QtGui.QPushButton("Check None")
        allCheckLayout.layout().addWidget(self.checkNone_button)
        self.checkNone_button.clicked.connect(self.checkNoneFunction) ## clicked
        
        ####################### Import button #####################################################
        
        self.import_button = QtGui.QPushButton("Import")
        layout.addWidget(self.import_button)
        self.import_button.setMinimumHeight(50)        
        self.import_button.clicked.connect(self.importButtonFunction) ## clicked
                
        ####################### Output Window ####################################################
        
        self.outWindow = QtGui.QTextEdit()
        self.outWindow.setReadOnly(True)
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(275)
        
        ############################################################################################
                
        self.setLayout(layout) # add main layout itself to this dialog
    
    #########################################################################
    ################### Functions ###########################################
    #########################################################################    
        
    ################### Save/Load Preset Functions ##########################    
    ################### Change yaml file path here ##########################
        
    def savePreset(self): ## Save Button Function
        getShowInfo()
        
        for x,y in self.cbButtonList.iteritems():
            if y.isChecked() == True:
                cbState = True
            else:
                cbState = False
            self.getState[x] = cbState
            
        if self.showRadio.isChecked() == True:           
            if not os.path.exists(getShowInfo.jobPath):
                os.makedirs(getShowInformation.jobPath)           
            with open('%s/utilToolbox.yml' % getShowInfo.jobPath, 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))                
            showConfig = "<font color=yellow>Saved SHOW preset.</font>"
            self.outWindow.setText(showConfig)
            
        elif self.seqRadio.isChecked() == True:           
            if not os.path.exists(getShowInfo.seqPath):
                os.makedirs(getShowInfo.seqPath)                
            with open('%s/utilToolbox.yml' % getShowInfo.seqPath, 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))                
            seqConfig = "<font color=yellow>Saved SEQ preset.</font>"
            self.outWindow.setText(seqConfig)
                
        elif self.shotRadio.isChecked() == True:            
            if not os.path.exists(getShowInfo.shotPath):
                os.makedirs(getShowInfo.shotPath)                 
            with open('%s/utilToolbox.yml' % getShowInfo.shotPath, 'w') as outfile:
                outfile.write(yaml.dump(self.getState, default_flow_style=False))                
            shotConfig = "<font color=yellow>Saved SHOT preset.</font>"
            self.outWindow.setText(shotConfig)                      
        
    def loadPreset(self): ## Load Button Function
    
        getShowInfo()
    
        try:
            if self.showRadio.isChecked() == True:
                infile = open('%s/utilToolbox.yml' % getShowInfo.jobPath)
                showConfig = "<font color=yellow>Loaded SHOW preset.</font>"
                self.outWindow.setText(showConfig)         
            elif self.seqRadio.isChecked() == True:
                infile = open('%s/utilToolbox.yml' % getShowInfo.seqPath)
                seqConfig = "<font color=yellow>Loaded SEQ preset.</font>"
                self.outWindow.setText(seqConfig)   
            elif self.shotRadio.isChecked() == True:
                infile = open('%s/utilToolbox.yml' % getShowInfo.shotPath)
                shotConfig = "<font color=yellow>Loaded SHOT preset.</font>"
                self.outWindow.setText(shotConfig)   
        except:
            noConfig = "<font color=red>NO CONFIG FILE EXISTS</font>"
            self.outWindow.setText(noConfig)
  
        inSettings = yaml.load(infile)
        infile.close()

        for x in self.cbButtonList:
            if x in inSettings.keys():
                if inSettings[x]:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Checked)' % (x))
                else:
                    exec('self.%s.buttonVarName.setCheckState(QtCore.Qt.Unchecked)' % (x))
          
    def importButtonFunction(self): ## Import Button Function
    
        #### sets to default layer and enables Vray is not already enabled#######
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
                   warningPlate.append("Could not link plate projection node to shotcam. Shotcam does not exist. Import the shotcam and run the tool again with this selection to fix the camera attachments.")
          
            if x == "Reflection_Catcher" and y.isChecked() == True:
                CreateCatchers('reflection')
                output.append("Created Reflection Catcher Vray Mtl")
                 
            if x == "Ref_Spheres" and y.isChecked() == True:
                CreateRefSphere()
                output.append("Created Reference Spheres and Color Chart")
                if not cmds.objExists(shotCam): 
                   warningSphere.append("Could not position and constrain ref spheres shotcam. Shotcam does not exist. Import the shotcam and run the tool again with this selection to fix the camera attachments.")
                   
        ############# Output Statements #################################           
        
        conformOutput = '\n'.join(output) ## reformats output list
        conformSphereWarn = '\n'.join(warningSphere) ## reformats output list
        conformPlateWarn = '\n'.join(warningPlate) ## reformats output list
                
        warningSphereOut = "<font color=red>" + conformSphereWarn + "</font>" ## turn that string red
        warningPlateOut = "<font color=red>" + conformPlateWarn + "</font>" ## turn that string red
        
        self.outWindow.setText(conformOutput) ## prints output in output box
        self.outWindow.append(warningSphereOut) ## prints warnings in output box 
        self.outWindow.append(warningPlateOut) ## prints warnings in output box        
        
    ############# Un/Check All Functions ######################
    
    def checkAllFunction(self): ## Check All Button Function
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(True)
        
    def checkNoneFunction(self): ## Check None Button Function
        for x,y in self.cbButtonList.iteritems():
            y.setChecked(False)
            

                
################ Toggle each line Functions ###################################
        
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
            
############ Get Show/Seq/Shot ###################################################        

def getShowInfo():

    tackOn = '/TECH/config'
    tackOnJob = '/TECH/lib/maya/config'
    
    getShowInfo.shotPath = os.environ.get('M_SHOT_PATH') + tackOn
    getShowInfo.seqPath = os.environ.get('M_SEQUENCE_PATH') + tackOn

    getShowInfo.jobPath = os.environ.get('M_JOB_PATH') + tackOnJob 
    

        
################## Create Checkbox Class ########################################
                     
class UtilCreateCheckBox(object):
    def __init__(self, buttonVarName, buttonLabelName, frame):
        
        self.buttonVarName = QtGui.QCheckBox(buttonLabelName)
        frame.layout().addWidget(self.buttonVarName)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonVarName.setFont(font)
        self.buttonVarName.setChecked(True)

################# Create Frames Class ###########################################
        
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
        


########################################################################
############################### BACK END ###############################
########################################################################

class CreateRGBLightMaterials(object):        
    def __init__(self, shaderName, R, G, B):
        
        self.shaderName = shaderName
        self.R = R
        self.G = G
        self.B = B
        
        if not cmds.objExists(shaderName):
            mtlName = cmds.shadingNode('VRayLightMtl', asShader=True, name=shaderName)
            cmds.setAttr('%s.color' % (mtlName), R,G,B, type='double3')
            cmds.setAttr('%s.emitOnBackSide' % (mtlName), 1)
        else:
            mtlName = cmds.ls(shaderName)[0]

## example creation ##    
## createRedShader = CreateRGBLightMaterials('RED',1,0,0)

class CreateCatchers(object):    
    def __init__(self, type):
        self.type = type
        ## type meaning 'shadow' or 'reflection' catcher
        
        if type.lower() == 'shadow':
            if not cmds.objExists('SHADOW_CATCHER'):
                shdCatcher = cmds.shadingNode('VRayMtl', asShader=True, name='SHADOW_CATCHER')
                cmds.setAttr('%s.reflectionColorAmount' % (shdCatcher), 0)
                cmds.setAttr('%s.diffuseColorAmount' % (shdCatcher), 1)
                cmds.setAttr('%s.brdfType' % (shdCatcher), 0)
                cmds.setAttr('%s.useFresnel' % (shdCatcher), 0)
            ## creates shadow catching VRayMtl
            
        if type.lower() == 'contact_shadow':           
            if not cmds.objExists('CONTACT_SHADOW_CATCHER'):
                contactShadCatcher = cmds.shadingNode('VRayDirt', asTexture=True, name='CONTACT_SHADOW_CATCHER')
                cmds.setAttr('%s.blackColor' % (contactShadCatcher), 1,1,1, type='double3')
                cmds.setAttr('%s.whiteColor' % (contactShadCatcher), 0,0,0, type='double3')
                cmds.setAttr('%s.radius' % (contactShadCatcher), 10)
                cmds.setAttr('%s.ignoreSelfOcclusion' % (contactShadCatcher), 1)
                cmds.setAttr('%s.resultAffectInclusive' % (contactShadCatcher), 0)
             ## creates VrayDirt used for ambient occlusion
        
        elif type.lower() == 'reflection':
                if not cmds.objExists('REFL_CATCHER'):
                    mirrorMtl = cmds.shadingNode('VRayMtl', asShader=True, name='REFL_CATCHER')
                    cmds.setAttr('%s.color' % (mirrorMtl), 0,0,0, type='double3')
                    cmds.setAttr('%s.reflectionColor' % (mirrorMtl), 1,1,1, type='double3')
                    cmds.setAttr('%s.reflectionColorAmount' % (mirrorMtl), 1)
                    cmds.setAttr('%s.diffuseColorAmount' % (mirrorMtl), 0)
                    cmds.setAttr('%s.useFresnel' % (mirrorMtl), 0)
                    mirrorOccl = cmds.shadingNode('VRayDirt', asTexture=True, name='MIRROR_REFLOCC')
                    cmds.setAttr('%s.blackColor' % (mirrorOccl), 1,1,1, type='double3')
                    cmds.setAttr('%s.whiteColor' % (mirrorOccl), 0,0,0, type='double3')
                    cmds.setAttr('%s.radius' % (mirrorOccl), 1000)
                    cmds.setAttr('%s.occlusionMode' % (mirrorOccl), 2)
                    cmds.connectAttr('%s.outColor' % (mirrorOccl), '%s.reflectionColor' % (mirrorMtl))
                    cmds.connectAttr('%s.reflectionGlossiness' % (mirrorMtl), '%s.glossiness' % (mirrorOccl))          
                    mkbrdfTypeOffset = cmds.shadingNode('plusMinusAverage', asUtility=True, name='brdfOffset')
                    cmds.connectAttr('%s.brdfType' % (mirrorMtl), '%s.input1D[0]' % (mkbrdfTypeOffset))
                    cmds.setAttr('%s.input1D[1]' % (mkbrdfTypeOffset), 1)
                    cmds.connectAttr('%s.output1D' % (mkbrdfTypeOffset), '%s.occlusionMode' % (mirrorOccl))
                    cmds.connectAttr('%s.reflectionSubdivs' % (mirrorMtl), '%s.subdivs' % (mirrorOccl))
                ## creates relfection catching VrayMtl and VRay dirt for an RO

## example creation ##    
## createReflectionCatcher = CreateCatchers('reflection') 

class CreateRenderElements(object):
    def __init__(self,type):
        
        self.type = type
        
        if type.lower() == 'shadow':
            if not cmds.objExists('vrayRE_MatteShadow'):
                vfb.matteShadow('vrayRE_MatteShadow', enabled=False)
            ## creates cast shadow render element
            
        if type.lower() == 'contactshadow':
            if not cmds.objExists('vrayRE_ContactShadow'):
                if cmds.objExists('CONTACT_SHADOW_CATCHER'):
                    vfb.extraTex('vrayRE_ContactShadow', 'CONTACT_SHADOW_CATCHER', explicit_channel='contactShadow', enabled=False)
            ## creates contact shadow render element
            
        if type.lower() == 'fresnel':       
            if not cmds.objExists('vrayRE_Fresnel'):
                createFresnel = cmds.shadingNode('VRayFresnel', asTexture=True, name='VrayFresnel')
                createFresnelTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dFresnel')
                cmds.connectAttr('%s.outUV' % (createFresnelTwoD), '%s.uvCoord' % (createFresnel))
                cmds.connectAttr('%s.outUvFilterSize' % (createFresnelTwoD), '%s.uvFilterSize' % (createFresnel))
                vfb.extraTex('vrayRE_Fresnel', 'VrayFresnel', explicit_channel='fresnel', enabled=False)
            ## creates fresnel render element
            
        if type.lower() == 'refl_occ':
            if not cmds.objExists('vrayRE_reflectionOcclusion'):
                if cmds.objExists('MIRROR_REFLOCC'):
                    vfb.extraTex('vrayRE_reflectionOcclusion', 'MIRROR_REFLOCC', explicit_channel='reflectionOcclusion', enabled=False)
            ## creates contact shadow render element
                
## example creation ##   
## createShadowRE = CreateRenderElements('contactShadow')
   
class PlateProject(object):    
    def __init__(self):
    
        projectCam = 'shotcam1:shot_camera'
        if not cmds.objExists('plateProject'):
            projShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='plateProject')
            cmds.setAttr('%s.emitOnBackSide' % (projShader), 1)
            ## creates shader
            
            plateTexture = cmds.shadingNode('file', asTexture=True, name='plateTexture')
            cmds.setAttr('%s.defaultColor' % (plateTexture), 0,0,0, type='double3')
            cmds.setAttr('%s.useFrameExtension' % (plateTexture), 1)
            ## creates texture node
            
            fileProject = cmds.shadingNode('projection', asTexture=True, name='projectNodePlate') 
            cmds.setAttr('%s.projType' % (fileProject), 8)
            cmds.setAttr('%s.fitType' % (fileProject), 0)
            cmds.setAttr('%s.fitFill' % (fileProject), 1)
            cmds.setAttr('%s.defaultColor' % (fileProject), 0,0,0, type='double3')
            ## creates projection node
            
            twoD = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2d')
            cmds.setAttr('%s.wrapU' % (twoD), 0)
            cmds.setAttr('%s.wrapV' % (twoD), 0)
            ## creates place2D for plate texture
            
            threeD = cmds.shadingNode('place3dTexture', asUtility=True, name='PlatePlace3d')
            ## creates place3D for camera
            
            cmds.connectAttr('%s.outColor' % (fileProject), '%s.color' % (projShader))
            cmds.connectAttr('%s.outColor' % (plateTexture), '%s.image' % (fileProject))
            cmds.connectAttr('%s.worldInverseMatrix' % (threeD), '%s.placementMatrix' % (fileProject))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityR' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityG' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityB' % (projShader))
            ## connects texture, alpha, shader, projection, and 3D placement
                
            place2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in place2DConnections:
                cmds.connectAttr('%s.%s' % (twoD, x), '%s.%s' % (plateTexture, x))               
            cmds.connectAttr('%s.outUV' % (twoD), '%s.uv' % (plateTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (twoD), '%s.uvFilterSize' % (plateTexture))
            ## connects place2D for plate texture

        if cmds.objExists(projectCam):
            fileProject = cmds.ls('projectNodePlate')[0]
            getIfConnect = cmds.listConnections('%s.linkedCamera' % (fileProject), d=False, s=True)
            if getIfConnect == None:
                cmds.connectAttr('%s' % (projectCam) + 'Shape.message', '%s.linkedCamera' % (fileProject), f=True)
            ## connects shotcam to the proj cam if it exists

## example creation ##   
## createPlateProject = PlateProject()  
  
class CreateRefSphere(object):    
    def __init__(self):
               
        if not cmds.objExists('greyBallShader'):
            diffShader = cmds.shadingNode('VRayMtl', asShader=True, name='greyBallShader')
            diffShaderSG = cmds.sets(name = 'greyBallSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (diffShader) ,'%s.surfaceShader' % (diffShaderSG))
            cmds.setAttr('%s.useFresnel' % (diffShader), 0)
            cmds.setAttr('%s.color' % (diffShader),  0.18,0.18,0.18, type='double3')
            ## creates and assigns grey ball shader    
        
        if not cmds.objExists('greyBall'):
            diffBall = cmds.polySphere(name='greyBall', r=2.5)
            cmds.setAttr('%s.translateY' % (diffBall[0]), 6)
            cmds.delete(diffBall, ch=True)
            ## creates grey ball geo
        
            cmds.sets(diffBall[0], e=True, forceElement='greyBallSG')
            ## assigns  grey ball shader to geo
        
        if not cmds.objExists('chromeBallShader'):
            refShader = cmds.shadingNode('VRayMtl', asShader=True, name='chromeBallShader')
            refShaderSG = cmds.sets(name = 'chromeBallSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (refShader) ,'%s.surfaceShader' % (refShaderSG))
            cmds.setAttr('%s.useFresnel' % (refShader), 0)
            cmds.setAttr('%s.color' % (refShader),  0, 0, 0, type='double3')
            cmds.setAttr('%s.reflectionColor' % (refShader),  1, 1, 1, type='double3')
            cmds.setAttr('%s.diffuseColorAmount' % (refShader),  0)
            cmds.setAttr('%s.reflectionsMaxDepth' % (refShader),  2)
            ## creates chrome ball shader
                
        if not cmds.objExists('chromeBall'):    
            refBall = cmds.polySphere(name='chromeBall', r=2.5)
            cmds.delete(refBall, ch=True)  
            ## creates chrome ball geo
            
            cmds.sets(refBall[0], e=True, forceElement='chromeBallSG')
            ## assigns chrome ball shader to geo        
    
        colorChartTexturePath = '/jobs/asset_library/sequences/assets/common/pub/hdr_library/ColorChecker_linear_from_Avg_16bit.exr'
        ## color chart texture path
               
        if not cmds.objExists('colorChartShader'):
            chartShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='colorChartShader')
            chartShaderSG = cmds.sets(name = 'chartShaderSG', renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (chartShader) ,'%s.surfaceShader' % (chartShaderSG))
            cmds.setAttr('%s.emitOnBackSide' % (chartShader), 1)

            ## creates color chart VrayLightMtl
        
        if not cmds.objExists('colorChart'):    
            colorChart =  cmds.polyPlane(name='colorChart', h=5,w=5,sx=1,sy=1)
            cmds.setAttr('%s.translate' % (colorChart[0]), 7,3,0)
            cmds.setAttr('%s.rotateX' % (colorChart[0]), 90)
            ## creates color chart geo
            
            cmds.sets(colorChart[0], e=True, forceElement='chartShaderSG')
            ## assigns shader
                
        if not cmds.objExists('chartTexture'):
            chartTexture = cmds.shadingNode('file', asTexture=True, name='chartTexture')
            chartTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='chartPlace2d')    
            chart2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in chart2DConnections:
                cmds.connectAttr('%s.%s' % (chartTwoD, x), '%s.%s' % (chartTexture, x))               
            cmds.connectAttr('%s.outUV' % (chartTwoD), '%s.uv' % (chartTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (chartTwoD), '%s.uvFilterSize' % (chartTexture))
            cmds.connectAttr('%s.outColor' % (chartTexture), '%s.color' % (chartShader))
            ## creates and connects file texture node
            
            cmds.setAttr('%s.fileTextureName' % (chartTexture), colorChartTexturePath, type='string')
            ############ So dumb but I can't get the file tetxture path to fully eval without selecting the file node ###################
            cmds.select(chartTexture, r=True)
            ## feeds in colro chart texture path
        
        if not cmds.objExists('RefSphere_GRP'):
            refSetupGroupName = 'RefSphere_GRP'
            refSetupTransGroup = 'TranslateThis'
            refSetupGroupMembers = (colorChart[0], refBall[0], diffBall[0])
            translateGroup = cmds.group(refSetupGroupMembers, name=refSetupTransGroup)
            refSetupGroup = cmds.group(translateGroup, name=refSetupGroupName)

        shotCam = 'shotcam1:shot_camera'
                
        if cmds.objExists(shotCam):
            refSetupGroup = cmds.ls('RefSphere_GRP')[0]
            translateGroup = cmds.ls('TranslateThis')[0]  
            getIfConnect = cmds.listConnections('%s.tx' % (refSetupGroup), d=False, s=True)
            if getIfConnect == None:
                cmds.parentConstraint(shotCam, refSetupGroup, mo=False)
                cmds.setAttr('%s.translate' % (translateGroup), -50, -25, -150)
            ## creates groups and constrains to camera

## example creation ##   
## createRefSpheres = CreateRefSphere()   

def launchUI():
    global vrayToolBoxUtil
    
    # will try and close the ui if it exists
    try: vrayToolBoxUtil.close()
    except: pass
    
    vrayToolBoxUtil = UtilityToolBoxUI()
    vrayToolBoxUtil.show()    
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()


    
    
