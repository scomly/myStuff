import nuke
import time
import csv
import os


#### Get multiple selected nodes ####
selectList = nuke.selectedNodes()

for x in selectList:

    #### Get name of read node ####
    getName = []
    getName = x['name'].value()
    #print getName

    #### Get frame in and out for selected read node ####
    getFirstFrame = []
    getLastFrame = []
    getFirstFrame = x['first'].value()
    getLastFrame = x['last'].value()
    #print getFirstFrame
    #print getLastFrame

    #### Creates path to save CSV files based on file read path ####
    getCurrentFilePath = []
    getCurrentFilePath = x['file'].value()
    filePathSplit = getCurrentFilePath.split('/')
    updatedFilePath = getCurrentFilePath.replace(filePathSplit[-1],'')
    #print updatedFilePath

    #### Get resolution for selected read node ####
    getWdith = []
    getHeight = []
    scriptFormats = nuke.formats()
    getWidth = x.width()
    getHeight = x.height()
    #print getWidth
    #print getHeight

    #### Creates and sets shuffle ####
    shuffle = []
    shuffle = nuke.nodes.Shuffle()
    shuffle['red'].setValue("red")
    shuffle['green'].setValue("red")
    shuffle['blue'].setValue("red")

    #### Connect shuffle to read node ####
    shuffle.connectInput(1,x)

    #### Creates and sets curveTool ####
    curveTool = []
    curveTool = nuke.nodes.CurveTool()
    curveTool['operation'].setValue('Auto Crop')
    curveTool['ROI'].setValue([0,0,getWidth,getHeight])
    curveTool['afterFrameRender'].setValue("frameData[nuke.frame()]=nuke.toNode(getCurveToolLabel).knob('autocropdata').getValue()")
    getCurveToolLabel = curveTool['name'].value()

    #### Connects curveTool to shuffle ####
    curveTool.connectInput(1,shuffle)

    #### Creates empty dictionary ####
    frameData = {}

    #### Executes curveTool ####
    nuke.execute(curveTool,getFirstFrame,getLastFrame)

    #### Sets current working directory ####
    path = updatedFilePath
    os.chdir(path)

    #### Writes CSV file ####
    frameData_csv_file = []
    with open('autoCropData.csv','wb') as frameData_csv_file:
        writer = csv.writer(frameData_csv_file)
        for key, value in frameData.items():
           writer.writerow([key, value])
