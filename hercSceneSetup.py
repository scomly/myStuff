import maya.cmds as cmds
import os
import re
import vrayObjectProperties as vop
import vrayFrameBuffers as vfb
import maya.mel as mel

######## Calls ############
###### hercSetup() ########
###########################

def hercSetup():
    organizeScene()
    createCatcherShader()
    createRGBShaders()
    createRenderElements()
    createSpearExtraTex()
    createArrowExtraTex()
    createMassiveMattes()
    createHeraGrad()
    createFxHeraExtraTex()
    createFxStatueExtraTex()
    createFxCariDudesExtraTex()
    createCanyonTex()

######### Sets default render layer as active later ###############

cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

####### Loads VRay if not loaded ##########################

if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
    cmds.loadPlugin('vrayformaya', qt=True)

######### Organzhize Outliner and Create Object Properties ########
def organizeScene():
    
    ############ Arrows Stuff ######################
    
    arrow_mask_list = ["*:*arrow*"]
    getArrow = cmds.ls(arrow_mask_list, assemblies=True)
    if len(getArrow) > 0:
        if cmds.objExists('ARROWS_GRP'):
            arrowGroup = cmds.ls('ARROWS_GRP')
            cmds.parent(getArrow, arrowGroup)
        else:
            arrowGroup = cmds.group(getArrow, name='ARROWS_GRP')
    if not cmds.objExists('ARROWS_VOP'):
        if cmds.objExists('ARROWS_GRP'):
            arrowGroup = cmds.ls('ARROWS_GRP')
            arrowProp = vop.createObjectProperties(arrowGroup, 'ARROWS_VOP')
    else:
        arrowProp = cmds.ls('ARROWS_VOP')
        
   ############ Spears Stuff ######################

    spears_mask_list = ["*:*spear*"]
    getSpears = cmds.ls(spears_mask_list, assemblies=True)
    if len(getSpears) > 0:
        if cmds.objExists('SPEARS_GRP'):
            bowGroup = cmds.ls('SPEARS_GRP')
            cmds.parent(getSpears, spearsGroup)
        else:
            spearsGroup = cmds.group(getSpears, name='SPEARS_GRP')
    if not cmds.objExists('SPEARS_VOP'):
        if cmds.objExists('SPEARS_GRP'):
            spearsGroup = cmds.ls('SPEARS_GRP')
            spearsProp = vop.createObjectProperties(spearsGroup, 'SPEARS_VOP')
    else:
        spearsProp = cmds.ls('SPEARS_VOP')
	
    ############ Shields Stuff ######################

    shield_mask_list = ["*:*shield*"]
    getShield = cmds.ls(shield_mask_list, assemblies=True)
    if len(getShield) > 0:
        if cmds.objExists('SHIELDS_GRP'):
            shieldGroup = cmds.ls('SHIELDS_GRP')
            cmds.parent(getShield, shieldGroup)
        else:
            shieldGroup = cmds.group(getShield, name='SHIELDS_GRP')
    if not cmds.objExists('SHIELDS_VOP'):
        if cmds.objExists('SHIELDS_GRP'):
            shieldGroup = cmds.ls('SHIELDS_GRP')
            shieldProp = vop.createObjectProperties(shieldGroup, 'SHIELDS_VOP')
    else:
        shieldProp = cmds.ls('SHIELDS_VOP')

    ############ Bows Stuff ######################

    bow_mask_list = ["*:*bow*"]
    getBow = cmds.ls(bow_mask_list, assemblies=True)
    if len(getBow) > 0:
        if cmds.objExists('BOWS_GRP'):
            bowGroup = cmds.ls('BOWS_GRP')
            cmds.parent(getBow, bowGroup)
        else:
            bowGroup = cmds.group(getBow, name='BOWS_GRP')
    if not cmds.objExists('BOWS_VOP'):
        if cmds.objExists('BOWS_GRP'):
            bowGroup = cmds.ls('BOWS_GRP')
            bowProp = vop.createObjectProperties(bowGroup, 'BOWS_VOP')
    else:
        bowProp = cmds.ls('BOWS_VOP')

    ############ Throwing Knives Stuff ######################

    throwingKnife_mask_list = ["*:*throwingKnife*"]
    getThrowingKnife = cmds.ls(throwingKnife_mask_list, assemblies=True)
    if len(getBow) > 0:
        if cmds.objExists('THROWINGKNIFE_GRP'):
            throwingKnifeGroup = cmds.ls('THROWINGKNIFE_GRP')
            cmds.parent(getThrowingKnife, throwingKnifeGroup)
        else:
            throwingKnifeGroup = cmds.group(getThrowingKnife, name='THROWINGKNIFE_GRP')
    if not cmds.objExists('THROWINGKNIFE_VOP'):
        if cmds.objExists('THROWINGKNIFE_GRP'):
            throwingKnifeGroup = cmds.ls('THROWINGKNIFE_GRP')
            throwingKnifeProp = vop.createObjectProperties(throwingKnifeGroup, 'THROWINGKNIFE_VOP')
    else:
        throwingKnifeProp = cmds.ls('THROWINGKNIFE_VOP')

    ############ TrackMan Stuff ######################

    trackMan_mask_list = ["*:*trackMan*", "*:*char_tydeus*", "*:*char_rhesus*", "*:*char_atalanta*", "*:*archer*"]
    getTrackMan = cmds.ls(trackMan_mask_list, assemblies=True)
    if len(getTrackMan) > 0:
        if cmds.objExists('TRACKMAN_GRP'):
            trackManGroup = cmds.ls('TRACKMAN_GRP')
            cmds.parent(getTrackMan, trackManGroup)
        else:
            trackManGroup = cmds.group(getTrackMan, name='TRACKMAN_GRP')
    if not cmds.objExists('TRACKMAN_VOP'):
        if cmds.objExists('TRACKMAN_GRP'):
            trackManGroup = cmds.ls('TRACKMAN_GRP')
            trackManProp = vop.createObjectProperties(trackManGroup, 'TRACKMAN_VOP')
    else:
        trackManProp = cmds.ls('TRACKMAN_VOP')

    ############ Citadel Stuff ################################       

    Citadel_mask_list = ["*:*courtyard*", "*:*hera*", "*:*mainGate*", "*:*mainTemple*", "*:*refugee*", "*:*palace*", "*:*amphi*", "*:*stables*", "*:*braziers*"]
    getCitadel = cmds.ls(Citadel_mask_list, assemblies=True)
    if len(getCitadel) > 0:
        if cmds.objExists('CITADEL_GRP'):
            citadelGroup = cmds.ls('CITADEL_GRP')
            cmds.parent(getCitadel, citadelGroup)
        else:
            citadelGroup = cmds.group(getCitadel, name='CITADEL_GRP')
    if not cmds.objExists('CITADEL_VOP'):
        if cmds.objExists('CITADEL_GRP'):
            citadelGroup = cmds.ls('CITADEL_GRP')   
            citadelProp = vop.createObjectProperties(citadelGroup, 'CITADEL_VOP')
    else:
        citadelProp = cmds.ls('CITADEL_VOP')
        
   ############ Posts Stuff ################################       

    Post_mask_list = ["*:*setDressing_bull*", "*:*setDressing_rams*"]
    getPost = cmds.ls(Post_mask_list, assemblies=True)
    if len(getPost) > 0:
        if cmds.objExists('POST_GRP'):
            postGroup = cmds.ls('POST_GRP')
            cmds.parent(getPost, postGroup)
        else:
            postGroup = cmds.group(getPost, name='POST_GRP')
    if not cmds.objExists('POST_VOP'):
        if cmds.objExists('POST_GRP'):
            postGroup = cmds.ls('POST_GRP')   
            postProp = vop.createObjectProperties(postGroup, 'POST_VOP')
    else:
        postProp = cmds.ls('POST_VOP')
        
  ############ Citadel Canyon Stuff ################################       
  

    CitadelCanyon_mask_list = ["*:*city*", "*:*aqua*", "*:*walls*", "*:*canyon*", "*:*shrine*", "*INSTANCER*", "*:*village*", "*:*dungeon*"]
    getCitadelCanyon = cmds.ls(CitadelCanyon_mask_list, assemblies=True)
    if len(getCitadelCanyon) > 0:
        if cmds.objExists('CITADELCANYON_GRP'):
            citadelCanyonGroup = cmds.ls('CITADELCANYON_GRP')
            cmds.parent(getCitadelCanyon, citadelCanyonGroup)
        else:
            citadelCanyonGroup = cmds.group(getCitadelCanyon, name='CITADELCANYON_GRP')
    if not cmds.objExists('CITADELCANYON_VOP'):
        if cmds.objExists('CITADELCANYON_GRP'):
            citadelCanyonGroup = cmds.ls('CITADELCANYON_GRP')   
            citadelCanyonProp = vop.createObjectProperties(citadelCanyonGroup, 'CITADELCANYON_VOP')
    else:
        citadelCanyonProp = cmds.ls('CITADELCANYON_VOP')
        
        
