import maya.cmds as cmds
import os
import glob
import re

######Calls########
#### makeGUI() ####
###################

######### Sets default render layer as active later ###############

cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )

def camPlateProject(getStateB1, getStateB2, getText):
    
    ################### Finds Plate ###########################################
    
    shotPath = os.environ['SHOT_PATH_']
    platePath = shotPath + '/images/plates'
    getPath = os.listdir(platePath)
    os.chdir(platePath)
    getMP = glob.glob('*mp*')
    
    findLOQ = glob.glob('*loq*')

    if len(findLOQ) >0:
        getMP.remove(findLOQ[0])
    
    getPlateVer = getMP[-1]
    listPlates = os.listdir('%s/%s/' % (platePath,getPlateVer))
    

    
    os.chdir('%s/%s/' % (platePath,getPlateVer))
    
    if len(glob.glob('*cgbg*')) > 0:
        plateType = glob.glob('*cgbg*')[0]
    else:
        plateType = glob.glob('2k*_lnf_exr')[0]
        
    os.chdir(('%s/%s/%s/' % (platePath,getPlateVer,plateType)))
    
    findFirst = glob.glob('*exr')[0]
    
    if not cmds.objExists('ProjectionNodes'):
        cmds.group(em=True, name='ProjectionNodes')
 
    ######### Finds and Connects HDRs #################################################################
    
    if not cmds.objExists('setProject'):
        setProjectMtl = cmds.shadingNode('VRayBlendMtl', asShader=True, name='setProject')
    else:
        setProjectMtl = cmds.ls('setProject')[0]
    
    if not cmds.objExists('hdrProject'):
        hdrLightMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='hdrProject')
        cmds.setAttr('%s.emitOnBackSide' % (hdrLightMtl), 1)
    else:
        hdrLightMtl = cmds.ls('hdrProject')[0] 
    
    getHDRDome = cmds.ls(type='VRayLightDomeShape')[0]
    
    getHDRTexture = cmds.listConnections('%s.domeTex' % (getHDRDome))[0]
    
    if not cmds.objExists('projectNodeHDR'):
        hdrProject = cmds.shadingNode('projection', asTexture=True, name='projectNodeHDR')
        cmds.setAttr('%s.projType' % (hdrProject), 2)
    else:
        hdrProject = cmds.ls('projectNodeHDR')[0]
    
    if not cmds.objExists('hdrMult'):
        hdrMult = cmds.shadingNode('multiplyDivide', au=True, name='hdrMult')
    else:
        hdrMult = cmds.ls('hdrMult')[0]
            
    if cmds.isConnected('%s.outColor' % (hdrLightMtl), '%s.base_material' % (setProjectMtl)) == 0:
        cmds.connectAttr('%s.outColor' % (hdrLightMtl), '%s.base_material' % (setProjectMtl))
            
    if cmds.isConnected('%s.outColor' % (hdrProject), '%s.input1' % (hdrMult)) == 0:
        cmds.connectAttr('%s.outColor' % (hdrProject), '%s.input1' % (hdrMult))
        
    if cmds.isConnected('%s.intensityMult' % (getHDRDome), '%s.input2.input2X' % (hdrMult)) == 0:
        cmds.connectAttr('%s.intensityMult' % (getHDRDome), '%s.input2.input2X' % (hdrMult))
        
    if cmds.isConnected('%s.intensityMult' % (getHDRDome), '%s.input2.input2Y' % (hdrMult)) == 0:
        cmds.connectAttr('%s.intensityMult' % (getHDRDome), '%s.input2.input2Y' % (hdrMult))    
        
    if cmds.isConnected('%s.intensityMult' % (getHDRDome), '%s.input2.input2Z' % (hdrMult)) == 0:
        cmds.connectAttr('%s.intensityMult' % (getHDRDome), '%s.input2.input2Z' % (hdrMult))        
    
    if cmds.isConnected('%s.outColor' % (getHDRTexture), '%s.image' % (hdrProject)) == 0:
        cmds.connectAttr('%s.outColor' % (getHDRTexture), '%s.image' % (hdrProject))
        
    if cmds.isConnected('%s.output' % (hdrMult), '%s.color' % (hdrLightMtl)) == 0:
        cmds.connectAttr('%s.output' % (hdrMult), '%s.color' % (hdrLightMtl))  
    
    
    ####################### Frame Loop Creates Frame Shaders and Textures #######################################################
    coats = range(0,9)
    
    if getStateB1 == 1:
        getText = [findFirst.split('.')[1]]
    else:
        getText = getText.split(',')
       
    print getText

    for frames in getText:
    
        getExr = glob.glob('*.%s.exr' % (frames))
        
        if len(getExr) > 0:    
            projectPath = ('%s/%s/%s/%s' % (platePath,getPlateVer,plateType,getExr[0]))
            
        if not cmds.objExists('plateProject%s' % frames):
            if getStateB2 == 1:
                lightMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='plateProject%s' % frames)
                cmds.setAttr('%s.emitOnBackSide' % (lightMtl), 1)
            else:
                lightMtl = cmds.shadingNode('VRayMtl', asShader=True, name='plateProject%s' % frames)
        else:
            lightMtl = cmds.ls('plateProject%s' % frames)[0]
            
        if not cmds.objExists('plateTexture%s' % frames):
            fileTexture = cmds.shadingNode('file', asTexture=True, name='plateTexture%s' % frames)
            cmds.setAttr('%s.defaultColor' % (fileTexture), 0,0,0, type='double3')
        else:
            fileTexture = cmds.ls('plateTexture%s' % frames)[0]
            
        if not cmds.objExists('projectNodePlate%s' % frames):
            fileProject = cmds.shadingNode('projection', asTexture=True, name='projectNodePlate%s' % frames) 
            if getStateB1 == 1:         
                cmds.setAttr('%s.useFrameExtension' % (fileTexture), 1)
            cmds.setAttr('%s.fileTextureName' % (fileTexture), projectPath, type='string')
	    cmds.setAttr('%s.filterType' %  (fileTexture), 1)
            cmds.setAttr('%s.projType' % (fileProject), 8)
            cmds.setAttr('%s.fitType' % (fileProject), 2)
            cmds.setAttr('%s.defaultColor' % (fileProject), 0,0,0, type='double3')        
        else:
            fileProject = cmds.ls('projectNodePlate%s' % frames)[0]
            
        if not cmds.objExists('PlatePlace3d%s' % frames):
            threeD = cmds.shadingNode('place3dTexture', asUtility=True, name='PlatePlace3d%s' % frames)
        else:
            threeD = cmds.ls('PlatePlace3d%s' % frames)[0]
            
        if not cmds.objExists('PlatePlace2d%s' % frames):
            twoD = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2d%s' % frames)
            cmds.setAttr('%s.wrapU' % (twoD), 0)
            cmds.setAttr('%s.wrapV' % (twoD), 0)
        else:
            twoD = cmds.ls('PlatePlace2d%s' % frames)[0]  
        
        if not cmds.objExists('plateMult%s' % frames):
            plateMult = cmds.shadingNode('multiplyDivide', au=True, name='plateMult%s' % frames)
            cmds.setAttr('%s.input2X' % (plateMult), 1000)
            cmds.setAttr('%s.input2Y' % (plateMult), 1000)
            cmds.setAttr('%s.input2Z' % (plateMult), 1000)
        else:
            plateMult = cmds.ls('plateMult%s' % frames)[0]
        
        if cmds.isConnected('%s.outColor' % (fileProject), '%s.input1' % (plateMult)) == 0:
            cmds.connectAttr('%s.outColor' % (fileProject), '%s.input1' % (plateMult))
        
        if not cmds.objExists('plateClamp%s' % frames):
            plateClamp = cmds.shadingNode('clamp', au=True, name='plateClamp%s' % frames)
            cmds.setAttr('%s.maxR' % (plateClamp), 1)
            cmds.setAttr('%s.maxG' % (plateClamp), 1)
            cmds.setAttr('%s.maxB' % (plateClamp), 1)
        else:
            plateClamp = cmds.ls('plateClamp%s' % frames)[0]
            
        if cmds.isConnected('%s.output' % (plateMult), '%s.input' % (plateClamp)) == 0:
            cmds.connectAttr('%s.output' % (plateMult), '%s.input' % (plateClamp))
            
        existConnectCoat = cmds.listConnections(lightMtl)
        existConnectBlend = cmds.listConnections(plateClamp)
    
        if not 'setProject' in existConnectCoat:
            for coat in coats:
                getConnectionsCoat = cmds.listConnections('%s.coat_material_%s' % (setProjectMtl, coat))
                if getConnectionsCoat == None:
                    cmds.connectAttr('%s.outColor' % (lightMtl), '%s.coat_material_%s' % (setProjectMtl, coat))
                    break
        if not 'setProject' in existConnectBlend:                
            for coat in coats:
                getConnectionsBlend = cmds.listConnections('%s.blend_amount_%s' % (setProjectMtl, coat))
                if getConnectionsBlend == None:
                    cmds.connectAttr('%s.output' % (plateClamp), '%s.blend_amount_%s' % (setProjectMtl, coat))
                    break
                    
                    
         ################## Checks Place2D Connection ##########################           
                    
        if cmds.isConnected('%s.outColor' % (fileProject), '%s.color' % (lightMtl)) == 0:    
            cmds.connectAttr('%s.outColor' % (fileProject), '%s.color' % (lightMtl))
        if cmds.isConnected('%s.outColor' % (fileTexture), '%s.image' % (fileProject)) == 0:
            cmds.connectAttr('%s.outColor' % (fileTexture), '%s.image' % (fileProject))
        if cmds.isConnected('%s.worldInverseMatrix' % (threeD), '%s.placementMatrix' % (fileProject)) == 0:
            cmds.connectAttr('%s.worldInverseMatrix' % (threeD), '%s.placementMatrix' % (fileProject))
        if cmds.isConnected('%s.coverage' % (twoD), '%s.coverage' % (fileTexture)) == 0:
            cmds.connectAttr('%s.coverage' % (twoD), '%s.coverage' % (fileTexture))
        if cmds.isConnected('%s.translateFrame' % (twoD), '%s.translateFrame' % (fileTexture)) == 0:
            cmds.connectAttr('%s.translateFrame' % (twoD), '%s.translateFrame' % (fileTexture))
        if cmds.isConnected('%s.rotateFrame' % (twoD), '%s.rotateFrame' % (fileTexture)) == 0:
            cmds.connectAttr('%s.rotateFrame' % (twoD), '%s.rotateFrame' % (fileTexture))
        if cmds.isConnected('%s.mirrorU' % (twoD), '%s.mirrorU' % (fileTexture)) == 0:
            cmds.connectAttr('%s.mirrorU' % (twoD), '%s.mirrorU' % (fileTexture))
        if cmds.isConnected('%s.mirrorV' % (twoD), '%s.mirrorV' % (fileTexture)) == 0:
            cmds.connectAttr('%s.mirrorV' % (twoD), '%s.mirrorV' % (fileTexture))
        if cmds.isConnected('%s.stagger' % (twoD), '%s.stagger' % (fileTexture)) == 0:
            cmds.connectAttr('%s.stagger' % (twoD), '%s.stagger' % (fileTexture))
        if cmds.isConnected('%s.wrapU' % (twoD), '%s.wrapU' % (fileTexture)) == 0:
            cmds.connectAttr('%s.wrapU' % (twoD), '%s.wrapU' % (fileTexture))
        if cmds.isConnected('%s.wrapV' % (twoD), '%s.wrapV' % (fileTexture)) == 0:
            cmds.connectAttr('%s.wrapV' % (twoD), '%s.wrapV' % (fileTexture))
        if cmds.isConnected('%s.repeatUV' % (twoD), '%s.repeatUV' % (fileTexture)) == 0:
            cmds.connectAttr('%s.repeatUV' % (twoD), '%s.repeatUV' % (fileTexture))
        if cmds.isConnected('%s.offset' % (twoD), '%s.offset' % (fileTexture)) == 0:
            cmds.connectAttr('%s.offset' % (twoD), '%s.offset' % (fileTexture))
        if cmds.isConnected('%s.rotateUV' % (twoD), '%s.rotateUV' % (fileTexture)) == 0:
            cmds.connectAttr('%s.rotateUV' % (twoD), '%s.rotateUV' % (fileTexture))
        if cmds.isConnected('%s.noiseUV' % (twoD), '%s.noiseUV' % (fileTexture)) == 0:
            cmds.connectAttr('%s.noiseUV' % (twoD), '%s.noiseUV' % (fileTexture))
        if cmds.isConnected('%s.vertexUvOne' % (twoD), '%s.vertexUvOne' % (fileTexture)) == 0:
            cmds.connectAttr('%s.vertexUvOne' % (twoD), '%s.vertexUvOne' % (fileTexture))
        if cmds.isConnected('%s.vertexUvTwo' % (twoD), '%s.vertexUvTwo' % (fileTexture)) == 0:
            cmds.connectAttr('%s.vertexUvTwo' % (twoD), '%s.vertexUvTwo' % (fileTexture))
        if cmds.isConnected('%s.vertexUvThree' % (twoD), '%s.vertexUvThree' % (fileTexture)) == 0:
            cmds.connectAttr('%s.vertexUvThree' % (twoD), '%s.vertexUvThree' % (fileTexture))
        if cmds.isConnected('%s.vertexCameraOne' % (twoD), '%s.vertexCameraOne' % (fileTexture)) == 0:
            cmds.connectAttr('%s.vertexCameraOne' % (twoD), '%s.vertexCameraOne' % (fileTexture))
        if cmds.isConnected('%s.outUV' % (twoD), '%s.uv' % (fileTexture)) == 0:
            cmds.connectAttr('%s.outUV' % (twoD), '%s.uv' % (fileTexture))
        if cmds.isConnected('%s.outUvFilterSize' % (twoD), '%s.uvFilterSize' % (fileTexture)) == 0:
            cmds.connectAttr('%s.outUvFilterSize' % (twoD), '%s.uvFilterSize' % (fileTexture))

        ############ Duplicate Shotcam at Frame #######################################   
        
        if getStateB1 == 2:      
            if not cmds.objExists('ProjCamFrame%s' % frames):   
                getPanel = cmds.getPanel(typ='modelPanel')
                for panel in getPanel:
                    cmds.modelEditor(modelPanel=panel , alo=False)
            
                cmds.currentTime(frames, update=True)
        
                framesShotCam = cmds.duplicate('shotcam1:shot_camera', n='ProjCamFrame%s' % frames)
            
                cmds.parent(framesShotCam, threeD, 'ProjectionNodes')
        
                letterbox_mask = ['*letterBox*']
                findBox = cmds.ls(letterbox_mask)
                if len(findBox) > 0:
                    cmds.delete(findBox)
               
                getPanel = cmds.getPanel(typ='modelPanel')
                for panel in getPanel:
                    cmds.modelEditor(modelPanel=panel , alo=True)
                
                cmds.connectAttr('%sShape.message' % (framesShotCam[0]), '%s.linkedCamera' % (fileProject), f=True)
        else:
            if cmds.objExists('shotcam1:shot_camera'):
                if cmds.isConnected ('shotcam1:shot_cameraShape.message', '%s.linkedCamera' % (fileProject)) == 0:
                    cmds.connectAttr('shotcam1:shot_cameraShape.message', '%s.linkedCamera' % (fileProject), f=True)
                    
            cmds.parent(threeD, 'ProjectionNodes')

        ############ So dumb but I can't get the frame expression to eval without selecting the node ###################
        if getStateB1 == 1:         
            cmds.select(fileTexture, r=True)
 
