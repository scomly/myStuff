thing = cmds.ls(sl=True, dag=True, o=True, s=True)

shaderDict = {}

#print shaderDict

for x in thing:
    #connect = []
    connect = cmds.listConnections(x,type='shadingEngine')
    shaderDict[x]=connect

    #cmds.sets(x, e=True, forceElement=connect)
    

for x,y in shaderDict.items():
    #print x
    #print y
    if y != None:
        cmds.sets(x, e=True, forceElement=shaderDict[x][0])

for x in thing:
    try:
        cmds.sets(x, e=True, forceElement=shaderDict[x][0])  
