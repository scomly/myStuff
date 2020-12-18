#### Get multiple selected nodes ####
selectList = nuke.selectedNodes()

for x in selectList:
#### Get name of read node ####
    getName = []
    getName = x['name'].value()
    #print getName

    x['colorspace'].setValue("linear")

#### Creates path to save CSV files based on file read path ####
    getCurrentFilePath = []
    getCurrentFilePath = x['file'].value()
    print getCurrentFilePath

    testSplit = getCurrentFilePath.split('UE_Ingest/')
    print testSplit

    setT = "T_"
    ueIngest = "UE_Ingest/"
    newName = testSplit[0] + ueIngest + setT + testSplit[1]
    print newName

    filePathSplit = []    
    filePathSplit = newName.split('.png')
    print filePathSplit
    
    udimSplit = []
    udimSplit = filePathSplit[0].split('.')
    print udimSplit

    colorSpaceSplit = udimSplit[0].split('_data')
    print colorSpaceSplit

    combineNumber = colorSpaceSplit[0] + '_' + udimSplit[1] + '_data'
    print combineNumber



    completePath = []
    addTiff = ".tif"
    completePath = combineNumber + addTiff
    print completePath

    writeNode = []
    writeNode = nuke.nodes.Write()
    writeNode['file'].setValue(completePath)
    writeNode['colorspace'].setValue("linear")
    writeNode['file_type'].setValue("tiff")
    writeNode['datatype'].setValue("16bit")

    writeNode.connectInput(1,x)

    nuke.execute(writeNode,1,1)





for i in nuke.selectedNode().knobs():
    print i