############ Massive Stuff ################################       

    Massive_mask_list = ["*crowd*"]
    getMassive = cmds.ls(Massive_mask_list, assemblies=True)
    if len(getMassive) > 0:
        if cmds.objExists('MASSIVE_GRP'):
            massiveGroup = cmds.ls('MASSIVE_GRP')
            cmds.parent(getMassive, massiveGroup)
        else:
            massiveGroup = cmds.group(getMassive, name='MASSIVE_GRP')
        
	
########## Shadow Cacther Shader Creation ################################
def createCatcherShader():
    if not cmds.objExists('Shad_Refl_Catcher'):
        mkCatcher = cmds.shadingNode('VRayMtl', asShader=True, name='Shad_Refl_Catcher')
    else:
        mkCatcher = cmds.ls('Shad_Refl_Catcher')[0]
    cmds.setAttr('%s.reflectionColorAmount' % (mkCatcher), 0)
    cmds.setAttr('%s.diffuseColorAmount' % (mkCatcher), 1)
    cmds.setAttr('%s.brdfType' % (mkCatcher), 0)


############# RGB Shaders Creation ###########################################
def createRGBShaders():
    if not cmds.objExists('RED'):
        redMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='RED')
    else:
        redMtl = cmds.ls('RED')[0]
    cmds.setAttr('%s.color' % (redMtl), 1,0,0, type='double3')
    cmds.setAttr('%s.emitOnBackSide' % (redMtl), 1)

    if not cmds.objExists('GREEN'):
        greenMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='GREEN')
    else:
        greenMtl = cmds.ls('GREEN')[0]
    cmds.setAttr('%s.color' % (greenMtl), 0,1,0, type='double3')
    cmds.setAttr('%s.emitOnBackSide' % (greenMtl), 1)

    if not cmds.objExists('BLUE'):
        blueMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='BLUE')
    else:
        blueMtl = cmds.ls('BLUE')[0]
    cmds.setAttr('%s.color' % (blueMtl), 0,0,1, type='double3')
    cmds.setAttr('%s.emitOnBackSide' % (blueMtl), 1) 

