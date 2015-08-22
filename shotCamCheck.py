connects shotcam to projection node if there are no connections

if cmds.objExists(projectCam):
    getIfConnect = cmds.listConnections('%s.linkedCamera' % (fileProject), d=False, s=True)
    if getIfConnect == None:
        cmds.connectAttr('%s' % (projectCam) + 'Shape.message', '%s.linkedCamera' % (fileProject), f=True)
## connects shotcam to the proj cam if it exists

Will only consrain things if there is already no incoming connecting to TranslateX

if cmds.objExists(shotCam):
    getIfConnect = cmds.listConnections('%s.tx' % (refSetupGroup), d=False, s=True)
    if getIfConnect == None:
        cmds.parentConstraint(shotCam, refSetupGroup, mo=False)
        cmds.setAttr('%s.translate' % (translateGroup), -50, -25, -150)
