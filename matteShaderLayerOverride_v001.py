
def matteShaderOverride():
    
    thing = cmds.ls(sl=True, dag=True, o=True, s=True)
    
    getMatteShader = cmds.ls('MatteSurfaceShader')
    
    if len(getMatteShader) == 0:
        surfaceShader = cmds.shadingNode('surfaceShader', asShader=True, name='MatteSurfaceShader')
        cmds.setAttr('%s.outMatteOpacity' % surfaceShader, 0,0,0, type='double3')
    else:
        surfaceShader = getMatteShader[0]
    
    for x in thing:
        connect = cmds.listConnections(x,type='shadingEngine')
        if connect != None:
            connect = connect[0]
            getOverride = cmds.editRenderLayerAdjustment(query=True)
            getShaderAssignmentOverride = (connect + '.surfaceShader')
            if getShaderAssignmentOverride not in getOverride:
                createOverride = cmds.editRenderLayerAdjustment('%s.surfaceShader' % connect)  
            getSurfaceShader = cmds.listConnections('%s.surfaceShader' % connect, type='surfaceShader')
            if getSurfaceShader == None:
                cmds.connectAttr('%s.outColor' % surfaceShader, '%s.surfaceShader' % (connect), force=True)
            getSurfaceShader = cmds.listConnections('%s.surfaceShader' % connect, type='surfaceShader')    
            if getSurfaceShader[0] != 'MatteSurfaceShader':
                cmds.connectAttr('%s.outColor' % surfaceShader, '%s.surfaceShader' % (connect), force=True)


matteShaderOverride()
