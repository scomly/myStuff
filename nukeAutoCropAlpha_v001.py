import nuke

#### Prints all knobs on selected node ####
print( nuke.selectedNode() )


#### Get name of selected read node ####
getSelect = nuke.selectedNode()
getName = getSelect['name'].value()
print getName

#### Get Frame in and Out for selected read node ####
getSelect = nuke.selectedNode()
getFirstFrame = getSelect['first'].value()
getLastFrame = getSelect['last'].value()
print getFirstFrame
print getLastFrame

#### Get Current Frame ####
frame = nuke.frame()
print frame

#### Set Current Frame ####
setFrame = nuke.frame(1040)

#### Creates and set Shuffle ####
shuffle = nuke.nodes.Shuffle()
shuffle['red'].setValue("alpha")
shuffle['green'].setValue("alpha")
shuffle['blue'].setValue("alpha")

#### Connect input of node to another ####
shuffle.connectInput(1,getSelect)

#### Creates and Sets CurveTool ####
curveTool = nuke.nodes.CurveTool()
curveTool['operation'].setValue('Auto Crop')
curveTool['color'].setValue(1)
nuke.execute(curveTool,1001,1040)

#### Get AutoCrop Data ####
value = nuke.toNode('CurveTool2').knob('autocropdata').getValue()
print value

#### Function to set frame ####
for x in range(getFirstFrame,getLastFrame+1):
    setFrame = nuke.frame(x)
    cropValue = nuke.toNode(curveTool).knob('autocropdata').getValue()
    print cropValue
