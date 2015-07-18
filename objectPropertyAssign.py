import maya.cmds as cmds
import os
import re
from mVray import vrayObjectProperties as vop
from mVray import vrayFrameBuffers as vfb
import maya.mel as mel

######### Sets default render layer as active later ###############

cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

####### Loads VRay if not loaded ##########################

if cmds.pluginInfo('vrayformaya', q=True, loaded=True) == False:
    cmds.loadPlugin('vrayformaya', qt=True)

#################################################################


def actOnPress():
    getAssignType = cmds.radioButtonGrp('ButtonOne', q=True, sl=True)
    getIDCheckState = cmds.checkBox('IDCheck', v=True, q=True)
    getUACheckState = cmds.checkBox('UACheck', v=True, q=True)
    getIDRemoveState = cmds.checkBox('IDRemove', v=True, q=True)
    getUARemoveState = cmds.checkBox('UARemove', v=True, q=True)
    
    
    if getAssignType == 1:
        nodes = cmds.ls(sl=True)
    else:
        getKeyword = cmds.textField("keyIn", tx=True, q=True)
        keyword_mask_list = ["*:*%s*" % (getKeyword), '*%s*' % (getKeyword)]
        nodes = cmds.ls(keyword_mask_list, transforms=True)

    setUserID = cmds.textField("IDIn", tx=True, q=True)
    if setUserID > 0:
        setUserID = int(setUserID)
    setUserAttr = cmds.textField("UAIn", tx=True, q=True)
        
    for node in nodes:
        getID = cmds.attributeQuery('vrayObjectID', node=node, ex=True)
        getUserAttr = cmds.attributeQuery('vrayUserAttributes', node=node, ex=True)
        if getIDCheckState == True and getIDRemoveState == False:
            if getID == False:
                addObjectID = cmds.addAttr(node, ln='vrayObjectID')
            cmds.setAttr('%s.vrayObjectID' % (node), setUserID)
        if getIDCheckState == True and getIDRemoveState == True:
            if getID == True:
                cmds.deleteAttr(node, at='vrayObjectID')                    
        if getUACheckState == True and getUARemoveState == False:
            if getUserAttr == False:
                addUser = cmds.addAttr(nodes, ln='vrayUserAttributes', dataType='string')
            cmds.setAttr('%s.vrayUserAttributes' % (node), setUserAttr, type='string')
        if getUACheckState == True and getUARemoveState == True:
            if getUserAttr == True:
                cmds.deleteAttr(node, at='vrayUserAttributes')  
            
            
def debugButton():
    getKeywordDebug = cmds.textField("keyIn", tx=True, q=True)
    keywordDebug_mask_list = ["*:*%s*" % (getKeywordDebug), '*%s*' % (getKeywordDebug)]
    selectList = cmds.ls(keywordDebug_mask_list, transforms=True)
    cmds.select(cl=True)
    for nodes in selectList:
        cmds.select(nodes, add=True)

def makeGUI():
    if cmds.window('VRayAtrributeAssigner', ex=1, q=1):
        cmds.deleteUI('VRayAttributeAssigner')      
    
    vrayAttrAssignWindow = cmds.window('VRayAttributeAssigner')
    form = cmds.formLayout()
    
    RB1 = cmds.radioButtonGrp('ButtonOne', label='Assign to objects  ', labelArray2=['By Selection', 'By Keyword'], numberOfRadioButtons=2, of2 = 'cmds.textField("keyIn", enable=0, edit=True)', on2 = 'cmds.textField("keyIn", enable=1, edit=True)',  cw3 = [150, 100, 50])
    getButtonState = cmds.radioButtonGrp('ButtonOne', q=True, sl=True)
    keyText = cmds.text(label = 'Keyword')
    keyInput = cmds.textField('keyIn', width = 200, enable=0)
    
    debugButton = cmds.button(label='DEBUG', width=50, command='debugButton()')
    
    IDcheckBox = cmds.checkBox('IDCheck', label = 'Object ID', ofc = 'cmds.textField("IDIn", enable=0, edit=True)\ncmds.checkBox("IDRemove", value=0, enable=0, edit=True)',  onc = 'cmds.textField("IDIn", enable=1, edit=True)\ncmds.checkBox("IDRemove", enable=1, edit=True)' )
    
    IDRemoveBox = cmds.checkBox('IDRemove', label = 'Remove', en=False, onc = 'cmds.textField("IDIn", enable=0, edit=True)',  ofc = 'cmds.textField("IDIn", enable=1, edit=True)')
    
    IDText = cmds.text(label = 'Object ID #')
    IDInput = cmds.textField('IDIn', tx = '0', width = 50, enable=0)
    
    UAcheckBox = cmds.checkBox('UACheck', label = 'User Attributes', ofc = 'cmds.textField("UAIn", enable=0, edit=True)\ncmds.checkBox("UARemove", value = 0, enable=0, edit=True)',  onc = 'cmds.textField("UAIn", enable=1, edit=True)\ncmds.checkBox("UARemove", enable=1, edit=True)')
    
    UARemoveBox = cmds.checkBox('UARemove', label = 'Remove', en=False, onc = 'cmds.textField("UAIn", enable=0, edit=True)',  ofc = 'cmds.textField("UAIn", enable=1, edit=True)')
    
    UAText = cmds.text(label = 'UserAttributes')
    UAInput = cmds.textField('UAIn', width = 500, enable=0)
    
    DOIT = cmds.button(label='DO IT!', width=100, command='actOnPress()')
    
    cmds.formLayout(form, edit=True, attachForm = [(RB1, 'left', 0), (RB1, 'top', 10), (keyText, 'top', 35), (keyText, 'left', 100), (keyInput, 'top', 30), (keyInput, 'left', 150), (debugButton, 'top', 30), (debugButton, 'left', 360), (IDcheckBox, 'top', 75), (IDcheckBox, 'left', 25), (IDRemoveBox, 'top', 75), (IDRemoveBox, 'left', 100), (IDText, 'left', 15), (IDText, 'top', 100), (IDInput, 'left', 80), (IDInput, 'top', 95), (UAcheckBox, 'top', 135), (UAcheckBox, 'left', 25), (UARemoveBox, 'top', 135), (UARemoveBox, 'left', 125), (UAText, 'left', 15), (UAText, 'top', 165), (UAInput, 'left', 100), (UAInput, 'top', 160), (DOIT, 'left', 500), (DOIT, 'top', 200)])
  
     
    cmds.showWindow(vrayAttrAssignWindow)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
