import fnmatch

thing = cmds.ls(sl=True)

getProject = cmds.workspace(expandName = 'relativePathName')
getAssetPath = getProject.split('build/')
getAssetName = getAssetPath[1].split('/m')
fullPath = (getAssetPath[0] + 'build/'+ getAssetName[0] + '/m_model/textures/wip/hi/')

refs = cmds.ls(type='reference')
refs.remove('sharedReferenceNode')
for i in refs:
    rFile = cmds.referenceQuery(i, f=True)
    if cmds.referenceQuery(rFile, il=True):
        cmds.file(rFile, importReference=True)

for tex in thing:

    
    getSG = cmds.listConnections(tex, p=True, s=True, d=False)
    
    getSourceName = tex    
     
    connectionDict = {}
    
    getTexDirectory = cmds.getAttr('%s.texDirectory' % tex) 
    #print getTexDirectory
    getTexDirectory = getTexDirectory.replace('call_of_duty_cod_eclipse_J83580', 'marvel_strike_force_J405577')
    getTexRes = cmds.getAttr('%s.texResolution' % tex)
    #print getTexRes
    compilePath = (getTexDirectory + '/wip/' + getTexRes + '/')
    getTexName = tex.split(':')[1]
    combineFullTexturePath = (compilePath + getTexName + '_u<U>_v<V>.exr')
    
    fileTexture = cmds.shadingNode('file', asTexture=True, name=tex)
  
    cmds.select(tex)
           
    for attr in getSG:
        getDest = cmds.listConnections(attr, d=True, s=False, p=True)
        getSourceNameWild = '*' + getSourceName + '*'
        getBadConnect = fnmatch.filter(getDest,getSourceNameWild)
        for x in getBadConnect:            
            getDest.remove(x)
        connectionDict[attr]=getDest

    for x,y in connectionDict.items():    
        if y != []:
            for obj in y:         
                isoPlug = x.split('.')[1]
                newTexture = (fileTexture + '.' + isoPlug)              
                cmds.connectAttr(newTexture,obj, force=True)   

    twoD = cmds.shadingNode('place2dTexture', asUtility=True, name='%sPlace2d' % tex)
    cmds.connectAttr('%s.outUV' % (twoD), '%s.uv' % (fileTexture))    
    cmds.setAttr('%s.fileTextureName' % (fileTexture), combineFullTexturePath, type='string')
 