################ Render Elements Creation ##############################################

def createRenderElements():
    if not cmds.objExists('vrayRE_MatteShadow'):
        vfb.matteShadow('vrayRE_MatteShadow', enabled=False)
        
        
################ Spears Extra Tex ###################################################
def createSpearExtraTex():
    spearMask = '/jobs/vfx_herc/sequences/assets/prop.arrow/pub/assets/PUBLISHED/prop/spear/new/texture/mid/v004/tex/spear_mask.<UDIM>.tex'
    findSpear = cmds.ls('*:*prop_spear_new*')

    if len(findSpear) > 0:
        if not cmds.objExists('spearGradMask'):
            fileTextureSpearMask = cmds.shadingNode('file', asTexture=True, name='spearGradMask')
            cmds.setAttr('%s.fileTextureName' % (fileTextureSpearMask), spearMask, type='string')
            twoDSP = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2dSP')
            cmds.setAttr('%s.wrapU' % (twoDSP), 0)
            cmds.setAttr('%s.wrapV' % (twoDSP), 0)
            if cmds.isConnected('%s.outUV' % (twoDSP), '%s.uv' % (fileTextureSpearMask)) == 0:
                cmds.connectAttr('%s.outUV' % (twoDSP), '%s.uv' % (fileTextureSpearMask))
            if cmds.isConnected('%s.outUvFilterSize' % (twoDSP), '%s.uvFilterSize' % (fileTextureSpearMask)) == 0:
                cmds.connectAttr('%s.outUvFilterSize' % (twoDSP), '%s.uvFilterSize' % (fileTextureSpearMask))
            if not cmds.objExists('SpearMask'):
                spearExtra = vfb.extraTex('SpearMask', fileTextureSpearMask, explicit_channel="Spear_GradMask", consider_aa=1, enabled=False)       
    else:
        fileTextureSpearMask = cmds.ls('spearGradMask')

