import os, re, sys, logging

import maya.cmds as cmds
import maya.mel as mel

import mVray.vrayObjectProperties as vop
import mVray.vrayFrameBuffers as vfb

import dloUtils
reload(dloUtils)

import assetSetup
reload(assetSetup)

######## UI Window ########
class bfSetupMessengerUI():
    def __init__(self): 
        winTile = "bfSetupMessengerUI"
        win = dloUtils.dloUIWindow(winTile, "Bigfoot Lighting Setup Messenger", 750, 650, 1)
        form = cmds.formLayout(p=win, bgc=(.2, .2, .2))
        messageScrlList = cmds.textScrollList("bfMessageScrollList", p=form)
        okBn = cmds.button(p=form, c="cmds.deleteUI('bfSetupMessengerUI')", bgc=(.4, .4, .4), l="Ok", w=80)
        cmds.formLayout(form, e=1, ac=[(messageScrlList, "bottom", 10, okBn)], af=[(messageScrlList, "top", 10), (messageScrlList, "left", 10), (messageScrlList, "right", 10)])
        cmds.formLayout(form, e=1, af=[(okBn, "bottom", 10), (okBn, "left", 10), (okBn, "right", 10)])
        dloUtils.dloEvokeUI(winTile, win, 800, 650)

############################
######## runSetup() ########
############################
def runSetup():
    msgs = []

    # Set default render layer as active layer
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

    # Make sure vray plugin is loaded
    if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
        cmds.loadPlugin('vrayformaya', qt=True)

    # Kick some ass
    organizeScene(msgs)
    createUtilShaders(msgs)
    createRenderElements(msgs)

    # dlo asset setup
    assetMsgs = assetSetup.dloAssetSetup()
    if assetMsgs:
        msgs.extend(assetMsgs)

    # Display UI with results
    if len(msgs):
        bfSetupMessengerUI()
        for msg in msgs: cmds.textScrollList("bfMessageScrollList", e=1, a=msg)

######## Utility to determine currently set sequence ########
def getSeq():
    return os.getenv("M_SEQUENCE", "")

######## Utility to log progress ########
def logInfo(infoString, accumulatedInfo=[]):
    print infoString
    accumulatedInfo.append(infoString)

######## Utility to set up a group and vrayObjectProperties ########
def updateGroupAndVop(searchList, groupName, vopName, msgs):
    nodes = cmds.ls(searchList, assemblies=True)
    groupNode = cmds.ls(groupName)
    vopNode = cmds.ls(vopName)
    if nodes:
        if groupNode:
            cmds.parent(nodes, groupNode)
            logInfo('Added to group %s: %s' % (groupNode, nodes), msgs)
        else:
            groupNode = cmds.group(nodes, name=groupName)
            logInfo('Created group %s containing %s' % (groupNode, nodes), msgs)
    if not vopNode:
        if groupNode:
            vopNode = vop.createObjectProperties(groupNode, vopName)
            logInfo('Created vrayObjectProperties %s containing %s' % (vopNode, groupNode), msgs)

