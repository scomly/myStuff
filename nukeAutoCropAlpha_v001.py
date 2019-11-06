import nuke
import time
import csv
import os

#### Prints all knobs on selected node ####
#### print( nuke.selectedNode() )

#### Get Current Frame ####
#### frame = nuke.frame()
#### print frame

#### Get AutoCrop Data ####
#### value = nuke.toNode('CurveTool2').knob('autocropdata').getValue()
#### print value

#### Get name of selected read node ####
getSelect = nuke.selectedNode()
getName = getSelect['name'].value()
#print getName

#### Get Frame in and Out for selected read node ####
getSelect = nuke.selectedNode()
getFirstFrame = getSelect['first'].value()
getLastFrame = getSelect['last'].value()
#print getFirstFrame
#print getLastFrame

#### Creates and set Shuffle ####
shuffle = nuke.nodes.Shuffle()
shuffle['red'].setValue("alpha")
shuffle['green'].setValue("alpha")
shuffle['blue'].setValue("alpha")

#### Connect shuffle to read node ####
shuffle.connectInput(1,getSelect)

#### Creates and Sets CurveTool ####
curveTool = nuke.nodes.CurveTool()
curveTool['operation'].setValue('Auto Crop')
curveTool['color'].setValue(1)
curveTool['ROI'].setValue([0,0,1920,1080])
curveTool['afterFrameRender'].setValue("frameData[nuke.frame()]=nuke.toNode(getCurveToolLabel).knob('autocropdata').getValue()")
getCurveToolLabel = curveTool['name'].value()
#print getCurveToolLabel

#### Connect curveTool to shuffle ####
curveTool.connectInput(1,shuffle)

#### Creates Empty Dictionary ####
frameData = {}

#### Executes Curve Tool ####
nuke.execute(curveTool,getFirstFrame,getLastFrame)

#### print frameData

#### Sets current working directory ####
path = 'P:\\projects\\googlemeasure_36793P\\design\\work\\'
os.chdir(path)

#### Writes CSV file ####
with open('frameData.csv','wb') as frameData_csv_file:
    writer = csv.writer(frameData_csv_file)
    for key, value in frameData.items():
       writer.writerow([key, value])
