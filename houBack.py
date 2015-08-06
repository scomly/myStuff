
import hou

sourceShader = hou.selectedNodes()[0]
#path = shader.path()
#print shader

#getShader = hou.node(path)

#shader.parent()

#ting = hou.node(path)

sourceParms = sourceShader.parms()

changedParms = {}

for x in parms:
    isAt = x.isAtDefault()
    if isAt == False:
        parmname = x.name()
        parmEval = x.eval()
        changedParms[parmname] = parmEval
        
destinShader =  hou.selectedNodes()[0]

for x,y in changedParms.iteritems():
   # print x
   # print y
    destinShader.parm(x).set(y)
        


#mat = hou.node('shop/mantrasurface')

#dest = hou.node('/shop/')

#hou.copyNodesTo([mat], dest)