######## Organize Outliner and Create Object Properties ########
def organizeScene(msgs=[]):
    # Trackman
    trackmanSearchList = ["trackman*:*", "pymSuit*:*"]
    updateGroupAndVop(trackmanSearchList, 'TRACKMAN_GRP', 'trackman_VOP', msgs)

    # Tracking Geo
    trackSearchList = ["*:*__track__*", "pymGuestRoom*:*"]
    updateGroupAndVop(trackSearchList, 'TRACK_GEO_GRP', 'track_geo_VOP', msgs)

    # Roots
    rootSearchList = ["*Heroroots*:*", "*Heroroots*_VRayFurPreviewTm"]
    updateGroupAndVop(rootSearchList, 'ROOTS_GRP', 'roots_VOP', msgs)

    # Tunnel
    tunnelSearchList = ["tunnel*:*", "env_tunnelDressing_*_Instancer_*"]
    updateGroupAndVop(tunnelSearchList, 'TUNNEL_GRP', 'tunnel_VOP', msgs)

    # Ants
    antSearchList = ["carpenterAnt*:*", "char_carpenterAnt*_Instancer_*",
                     "bulletAnt*:*", "char_bulletAnt*_Instancer_*",
                     "crazyAnt*:*", "char_crazyAnt*_Instancer_*",
                     "fireAnt*:*", "char_fireAnt*_Instancer_*",]
    updateGroupAndVop(antSearchList, 'ANTS_GRP', 'ants_VOP', msgs)

    # Sugar Cubes
    sugarcubeSearchList = ["sugarcube*:*", "*sugarcube*_Instancer*"]
    updateGroupAndVop(sugarcubeSearchList, 'SUGARCUBES_GRP', 'sugarcubes_VOP', msgs)

    # Antman
    updateGroupAndVop(["antman*:*"], 'ANTMAN_GRP', 'antman_VOP', msgs)

    # Wasp
    updateGroupAndVop(["wasp*:*"], 'WASP_GRP', 'wasp_VOP', msgs)

    # Yellowjacket
    updateGroupAndVop(["yellowJacket*:*"], 'YELLOWJACKET_GRP', 'yellowjacket_VOP', msgs)

    # Missile
    updateGroupAndVop(["missile*:*"], 'MISSILE_GRP', 'missile_VOP', msgs)

######## Util Shaders Creation ##################################
def createUtilShaders(msgs=[]):
    if not cmds.objExists('RED'):
        redMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='RED')
        cmds.setAttr('%s.color' % (redMtl), 1,0,0, type='double3')
        cmds.setAttr('%s.emitOnBackSide' % (redMtl), 1)
        logInfo('Created RED shader', msgs)

    if not cmds.objExists('GREEN'):
        greenMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='GREEN')
        cmds.setAttr('%s.color' % (greenMtl), 0,1,0, type='double3')
        cmds.setAttr('%s.emitOnBackSide' % (greenMtl), 1)
        logInfo('Created GREEN shader', msgs)

    if not cmds.objExists('BLUE'):
        blueMtl = cmds.shadingNode('VRayLightMtl', asShader=True, name='BLUE')
        cmds.setAttr('%s.color' % (blueMtl), 0,0,1, type='double3')
        cmds.setAttr('%s.emitOnBackSide' % (blueMtl), 1) 
        logInfo('Created BLUE shader', msgs)

    if not cmds.objExists('BLACK'):
        blackMtl = cmds.shadingNode('VRayMtl', asShader=True, name='BLACK')
        cmds.setAttr('%s.color' % (blackMtl), 0,0,0, type='double3')
        cmds.setAttr('%s.reflectionColorAmount' % (blackMtl), 0)
        cmds.setAttr('%s.diffuseColorAmount' % (blackMtl), 0)
        logInfo('Created BLACK shader', msgs)

    if not cmds.objExists('SHADOW_CATCHER'):
        shdCatcher = cmds.shadingNode('VRayMtl', asShader=True, name='SHADOW_CATCHER')
        cmds.setAttr('%s.reflectionColorAmount' % (shdCatcher), 0)
        cmds.setAttr('%s.diffuseColorAmount' % (shdCatcher), 1)
        cmds.setAttr('%s.brdfType' % (shdCatcher), 0)
        logInfo('Created SHADOW_CATCHER shader', msgs)

    if not cmds.objExists('MIRROR'):
        mirrorMtl = cmds.shadingNode('VRayMtl', asShader=True, name='MIRROR')
        cmds.setAttr('%s.color' % (mirrorMtl), 0,0,0, type='double3')
        cmds.setAttr('%s.reflectionColor' % (mirrorMtl), 1,1,1, type='double3')
        cmds.setAttr('%s.reflectionColorAmount' % (mirrorMtl), 1)
        cmds.setAttr('%s.diffuseColorAmount' % (mirrorMtl), 0)
        cmds.setAttr('%s.useFresnel' % (mirrorMtl), 0)
        mirrorOccl = cmds.shadingNode('VRayDirt', asTexture=True, name='MIRROR_OCCLUSION')
        cmds.setAttr('%s.blackColor' % (mirrorOccl), 1,1,1, type='double3')
        cmds.setAttr('%s.whiteColor' % (mirrorOccl), 0,0,0, type='double3')
        cmds.setAttr('%s.radius' % (mirrorOccl), 1000)
        cmds.setAttr('%s.occlusionMode' % (mirrorOccl), 2)
        cmds.connectAttr('%s.outColor' % (mirrorOccl), '%s.reflectionColor' % (mirrorMtl))
        logInfo('Created MIRROR shader', msgs)

    if not cmds.objExists('CONTACT_SHAD_OCCL'):
        contactShadOccl = cmds.shadingNode('VRayDirt', asTexture=True, name='CONTACT_SHAD_OCCL')
        cmds.setAttr('%s.blackColor' % (contactShadOccl), 1,1,1, type='double3')
        cmds.setAttr('%s.whiteColor' % (contactShadOccl), 0,0,0, type='double3')
        cmds.setAttr('%s.radius' % (contactShadOccl), 2)
        cmds.setAttr('%s.ignoreSelfOcclusion' % (contactShadOccl), 1)
        cmds.setAttr('%s.resultAffectInclusive' % (contactShadOccl), 0)
        contactShadNonCastSet = cmds.sets(name='contactShadNonCastSet')
        cmds.connectAttr('%s.usedBy' % (contactShadNonCastSet), '%s.resultAffect' % (contactShadOccl))
        logInfo('Created CONTACT_SHAD_OCCL texture', msgs)

    if (getSeq() != 'bak') and (not cmds.objExists('BG_PROJ')):
        cmds.file("/jobs/vfx_bf/TASKS/light/maya/renderData/shaders/bf_light_plateProjectionShaders_v0002.mb", i=True)
        logInfo('Imported BG_PROJ and BLACK_PROJ shaders (if your shot has a plate, connect shot camera to BG_CAMERA_PROJECTION and add plate path to BG_PLATE)', msgs)

