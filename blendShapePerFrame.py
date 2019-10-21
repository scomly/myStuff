my_mesh = cmds.ls(sl=True)
my_history = cmds.listHistory(my_mesh)
blendShapes = cmds.ls(type='blendShape')

for x in blendShapes:
    blendShapeWeight = cmds.listAttr('%s.w' % x, m=True)
    
    getFrame = cmds.currentTime(q=True)
    lastFrame = getFrame - 1
    cmds.currentTime(lastFrame)
    cmds.setKeyframe(x, at=blendShapeWeight, v=0)
    
    getFrame = cmds.currentTime(q=True)
    nextFrame = getFrame + 1
    cmds.currentTime(nextFrame)       
    cmds.setKeyframe(x, at=blendShapeWeight, v=1)
    
    getFrame = cmds.currentTime(q=True)
    nextFrame = getFrame + 1
    cmds.currentTime(nextFrame)
    cmds.setKeyframe(x, at=blendShapeWeight, v=0)
