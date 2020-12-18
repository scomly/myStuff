


import nuke
import time
import csv
import os


#### Get multiple selected nodes ####
selectList = nuke.selectedNodes()

for x in selectList:

    #### Creates empty dictionary ####
    frameData = {}

    #### Get name of read node ####
    getName = []
    getName = x['name'].value()
    #print getName

    #### Get frame in and out for selected read node ####
    getFirstFrame = []
    getLastFrame = []
    getFirstFrame = x['first'].value()
    getLastFrame = x['last'].value()
    #getFirstFrame = 500
    #getLastFrame = 500

    #print getFirstFrame
    #print getLastFrame

    #### Creates path to save CSV files based on file read path ####
    getCurrentFilePath = []
    getCurrentFilePath = x['file'].value()
    filePathSplit = []    
    filePathSplit = getCurrentFilePath.split('/')
    updatedFilePath = []
    updatedFilePath = getCurrentFilePath.replace(filePathSplit[-1],'')
    splitName = []
    splitName = filePathSplit[-1].split('.')
    splitNameFile = []
    splitNameFile = splitName[0]
    #print splitNameFile
    getFilePathName = []
    getFilePathName = filePathSplit[-1]
    getFileNameDot = []
    getFileNameDot = getFilePathName + '.'
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
    curveTool['ccrange'].setValue(0.9999)
    curveTool['ROI'].setValue([0,0,getWidth,getHeight])
    curveTool['afterFrameRender'].setValue("frameData[nuke.frame()]=nuke.toNode(getCurveToolLabel).knob('autocropdata').getValue()")
    getCurveToolLabel = curveTool['name'].value()

    #### Connects curveTool to shuffle ####
    curveTool.connectInput(1,shuffle)

    #### Executes curveTool ####
    nuke.execute(curveTool,getFirstFrame,getLastFrame)

    #### Sets current working directory ####
    path = []
    path = updatedFilePath
    os.chdir(path)
    
    nameCSV = '_frameData.csv'
    nameCSV2 = '_frameData2.csv'
    name = []
    name = splitNameFile + nameCSV
    name2 = splitNameFile + nameCSV2
    #print x
    #print name
    #print getFirstFrame
    #print getLastFrame

    #### Writes CSV file ####
    writer = []
    frameData_csv_file = []
    with open(name,'wb') as frameData_csv_file:
        writer = csv.writer(frameData_csv_file)
        #frameData.keys().sort(key = lambda s: s[1])
        for key in sorted(frameData.keys()):
            #print key
            value = frameData[key]
            #print value
            writer.writerow([key, value])