##################### Arrow Extra Tex Setup ########################################################################        

def createArrowExtraTex():
    arrowMask = '/jobs/vfx_herc/sequences/assets/prop.arrow/pub/assets/PUBLISHED/prop/arrow/<type>/texture/mid/<ver>/tex/arrow_mask.<UDIM>.tex'

    findArrowAny = cmds.ls('*:*prop_arrow*')
    findArrowAtalanta = cmds.ls('*:*prop_arrow_atalanta*')
    findArrowVarA = cmds.ls('*:*prop_arrow_varA*')
    findArrowVarB = cmds.ls('*:*prop_arrow_varB*')
    findArrowVarC = cmds.ls('*:*prop_arrow_varC*')
    findArrowVarD = cmds.ls('*:*prop_arrow_varD*')
    findArrowVarE = cmds.ls('*:*prop_arrow_varE*')

    if len(findArrowAny) > 0:
        if not cmds.objExists('ArrowMMTypeOne'):
            ArrowMMTypeOne = vfb.multiMatte('ArrowTypeOne', 'ArrowTypeOne', enabled=False)
            cmds.setAttr('ArrowTypeOne.vray_redid_multimatte', 1)
            cmds.setAttr('ArrowTypeOne.vray_greenid_multimatte', 2)
            cmds.setAttr('ArrowTypeOne.vray_blueid_multimatte', 3)
    
    if len(findArrowAny) > 0:        
        if not cmds.objExists('ArrowMMTypeTwo'):
            ArrowMMTypeOne = vfb.multiMatte('ArrowTypeTwo', 'ArrowTypeTwo', enabled=False)
            cmds.setAttr('ArrowTypeTwo.vray_redid_multimatte', 4)
            cmds.setAttr('ArrowTypeTwo.vray_greenid_multimatte', 5)
            cmds.setAttr('ArrowTypeTwo.vray_blueid_multimatte', 6)       
    
    for nodes in findArrowAtalanta:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 1)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=atalanta;ver=v007', type='string') 
         
    for nodes in findArrowVarA:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 2)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=varA;ver=v002', type='string') 
            
    for nodes in findArrowVarB:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 3)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=varB;ver=v002', type='string')
                
    for nodes in findArrowVarC:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 4)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=varC;ver=v002', type='string')    
              
    for nodes in findArrowVarD:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 5)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=varD;ver=v002', type='string')
         
    for nodes in findArrowVarE:
        getID = cmds.attributeQuery('vrayObjectID', node=nodes, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=nodes, ex=True)
        if getID == False:
            addObjectID = cmds.addAttr(nodes, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (nodes), 6)
        if getUserAttr == False:
            addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (nodes), 'type=varE;ver=v003', type='string')
                
    if len(findArrowAny) > 0:
        if not cmds.objExists('arrowAllGradMask'):    
            fileTextureArrowMask = cmds.shadingNode('file', asTexture=True, name='arrowGradMask')
            cmds.setAttr('%s.fileTextureName' % (fileTextureArrowMask), arrowMask, type='string')
            twoDAR = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2dArrow')
            cmds.setAttr('%s.wrapU' % (twoDAR), 0)
            cmds.setAttr('%s.wrapV' % (twoDAR), 0)
            if cmds.isConnected('%s.outUV' % (twoDAR), '%s.uv' % (fileTextureArrowMask)) == 0:
                cmds.connectAttr('%s.outUV' % (twoDAR), '%s.uv' % (fileTextureArrowMask))
            if cmds.isConnected('%s.outUvFilterSize' % (twoDAR), '%s.uvFilterSize' % (fileTextureArrowMask)) == 0:
                cmds.connectAttr('%s.outUvFilterSize' % (twoDAR), '%s.uvFilterSize' % (fileTextureArrowMask))
            if not cmds.objExists('ArrowMask'):
                ArrowExtra = vfb.extraTex('Arrow_GradMask', fileTextureArrowMask, explicit_channel="Arrow_GradMask", consider_aa=1, enabled=False)       
    else:
        fileTextureArrowMask = cmds.ls('arrowGradMask')     

        
