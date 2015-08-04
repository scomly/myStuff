import hou

shader = hou.selectedNodes()[0]
path = shader.path()
print shader

getShader = hou.node(path)



parms = shader.parms()

changedParms = []

for x in parms:
    isAt = x.isAtDefault()
    if isAt == False:
        parmname = x.name()
        parmEval = x.eval()
        print parmname
        print parmEval
        #changedParms.append(x)
        
   
for x in changedParms:
    print x
    test = getShader.evalParm(x)