############## GO Button Action Command #####################################    

def actOnPress():
    getStateB1 = cmds.radioButtonGrp('ButtonOne', q=True, sl=True)
    getStateB2 = cmds.radioButtonGrp('ButtonTwo', q=True, sl=True)
    getText = cmds.textField('textField', tx=True, q=True)
    camPlateProject(getStateB1,getStateB2,getText)
    
############## Creates GUI ########################################################

def makeGUI():

    if cmds.window('CameraProject', ex=1, q=1): 
        cmds.deleteUI('CameraProject')
    camProjWindow = cmds.window('CameraProject')
    form = cmds.formLayout(numberOfDivisions=125)
    b1 = cmds.radioButtonGrp('ButtonOne', label='Frame Type', labelArray2=['Animated', 'Specific Frame(s)'], numberOfRadioButtons=2)
    b2 = cmds.radioButtonGrp('ButtonTwo', label='Material Type', labelArray2=['VRayLight', 'VRayMtl'], numberOfRadioButtons=2)
    tf3 = cmds.textField('textField', width=200)
    sepText = cmds.text(label = 'Separate frames by comma (limit 9)')
    b3 = cmds.button(label='GO', width=100, command='cameraProject.actOnPress()')
    
    ########## Checks for ShotCam #############
    
    if not cmds.objExists('*shotcam*'):
        shotcamWarn = cmds.text(label = 'Could not find shotcam. Please import and re-run tool.', bgc = [1,0,0])
    else:
        shotcamWarn = cmds.text(label = 'Found shotcam', bgc = [0,1,0])
        
    ######## Checks for HDR #################
        
    hdrExists = cmds.ls(type='VRayLightDomeShape')
    if len(hdrExists) == 0:
        hdrWarn = cmds.text(label = 'Could not find HDR. Please import and re-run tool', bgc = [1,0,0])
    else:
        hdrWarn = cmds.text('Found HDR', bgc = [0,1,0])
        
    ####### Loads VRay ##########################
    
    if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
        cmds.loadPlugin('vrayformaya', qt=True)
    
    cmds.formLayout(form, edit=True, attachControl=[(b1, 'bottom', 5, b2), (tf3, 'left', 25, b1), (b2, 'bottom', 25, b3), (tf3, 'bottom', 5, sepText), (b3, 'bottom', 50, shotcamWarn), (shotcamWarn, 'bottom', 75, hdrWarn)], attachForm = [(b3, 'left', 500), (sepText, 'left', 410), (shotcamWarn, 'left', 25), (hdrWarn, 'left', 25)])
    cmds.showWindow(camProjWindow)