####################### Massive Multimattes ####################################################

def createMassiveMattes():
    findMassive = cmds.ls('*crowd*')

    if len(findMassive) > 0:
        if not cmds.objExists('Soldier_multimatte_one'):
            soldierMatteOne = vfb.multiMatte('Soldier_multimatte_one', 'Soldier_multimatte_one', material_ids=1, enabled=False)
            cmds.setAttr('Soldier_multimatte_one.vray_redid_multimatte', 5101)
            cmds.setAttr('Soldier_multimatte_one.vray_greenid_multimatte', 5102)
            cmds.setAttr('Soldier_multimatte_one.vray_blueid_multimatte', 5103)
            
        if not cmds.objExists('Soldier_multimatte_two'):
            soldierMatteTwo = vfb.multiMatte('Soldier_multimatte_two', 'Soldier_multimatte_two', material_ids=1, enabled=False)
            cmds.setAttr('Soldier_multimatte_two.vray_redid_multimatte', 5104)
            cmds.setAttr('Soldier_multimatte_two.vray_greenid_multimatte', 5105)
            
        if not cmds.objExists('Shield_type_matte'):
            shieldMatte = vfb.multiMatte('Shield_type_matte', 'Shield_type_matte', material_ids=1, enabled=False)
            cmds.setAttr('Shield_type_matte.vray_redid_multimatte', 5201)
            cmds.setAttr('Shield_type_matte.vray_greenid_multimatte', 5202)
            cmds.setAttr('Shield_type_matte.vray_blueid_multimatte', 5203)
            
        if not cmds.objExists('Spear_multimatte'):
            spearMatte = vfb.multiMatte('Spear_multimatte', 'Spear_multimatte', material_ids=1, enabled=False)
            cmds.setAttr('Spear_multimatte.vray_redid_multimatte', 5211)
            
        if not cmds.objExists('Sword_type_matte'):
            swordMatte = vfb.multiMatte('Sword_type_matte', 'Sword_type_matte', material_ids=1, enabled=False)
            cmds.setAttr('Sword_type_matte.vray_redid_multimatte', 5221)
            cmds.setAttr('Sword_type_matte.vray_greenid_multimatte', 5222)
            cmds.setAttr('Sword_type_matte.vray_blueid_multimatte', 5223)
            
        mel.eval('source dloVRayRenderElemTools')
        mel.eval('dloImportAllPublishedRenderElemCB "/jobs/vfx_herc/sequences/assets/char.soldier/lib/maya/presets/renderElem/" 0 0')
	
	
################# Hera Temple Grad Mask ##################################################################

def createHeraGrad():
    findHera = cmds.ls('*:*hera*')

    if len(findHera) > 0:    
        mel.eval('source dloVRayRenderElemTools')
        mel.eval('dloImportAllPublishedRenderElemCB "/jobs/vfx_herc/sequences/th/th000/lib/maya/presets/renderElem/" 0 0')
        mel.eval('dloImportAllPublishedRenderElemCB "/jobs/vfx_herc/sequences/assets/env.heraTemple/lib/maya/presets/renderElem/" 0 0')
        mel.eval('dloImportAllPublishedRenderElemCB "/jobs/vfx_herc/sequences/assets/env.heraStatue/lib/maya/presets/renderElem/" 0 0')



############### Creates Extra Tex MultiMatte for fx Hera Temple #####################################################

