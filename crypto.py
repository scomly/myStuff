from PySide import QtGui
from PySide import QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken
import mtoa.aovs as aovs
import itertools

########################################################################
############################### GUI ####################################
########################################################################

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    
class cryptoSetup(QtGui.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(cryptoSetup, self).__init__(parent)
                
        self.setWindowTitle("Cryptomatte Utility Pass Setup")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed    
      
        #############################################################################

        self.createLayout() # runs function below
                
    ################################################################################    
    ##################### Layout Creation ##########################################    
    ################################################################################
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        #self.setMinimumHeight(650)
        #self.setMinimumWidth(750)
        #layout.setSpacing(0)
        
        self.renderGlobalsButton = QtGui.QPushButton("Optimize Render Globals Settings")
        self.renderGlobalsButton.setToolTip("cuts bounces and samples,sets precison,kills sample clamp,kills")
        layout.addWidget(self.renderGlobalsButton)
        self.renderGlobalsButton.clicked.connect(self.setupLayerForCyprto) ## clicked
        
        self.matteShaderButton = QtGui.QPushButton("Matte Shader Geo Override")
        self.matteShaderButton.setToolTip("Override surface Shader with black flat aiUtility shader")
        layout.addWidget(self.matteShaderButton)
        self.matteShaderButton.clicked.connect(self.matteShader) ## clicked
        
        self.cryptoMaterialButton = QtGui.QPushButton("Cypto Material AOV setup")
        self.cryptoMaterialButton.setToolTip("Material based ID setup")
        layout.addWidget(self.cryptoMaterialButton)
        self.cryptoMaterialButton.clicked.connect(self.cryptoMaterial) ## clicked
        
        self.cryptoObjectButton = QtGui.QPushButton("Cypto Object AOV setup")
        self.cryptoObjectButton.setToolTip("Material based ID setup")
        layout.addWidget(self.cryptoObjectButton)
        self.cryptoObjectButton.clicked.connect(self.cryptoObject) ## clicked

        self.cryptoAssetButton = QtGui.QPushButton("Cypto Asset AOV setup")
        self.cryptoAssetButton.setToolTip("Asset based ID setup")
        layout.addWidget(self.cryptoAssetButton)
        self.cryptoAssetButton.clicked.connect(self.cryptoAsset) ## clicked
        
        self.runAllButton = QtGui.QPushButton()
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.runAllButton.setFont(font)
        self.runAllButton.setText('RUN ALL')
        self.runAllButton.setToolTip("Run All")
        self.runAllButton.setMinimumHeight(50)
        layout.addWidget(self.runAllButton)
        self.runAllButton.clicked.connect(self.runAllCrypto) ## clicked

        
        ########### Output Window #################
        
        self.outWindow = QtGui.QTextEdit()
        self.outWindow.setReadOnly(True)
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(50)
        self.outWindow.setText("Docs -- http://redmine.mill.co.uk/projects/millla/wiki/Cryptomatte_Render_Layer_Setup")
        
        #######################################################################################        
                
        self.setLayout(layout)

    def getLayerMembers(self):
        ######## Get Layer Members ###############    
        getCurrentRenderLayer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        getAssets = cmds.editRenderLayerMembers(getCurrentRenderLayer,query=True)
        self.geoSelections = cmds.ls(getAssets, dag=True, o=True, s=True)  
         
    def setupLayerForCyprto(self):        
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:                    
                ##### Hide Lights #####
            getGlobalLights = []
            
            getMayaLights = cmds.ls(lights=True)
            for x in getMayaLights:
                if len(getMayaLights) > 0:
                    getGlobalLights.append(x)    
            
            arnoldLightTypes = ("aiLightPortal","aiSkyDomeLight","aiAreaLight","aiMeshLight")
            for aiLight in arnoldLightTypes:
                getAiLights = cmds.ls(type=aiLight)
                if len(getAiLights) > 0:
                    for y in getAiLights:
                        getGlobalLights.append(y)
                 
            getLightTransforms = cmds.listRelatives(getGlobalLights,parent=True,fullPath=True)        
            
            for light in getLightTransforms:
                cmds.setAttr('%s.visibility' % light, 0)
                
            ##### Hide AOVs #####    
            aovList = ['*aiAOV_*']
            getAOVs = cmds.ls(aovList)
            cryptoAOVList = ['aiAOV_crypto*']
            getCryptoAOVs = cmds.ls(cryptoAOVList)
            
            for aov in getAOVs:
                if aov not in getCryptoAOVs:
                    cmds.editRenderLayerAdjustment("%s.enabled" % aov)
                    cmds.setAttr("%s.enabled" % aov, 0)
            
            ##### Set Render Globals #####
            cmds.editRenderLayerAdjustment("defaultArnoldDriver.halfPrecision")
            cmds.setAttr("defaultArnoldDriver.halfPrecision", 0)
            
            renderLayerAttributeOverrides = ("use_sample_clamp","GIDiffuseDepth","GIReflectionDepth","GIRefractionDepth","GIGlossyDepth","GIVolumeDepth","GIDiffuseSamples","GIGlossySamples","GIRefractionSamples","GISssSamples","GISingleScatterSamples","GISingleScatterSamples","GIVolumeSamples")
            
            for attribute in renderLayerAttributeOverrides:
                cmds.editRenderLayerAdjustment("defaultArnoldRenderOptions.%s" % attribute)
                if attribute == 'GISingleScatterSamples':
                    cmds.setAttr("defaultArnoldRenderOptions.%s" % attribute, 1)
                else:
                    cmds.setAttr("defaultArnoldRenderOptions.%s" % attribute, 0)
                        
            cmds.warning("Optimized Render Globals for Crypto")

###########

    def cryptoPlaceholder(self):        
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:   
            getCryptoPlaceholder = cmds.ls('aiAOV_crypto_placeholder')
            if len(getCryptoPlaceholder) == 0:
                createCustomAOV = aovs.AOVInterface().addAOV('crypto_placeholder')
                cmds.setAttr("aiAOV_crypto_placeholder.enabled", 0)
            cmds.editRenderLayerAdjustment("aiAOV_crypto_placeholder.enabled")
            cmds.setAttr("aiAOV_crypto_placeholder.enabled", 1)
            
            getCryptoAOVShader = cmds.ls('cryptomatteAOV')
            if len(getCryptoAOVShader) == 0:
                cryptoMatteAOVShader = cmds.shadingNode('cryptomatteAOV', asShader=True, name='cryptomatteAOV')        
                cmds.connectAttr('cryptomatteAOV.outColor','aiAOV_crypto_placeholder.defaultValue', force=True)

###########

    def cryptoMaterial(self):
        self.cryptoPlaceholder()
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:              
            getCryptoMaterial = cmds.ls('aiAOV_crypto_material')
            if len(getCryptoMaterial) == 0:       
                createCyptoMaterial = aovs.AOVInterface().addAOV('crypto_material')
                cmds.setAttr("aiAOV_crypto_material.enabled", 0)
            cmds.editRenderLayerAdjustment("aiAOV_crypto_material.enabled")
            cmds.setAttr("aiAOV_crypto_material.enabled", 1)
            cmds.warning("Setup Crypto Material AOV")

##########

    def cryptoObject(self):
        self.cryptoPlaceholder()
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:     
            getCryptoObject = cmds.ls('aiAOV_crypto_object')
            if len(getCryptoObject) == 0:
                createCyptoObject = aovs.AOVInterface().addAOV('crypto_object')        
                cmds.setAttr("aiAOV_crypto_object.enabled", 0)
            cmds.editRenderLayerAdjustment("aiAOV_crypto_object.enabled")
            cmds.setAttr("aiAOV_crypto_object.enabled", 1)
            cmds.warning("Setup Crypto Object AOV")

###########

    def cryptoAsset(self):
        self.cryptoPlaceholder()
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:              
            getCryptoAsset = cmds.ls('aiAOV_crypto_asset')
            if len(getCryptoAsset) == 0:       
                createCyptoAsset = aovs.AOVInterface().addAOV('crypto_asset')
                cmds.setAttr("aiAOV_crypto_asset.enabled", 0)
            cmds.editRenderLayerAdjustment("aiAOV_crypto_asset.enabled")
            cmds.setAttr("aiAOV_crypto_asset.enabled", 1)
            
            #### Gets layer members ####
            self.getLayerMembers()
            
            #### Adds mtoa string attribute to shapes #######
            for x in self.geoSelections:   
                if cmds.attributeQuery('mtoa_constant_crypto_asset', node=x, exists=True) != True:
                    getObjectType = cmds.objectType(x)            
                    if getObjectType == 'nurbsSurface' or getObjectType == 'mesh':
                        getNameSpace = x.split(':')[0]
                        if len(getNameSpace) > 0:
                            cmds.addAttr(x, longName='mtoa_constant_crypto_asset', dataType='string')
                            cmds.setAttr('%s.mtoa_constant_crypto_asset' % x, getNameSpace, type='string')
            cmds.warning("Setup Crypto Asset AOV")
 
############# 
                    
    def matteShader(self):                   
        getMatteShader = cmds.ls('matteShader')
        
        if len(getMatteShader) == 0:
            surfaceShader = cmds.shadingNode('aiUtility', asShader=True, name='matteShader')
            cmds.setAttr('%s.shadeMode' % surfaceShader, 2)        
            cmds.setAttr('%s.color' % surfaceShader, 0,0,0, type='double3')
        else:
            surfaceShader = getMatteShader[0]
        ##### Check if in default render layer #####
        if cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True ) == "defaultRenderLayer":
            print "Tool can't be run in the Default Layer"
        else:
            
            #### Gets layer members ####
            self.getLayerMembers()
            
            #### Overrides Shader ####  
            for y in self.geoSelections:
                connect = cmds.listConnections(y,type='shadingEngine')
                if connect != None:
                    connect = connect[0]
                    getOverride = cmds.editRenderLayerAdjustment(query=True)
                    getShaderAssignmentOverride = (connect + '.surfaceShader')
                    if getOverride != None:
                        if getShaderAssignmentOverride not in getOverride:    
                            createOverride = cmds.editRenderLayerAdjustment('%s.surfaceShader' % connect)
                    if getOverride == None:
                        createOverride = cmds.editRenderLayerAdjustment('%s.surfaceShader' % connect)              
                    getSurfaceShader = cmds.listConnections('%s.surfaceShader' % connect, type='aiUtility')
                    if getSurfaceShader == None:
                        cmds.connectAttr('%s.outColor' % surfaceShader, '%s.surfaceShader' % (connect), force=True)
                    getSurfaceShader = cmds.listConnections('%s.surfaceShader' % connect, type='aiUtility')    
                    if getSurfaceShader[0] != 'matteShader':
                        cmds.connectAttr('%s.outColor' % surfaceShader, '%s.surfaceShader' % (connect), force=True)
            cmds.warning("Assigned Matte Shader as a layer override")
                        
    def runAllCrypto(self):
        self.setupLayerForCyprto()
        self.cryptoMaterial()
        self.cryptoObject()
        self.cryptoAsset()
        self.matteShader()
        cmds.warning("Your CryptoMattes are ready!")        

########################################################################################

def launchUI():
    global cryptoSet
    
    # will try and close the ui if it exists
    try: cryptoSet.close()
    except: pass
    
    cryptoSet = cryptoSetup()
    cryptoSet.show()
    cryptoSet.raise_()
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()
