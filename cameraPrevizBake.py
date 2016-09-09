import maya.cmds as cmds
import os


cmds.file(new=True, f=True)

currentShow = 'lovecraft_champions'
currentSeq = 'lcr'
currentShot = 'lcr530'
pathShot = currentShot.upper()

getCamPath = "/next/previs/xjobs/shows/prv_lovecraft/scenes/VFX_SHOTS/%s/cam/" % (pathShot)
getMetaPath = '/next/previs/xjobs/shows/prv_lovecraft/scenes/VFX_SHOTS/%s/.metadata/' % (pathShot)

getCamFile = os.listdir(getCamPath)
getMetaFiles = os.listdir(getMetaPath)

getMetaVers = []

for x in getMetaFiles:
    getIntA = x.split('_v')[1]
    getIntB = getIntA.split('.ma')[0]
    getMetaVers.append(getIntB)

getMax = str(max(getMetaVers))
getMaxMetaFile = []

for x in getMetaFiles:
    if getMax in x:
        getMaxMetaFile.append(x)
        
getCamVers = []
        
for x in getCamFile:
    getIntA = x.split('_v')[1]
    getIntB = getIntA.split('.m')[0]
    getCamVers.append(getIntB)

getMaxCam = str(max(getCamVers))
getMaxCamFile = []

for x in getCamFile:
    if getMaxCam in x:
        getMaxCamFile.append(x)

previzCamPath = "%s%s" % (getCamPath,getMaxCamFile[0])
metaDataFile = '%s%s' % (getMetaPath,getMaxMetaFile[0])

splitA = previzCamPath.split('camExport')[1]
splitB = splitA.split('_')[0]

#def getMetaDataDict(metaDataFile):
fileID = open(metaDataFile, 'r')
datas = fileID.readlines()
fileID.close()    
sceneFile = datas[0].split("Generated From Scene: ")[1]     
metaDataDictString = ""    
for i in range(1, len(datas), 1): metaDataDictString += datas[i].replace("\n", "")   
exec("metaDataDict = %s" %metaDataDictString)    
#return sceneFile, metaDataDict



camDict = metaDataDict['cameras']

for i in range(len(camDict)):
    if camDict[i]['camID'] == splitB:
        gotDict = i

previsCamImport = cmds.file(previzCamPath, i=True)

previzStartFrame = camDict[gotDict]['startFrame']
previzEndFrame = camDict[gotDict]['endFrame']

offset = 1001 - previzStartFrame

shiftStartFrame = previzStartFrame + offset
shiftEndFrame = previzEndFrame + offset

previsCam = cmds.ls("*:*camera")[0]

shotCamPath = '/jobs/lovecraft_champions/assets/cam.shotcam.previz/PRODUCTS/rigs/cam.shotcam.previz/rig/camera/highest/mb/cam.shotcam.previz_rig_camera.mb'
shotCamImport = cmds.file(shotCamPath,r=True, ns='shotcam_previz')

shotCamCamera = cmds.ls("*:*shot_camera")[0]
shotCamTopNode = cmds.ls('shotcam*:*camera')[0]

#save shot cam anim file
cmds.playbackOptions(e=1, min=shiftStartFrame)
cmds.playbackOptions(e=1, ast=shiftStartFrame)
cmds.playbackOptions(e=1, max=shiftEndFrame)
cmds.playbackOptions(e=1, aet=shiftEndFrame)

#shift keys
curvesToShift = cmds.ls(type="animCurve")    
cmds.select(curvesToShift)
cmds.selectKey()
cmds.keyframe(relative=1, timeChange=offset, animation='keys')

#snap previs to shot cam
makeCamConst = cmds.parentConstraint(previsCam, shotCamCamera)
cmds.connectAttr("%s.focalLength" %previsCam, "%s.focalLength" %shotCamTopNode, f=1)
cmds.connectAttr("%s.horizontalFilmAperture" %previsCam, "%s.horizontalFilmAperture" %shotCamTopNode, f=1)
cmds.connectAttr("%s.verticalFilmAperture" %previsCam, "%s.verticalFilmAperture" %shotCamTopNode, f=1)

    
#bake previs cam
bakeAttrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
cmds.bakeResults(shotCamCamera, hi=0, at=bakeAttrs, sac=0, dic=1, s=0, pok=0, sm=1, sb=1, cp=0, t=(shiftStartFrame, shiftEndFrame))
cmds.filterCurve(shotCamCamera)
cmds.delete(shotCamCamera, hierarchy=0, unitlessAnimationCurves=False, staticChannels=1, shape=0, controlPoints=0, cn=1)
bakeAttrsTop = ["focalLength"]
cmds.bakeResults(shotCamTopNode, hi=0, at=bakeAttrsTop, sac=0, dic=1, s=0, pok=0, sm=1, sb=1, cp=0, t=(shiftStartFrame,shiftEndFrame))
cmds.filterCurve(shotCamTopNode)
cmds.delete(shotCamTopNode, hierarchy=0, unitlessAnimationCurves=False, staticChannels=1, shape=0, controlPoints=0, cn=1)

#disconnect attrs from new cam
#cmds.disconnectAttr("%s.focalLength" %previsCam, "%s.focalLength" %shotCamTopNode)
cmds.disconnectAttr("%s.horizontalFilmAperture" %previsCam, "%s.horizontalFilmAperture" %shotCamTopNode)
cmds.disconnectAttr("%s.verticalFilmAperture" %previsCam, "%s.verticalFilmAperture" %shotCamTopNode)
#cmds.delete(makeCamConst[0])


#save shot cam anim file
cmds.playbackOptions(e=1, min=shiftStartFrame)
cmds.playbackOptions(e=1, ast=shiftStartFrame)
cmds.playbackOptions(e=1, max=shiftEndFrame)
cmds.playbackOptions(e=1, aet=shiftEndFrame)



shotFolder = "/jobs/%s/%s/%s/TASKS/layout/maya/scenes" %(currentShow, currentSeq, currentShot)
#print shotFolder
    
if not os.path.isdir(shotFolder):
    #print "no folder"
    #cmd = "mss %s; mkshot -f %s; mss %s/%s:track" %(currentShow, currentShot, currentShow, currentShot)
    cmd = "mss %s/%s; mktask -f %s:layout; mss %s/%s:layout" %(currentShow, currentShot, currentShot, currentShow, currentShot)
    os.system(cmd) 
    
sceneBaseName = "%s_layout_v" %currentShot
count = 1

while os.path.isfile("%s/%s%s.mb" %(shotFolder, sceneBaseName, str(count).zfill(4))): count += 1
    
sceneFileName = "%s/%s%s.mb" %(shotFolder, sceneBaseName, str(count).zfill(4))

    
cmds.select(shotCamTopNode)
    
    
cmds.file(sceneFileName, es=True, pr=True, typ="mayaBinary", f=True)

print ("Exported previs cam file: %s..." %sceneFileName)

cmds.file(new=True, f=True)

shotCamImport = cmds.file(sceneFileName, o=True)

#save shot cam anim file
cmds.playbackOptions(e=1, min=shiftStartFrame)
cmds.playbackOptions(e=1, ast=shiftStartFrame)
cmds.playbackOptions(e=1, max=shiftEndFrame)
cmds.playbackOptions(e=1, aet=shiftEndFrame)
    