def createFxHeraExtraTex():
    findHeraTemple = cmds.ls('*:*heraTemple*')
    
    if len(findHeraTemple) > 0:      
        ############ Creates Solid Colors #####################################
        if not cmds.objExists('fxHeraBlack'): 
            blackRamp = cmds.shadingNode('ramp', asTexture=True, name='fxHeraBlack')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blackRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blackRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blackRamp), 0,0,0, type='double3')
        else:
            blackRamp = cmds.ls('fxHeraBlack')[0]
        
        if not cmds.objExists('fxHeraRed'):
            redRamp = cmds.shadingNode('ramp', asTexture=True, name='fxHeraRed')
            cmds.setAttr('%s.defaultColor' % (redRamp), 0,0,0, type='double3') 
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (redRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (redRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (redRamp), 1,0,0, type='double3') 
            redTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_red')
            cmds.setAttr('%s.wrapU' % (redTwoD), 0)
            cmds.setAttr('%s.wrapV' % (redTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (redTwoD), 1)
            cmds.setAttr('%s.translateFrameV' % (redTwoD), 0)
            if cmds.isConnected('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp), f=True)
        else:
            redRamp = cmds.ls('fxHeraRed')[0]
        
        if not cmds.objExists('fxHeraGreen'):
            greenRamp = cmds.shadingNode('ramp', asTexture=True, name='fxHeraGreen')
            cmds.setAttr('%s.defaultColor' % (greenRamp), 0,0,0, type='double3') 
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (greenRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (greenRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (greenRamp), 0,1,0, type='double3') 
            greenTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_green')
            cmds.setAttr('%s.wrapU' % (greenTwoD), 0)
            cmds.setAttr('%s.wrapV' % (greenTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (greenTwoD), 2)
            cmds.setAttr('%s.translateFrameV' % (greenTwoD), 1)
            if cmds.isConnected('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp), f=True)
        else:
            greenRamp = cmds.ls('fxHeraGreen')[0]
        
        if not cmds.objExists('fxHeraBlueOne'):
            blueOneRamp = cmds.shadingNode('ramp', asTexture=True, name='fxHeraBlueOne')
            cmds.setAttr('%s.defaultColor' % (blueOneRamp), 0,0,0, type='double3') 
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blueOneRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blueOneRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blueOneRamp), 0,0,1, type='double3') 
            blueOneTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_blueOne')
            cmds.setAttr('%s.wrapU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.wrapV' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (blueOneTwoD), 2)
            if cmds.isConnected('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp), f=True)
        else:
            blueOneRamp = cmds.ls('fxHeraBlueOne')[0]
                    
        if not cmds.objExists('fxHeraBlueTwo'):
            blueTwoRamp = cmds.shadingNode('ramp', asTexture=True, name='fxHeraBlueTwo')
            cmds.setAttr('%s.defaultColor' % (blueTwoRamp), 0,0,0, type='double3') 
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blueTwoRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blueTwoRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blueTwoRamp), 0,0,1, type='double3') 
            blueTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_blueTwo')
            cmds.setAttr('%s.wrapU' % (blueTwoD), 0)
            cmds.setAttr('%s.wrapV' % (blueTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (blueTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (blueTwoD), 3)
            if cmds.isConnected('%s.outUV' % (blueTwoD), '%s.uvCoord' % (blueTwoRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (blueTwoD), '%s.uvCoord' % (blueTwoRamp), f=True)
        else:
            blueTwoRamp = cmds.ls('fxHeraBlueTwo')[0]
        
        ########## Creates Latered Texture and Connects Ramps ###########################
        fxLayered = cmds.shadingNode('layeredTexture', asTexture=True, name='fxHeraLayered')   
        
        if cmds.isConnected('%s.outColor' % (blueTwoRamp), '%s.inputs[1].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (blueTwoRamp), '%s.inputs[1].color' % (fxLayered))    
        if cmds.isConnected('%s.outColorB' % (blueTwoRamp), '%s.inputs[1].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorB' % (blueTwoRamp), '%s.inputs[1].alpha' % (fxLayered))
               
        if cmds.isConnected('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered))    
        if cmds.isConnected('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered))        
        
        if cmds.isConnected('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered))    
        if cmds.isConnected('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered))
            
        if cmds.isConnected('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered))    
        if cmds.isConnected('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered))
        
        if cmds.isConnected('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered))
            
        cmds.removeMultiInstance('%s.inputs[0]' % (fxLayered)) 
        
        ########### Makes Extra Tex ######################################
        fxHeraExtra = vfb.extraTex('fxHeraMatte', fxLayered, explicit_channel="fxHeraMatte", consider_aa=1, enabled=False)
        
############### Creates Extra Tex MultiMatte for fx Hera Caricatures #####################################################
   
def createFxCariDudesExtraTex():
    findHeraCaric = cmds.ls('*:*cariatides*')
    
    if len(findHeraCaric) > 0:      
        if not cmds.objExists('fxCariDudesBlack'):
            blackRamp = cmds.shadingNode('ramp', asTexture=True, name='fxCariDudesBlack')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blackRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blackRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blackRamp), 0,0,0, type='double3')
        else:
            blackRamp = cmds.ls('fxCariDudesBlack')[0]
    
        if not cmds.objExists('fxCariDudesRed'):
            redRamp = cmds.shadingNode('ramp', asTexture=True, name='fxCariDudesRed')
            cmds.setAttr('%s.defaultColor' % (redRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (redRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (redRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (redRamp), 1,0,0, type='double3')
            redTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_redCariDudes')
            cmds.setAttr('%s.wrapU' % (redTwoD), 0)
            cmds.setAttr('%s.wrapV' % (redTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (redTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (redTwoD), 0)
            if cmds.isConnected('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp), f=True)
        else:
            redRamp = cmds.ls('fxCariDudesRed')[0]
    
        if not cmds.objExists('fxCariDudesGreen'):
            greenRamp = cmds.shadingNode('ramp', asTexture=True, name='fxCariDudesGreen')
            cmds.setAttr('%s.defaultColor' % (greenRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (greenRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (greenRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (greenRamp), 0,1,0, type='double3')
            greenTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_greenCariDudes')
            cmds.setAttr('%s.wrapU' % (greenTwoD), 0)
            cmds.setAttr('%s.wrapV' % (greenTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (greenTwoD), 1)
            cmds.setAttr('%s.translateFrameV' % (greenTwoD), 0)
            if cmds.isConnected('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp), f=True)
        else:
            greenRamp = cmds.ls('fxCariDudesGreen')[0]
    
        if not cmds.objExists('fxCariDudesBlueOne'):
            blueOneRamp = cmds.shadingNode('ramp', asTexture=True, name='fxCariDudesBlueOne')
            cmds.setAttr('%s.defaultColor' % (blueOneRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blueOneRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blueOneRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blueOneRamp), 0,0,1, type='double3')
            blueOneTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_blueOneCariDudes')
            cmds.setAttr('%s.wrapU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.wrapV' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (blueOneTwoD), 1)
            cmds.setAttr('%s.coverageU' % (blueOneTwoD), 1)
            cmds.setAttr('%s.coverageV' % (blueOneTwoD), 3)
            if cmds.isConnected('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp), f=True)
        else:
            blueOneRamp = cmds.ls('fxCariDudesBlueOne')[0]
    
        fxLayered = cmds.shadingNode('layeredTexture', asTexture=True, name='fxCariDudesLayered')
        if cmds.isConnected('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered))
        if cmds.isConnected('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered))
        if cmds.isConnected('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered))
        if cmds.isConnected('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered)) == 0:
           cmds.connectAttr('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered))
    
        cmds.removeMultiInstance('%s.inputs[0]' % (fxLayered))
    
        fxCariDudesExtra = vfb.extraTex('fxCariDudesMatte', fxLayered, explicit_channel="fxCariDudesMatte", consider_aa=1, enabled=False)
        
############### Creates Extra Tex MultiMatte for fx Hera Statue #####################################################
        
def createFxStatueExtraTex():
    findHeraStatue = cmds.ls('*:*heraStatue*')
    if len(findHeraStatue) > 0:      
        if not cmds.objExists('fxStatueBlack'):
            blackRamp = cmds.shadingNode('ramp', asTexture=True, name='fxStatueBlack')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blackRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blackRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blackRamp), 0,0,0, type='double3')
        else:
            blackRamp = cmds.ls('fxStatueBlack')[0]
    
        if not cmds.objExists('fxStatueRed'):
            redRamp = cmds.shadingNode('ramp', asTexture=True, name='fxStatueRed')
            cmds.setAttr('%s.defaultColor' % (redRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (redRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (redRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (redRamp), 1,0,0, type='double3')
            redTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_redStatue')
            cmds.setAttr('%s.wrapU' % (redTwoD), 0)
            cmds.setAttr('%s.wrapV' % (redTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (redTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (redTwoD), 0)
            cmds.setAttr('%s.coverageU' % (redTwoD), 8)
            cmds.setAttr('%s.coverageV' % (redTwoD), 2)
            if cmds.isConnected('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (redTwoD), '%s.uvCoord' % (redRamp), f=True)
        else:
            redRamp = cmds.ls('fxStatueRed')[0]
    
        if not cmds.objExists('fxStatueGreen'):
            greenRamp = cmds.shadingNode('ramp', asTexture=True, name='fxStatueGreen')
            cmds.setAttr('%s.defaultColor' % (greenRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (greenRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (greenRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (greenRamp), 0,1,0, type='double3')
            greenTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_greenStatue')
            cmds.setAttr('%s.wrapU' % (greenTwoD), 0)
            cmds.setAttr('%s.wrapV' % (greenTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (greenTwoD), 8)
            cmds.setAttr('%s.translateFrameV' % (greenTwoD), 0)
            cmds.setAttr('%s.coverageU' % (greenTwoD), 2)
            cmds.setAttr('%s.coverageV' % (greenTwoD), 1)
            if cmds.isConnected('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (greenTwoD), '%s.uvCoord' % (greenRamp), f=True)
        else:
            greenRamp = cmds.ls('fxStatueGreen')[0]
    
        if not cmds.objExists('fxStatueBlueOne'):
            blueOneRamp = cmds.shadingNode('ramp', asTexture=True, name='fxStatueBlueOne')
            cmds.setAttr('%s.defaultColor' % (blueOneRamp), 0,0,0, type='double3')
            cmds.removeMultiInstance('%s.colorEntryList[1]' % (blueOneRamp), b=True)
            cmds.removeMultiInstance('%s.colorEntryList[2]' % (blueOneRamp), b=True)
            cmds.setAttr('%s.colorEntryList[0].color' % (blueOneRamp), 0,0,1, type='double3')
            blueOneTwoD = cmds.shadingNode('place2dTexture', au=True, name='place2d_blueOneStatue')
            cmds.setAttr('%s.wrapU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.wrapV' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameU' % (blueOneTwoD), 0)
            cmds.setAttr('%s.translateFrameV' % (blueOneTwoD), 2)
            cmds.setAttr('%s.coverageU' % (blueOneTwoD), 1)
            cmds.setAttr('%s.coverageV' % (blueOneTwoD), 3)
            if cmds.isConnected('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp)) == 0:
                cmds.connectAttr('%s.outUV' % (blueOneTwoD), '%s.uvCoord' % (blueOneRamp), f=True)
        else:
            blueOneRamp = cmds.ls('fxStatueBlueOne')[0]
    
        fxLayered = cmds.shadingNode('layeredTexture', asTexture=True, name='fxStatueLayered')
        if cmds.isConnected('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (blueOneRamp), '%s.inputs[2].color' % (fxLayered))
        if cmds.isConnected('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorB' % (blueOneRamp), '%s.inputs[2].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (greenRamp), '%s.inputs[3].color' % (fxLayered))
        if cmds.isConnected('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorG' % (greenRamp), '%s.inputs[3].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (redRamp), '%s.inputs[4].color' % (fxLayered))
        if cmds.isConnected('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColorR' % (redRamp), '%s.inputs[4].alpha' % (fxLayered))
    
        if cmds.isConnected('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered)) == 0:
            cmds.connectAttr('%s.outColor' % (blackRamp), '%s.inputs[5].color' % (fxLayered))
    
        cmds.removeMultiInstance('%s.inputs[0]' % (fxLayered))
    
        fxStatueExtra = vfb.extraTex('fxStatueMatte', fxLayered, explicit_channel="fxStatueMatte", consider_aa=1, enabled=False) 

        
        
################# Canyon ExtraTex ##################################################################
     
def createCanyonTex():
    findCanyon = cmds.ls('*canyon*')     
    
    if len(findCanyon) > 0:
        mel.eval('source dloVRayRenderElemTools')
        mel.eval('dloImportAllPublishedRenderElemCB "/jobs/vfx_herc/sequences/assets/env.canyon/lib/maya/presets/renderElem/" 0 0') 