################ Render Elements Creation ###########################################
def createRenderElements(msgs=[]):
    if not cmds.objExists('vrayRE_MatteShadow'):
        vfb.matteShadow('vrayRE_MatteShadow', enabled=False)
        logInfo('Created vray render element vrayRE_MatteShadow', msgs)

    if not cmds.objExists('vrayRE_ContactShadow'):
        if cmds.objExists('CONTACT_SHAD_OCCL'):
            vfb.extraTex('vrayRE_ContactShadow', 'CONTACT_SHAD_OCCL', explicit_channel='contactShadow', enabled=False)
            logInfo('Created vray render element vrayRE_ContactShadow', msgs)

######## Ref Spheres Setup ########
def refSphereSetup():
    refSphereNode = 'REF_SPHERES_COLORCHART'
    shotCamNode = 'shotcam1:shot_camera'
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
    if not cmds.objExists(refSphereNode):
        cmds.file('/jobs/vfx_bf/TECH/lib/maya/presets/lightRigs/REF_SPHERES_COLORCHART/v0002/lightRig.ma', i=True)
        if cmds.objExists(shotCamNode):
            constraintNode = cmds.parentConstraint(shotCamNode, refSphereNode)
            if constraintNode:
                constraintNode = constraintNode[0]
                cmds.setAttr('%s.target[0].targetOffsetTranslate' % (constraintNode), 0, 0, -50)
                cmds.setAttr('%s.target[0].targetOffsetRotate' % (constraintNode), 0, 180, 0)
                cmds.delete(constraintNode)
