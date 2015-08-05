
import hou

shader = hou.selectedNodes()[0]
path = shader.path()
print shader

getShader = hou.node(path)

shader.parent()

ting = hou.node(path)

parms = shader.parms()

changedParms = {}

for x in parms:
    isAt = x.isAtDefault()
    if isAt == False:
        parmname = x.name()
        parmEval = x.eval()
        changedParms[parmname] = parmEval
        
hou.copyNodesTo('/shop/mantrasurface', hou.node( '/shop/shaderOne/'))


mat = hou.node('shop/mantrasurface')
print mat
list(mat)


dest = hou.node('/shop/')
hou.copyNodesTo(mat, dest)
