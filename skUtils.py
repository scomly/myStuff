"""
=============================================================================
Copyright (c) 2016, Sean Kealey (skealeye@gmail.com) 
All rights reserved. 

sk_gameUtils
1.5.16
_____________________________________________________________________________
Description: rig and clip export mgmt for gameEngine 
_____________________________________________________________________________
Update history: 

1.1.1 - add global check for ui
1.1.2 - scrollBar for clip ui
1.2.0 - fixed but in get mesh function
1.3.0 - changed root directory 
1.4.0 - adding camera export 
1.5.0 - fixed exporter layout 
1.5.1 - clip creator opens/closes faster
1.5.2 - added namespace function to clip (need export func)
1.5.3 - added backup func added to cam (need to add to assets)
1.6.0 - added ui based asset export
1.7.0 - added archive func to all export types
1.8.0 - added texture packaging 
1.9.0 - added export from namespace fun to anim exporter
1.9.1 - fixed issues with clip saving namespace on edit
1.9.2 - fixed export smoothing on mesh
1.9.3 - auto setup init folder structure 
1.9.4 - added game rig setup ui 
1.9.5 - update to fbx export settings
2.0.0 - added mesh/blendshape export support
2.0.1 - auto gen assets from shotgun and gameelements in asset and clip export 
2.0.2 - added auto seqence detection on new clip 
2.0.3 - added auto char detection on new clip
2.1.0 - added a key reduction filter on redundant keys (anim clips)
2.1.1 - added a key reduction filter on redundant keys (cam)
2.1.2 - run eulerFilter on bakes keys
2.2.0 - str(rendercam) or cam.renderable are now able to be used in cam export
2.2.1 - added a toggle render cam menu option will dynamicly update camera list
2.2.2 - bug fix: disabled spinBox mouse wheel on animClip with clip is not in edit mode
2.2.3 - set anim exported clips to sorted
2.3.0 - added internal and exteral logic for UI settings save on AnimClip Exporter
2.3.1 - combined simple export functions into a class
2.4.0 - converted over to Pyside2 via Qt module
2.4.1 - fixed bug on unicode return from Pyside2 conversion
2.4.2 - added stop button on anim clips
2.4.3 - added functions from skar_importExport (better now at finding skinCluster)
2.5.0 - added options to turn of texture packing on export
2.6.0 - added support for clipTitle export in fbx for Motionbuilder
2.6.1 - fixed bug with fbx setting storing previous clip export take name 
2.7.0 - added hairUtils class
2.7.1 - added psyopMocapTools to classes
2.7.2 - updated fbx default version and removed default take001 from anim export
2.7.3 - bug fix with mesh being deleted on animexport with blenshapes
 
_____________________________________________________________________________
Notes:

_____________________________________________________________________________
TO DO:
-# NEED TO LOOK INTO UPSTEAM NODE ISSUE
-Set Geo Export to only Mesh under GEO 
_____________________________________________________________________________
Example:

import sk_gameUtils as game
reload(game)
game.callWindowAnim()
=============================================================================
"""

import maya.cmds as mc
import maya.mel  as mel
import maya.OpenMayaUI as omui
import sys,os,shutil,json,yaml
#import psyop.env as env
import skar.utilities.sk_objectUtils as util

from operator import itemgetter
from Qt import QtCore, QtGui, QtWidgets
import shiboken2
from   functools     import *

__version__   = '2.7.3'


__root__ = os.path.dirname(os.path.dirname(__file__))


def getCurrentProject():
    '''get list of current active project'''
    #proj = env.get_project_name()
    proj = ''
    return proj

def createFolder(path=''):
    '''createFolder based on path name'''
    if not os.path.exists(path):
        os.makedirs(path)
    return path

class generalUtils(object):

    def removeRedundantKeys(self,selLs=None):
        '''delete reduant keyframes on selected object'''
        if not selLs:
            selLs = mc.ls(sl=True)
        if selLs:
            for i in selLs:
                animCurves = mc.keyframe(i,q=True,n=True)
                if animCurves:
                    for x in animCurves:
                        keyVal  = mc.keyframe(x,q=True,valueChange=True)
                        keyTime = mc.keyframe(x,q=True,timeChange=True)
                        currentVal = keyVal[0]
                        keyIndexRemove = []
                        for i in range(1,len(keyTime)-1,1):
                            val = keyVal[i]
                            if val == currentVal:
                                nextVal = keyVal[i+1]
                                if nextVal == val:
                                    keyIndexRemove.append(keyTime[i])
                            else:
                               currentVal = keyVal[i]
                        if keyIndexRemove:
                            for i in keyIndexRemove:
                                mc.cutKey(x,t=(i,i),clear=True)

    def setUE4_Grid(self):
        '''set maya gradspace to match ue4'''
        mc.grid(s=184,sp=10,d=1)

    def __createDistanceNode(self,n='',pnt1=[],pnt2=[]):
        distGrp = mc.group(n='%s_Dist_Grp'%n,em=True)
        pntA = mc.spaceLocator(n='%s_1_Loc'%n,p=pnt1)[0]
        pntB = mc.spaceLocator(n='%s_2_Loc'%n,p=pnt2)[0]
        dist = mc.createNode('distanceDimShape',n='%s_DistShape'%n)
        distParent = mc.listRelatives(dist,parent=True)[0]
        mc.rename(distParent,dist.replace('Shape',''))

        mc.connectAttr('%s.worldPosition[0]'%pntA,'%s.startPoint'%dist)
        mc.connectAttr('%s.worldPosition[0]'%pntB,'%s.endPoint'%dist)
        mc.parent(pntA,pntB,distParent,distGrp)

    def makeFolder(self,path):
        if not os.path.exists(path):
             os.makedirs(path)

class assetUtils(object):

    def __init__(self,skelMain='game_RIG_Grp',skelMesh='game_GEO_Grp',rootDrive='mover_Ctrl'):
        self.rootDriver = rootDrive
        self.main       = skelMain
        self.mesh       = skelMesh
        self.mainTag    = 'skelJnt'
        self.rootDir    = __root__
        self.animFold   = 'anim'
        self.jobcode    = getCurrentProject()
        self.cacheRoot  = r'%s\%s\production\gameElements'%(self.rootDir,self.jobcode)
        self.gameDir    = r'%s\gameExport'%self.cacheRoot  
        self.camDir     = r'%s\camera'%(self.cacheRoot)
        self.textDir    = r'%s\texture'%(self.cacheRoot)
        self.backup     = "__archive__"

    def __setupDir__(self):
        '''init setup of folder base level folder struct'''
        generalUtils().makeFolder(self.gameDir)
        generalUtils().makeFolder(self.textDir)
        generalUtils().makeFolder(self.camDir)

    def __archiveFile__(self,source=''):
        '''autoBackup of file / source is full path'''
        if os.path.exists(source):
            if '\\' in source:
                source = source.replace('\\','/')
            rootPath = source.strip(source.split('/')[-1])
            fileName = source.split('/')[-1]
            arcPath  = r'%s%s'%(rootPath,self.backup)
            try:
                if not os.path.exists(arcPath):
                    os.makedirs(arcPath)
            except:
                pass

            iter = 1
            extType      = fileName.split('.')[-1]
            baseName     = fileName.split('.')[0]
            archiveName  = '%s_%s.%s'%(baseName,'%02d'%(iter,),extType)
            dest = r'%s/%s'%(arcPath,archiveName)

            while (os.path.exists(dest)):
                iter += 1
                archiveName  = '%s_%s.%s'%(baseName,'%02d'%(iter,),extType)
                dest         = r'%s/%s'%(arcPath,archiveName)
            try:
                shutil.copy(source,dest)
            except:
                pass
            return dest
        else:
            return None
    
    def __frameInfo__(self):
        min = mc.playbackOptions(q=True,min=True)
        max = mc.playbackOptions(q=True,max=True)
        return min,max

    def __bakeJnts(self,rootGrp=None,cleanup=True,fRange=[],keyRed=False):
        '''bake all joints from rootGrp'''
        if not rootGrp:
            rootGrp = self.main
        jntLs = self.__skelLs(rootGrp)
        if jntLs:
            for i in jntLs:
                util.attributeUtil().unlockandHide(i,'translate','rotate','scale')
                util.attributeUtil().keyable(i,'translate','rotate','scale')
            if not fRange:
                fRange = self.__frameInfo__()
            mc.bakeResults(jntLs,t=(fRange[0],fRange[1]),sm=True)
            #euler filter
            mc.filterCurve(jntLs)

            if keyRed:
                mc.delete(jntLs,sc=True,uac=False,s=True,cp=False,hi='none')
                generalUtils().removeRedundantKeys(jntLs)
            if cleanup:
                self.disconnectSkeleton(rootGrp)

    def __bakeBlend(self,rootGrp=None,fRange=[],keyRed=False):
        '''bake all blend attrs from rootGrp'''
        blendLs = []
        bakeLs  = []
        print rootGrp
        skinGeo = self.getSkinLs(rootGrp)
        for i in skinGeo :
            skinShp = mc.listRelatives(i,shapes=True)[0]
            conn =  mc.listConnections(skinShp,s=True,d=False,type='objectSet')
            for x in conn:
                bsConn = mc.listConnections(x,s=True,d=False,type='blendShape')
                if bsConn:
                    if not bsConn in blendLs:
                        blendLs.extend(bsConn)
        for i in blendLs:
           attr = mc.listAttr(i,k=True,m=True,string='weight')
           for x in attr:
            bakeLs.append('%s.%s'%(i,x))
        if not fRange:
            fRange = self.__frameInfo__()
        if bakeLs:
            mc.bakeResults(bakeLs,t=(fRange[0],fRange[1]),sm=True)
            #euler filter
            mc.filterCurve(bakeLs)
            if keyRed:
                mc.delete(bakeLs,sc=True,uac=False,s=True,cp=False,hi='none')
                generalUtils().removeRedundantKeys(bakeLs)
        return skinGeo

    def __skelMainCheck(self):
        '''check for main skelRig grp'''
        if mc.objExists(self.main):
            return True
        else:
            return None

    def __skelLs(self,skelInput= None,fullPath=True):
        '''get list of joints in skelRig'''
        if skelInput: 
            main = skelInput
        else:
            main = self.main
        jntLs = mc.listRelatives(main,ad=True,type='joint',f=fullPath)
        if jntLs:
            return jntLs
        else:
            return None

    
    def __fbxSettingsExport__(self,worldType='z',ver=2018,keyRed=False):
        '''fbx setting for setup export'''
        if keyRed:
            keyRedCond = 'true'
        else:
            keyRedCond = 'false'
        
        settings = [
                    'FBXExportUpAxis %s;'%worldType,
                    'FBXExportFileVersion -v FBX%i00;'%ver,
                    'FBXExportSmoothingGroups -v true;',
                    'FBXExportSmoothMesh -v true;',
                    'FBXExportTangents -v true;',
                    'FBXExportSkins -v true',
                    'FBXExportShapes -v true',
                    'FBXExportEmbeddedTextures -v false',
                    'FBXExportApplyConstantKeyReducer -v %s'%keyRedCond,
                    'FBXExportDeleteOriginalTakeOnSplitAnimation -v true',
                    ''
                    ]
        for i in settings:
            mel.eval(i)


    def removeLayers(self,rootGrp=None):
        ''' remove all objs under root from layers'''
        if rootGrp:
            meshLs = mc.listRelatives(rootGrp,ad=True)
            if meshLs:
                for i in meshLs:
                    conn = mc.listConnections('%s.drawOverride'%i,c=True,p=True)
                    if conn:
                        try:
                            mc.disconnectAttr(conn[1],conn[0])        
                        except:
                            print 'failed: %s'%conn

    def checkPlugin(self,plugType='gameFbxExporter'):
        '''check for plugin (fbxmaya/gameFbxExporter)'''
        isLoaded = mc.pluginInfo(plugType,q=True,loaded=True)
        if not isLoaded:
            try:
                mc.loadPlugin(plugType)
                return True
            except:
                sys.stderr.write('\n%s could not be found\n'%plugType)
                return None
        return True

    def getSkinClusterNode(self,node):
        '''return connected skinCluster from input'''
        shape    = self.getSkinnedShapeNode(node)
        if shape:
            hist = mc.listHistory(node,pdo=True,il=2)
            if hist:
                for i in hist:
                    if mc.objectType(i,isType='skinCluster'):
                        return i
        return None
    
    def getSkinnedShapeNode(self,node):
        ''' return valid shape node from input'''
        shapeLs = []
        if node:
            if mc.objectType(node,isType='transform'):
                shapeLs = mc.listRelatives(node,shapes=True,path=True)
            elif mc.objectType(node) in ['mesh','nurbsSurface','nurbsCurve','subdiv']:
                shapeLs = [node]
            if shapeLs:
                for i in shapeLs:
                    conn = mc.listConnections(i,s=True,d=False,type='skinCluster')
                    if conn:
                        return i
                    else:
                        return shapeLs[0]
        return None  

    def createSkelRig(self,incRoot=True):
        '''create joints for skelRig'''
        sel = mc.ls(sl=True)
        main = self.__skelMainCheck()
        if not main:
            mc.group(n=self.main,em=True)
            if mc.objExists('RIG'):
                mc.parent(self.main,'RIG')
        for i in sel:
            mc.select(clear=True)
            skelJnt = i.replace('Jnt',self.mainTag)
            if not mc.objExists(skelJnt):
                jnt = mc.joint(n=skelJnt)
                temp = mc.parentConstraint(i,jnt,mo=False)
                mc.delete(temp)
                mc.parent(jnt,self.main)
                mc.makeIdentity(jnt,apply=True,t=1,r=1,s=1)
        if incRoot:
            root = 'root_%s'%self.mainTag
            if not mc.objExists(root):
                mc.select(clear=True)
                rootJnt = mc.joint(n=root)            
                mc.parent(rootJnt,self.main)

    def tagGameJnts(self):
        '''tag joints as skelRig'''
        sel = mc.ls(sl=True)
        for i in sel:
            if mc.objectType(i,isType='joint'):
                if i.endswith(self.mainTag):
                    pass
                else:
                    if i.endswith('Jnt'):
                        mc.rename(i,i.replace('Jnt',self.mainTag))
                    else:
                        mc.rename(i,'%s_%s'%(i,self.mainTag))

    def getSkinLs(self,skelInput=None,fullPath=True):
        '''get ls of geo associated with skelRig'''
        meshLs = []
        jntLs  = self.__skelLs(skelInput,fullPath)
        print "########", jntLs, "###########" 
        if jntLs:
            for i in jntLs:
                skin = mc.listConnections(i,s=False,d=True,type='skinCluster')
                print skin
                if skin:
                    for x in skin:
                        meshShp = mc.skinCluster(x,q=True,g=True)
                        if meshShp:
                            if mc.objectType(meshShp,isType='mesh'):
                                mesh = mc.listRelatives(meshShp,parent=True)
                                if mesh:
                                    if not mesh[0] in meshLs:
                                        meshLs.append(mesh[0])
            if meshLs:
                return meshLs
        else:
            return None

    def disconnectSkeleton(self,skelInput=None):
        '''disconnect skelJnts from main rig'''
        if skelInput:
            main = skelInput
        else:
            if self.__skelMainCheck():
                main = self.main
            else:
                return None
        cnstLs = mc.listRelatives(main,ad=True,type='constraint',f=True)
        if cnstLs:
            mc.delete(cnstLs)
        jntLs = self.__skelLs(skelInput=main)
        for i in jntLs:
            dp = mc.listConnections(i,type='dagPose')
            if dp:
                mc.delete(dp)
        rootLs = mc.listRelatives(main,children=True)
        for i in rootLs:
            mc.dagPose(i,bp=True,save=True,n='%s_bindPose'%i) 

    def connectSkeleton(self,skelInput=None,ns=None,fullPath=False,scale=True):
        '''connect skelJnts to main rig'''
        if skelInput:
            main = skelInput
            ns   = '%s:'%ns
        else:
            if self.__skelMainCheck():
                main = self.main
                ns   = ''
            else:
                return None
        self.disconnectSkeleton(skelInput)
        jntLs = self.__skelLs(skelInput,fullPath=fullPath)
        if jntLs:
            for i in jntLs:
                mc.setAttr('%s.segmentScaleCompensate'%i,0)
                prnt = ns + i.replace(self.mainTag,'Jnt')
                if  mc.objExists(prnt):
                    try:
                        mc.parentConstraint(prnt,i,n='%s_PrntCnst'%i,mo=True)
                    except:
                        print prnt
                    if scale:
                        try:
                            mc.scaleConstraint(prnt,i,n='%s_ScaleCnst'%i,mo=False)
                        except:
                            print prnt


                if i == 'root_%s'%self.mainTag:
                    mc.parentConstraint(ns + self.rootDriver,'root_%s'%self.mainTag,
                        n='root_%s_PrntCnst'%self.mainTag,mo=True)
                    mc.scaleConstraint(ns + self.rootDriver,'root_%s'%self.mainTag,
                        n='root_%s_ScaleCnst'%self.mainTag,mo=True)

    def exportSkel(self,name,path):
        '''export skelJnts to fbx'''
        filePath = r'%s/%s.fbx'%(path,name)
        self.checkPlugin('fbxmaya')
        if self.__skelMainCheck():
            jntLs = self.__skelLs()
            if jntLs:
                self.disconnectSkeleton()
                skelPrnt = mc.listRelatives(self.main,parent=True)
                mc.parent(self.main,w=True)
                mc.select(self.main,r=True)
                self.__fbxSettingsExport__()
                #mc.file(filePath,f=True,options='v=0',typ='FBX export',es=True)
                filePath = filePath.replace('\\','/')
                mel.eval('FBXExport -f "%s" -s;'%filePath)
                #revert actions 
                mc.parent(self.main,skelPrnt)
                sys.stderr.write('\nskeleton exported to: %s\n'%filePath)
                return filePath
        return None

    def exportModel(self,name,path,all=False,incTexture=True):
        filePath = r'%s/%s.fbx'%(path,name)
        self.checkPlugin('fbxmaya')
        self.__fbxSettingsExport__()
        meshLs = []
        if all:
            mesh = mc.ls(type='mesh')
            for i in mesh:
                trans=mc.listRelatives(i,parent=True,type='transform')
                if trans:
                    meshLs.extend(trans)
        else:
            mesh = mc.ls(sl=True)
            for i in mesh:
                shape=mc.listRelatives(i,children=True,type='mesh')
                if shape:
                    meshLs.append(i)
        if meshLs:
            meshGrp = self.mesh
            if not mc.objExists(meshGrp):
                meshGrp  = mc.group(n=self.mesh,em=True)
            prntDict = {}
            if incTexture:
                self.exportTexture(name,meshLs,self.textDir)
            for i in meshLs:
                util.attributeUtil().unlockandHide(i,'translate','rotate','scale')
                util.attributeUtil().keyable(i,'translate','rotate','scale')
                prnt = mc.listRelatives(i,parent=True)
                if prnt:
                    prntDict[i] = prnt[0]
                try:
                    mc.parent(i,meshGrp)
                except:
                    pass
            mc.select(meshGrp,r=True)
            #mc.file(filePath,f=True,options='v=0',typ='FBX export',es=True)
            filePath = filePath.replace('\\','/')
            print filePath
            self.__archiveFile__(filePath)
            mel.eval('FBXExport -f "%s" -s;'%filePath)
            #revert actions 
            grpChild = mc.listRelatives(meshGrp,ad=True,type='transform')
            if grpChild:
                for i in grpChild:
                    mc.parent(i,w=True)
            for i in prntDict.keys():
                mc.parent(i,prntDict[i])
            mc.delete(meshGrp)
            sys.stderr.write('\nmesh exported to: %s\n'%filePath)
            return filePath
        return None

    def exportSetup(self,name,path,incTexture=True):
        filePath = r'%s/%s.fbx'%(path,name)
        self.checkPlugin('fbxmaya')
        if self.__skelMainCheck():
            meshLs = self.getSkinLs()
            if meshLs:
                if incTexture:
                    self.exportTexture(name,meshLs,self.textDir)
                prntDict = {}
                for i in meshLs:
                    util.attributeUtil().unlockandHide(i,'translate','rotate','scale')
                    util.attributeUtil().keyable(i,'translate','rotate','scale')
                    prnt = mc.listRelatives(i,parent=True)
                    prntDict[i] = prnt[0]
                jntLs = self.__skelLs()
                if jntLs:
                    self.disconnectSkeleton()
            jntRoots = mc.listRelatives(self.main,children=True)
            exportLs = meshLs + jntRoots
            for i in exportLs:
                mc.parent(i,world=True)
            mc.select(exportLs,r=True)
            self.__fbxSettingsExport__()
            #mc.file(filePath,f=True,options='v=0',typ='FBX export',es=True)
            filePath = filePath.replace('\\','/')
            self.__archiveFile__(filePath)
            mel.eval('FBXExport -f "%s" -s;'%filePath)
            #revert actions
            for i in jntRoots:
                mc.parent(i,self.main)
            for i in prntDict.keys():
                mc.parent(i,prntDict[i])
            self.connectSkeleton()
            sys.stderr.write('\nsetup exported to: %s\n'%filePath)
            return filePath
        return None
      
    def bakeAnim(self,selInput=None,fRange=[],incMesh=True,staticChannel=True,keyRed=False):
        mc.undoInfo(ock=True)
        currentRange = [mc.playbackOptions(q=True,min=True),mc.playbackOptions(q=True,max=True)]
        if not fRange:
            fRange = self.__frameInfo__()
        mc.playbackOptions(minTime=fRange[0],maxTime=fRange[1])
        nsLs      = []
        bakeSetNs = []
        bakeGrpLs = []
        if not selInput:
            selInput = mc.ls(sl=True)
        if not selInput:
            return None
        else:
            for i in selInput:
                if ':' in i:
                    ns = i.split(':')[0]
                    if not ns in nsLs:
                        nsLs.append(ns)
        if nsLs:
            for i in nsLs:
                rigMain = '%s:%s'%(i,self.main)
                if mc.objExists(rigMain):
                    bakeSetNs.append(rigMain)

            for i in bakeSetNs:
                ns = i.split(':')[0]
                bakeGrp = '%s_AnimBakeSet'%ns
                if  mc.objExists(bakeGrp):
                    mc.delete(bakeGrp)
                if mc.objExists('%s:cRoot'%ns):
                    rootNode = '%s:cRoot'%ns
                elif mc.objExists('%s:pRoot'%ns):
                    rootNode = '%s:pRoot'%ns
                elif mc.objExists('%s:pROOT'%ns):
                    rootNode = '%s:pROOT'%ns
                if rootNode:
                    # NEED TO LOOK INTO UPSTEAM NODE ISSUE
                    rootDup = mc.duplicate(rootNode,rr=True,ic=True,n=bakeGrp,un=True)[0]
                  
                    #find/bake skelGrp 
                    trans = mc.listRelatives(rootDup,ad=True,type='transform',f=True)
                    rigGrp = ''
                    for i in trans:
                        if self.main in i:
                            rigGrp = i
                    rootJnts = mc.listRelatives(rigGrp,children=True,f=True,type='joint')
                    self.__bakeJnts(rigGrp,keyRed=keyRed)
                    if not staticChannel:
                        mc.delete(rigGrp,hi='below',sc=True,uac=False)        
                if incMesh:
                    #find/bake skelMesh
                    geoLs = self.__bakeBlend(rigGrp,keyRed=keyRed)
                    mc.parent(geoLs,w=True)
                mc.parent(rootJnts,w=True)
                #cleanup

                bakeChld = mc.listRelatives(bakeGrp,children=True,f=True)
                if incMesh:
                    bakeConnGrp = mc.listRelatives(bakeGrp,ad=True)
                    bakeConn = []
                    for x in bakeConnGrp:
                        conn = mc.listConnections(x)
                        if conn:
                            for xx in conn:
                                bakeConn.append(xx)
                    bakeConn = list(set(bakeConn))

                    keepConn = []
                    for x in geoLs:
                        conn = mc.listHistory(x)
                        if conn:
                            for xx in conn:
                                keepConn.append(xx)
                    keepConn      = list(set(keepConn))
                    removeConnSet = set(bakeConn).difference(keepConn)
                    #TEMP SOLUTION FOR A BUG WHERE MESH IS GETTING DELETED
                    removeList = list(removeConnSet)
                    for item in removeList:
                        if item.endswith('_Geo'):
                            removeList.remove(item)
                    mc.delete(removeList)
     
                mc.delete(bakeChld)
                for x in rootJnts:
                    mc.parent(x.split('|')[-1],bakeGrp)
                if incMesh:
                    #parent geo back into bakeGrp
                    if geoLs:
                        for x in geoLs:
                            mc.parent(x.split('|')[-1],bakeGrp)
                self.removeLayers(bakeGrp)
                bakeGrpLs.append(bakeGrp)
        mc.playbackOptions(minTime=currentRange[0],maxTime=currentRange[1])
        mc.undoInfo(cck=True)
        mc.select(clear=True)

        return bakeGrpLs
                 
    def exportAnim(self,path,name,selInput=None,fRange=[],incMesh=False,keyRed=False,take=None):
        '''export out selected to fbx clips'''
        self.checkPlugin('fbxmaya')
        self.__fbxSettingsExport__(keyRed=keyRed)
        oRange = self.__frameInfo__()
        mc.undoInfo(ock=True)
        if not fRange:
            fRange = self.__frameInfo__()
        if not selInput:
            selInput = mc.ls(sl=True)
        animSets = self.bakeAnim(selInput,fRange,incMesh,keyRed=keyRed)
        
        if len(animSets) > 1:
            clipIter = 1
        else:
            clipIter = ''
        for i in animSets:
            filePath = r'%s/%s%s.fbx'%(path,name,clipIter)
            if incMesh:
                objRoot = mc.listRelatives(i,children=True)
            else:
                objRoot = mc.listRelatives(i,children=True,type='joint')
            if objRoot:
                mc.playbackOptions(min=fRange[0],max=fRange[1])
                mc.parent(objRoot,w=True)
                mc.select(objRoot)
                filePath = filePath.replace('\\','/')
                self.__archiveFile__(filePath)
                mel.eval('FBXExportUseSceneName -v false')
                if take:
                    mel.eval('FBXExportSplitAnimationIntoTakes -c')
                    mel.eval('FBXExportSplitAnimationIntoTakes -v \"%s\" %s %s'%(take,fRange[0],fRange[1]))
                mel.eval('FBXExport -f "%s" -s;'%filePath)
                mc.playbackOptions(min=oRange[0],max=oRange[1])
                mc.delete(objRoot)
            mc.delete(i)
            if clipIter:
                clipIter += 1
        self.__fbxSettingsExport__(keyRed=False)

    def getSkinInf(self,skinClust=''):
        '''get joints bound to a skincluster, on input of geo selection'''
        jntLs = []
        skinLs =[]
        if skinClust:
            skinLs.append(skinClust)
        else:
            sel   = mc.ls(sl=True)
            for i in sel:
                skin = self.getSkinClusterNode(i)
                if skin:
                    skinLs.append(skin)
        for i in skinLs:
            print i
            inf = mc.skinCluster(i, q=1, weightedInfluence=1)
            if not inf in jntLs:
                jntLs.extend(inf)
        return jntLs

    def getSkinCluster(self,objLs=[]):
        '''get skincluster from mesh'''
        skinLs =[]
        if not objLs:
            objLs   = mc.ls(sl=True)
        for i in objLs:
            skin = self.getSkinClusterNode(i)
            if skin:
                skinLs.append(skin)
        return skinLs

    def generateSkelInf(self,skinClust=''):
        '''generate skelJnts based on skinInf'''
        inf = self.getSkinInf(skinClust)
        mc.select(inf,r=True)
        self.createSkelRig()

    def generateSkelInfSelection(self):
        sel = mc.ls(sl=True)
        for i in sel:
            self.generateSkelInf()

    def transferToGameInf(self,objLs=''):
        '''transfer inf to a game JOINT'''
        if not objLs:
            objLs = mc.ls(sl=True)
        if objLs:
            skinLs = self.getSkinCluster(objLs)
            print skinLs
        infLs = []
        sceneJnt = mc.ls(type='joint')
        for i in sceneJnt:
            if i.endswith(self.mainTag):
                pass
            else:
                infLs.append(i)
        if infLs:
            for i in infLs:
                conn = mc.listConnections(i,type='skinCluster',c=True,p=True)
                if conn:
                    gameJnt = i.replace('Jnt',self.mainTag)
                    if mc.objExists(gameJnt):
                        jntConn = conn[::2]
                        skinConn = conn[1::2]
                        for x in range(0,len(jntConn),1):
                            skinClst = skinConn[x].split('.')[0]
                            if skinClst in skinLs:
                                try:
                                    mc.connectAttr(jntConn[x].replace(i,gameJnt),skinConn[x],f=True)
                                except:
                                    pass

    def transferToAnimInf(self,objLs=''):
        '''transfer inf to a Anim JOINT'''
        if not objLs:
            objLs = mc.ls(sl=True)
        if objLs:
            skinLs = self.getSkinCluster(objLs)
        infLs = []
        sceneJnt = mc.ls(type='joint')
        for i in sceneJnt:
            if i.endswith(self.mainTag):
                pass
            else:
                infLs.append(i)
        if infLs:
            for i in infLs:
                conn = mc.listConnections(i,type='skinCluster',c=True,p=True)
                if conn:
                    gameJnt = i.replace(self.mainTag,'Jnt')
                    if mc.objExists(gameJnt):
                        jntConn = conn[::2]
                        skinConn = conn[1::2]
                        for x in range(0,len(jntConn),1):
                            skinClst = skinConn[x].split('.')[0]
                            if skinClst in skinLs:
                                try:
                                    mc.connectAttr(jntConn[x].replace(i,gameJnt),skinConn[x],f=True)
                                except:
                                    pass

    def returnGeoTexture(self,objLs=''):
        '''return path of all valid linked textures'''
        if not objLs:
            sel = mc.ls(sl=True,tr=True)
        else:
            sel = objLs
        texturePath = []
        if sel:
            for i in sel:   
                shd  = mc.listHistory(i,f=True)
                hist = mc.listHistory(shd)
                text = mc.ls(hist,type="file")
                if text:
                    for x in text:
                        texture = mc.getAttr('%s.fileTextureName '%x)
                        texturePath.append(texture)
            texturePath = list(set(texturePath))
            for i in texturePath[:]:
                if not os.path.exists(i):
                    texturePath.remove(i)
        if texturePath:
            return texturePath
        return None

    def exportTexture(self,name,objLs,path):
        '''export texture to path, from obj'''
        if objLs:
            destFolder = r'%s/%s/'%(path,name)
            createFolder(destFolder)
            texturePath = self.returnGeoTexture(objLs)
            if texturePath:
                for x in texturePath:
                    textFile = r'%s/%s'%(destFolder,x.split('/')[-1])
                    self.__archiveFile__(textFile)
                    shutil.copy(x,destFolder)

class prodUtils(assetUtils):

    def __init__(self):
        super(prodUtils, self).__init__()
    
    def charFolders(self,char=None,subFolder=''):
        '''return/create base folder struct'''
        if char:
            charRoot = r'%s\%s'%(self.gameDir,char)
            animRoot = createFolder(r'%s\%s\%s'%(charRoot,self.animFold,subFolder))
            return charRoot,animRoot
        return None

    def camFolders(self):
        '''return/create base folder struct'''
        
        createFolder(self.camDir)
        shotgunDict = self.__getSeqShotDict__()
        for i in shotgunDict.keys():
            if shotgunDict[i]:
                for x in shotgunDict[i]:
                    createFolder(r'%s/%s/%s'%(self.camDir,i,x))
            else:
                createFolder(r'%s/%s'%(self.camDir,i))
        return shotgunDict

    def __getAssetList__(self,fullPath=False,incGameEx=False):
        '''return list of current Shotgun Assets (char,prop,set)'''
        assetRoot     = r'%s/%s/assets/3D'%(self.rootDir,self.jobcode)
        findDir = ['character','prop','set']
        assetList = []
        for i in findDir:
            basePath = r'%s/%s'%(assetRoot,i)
            if os.path.exists(basePath):
                asset = os.listdir(r'%s/%s'%(assetRoot,i))
                if fullPath:
                    for x in asset:
                        assetList.append(r'%s/%s/%s'%(assetRoot,i,x))
                else:
                    assetList.extend(asset)
        if incGameEx:
            gameAsset = os.listdir(self.gameDir)
            if fullPath:
                for i in gameAsset:
                    assetList.append(r'%s/%s'%(self.gameDir,i))
            else:
                assetLower = [x.lower() for x in assetList]
                for i in gameAsset:
                    if not i.lower() in assetLower:
                        assetList.append(i)
            assetList =list(set(assetList))
        assetList = sorted(assetList,key=str.lower)
        return assetList

    def __getSequenceList__(self):
        '''return list of current Shotgun anim shots'''
        return os.listdir(r'%s/%s/sequences'%(self.rootDir,self.jobcode))

    def __getShotList__(self,sequence=None):
        '''return list of current Shotgun anim shots'''
        return os.listdir(r'%s/%s/sequences/%s'%(self.rootDir,self.jobcode,sequence))

    def __getSeqShotDict__(self):
        '''return dictionary of project based sequences/shots'''
        animDict = {}
        for i in self.__getSequenceList__():
            animDict[i] = self.__getShotList__(i)
        return animDict

    def getAssetFromRefSelection(self):
        '''returns asset nice name from a selected ref obj'''
        sel = mc.ls(sl=True)
        if sel:
            if ':' in sel[0]:
                ns = sel[0].split(':')[0]
                refLs = mc.ls('%s*'%ns)
                if refLs:
                    refNode = ''
                    for i in refLs:
                        if mc.objectType(i,isType='reference'):
                            refNode = i
                            break
                    if refNode:
                        refPath = mc.referenceQuery(refNode,filename=True)
                        if refPath:
                            fileName  = refPath.split('/')[-1]
                            assetName = fileName.split('_rig')[0]
                            return assetName
        return None
        
    def exportCharSetup(self,char=None,subName='',incTexture=True):
        '''export charSetup'''
        if char:
            charPath = self.charFolders(char)
            exportName = char
            if subName:
                exportName = '%s_%s'%(char,subName)
            self.exportSetup(exportName,charPath[0],incTexture=incTexture)
    def exportModelSetup(self,char=None,sceneExport=False,incTexture=True):
        if char:
            charPath = self.charFolders(char)
            self.exportModel(char,charPath[0],sceneExport,incTexture=incTexture)

    def exportModelBatch(self,char=None,incTexture=True):
        if char:
            charPath = self.charFolders(char) 
            sel = mc.ls(sl=True)
            for i in sel:
                mc.select(i,r=True)
                self.exportModel(i.replace('_Geo',''),charPath[0],incTexture=incTexture)

    def exportAnimClip(self,char,name,subFolder='',selInput=None,fRange=[],incMesh=False,chrPrfx=True,showDialog=False,keyRed=False):
        '''export animClip'''
        animPath = self.charFolders(char,subFolder)
        if chrPrfx:
            clip = '%s_%s'%(char,name)
            if subFolder:
                clip = '%s_%s'%(clip,subFolder)
        else:
            clip = name
        self.exportAnim(animPath[1],clip,selInput,fRange,incMesh,keyRed=keyRed,take=name)
        print animPath
        if not showDialog:
            try:
                mc.deleteUI('FbxWarningWindow',window=True)
            except:
                pass

    def exportAnimDict(self,char,subFolder='',clipDict={},selInput=None,incMesh=True,charPrefix=True,keyRed=False):
        '''export multi anim clips based on dict data (clipName :[range]'''
        if not selInput:
            selInput = mc.ls(sl=True)
        if not selInput:
            raise RuntimeError,'MUST SELECT AN ASSET TO EXPORT'
        animPath = self.charFolders(char)
        if clipDict:
            for i in clipDict.keys():
                self.exportAnimClip(char,i,subFolder,selInput,clipDict[i],incMesh,charPrefix,keyRed=keyRed)

        sys.stderr.write('\nANIM EXPORT COMPLETE\n')

    def openDir(self,char=None):
        '''open dir of gameRoot or charPath'''
        if char:
            os.startfile(r'%s\%s'%(self.gameDir,char))
        else:
            os.startfile(self.gameDir)

    def returnAssetList(self,log=True):
        '''return asset list of gameRoot'''
        assetLs = os.listdir(self.gameDir)
        if log:
            print assetLs
        return assetLs                                
                        
class cameraUtils(assetUtils):

    def __camFbxSettingsExport__(self,worldType='z',ver=2014):
        '''fbx setting for setup export'''
        settings = [
                    'FBXExportUpAxis %s;'%worldType,
                    'FBXExportFileVersion -v FBX%i00;'%ver,
                    'FBXExportTangents -v true;',
                    'FBXExportCameras -v true;',
                    ]
        for i in settings:
            mel.eval(i)

    def toggleRender(self,bIsRender):
        '''sets renderstate of selected camera'''
        sel = mc.ls(sl=True)
        rtrnLs = []
        for i in sel:
            cam = i
            if not mc.objectType(i,isType='camera'):
                cam = mc.listRelatives(cam,shapes=True)[0]
            if mc.attributeQuery('renderable',n=cam,ex=True):
                mc.setAttr('%s.renderable'%cam,bIsRender)
                rtrnLs.append(cam)
        if rtrnLs:
            sys.stderr.write('\n%s : render status set to %s\n'%(rtrnLs,bool(bIsRender)))
            
    def __getRenderCamScene__(self):
        '''get valid renderCam in scene by name or renderable status'''        
        camLs = mc.ls(type='camera')
        for i in camLs[:]:
            camTrans = mc.listRelatives(i,parent=True)[0]
            if 'renderCam' in camTrans:
                camLs.append(camTrans)
            elif mc.getAttr('%s.renderable'%i) == 1 and i != 'perspShape':
                camLs.append(camTrans)
            camLs.remove(i)
        return camLs
                
    def createExportCamera(self):
        cam = mc.camera(n='exportCam',coi=5,fl=35,lsr=1,cs=1,hfa=1.41732,hfo=0,vfa=.94488,vfo=0,ff='Fill',\
            ovr=1,mb=0,sa=144,ncp=.1,fcp=10000,o=0,ow=30,pze=1,hpn=0,vpn=0,zoom=1)
        return cam

    def bakeCamAnim(self,selInput=None,fRange=[],setYaw=True,keyRed=False):
        if not selInput:
            selInput = mc.ls(sl=True)
            if selInput:
                selInput = selInput[0]
        if not selInput:
            return None

        mc.undoInfo(ock=True)
        currentRange = [mc.playbackOptions(q=True,min=True),mc.playbackOptions(q=True,max=True)]
        if not fRange:
            fRange = self.__frameInfo__()
        mc.playbackOptions(minTime=fRange[0],maxTime=fRange[1])

        #createExport Cam 
        cam = self.createExportCamera()
        mc.setAttr('%s.rotateOrder'%cam[0],1)

        #connectCam
        print selInput
        tempConstraint = mc.parentConstraint(selInput,cam[0],mo=False)

        #set Yaw difference for UE4
        if setYaw:
            mc.setAttr('%s.target[0].targetOffsetRotateY'%tempConstraint[0],90)

        mc.setAttr('%s.rotateOrder'%cam[0],0)
        
        selInputShp = mc.listRelatives(selInput)
        if selInputShp:
            if mc.objectType(selInputShp[0],isType='camera'):
                 #Connect Supported Shape Attrs
                 mc.connectAttr('%s.focalLength'%selInputShp[0],'%s.focalLength'%cam[1])
                 mc.connectAttr('%s.hfa'%selInputShp[0],'%s.hfa'%cam[1])
                 mc.connectAttr('%s.vfa'%selInputShp[0],'%s.vfa'%cam[1])
                 mc.connectAttr('%s.lsr'%selInputShp[0],'%s.lsr'%cam[1])
                 mc.connectAttr('%s.fStop'%selInputShp[0],'%s.fStop'%cam[1])
                 mc.connectAttr('%s.sa'%selInputShp[0],'%s.sa'%cam[1])
                 mc.connectAttr('%s.coi'%selInputShp[0],'%s.coi'%cam[1])
                 mc.connectAttr('%s.focusDistance'%selInputShp[0],'%s.focusDistance'%cam[1])

        #bake anim 
        mc.bakeResults(cam,t=(fRange[0],fRange[1]),sm=True)
        if keyRed:
            mc.delete(cam,sc=True,uac=False,s=True,cp=False,hi='none')
            generalUtils().removeRedundantKeys(cam)

        #cleanUp exportCam
        mc.delete(tempConstraint)

        mc.playbackOptions(minTime=currentRange[0],maxTime=currentRange[1])
        mc.undoInfo(cck=True)
        mc.select(clear=True)

        return cam

    def exportCamAnim(self,path=None,name=None,selInput=None,fRange=[],setYaw=True,keyRed=False):
        '''export out selected to fbx clips'''
        filePath = r'%s/%s.fbx'%(path,name)

        self.__archiveFile__(filePath)

        self.checkPlugin('fbxmaya')
        #self.__camFbxSettingsExport__()
        oRange = self.__frameInfo__()
        mc.undoInfo(ock=True)
        if not fRange:
            fRange = self.__frameInfo__()
        if not selInput:
            selInput = mc.ls(sl=True)
            if selInput:
                selInput = selInput[0]
        if not selInput:
            return None
        
        cam = self.bakeCamAnim(selInput,fRange,setYaw,keyRed=keyRed)
        mc.select(cam,r=True)
        filePath = filePath.replace('\\','/')
        mel.eval('FBXExport -f "%s" -s;'%filePath)
        mc.playbackOptions(min=oRange[0],max=oRange[1])
        mc.delete(cam)

class physxUtils(assetUtils):

    def stripRig(self):
        '''prep for cloth rig'''
        self.disconnectSkeleton()

        if mc.objExists('CTRL'):
            mc.delete('CTRL')

        if mc.objExists('NO_TOUCH'):
            mc.delete('NO_TOUCH')

        if mc.objExists('mocap_RIG_Grp'):
            mc.delete('mocap_RIG_Grp')

        if mc.objExists('anim_RIG_Grp'):
            mc.delete('anim_RIG_Grp')

        if mc.objExists('game_RIG_Grp'):
            mc.setAttr('%s.v'%'game_RIG_Grp',1)

    def getCollisionCapsules(self,details=True):
        '''get list or details dict of all physx capsules'''
        capLs = mc.ls(type='physicsShape')
        if not details:
            return capLs
        else:
            capDict = {}
            for i in capLs:
                capDict[i] = {}
                shapeType = mc.getAttr('%s.shapeType'%i)
                size = mc.getAttr('%s.size'%i)
                radius = mc.getAttr('%s.radius'%i)
                height = mc.getAttr('%s.height'%i)
                fit = mc.getAttr('%s.bestFit'%i)

                transObj  = mc.listRelatives(i,parent=True)[0]
                translate = mc.getAttr('%s.translate'%transObj)
                rotate    = mc.getAttr('%s.rotate'%transObj)
                scale     = mc.getAttr('%s.scale'%transObj)

                capDict[i].update({'shapeType':shapeType})
                capDict[i].update({'size':size}) 
                capDict[i].update({'radius':radius}) 
                capDict[i].update({'height':height})
                capDict[i].update({'bestFit':fit})

                capDict[i].update({'transform':transObj})
                capDict[i].update({'translate':translate})
                capDict[i].update({'rotate':rotate})
                capDict[i].update({'scale':scale})

            return capDict


    def mirrorRagDoll(self,direction=1):
        '''mirror collision capsules, direction 1 == LF_RT, direction -1 == RT_LF'''
        capDict = self.getCollisionCapsules(True)
        if capDict:
            sideDict = {}
            if direction == 1:
                prntDir = 'Lf_'
                mirDir  = 'Rt_'
            else:
                prntDir = 'Rt_'
                mirDir  = 'Lf_'
            
            for i in capDict.keys():
                if i.startswith(prntDir):
                    sideDict[i] = capDict[i]
            if sideDict:
                for i in sideDict.keys():
                    mirCap = i.replace(prntDir,mirDir)
                    if mc.objExists(mirCap):
                     
                        mc.setAttr('%s.bestFit'%mirCap,capDict[i]['bestFit'])
                        mc.setAttr('%s.shapeType'%mirCap,capDict[i]['shapeType'])
                        mc.setAttr('%s.sizeX'%mirCap,capDict[i]['size'][0][0])
                        mc.setAttr('%s.sizeY'%mirCap,capDict[i]['size'][0][1])
                        mc.setAttr('%s.sizeZ'%mirCap,capDict[i]['size'][0][2])
                        mc.setAttr('%s.radius'%mirCap,capDict[i]['radius'])
                        mc.setAttr('%s.height'%mirCap,capDict[i]['height'])

                        mc.setAttr('%s.translateX'%capDict[mirCap]['transform'],(capDict[i]['translate'][0][0])*-1)
                        mc.setAttr('%s.translateY'%capDict[mirCap]['transform'],(capDict[i]['translate'][0][1])*-1)
                        mc.setAttr('%s.translateZ'%capDict[mirCap]['transform'],(capDict[i]['translate'][0][2])*-1)
                        mc.setAttr('%s.scaleX'%capDict[mirCap]['transform'],capDict[i]['scale'][0][0])
                        mc.setAttr('%s.scaleY'%capDict[mirCap]['transform'],capDict[i]['scale'][0][1]) 
                        mc.setAttr('%s.scaleZ'%capDict[mirCap]['transform'],capDict[i]['scale'][0][2])
                        mc.setAttr('%s.rotateX'%capDict[mirCap]['transform'],capDict[i]['rotate'][0][0])
                        mc.setAttr('%s.rotateY'%capDict[mirCap]['transform'],capDict[i]['rotate'][0][1]) 
                        mc.setAttr('%s.rotateZ'%capDict[mirCap]['transform'],capDict[i]['rotate'][0][2])        

class hairUtils(assetUtils):
    
    def seperateCurves(self,inputCurve,outputName):
        shp = mc.listRelatives(inputCurve,shapes=True)
        curveList = []
        for x, i in enumerate(shp):
            trans = mc.createNode('transform',n='%s_%i_Crv'%(outputName,x))
            mc.parent(i,trans,shape=True,r=True)
            curveList.append(trans)
        return curveList

    # NEED TO CLEANUP, CODE CURVE CREATION, USE:SELECT VTX
    def generateGuidesOnVtx(self,inputGeo=''):
        sel = mc.ls(sl=True,fl=True)
        crv = 'Test'
        geo = sel[0].split('.vtx[')[0]

        for i in sel:
            base = mc.duplicate(crv)[0]
            pos = mc.xform(i,q=True,ws=True,t=True)
            mc.xform(base,ws=True,t=pos)
            temp = mc.normalConstraint(geo,base,wut='scene')
            mc.delete(temp)

class mocapUtils(object):

    def __init__(self):
        pass

    def _getPoseInfo(self):
        infoDict =  {}
        rootBone = 'root_skelJnt'
        skelHi   = mc.listRelatives(rootBone,c=True,ad=True)
        skelHi.append(rootBone)
        for i in skelHi:
            infoDict[i] = {'translate':[],'rotate':[],'scale':[]}
            for attr in ['translate','rotate','scale']:
                attrLs  = []
                conn    = mc.listConnections('%s.%s'%(i,attr),s=True,d=False)
                if conn:
                    infoDict[i][attr] =  3*['NULL']
                else:
                    for vec in ['X','Y','Z']:
                        conn = mc.listConnections('%s.%s%s'%(i,attr,vec),s=True,d=False)
                        if not conn:
                            attrLs.append(mc.getAttr('%s.%s%s'%(i,attr,vec)))
                        else:
                            attrLs.append('NULL')
                    infoDict[i][attr] =  attrLs 
        return infoDict

    def _writePoseToFile(self,charName,path,info):
        poseInfo = {'character':charName,'data':info}
        poseFilePath = r'{0}/{1}.pose'.format(path,charName)
        with open(poseFilePath, 'w') as json_file:
            json.dump(poseInfo,json_file)

    def _readPoseFromFile(self,file):
        with open(file) as f:
            data = json.load(f)
            return data
        return None

    def setBindPose(self,file,namespace=None):
        if file.endswith('.pose'):
            pose = self._readPoseFromFile(file)
            mc.currentTime(-1,edit=True)
            if pose:
                for i in pose['data'].keys():
                    if namespace:
                        obj = '%s%s'%(namespace,i)
                    else:
                        obj = i
                    for attr in ['translate','rotate','scale']:
                        for index, vec in enumerate(['X','Y','Z']):
                            if  not pose['data'][i][attr][index] == 'NULL':
                                try:
                                    mc.setAttr('%s.%s%s'%(obj,attr,vec),pose['data'][i][attr][index])
                                    mc.setKeyframe('%s.%s%s'%(obj,attr,vec))
                                except:
                                    pass
            return pose

    def setBindPoseAuto(self,namespace=None):
        poseFile = os.path.join(__root__,'production\gameElements\gameExport\partyKing\data\partyKing.pose') 
        self.setBindPose(poseFile,namespace)

    def __returnMocapPartner(self,mocapJoint):

        #ROOT DEF 
        if mocapJoint == "root_skelJnt":
            return {'placer_Ctrl': ['translate','rotate']}

        #SPINE DEF 
        if mocapJoint == "spine_hip_skelJnt":
            return {'cog_Ctrl': ['translate','rotate']}

        if mocapJoint == "spine_2_twist_skelJnt":
            return {'fk_2_Ctrl': ['rotate']}

        #NECK DEF
        if mocapJoint == "neck_root_skelJnt":
            return {'lowerNeck_Ctrl': ['rotate']}

        if mocapJoint == "neck_end_skelJnt":
            return {'upperNeck_Ctrl': ['rotate']}

        #CLAV DEF
        if mocapJoint == "Lf_clavicle_base_skelJnt":
            return {'Lf_clavicleMaster_Ctrl': ['rotate']}

        if mocapJoint == "Rt_clavicle_base_skelJnt":
            return {'Rt_clavicleMaster_Ctrl': ['rotate']}

        #ARM DEF
        if mocapJoint == "Lf_armUpper_skelJnt":
            return {'Lf_armFk_1_Ctrl':['rotate'], 'Lf_armPole_Ctrl':['translate','rotate']}

        if mocapJoint == "Lf_armBendElbow_skelJnt":
            return {'Lf_armFk_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_root_skelJnt":
            return {'Lf_armFk_3_Ctrl': ['rotate'],'Lf_armIk_Ctrl': ['translate','rotate']}

        if mocapJoint == "Rt_armUpper_skelJnt":
            return {'Rt_armFk_1_Ctrl':['rotate'],'Rt_armPole_Ctrl':['translate','rotate']}

        if mocapJoint == "Rt_armBendElbow_skelJnt":
            return {'Rt_armFk_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_root_skelJnt":
            return {'Rt_armFk_3_Ctrl': ['rotate'],'Rt_armIk_Ctrl': ['translate','rotate']}

        #LEG DEF
        if mocapJoint == "Lf_legUpper_skelJnt":
            return {'Lf_legFk_1_Ctrl': ['rotate'], 'Lf_legPole_Ctrl':['translate','rotate']}

        if mocapJoint == "Lf_legBendKnee_skelJnt":
            return {'Lf_legFk_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_ankleGimbal_skelJnt":
            return {'Lf_legFk_3_Ctrl': ['rotate'],'Lf_legIk_Ctrl': ['translate','rotate']}

        if mocapJoint == "Lf_footBnd_1_skelJnt":
            return {'Lf_legFk_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_legUpper_skelJnt":
            return {'Rt_legFk_1_Ctrl': ['rotate'], 'Rt_legPole_Ctrl':['translate','rotate']}

        if mocapJoint == "Rt_legBendKnee_skelJnt":
            return {'Rt_legFk_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_ankleGimbal_skelJnt":
            return {'Rt_legFk_3_Ctrl': ['rotate'],'Rt_legIk_Ctrl': ['translate','rotate']}

        if mocapJoint == "Rt_footBnd_1_skelJnt":
            return {'Rt_legFk_4_Ctrl': ['rotate']}

        #HAND DEF
        if mocapJoint == "Lf_finger_pinky_1_skelJnt":
            return {'Lf_pinky_1_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_pinky_2_skelJnt":
            return {'Lf_pinky_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_pinky_3_skelJnt":
            return {'Lf_pinky_3_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_pinky_4_skelJnt":
            return {'Lf_pinky_4_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_ring_1_skelJnt":
            return {'Lf_ring_1_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_ring_2_skelJnt":
            return {'Lf_ring_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_ring_3_skelJnt":
            return {'Lf_ring_3_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_ring_4_skelJnt":
            return {'Lf_ring_4_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_middle_1_skelJnt":
            return {'Lf_middle_1_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_middle_2_skelJnt":
            return {'Lf_middle_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_middle_3_skelJnt":
            return {'Lf_middle_3_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_middle_4_skelJnt":
            return {'Lf_middle_4_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_index_1_skelJnt":
            return {'Lf_index_1_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_index_2_skelJnt":
            return {'Lf_index_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_index_3_skelJnt":
            return {'Lf_index_3_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_index_4_skelJnt":
            return {'Lf_index_4_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_thumb_1_skelJnt":
            return {'Lf_thumb_1_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_thumb_2_skelJnt":
            return {'Lf_thumb_2_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_thumb_3_skelJnt":
            return {'Lf_thumb_3_Ctrl': ['rotate']}

        if mocapJoint == "Lf_finger_thumb_4_skelJnt":
            return {'Lf_thumb_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_pinky_1_skelJnt":
            return {'Rt_pinky_1_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_pinky_2_skelJnt":
            return {'Rt_pinky_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_pinky_3_skelJnt":
            return {'Rt_pinky_3_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_pinky_4_skelJnt":
            return {'Rt_pinky_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_ring_1_skelJnt":
            return {'Rt_ring_1_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_ring_2_skelJnt":
            return {'Rt_ring_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_ring_3_skelJnt":
            return {'Rt_ring_3_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_ring_4_skelJnt":
            return {'Rt_ring_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_middle_1_skelJnt":
            return {'Rt_middle_1_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_middle_2_skelJnt":
            return {'Rt_middle_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_middle_3_skelJnt":
            return {'Rt_middle_3_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_middle_4_skelJnt":
            return {'Rt_middle_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_index_1_skelJnt":
            return {'Rt_index_1_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_index_2_skelJnt":
            return {'Rt_index_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_index_3_skelJnt":
            return {'Rt_index_3_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_index_4_skelJnt":
            return {'Rt_index_4_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_thumb_1_skelJnt":
            return {'Rt_thumb_1_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_thumb_2_skelJnt":
            return {'Rt_thumb_2_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_thumb_3_skelJnt":
            return {'Rt_thumb_3_Ctrl': ['rotate']}

        if mocapJoint == "Rt_finger_thumb_4_skelJnt":
            return {'Rt_thumb_4_Ctrl': ['rotate']}

        #FACE DEF
        if mocapJoint == "Lf_eye_skelJnt":
            return {'Lf_eyeFk_Ctrl': ['rotate']}

        if mocapJoint == "Lf_eyeLowerLid_skelJnt":
            return {'Lf_lowerLidFk_Ctrl': ['rotate']}

        if mocapJoint == "Lf_eyeUpperLid_skelJnt":
            return {'Lf_upperLidFk_Ctrl': ['rotate']}

        if mocapJoint == "Rt_eye_skelJnt":
            return {'Rt_eyeFk_Ctrl': ['rotate']}

        if mocapJoint == "Rt_eyeLowerLid_skelJnt":
            return {'Rt_lowerLidFk_Ctrl': ['rotate']}

        if mocapJoint == "Rt_eyeUpperLid_skelJnt":
            return {'Rt_upperLidFk_Ctrl': ['rotate']}

        if mocapJoint == "jaw_skelJnt":
            return {'jawMain_Ctrl': ['rotate']}

        else:
            return None

    def constrainMocap(self,mocapPrefix=None,namespace=None):
        rootBone = '%sroot_skelJnt'%mocapPrefix 
        skelHi   = mc.listRelatives(rootBone,c=True,ad=True)
        skelHi.append(rootBone)
        for i in skelHi:
            boneInfo = i
            if mocapPrefix:
                boneInfo = i.split(mocapPrefix)[-1]
            info = self.__returnMocapPartner(boneInfo)
            if not info:
                print 'def not found :%s'%boneInfo
            else:
                for ctrl in info.keys():
                    if namespace:
                        childObj = '%s:%s'%(namespace,ctrl)
                    else:
                        childObj = ctrl
                    if 'rotate' and 'translate' in info[ctrl]:
                        mc.parentConstraint(i,childObj,mo=True)
                    elif 'rotate' in info[ctrl]:
                        #eyelid exception
                        if 'LidFk_Ctrl' in childObj:
                            mc.parentConstraint(i,childObj,mo=True,st=('x','y','z'),sr=('y'))
                        else:
                            mc.parentConstraint(i,childObj,mo=True,st=('x','y','z'))
                    elif 'translate' in info[ctrl]:
                        mc.parentConstraint(i,childObj,mo=True,sr=('x','y','z'))

            #Toe connection
            if 'footBnd_1_skelJnt' in i:
                side = boneInfo.split('_')[0]
                driven = '%s_legIk_Ctrl'%side
                if namespace:
                    driven = '%s:%s'%(namespace,driven)
                mc.connectAttr('%s.rotateX'%i,'%s.Toe_Rotate'%driven)



####################
#######**UI**#######
####################

class uiInfo(prodUtils):
    '''ui/pyside utils'''

    def __init__(self):
        super(uiInfo, self).__init__()
        
        self.gameInfo   = 'gameInfo'
        self.clipActive = 'clipCbInfo'
        self.clipCt     = 'clipAnimInfo' #internal attr catagory
        self.clipName   = 'clipAnim' 

    def _nodeLock(self,node='',lock=True):
        if mc.objExists(node):
            mc.lockNode(node,l=lock)

    def _attrLock(self,node='',attr='',lock=True):
        if mc.objExists(node):
            if mc.attributeQuery(attr,n=node,ex=True):
                lockState = mc.lockNode(node,q=True,l=True)[0]
                self._nodeLock(node,False)
                mc.setAttr('%s.%s'%(node,attr),l=lock)
                self._nodeLock(node,lockState)

    def __clipDict(self,char='',sub='',clip='',inf=0,outf=0,namespace=''):
        clipDict ={'CHAR':char,'SUB':sub,'EXPORT':{clip:[inf,outf]},'NS':namespace}
        return clipDict

    def getSceneCamera(self,shortName=False):
        '''get list of renerCam in scene'''
        cam = cameraUtils().__getRenderCamScene__()
        if shortName:
            for i in cam[:]:
                if ':' in i:
                    cam.append(i.split(':')[0])
                    cam.remove(i)
        return cam

    def getSelNamespace(self):
        '''get the nice namespace of the selected asset'''
        sel = mc.ls(sl=True)
        if sel:
            asset = mc.ls(sl=True)[0]
            if ":" in asset:
                return asset.split(':')[0]
            else:
                return None

    def getCameraShotgunInfo(self):
        folderInfo = self.camFolders()
        return folderInfo

    def getAssetShotgunInfo(self):
        '''return asset list from shotgun'''
        assetInfo = self.__getAssetList__()
        return assetInfo

    def getAssetInfo(self):
        '''return returnAssetList from shotgun and gameElements'''
        assetInfo = self.__getAssetList__(incGameEx=True)
        return assetInfo

    def listAssets(self):
        ''' list of gameExport Assets'''
        path = self.gameDir
        cont = os.listdir(path)
        cont.sort()
        for i in cont:
            if i.startswith('_'):
                cont.remove(i)
        return cont

    def listAnimSequences(self,character):
        '''list anim sequences of form a given asset'''
        try:
            animSeq = os.listdir(r'%s/%s/%s'%(self.gameDir,character,self.animFold))
            if animSeq:
                animSeq = sorted(animSeq,key=str.lower)
                return animSeq
        except:
            pass
            return None

    def listSequences(self):
        '''list gameElements camera sequences'''
        path = self.camDir
        cont = os.listdir(path)
        cont.sort()
        return cont

    def listShots(self,sequence):
        '''list gameElements camera shots'''
        path = r'%s/%s'%(self.camDir,sequence)
        try:
            cont = os.listdir(path)
            cont.sort()
            return cont
        except:
            return None

    def getGameInfo(self):
        '''get current gameInfo node / or create new'''
        gameNetwork = mc.ls(type='network')
        if gameNetwork:
            for i in gameNetwork:
                if i == self.gameInfo:
                    gameNetwork = i
                    break
                else:
                    gameNetwork = None
        if not gameNetwork:
            gameNetwork = mc.createNode('network',n=self.gameInfo)
            mc.addAttr(gameNetwork,ln='ExportPath',dt='string')
            mc.setAttr('%s.ExportPath'%(gameNetwork),self.gameDir,type='string',l=True)
            mc.addAttr(gameNetwork,ln=self.clipActive,dt='string')
            mc.setAttr('%s.%s'%(gameNetwork,self.clipActive),l=True)
        self._nodeLock(gameNetwork,True)
        return gameNetwork

    def getClipAttrLs(self,bIsSorted=True):
        '''return a list of all clipNames'''
        gameNode  = self.getGameInfo()
        clipLs    = []
        internal  = mc.attributeInfo(gameNode,i=False)
        for i in internal:
            ct = mc.attributeQuery(i,n=gameNode,ct=True)
            if ct:
                if ct[0] == self.clipCt:
                    clipLs.append(i)

        if bIsSorted:
            dictLs = []
            for i in clipLs:
                attr = eval(mc.getAttr('%s.%s'%(gameNode,i)))
                attr['clipIndex']=i
                dictLs.append(attr)

            sortedDict = sorted(dictLs, key=itemgetter('CHAR'))
            clipLs = []
            for i in sortedDict:
                clipLs.append(i['clipIndex'])

        return clipLs

    def getClipAttr(self,clipName):
        '''return dict info back into a readable form'''
        gameNode = self.getGameInfo()
        if mc.attributeQuery(clipName,n=gameNode,ex=True):
            attrInfo = eval(mc.getAttr('%s.%s'%(gameNode,clipName)))
            char     = attrInfo['CHAR']
            sub      = attrInfo['SUB']
            animDict = attrInfo['EXPORT']
            
            #FAILSAFE FOR OLD CLIPS WITHOUT 'NS' OPTION
            if 'NS' in attrInfo.keys():
                ns = attrInfo['NS']
            else:
                ns = ''

            return char,sub,animDict,ns 
        else:
            return None


    def addGameInfo(self,char='',sub='',clip='',inf=0,outf=0,namespace=''):
        '''add clip attr info into a single dict'''
        gameNode = self.getGameInfo()
        clipLs   = self.getClipAttrLs()
        iter = 1
        clipName = self.clipName + str(iter) 
        while True:
            if clipName in clipLs:
                iter +=1
                clipName = self.clipName + str(iter)
            else:
                break
        clipDict = self.__clipDict(char,sub,clip,inf,outf,namespace)
        self._nodeLock(gameNode,False)
        mc.addAttr(gameNode,ln=clipName,dt='string',ct=self.clipCt)
        mc.setAttr('%s.%s'%(gameNode,clipName),clipDict,type='string',l=True)
        self._nodeLock(gameNode,True)
        return clipName

    def editClipAttr(self,clipName,char='',sub='',clip='',inf=0,outf=0,ns=''):
        '''change info in exsisting clipName'''
        gameNode = self.getGameInfo()
        if mc.attributeQuery(clipName,n=gameNode,ex=True):
            self._nodeLock(gameNode,False)
            self._attrLock(gameNode,clipName,False)
            clipDict = self.__clipDict(char,sub,clip,inf,outf,ns)
            mc.setAttr('%s.%s'%(gameNode,clipName),clipDict,type='string',l=True)
            self._nodeLock(gameNode,True)
            clipInfo = self.getClipAttr(clipName)
            return clipInfo
        return None

    def deleteClipAttr(self,clipName):
        '''remove clip from gameInfo'''
        gameNode = self.getGameInfo()
        if mc.attributeQuery(clipName,n=gameNode,ex=True):
            self._nodeLock(gameNode,False)
            self._attrLock(gameNode,clipName,False)
            mc.deleteAttr(gameNode,at=clipName)
            self._nodeLock(gameNode,True)

    def getMayaWindow(self):
        #get maya MainWindow Pointer

        # win = QtWidgets.qApp.topLevelWidgets()
        # mw = None
        # for i in win:
            
        #     if i.objectName() == 'MayaWindow':
        #         mw = i
        #         break


        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            return shiboken2.wrapInstance(long(ptr),QtWidgets.QWidget)
        return None

    def removeWindow(self,windowName):
      #remove a maya ui
      if mc.window(windowName,q=True,ex=True):
          mc.deleteUI(windowName)

class gameRigToolsUi(QtWidgets.QMainWindow):
    '''gameRig ui'''
    def __init__(self,parent=uiInfo().getMayaWindow(),
        width=None,height=None,dev=False):
        QtWidgets.QMainWindow.__init__(self,parent)
        # init window settings
        self.__version__ = __version__
        self.windowName = 'gameRig %s'%__version__
        uiInfo().removeWindow(self.windowName)

        if width:
          self.windowWidth = width
        else:
          self.windowWidth  = 200
        if height:
          self.windowHeight = height
        else:
          self.windowHeight = 150

        self.setWindowTitle(self.windowName)
        self.setObjectName (self.windowName)
        self.setGeometry(300,300,200,150)
        self.resize(self.windowWidth,self.windowHeight)
        main = self.mainLayout(dev)
        self.setCentralWidget(main)

        self.setMinimumWidth(self.windowWidth)
        self.setMaximumWidth(self.windowWidth)
        self.setMinimumHeight(self.windowHeight)
        self.setMaximumHeight(self.windowHeight)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def mainLayout(self,dev):
        main = QtWidgets.QWidget(self)
        #construct layouts
        self.mainLay = QtWidgets.QVBoxLayout(main)

        clipMain = self.mainTools()
    
        #add layouts to main 
        self.mainLay.addWidget(clipMain)
  
        return main

    def mainTools(self):
        '''mainTool layout '''
        hBoxLayWid   = QtWidgets.QWidget() 
        hBoxLayTitle = QtWidgets.QGridLayout(hBoxLayWid)
        hBoxLayTitle.setObjectName('gameTools')


        genButton  = QtWidgets.QPushButton("Gen SkelJnt")
        tagButton  = QtWidgets.QPushButton("Tag SkelJnt")
        conButton  = QtWidgets.QPushButton("Attach Rig ")
        disButton  = QtWidgets.QPushButton("Detach Rig ")
        trGmButton = QtWidgets.QPushButton("Trans2Game")
        trAnButton = QtWidgets.QPushButton("Trans2Anim")

        buttonLs = [genButton,tagButton,conButton,disButton,trGmButton,trAnButton]
        x = 0
        for i in buttonLs:
            if x%2==0:
                i.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
                 #4D9A63;font-weight: bold")
            else:
                i.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
                 #d6713b;font-weight: bold")
            x +=1

        hBoxLayTitle.addWidget(genButton,0,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(tagButton,0,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(conButton,1,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(disButton,1,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(trGmButton,2,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(trAnButton,2,1,QtCore.Qt.AlignLeft)


        genButton.clicked.connect(lambda:assetUtils().generateSkelInf())
        tagButton.clicked.connect(lambda:assetUtils().tagGameJnts())
        conButton.clicked.connect(lambda:assetUtils().connectSkeleton())
        disButton.clicked.connect(lambda:assetUtils().disconnectSkeleton())
        trGmButton.clicked.connect(lambda:assetUtils().transferToGameInf())
        trAnButton.clicked.connect(lambda:assetUtils().transferToAnimInf())

        return hBoxLayWid

class gameFbxExporterAnimUi(QtWidgets.QMainWindow):
    '''gameFbx ui'''
    def __init__(self,parent=uiInfo().getMayaWindow(),
        width=None,height=None,dev=False):
        QtWidgets.QMainWindow.__init__(self,parent)
        # init window settings
        self.__version__ = __version__
        self.windowName = 'sk_gameFbxExporter %s'%__version__
        uiInfo().removeWindow(self.windowName)

        self.settings_path = os.path.join(os.getenv('HOME'), "settingsFile.ini")

        if width:
          self.windowWidth = width
        else:
          self.windowWidth  = 700
        if height:
          self.windowHeight = height
        else:
          self.windowHeight = 500

        self.setWindowTitle(self.windowName)
        self.setObjectName (self.windowName)
        self.setGeometry(300,300,200,150)
        self.resize(self.windowWidth,self.windowHeight)
        main = self.mainLayout(dev)
        self.setCentralWidget(main)

        self.setMinimumWidth(self.windowWidth)
        self.setMaximumWidth(self.windowWidth)
        self.setMinimumHeight(self.windowHeight)
        self.setMaximumHeight(self.windowHeight*5)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.__menuBar(self)

        # Restore UI Settings
        self.__loadClipCb_Info()
        if os.path.exists(self.settings_path):
            settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
            self.restoreGeometry(settings_obj.value("windowGeometry"))
            for i in ['check_ns','check_mesh','check_keyFilt']:
                cb = self.findChild(QtWidgets.QCheckBox,i)
                
                #pyside2 now returns a bool instead of unicode so checking for either case 
                val = str(settings_obj.value(i))
                if val == 'false' or val == 'False':
                    val = 0
                else:
                    val = 1  
                cb.setChecked(val)

                
    def closeEvent(self,event):
        # Save window's geometry
        settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        settings_obj.setValue("windowGeometry", self.saveGeometry())

        # Save checkbox settings
        for i in ['check_ns','check_mesh','check_keyFilt']:
            cb = self.findChild(QtWidgets.QCheckBox,i)
            settings_obj.setValue(i, cb.isChecked())
        self.__saveClipCB_Info()

        
    
    def mainLayout(self,dev):
        main = QtWidgets.QWidget(self)
        #construct layouts
        self.mainLay = QtWidgets.QVBoxLayout(main)

        clipMain       = self.clipMainLayout()
        clipMainScroll = QtWidgets.QScrollArea()
        clipMainScroll.setWidget(clipMain)
        clipMainScroll.setWidgetResizable(True)

        clipTitle      = self.clipTitleLayout(main)
    
        #add layouts to main 
        self.mainLay.addWidget(clipTitle)
        self.mainLay.addWidget(clipMainScroll)

        return main

    def clipMainLayout(self):
        '''generate a layout based on gameInfo'''
        hBoxLayWid   = QtWidgets.QWidget() 
        hBoxLayTitle = QtWidgets.QGridLayout(hBoxLayWid)
        hBoxLayTitle.setObjectName('clipGrid')
        
    
        #title 
        globalCheck = QtWidgets.QCheckBox() ; globalCheck.setChecked(True)
        charLbl  = QtWidgets.QLabel('Character:')   
        charLbl.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        nsLbl    = QtWidgets.QLabel('Namespace:')
        nsLbl.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        subLbl   = QtWidgets.QLabel('Sequence:')   
        subLbl.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        clipLbl  = QtWidgets.QLabel('Clip Title:')  
        clipLbl.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        inLbl    = QtWidgets.QLabel('Start:')    
        inLbl .setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        outLbl   = QtWidgets.QLabel('End:')  
        outLbl.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")

        hBoxLayTitle.addWidget(globalCheck,0,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(charLbl,0,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(nsLbl,0,2,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subLbl,0,3,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipLbl,0,4,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(inLbl,0,5,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outLbl,0,6,QtCore.Qt.AlignLeft)

        spacer = QtWidgets.QSpacerItem(40,5,QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        hBoxLayTitle.addItem(spacer,1,5,QtCore.Qt.AlignTop)        

        #dyn clip list
        gameInfo = uiInfo()
        clipLs   = gameInfo.getClipAttrLs()
        for x, i in enumerate(clipLs,1):
            clipInfo = gameInfo.getClipAttr(i)
            clipDict = clipInfo[2]
            clipDictKey = clipDict.keys()[0]

            checkInput = QtWidgets.QCheckBox()
            checkInput.setChecked(True)
            checkInput.setObjectName(i)

            charInput = QtWidgets.QLineEdit(clipInfo[0])
            nsInput   = QtWidgets.QLineEdit(clipInfo[-1])
            subInput  = QtWidgets.QLineEdit(clipInfo[1])
            clipInput = QtWidgets.QLineEdit(clipDictKey)
            playInput = QtWidgets.QPushButton('PLAY')
            stopInput = QtWidgets.QPushButton('STOP')

            infInput  = QtWidgets.QSpinBox()
            infInput.setMaximum(99999)
            infInput.setMinimum(-99999)
            infInput.setValue(clipDict[clipDictKey][0])
            outfInput = QtWidgets.QSpinBox()
            outfInput.setMaximum(99999)
            outfInput.setMinimum(-99999)
            outfInput.setValue(clipDict[clipDictKey][1])

            widInfo = [charInput,subInput,clipInput,infInput,outfInput,nsInput]

            hBoxLayTitle.addWidget(checkInput,x,0,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(charInput,x,1,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(nsInput,x,2,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(subInput,x,3,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(clipInput,x,4,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(infInput,x,5,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(outfInput,x,6,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(playInput,x,7,QtCore.Qt.AlignLeft)
            hBoxLayTitle.addWidget(stopInput,x,8,QtCore.Qt.AlignLeft)

            
            #widget functions
            playInput.clicked.connect(partial(self.__playClip_Cb,infInput,outfInput))
            playInput.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
             #4D9A63;font-weight: bold")

            stopInput.clicked.connect(partial(self.__stopClip_Cb,infInput,outfInput))
            stopInput.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
             #BA1F1F;font-weight: bold")

            for ii in widInfo:
                ii.setStyleSheet("::disabled{color: #dd3535;font-weight: bold;font-size: 12px}\
                ::enabled{color:#39b82e;font-weight: bold;font-size: 12px}")

                ii.setEnabled(False)
                ii.setReadOnly(True)

            lineInfo = [checkInput,playInput,stopInput]
            lineInfo.extend(widInfo)

            self.__checkBoxContext_Cb(checkInput,widInfo,lineInfo,hBoxLayTitle)

        globalCheck.clicked.connect(lambda:self.__globalCheck_Cb(globalCheck))

        return hBoxLayWid

    def clipTitleLayout(self,mainWid):
        hBoxWid  = QtWidgets.QWidget()
        vBoxWid = QtWidgets.QVBoxLayout(hBoxWid)
        hBoxLay  = QtWidgets.QHBoxLayout()

        nsCheck =QtWidgets.QCheckBox("Export from Namespace")
        nsCheck.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        nsCheck.setChecked(True)
        nsCheck.setObjectName('check_ns')


        meshCheck =QtWidgets.QCheckBox("Export Mesh (turn on for morph target support)")
        meshCheck.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        meshCheck.setChecked(True)
        meshCheck.setObjectName('check_mesh')

        keyCheck =QtWidgets.QCheckBox("Redundant Keyframe Filter")
        keyCheck.setStyleSheet("font-size: 14px; color: #ffffff;font-weight: bold")
        keyCheck.setChecked(True)
        keyCheck.setObjectName('check_keyFilt')

        vBoxWid.addLayout(hBoxLay)
        vBoxWid.addWidget(nsCheck)
        vBoxWid.addWidget(meshCheck)
        vBoxWid.addWidget(keyCheck)

        
        addBut = QtWidgets.QPushButton('NEW CLIP')
        addBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #1D77A8;font-weight: bold")
        addBut.clicked.connect(lambda:self.clipWin(mainWid))

        expBut = QtWidgets.QPushButton('EXPORT CLIPS')
        expBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #4D9A63;font-weight: bold")
        expBut.clicked.connect(lambda:self.__exportClip_Cb(nsCheck,meshCheck,keyCheck))

        canBut = QtWidgets.QPushButton('CANCEL')
        canBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #d6713b;font-weight: bold")
        canBut.clicked.connect(lambda:self.__clipWinClose_Cb(self))

        hBoxLay.addWidget(addBut)
        hBoxLay.addWidget(expBut)
        hBoxLay.addWidget(canBut)

        return hBoxWid

    def __menuBar(self,parent):
        
        menubar = QtWidgets.QMenuBar(parent)
        menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        menubar.setObjectName("menubar")
        menubar.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #7c7c7c;font-weight: bold")

        menuExtra = QtWidgets.QMenu(menubar)
        menuExtra.setTitle('Fbx Exporter')
        menuExtra.setObjectName("menuExtra")
        parent.setMenuBar(menubar)

        self.im= QtWidgets.QAction(parent)
        self.im.setObjectName("Camera")
        self.im.setText("Camera Export ")

        assetMenu = QtWidgets.QAction(parent)
        assetMenu.setObjectName("Asset")
        assetMenu.setText("Asset Export ")
  
        menuExtra.addAction(self.im)
        menuExtra.addAction(assetMenu)
        menubar.addAction(menuExtra.menuAction())

        self.im.triggered.connect(lambda:self.__menuFbxCamera_Cb(1))
        assetMenu.triggered.connect(lambda:self.__menuFbxCamera_Cb(2))

        #--/
        return menubar

    def __menuFbxCamera_Cb(self,call=1):
        if call == 1:
            callWindowCam()
        if call == 2:
            callWindowAsset()

    def __globalCheck_Cb(self,check):
        gameInfo = uiInfo()
        prodInfo = prodUtils()
        clipLs = gameInfo.getClipAttrLs()
        if check.isChecked():
            for i in clipLs:
                check = self.findChild(QtWidgets.QCheckBox,i)
                check.setChecked(True)
        else:
            for i in clipLs:
                check = self.findChild(QtWidgets.QCheckBox,i)
                check.setChecked(False)
         
    def __playClip_Cb(self,inWid,outWid):
        mc.playbackOptions(minTime=inWid.value(),maxTime=outWid.value(),loop='continuous')
        mc.play(f=True)

    def __stopClip_Cb(self,inWid,outWid):
        mc.play(state=False)

    def __checkBoxContext_Cb(self,checkWid,widList,lineList,layout):
        checkWid.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        editAction   = QtWidgets.QAction('Edit', checkWid)
        removeAction = QtWidgets.QAction('Remove', checkWid)
 
        editAction.triggered.connect(partial(self.__clipEnable_Cb,widList,checkWid))
        checkWid.addAction(editAction)

        removeAction.triggered.connect(partial(self.__clipDelete_Cb,checkWid,layout,lineList))
        checkWid.addAction(removeAction)
       
    def __clipEnable_Cb(self,widList,checkWid):
        status = widList[0].isEnabled()
        if status:
            cInfo = [str(checkWid.objectName())]
            for i in widList:
                i.setEnabled(False)
                i.setReadOnly(True)
                cInfo.append(str(i.text()))    
            uiInfo().editClipAttr(cInfo[0],cInfo[1],cInfo[2],cInfo[3],int(cInfo[4]),int(cInfo[5]),cInfo[6])
        else:
            for i in widList:
                i.setEnabled(True)
                i.setReadOnly(False)

    def __clipDelete_Cb(self,checkWid,layout,lineList):
        cInfo = str(checkWid.objectName())
        for i in lineList:
            #layout.takeAt(2)
            layout.removeWidget(i)
            i.deleteLater()
        uiInfo().deleteClipAttr(cInfo)

    def __exportClip_Cb(self,nsWid,meshWid,keyWid):
        gameInfo = uiInfo()
        prodInfo = prodUtils()
        clipLs = gameInfo.getClipAttrLs()
        exportLs = []
        for i in clipLs:
            check = self.findChild(QtWidgets.QCheckBox,i)
            if check.isChecked():
                exportLs.append(i)
        if meshWid.isChecked():
            meshEx = True
        else:
            meshEx = False
        if keyWid.isChecked():
            keyRed = True
        else:
            keyRed = False
        if exportLs:
            if not nsWid.isChecked():
                capSel = mc.ls(sl=True)
                for i in exportLs:
                    if capSel:
                        mc.select(capSel[0],r=True)
                    expt = gameInfo.getClipAttr(i)
                    prodInfo.exportAnimDict(expt[0],expt[1],expt[2],incMesh=meshEx)
            else:
                invalidNs = []
                for i in exportLs:
                    expt = gameInfo.getClipAttr(i)
                    if expt[-1]:
                        ns = mc.ls('%s:*'%(expt[-1]))
                        if ns:
                            mc.select(ns[0],r=True)
                            prodInfo.exportAnimDict(expt[0],expt[1],expt[2],incMesh=meshEx,keyRed=keyRed)
                    else:
                        invalidNs.append(expt)
                if invalidNs:
                    print "NO VALID NAMESPACE THE FOLLOW HAVE NOT BEEN EXPORTED:"
                    for i in invalidNs:
                        print i

    def clipWin(self,mainWid=None):
        global saveWin
        title   = 'CLIP'

        min = mc.playbackOptions(q=True,min=True)
        max = mc.playbackOptions(q=True,max=True)
        
        saveWin = QtWidgets.QWidget()
        saveLay = QtWidgets.QVBoxLayout(saveWin)
        #saveWin.setWindowModality(QtCore.Qt.ApplicationModal)
        saveWin.setWindowTitle(title)
        saveWin.setMinimumWidth(230)
        saveWin.setMaximumWidth(230)
        saveWin.setMinimumHeight(225)
        saveWin.setMaximumHeight(225)

        if mainWid:
            mainWid = mainWid.parent()
            winVal = [mainWid.x(),mainWid.y()]
            saveWin.move(winVal[0],winVal[1])

        hBoxWidTitle = QtWidgets.QWidget()
        hBoxLayTitle = QtWidgets.QGridLayout(hBoxWidTitle)

        font      = QtGui.QFont() ; font.setBold(True)
        charLbl   = QtWidgets.QLabel('Character:')    ; charLbl.setFont(font)
        subLbl    = QtWidgets.QLabel('Sequence:')     ; subLbl.setFont(font)
        clipLbl   = QtWidgets.QLabel('Clip Title:')   ; clipLbl.setFont(font)
        infLbl    = QtWidgets.QLabel('Start:')       ; infLbl.setFont(font)
        outfLbl   = QtWidgets.QLabel('End:')         ; outfLbl.setFont(font)

        charInput = QtWidgets.QComboBox()
        gameInfo  = uiInfo()
        items     = gameInfo.getAssetInfo()
        charInput.addItems(items)
        charInput.setEditable(False)
        
        
        subInput  = QtWidgets.QComboBox()
        clipInput = QtWidgets.QLineEdit()

        infInput  = QtWidgets.QSpinBox()
        infInput.setMaximum(99999)
        infInput.setMinimum(-99999)
        infInput.setValue(min)
        outfInput = QtWidgets.QSpinBox()
        outfInput.setMaximum(99999)
        outfInput.setMinimum(-99999)
        outfInput.setValue(max)

        subInput.setEditable(True)

        hBoxLayTitle.addWidget(charLbl,0,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subLbl,1,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipLbl,2,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(infLbl,3,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outfLbl,4,0,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(charInput,0,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subInput,1,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipInput,2,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(infInput,3,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outfInput,4,1,QtCore.Qt.AlignLeft)


        vBoxWid = QtWidgets.QWidget()
        vBoxLay = QtWidgets.QHBoxLayout(vBoxWid)
        saveBut = QtWidgets.QPushButton('SAVE')
        saveBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #4D9A63;font-weight: bold")
        canBut  = QtWidgets.QPushButton('CANCEL')
        canBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #d6713b;font-weight: bold")
        vBoxLay.addWidget(saveBut)
        vBoxLay.addWidget(canBut)

        saveLay.addWidget(hBoxWidTitle)
        saveLay.addWidget(vBoxWid)

        widInfo = [charInput,subInput,clipInput,infInput,outfInput]
        
        canBut.clicked.connect(lambda:self.__clipWinClose_Cb(saveWin))
        saveBut.clicked.connect(lambda:self.__clipWinSave_Cb(saveWin,widInfo))

        charInput.currentIndexChanged.connect(lambda:self.__comboLoadSeqCallBack(charInput,subInput))

        self.__defaultCharSelection(charInput)
        self.__comboLoadSeqCallBack(charInput,subInput)
        self.__comboContext(charInput,subInput)
        
        saveWin.show()
        
        return saveWin

    def __clipWinClose_Cb(self,window):
        window.close()

    def __clipWinSave_Cb(self,window,widList):
        widInfo = []
        for i in widList:
            try:
                widInfo.append(str(i.text()))
            except:
                widInfo.append(str(i.currentText()))
        ns = uiInfo().getSelNamespace()
        if not ns:
            ns = '' 
        clip = uiInfo().addGameInfo(widInfo[0],widInfo[1],widInfo[2],int(widInfo[3]),int(widInfo[4]),str(ns))
        self.__clipWinClose_Cb(window)
        
        #dyn clip list
        gameInfo = uiInfo()
        hBoxLayTitle = self.findChild(QtWidgets.QGridLayout,'clipGrid')
        #x =  hBoxLayTitle.rowCount()
        x = len(gameInfo.getClipAttrLs())
        clipInfo = gameInfo.getClipAttr(clip)
        clipDict = clipInfo[2]
        clipDictKey = clipDict.keys()[0]

        checkInput = QtWidgets.QCheckBox()
        checkInput.setChecked(True)
        checkInput.setObjectName(clip)

        charInput = QtWidgets.QLineEdit(clipInfo[0])
        nsInput   = QtWidgets.QLineEdit(clipInfo[-1])
        subInput  = QtWidgets.QLineEdit(clipInfo[1])
        clipInput = QtWidgets.QLineEdit(clipDictKey)
        playInput = QtWidgets.QPushButton('PLAY')
        stopInput = QtWidgets.QPushButton('STOP')

        infInput  = QtWidgets.QSpinBox()
        infInput.setMaximum(99999)
        infInput.setMinimum(-99999)
        infInput.setValue(clipDict[clipDictKey][0])
        outfInput = QtWidgets.QSpinBox()
        outfInput.setMaximum(99999)
        outfInput.setMinimum(-99999)
        outfInput.setValue(clipDict[clipDictKey][1])

        widInfo = [charInput,subInput,clipInput,infInput,outfInput,nsInput]

        hBoxLayTitle.addWidget(checkInput,x,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(charInput,x,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(nsInput,x,2,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subInput,x,3,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipInput,x,4,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(infInput,x,5,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outfInput,x,6,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(playInput,x,7,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(stopInput,x,8,QtCore.Qt.AlignLeft)

        

        #widget functions
        playInput.clicked.connect(partial(self.__playClip_Cb,infInput,outfInput))
        playInput.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
         #4D9A63;font-weight: bold")

        stopInput.clicked.connect(partial(self.__stopClip_Cb,infInput,outfInput))
        stopInput.setStyleSheet("font-size: 12px; color: #ffffff;background-color:\
         #BA1F1F;font-weight: bold")

        for ii in widInfo:
            ii.setStyleSheet("::disabled{color: #dd3535;font-weight: bold;font-size: 12px}\
            ::enabled{color:#39b82e;font-weight: bold;font-size: 12px}")

            ii.setEnabled(False)
            ii.setReadOnly(True)

        lineInfo = [checkInput,playInput,stopInput]
        lineInfo.extend(widInfo)

        self.__checkBoxContext_Cb(checkInput,widInfo,lineInfo,hBoxLayTitle)

    def __comboContext(self,combo,comboSeq):
        combo.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        loadAction  = QtWidgets.QAction('Edit',self)
        loadAction.triggered.connect(lambda:self.__comboContextCallBack(combo,comboSeq))
        combo.addAction(loadAction)

    def __comboPressEnterCallBack(self,combo,comboSeq):
        line = combo.lineEdit()
        line.returnPressed.connect(lambda:self.__comboContextCallBack(combo,comboSeq))
        self.__comboLoadSeqCallBack(combo,comboSeq)

    def __comboContextCallBack(self,combo,comboSeq):
        if combo.isEditable():
            items = [combo.itemText(i) for i in range(combo.count())]
            currentItem = combo.currentText()
            if not currentItem in items:
                items.append(currentItem)
            items.sort()
            combo.clear()
            combo.addItems(items)
            combo.setEditable(False)
            getAsset = combo.findText(currentItem)
            if getAsset != -1:
                combo.setCurrentIndex(getAsset)
        else:
            combo.setEditable(True)
            self.__comboPressEnterCallBack(combo,comboSeq)

    def __comboLoadSeqCallBack(self,comboChar,comboSeq):
        seqLs = uiInfo().listAnimSequences(str(comboChar.currentText()))
        comboSeq.clear()
        if seqLs:
            comboSeq.addItems(seqLs)

    def __defaultCharSelection(self,comboChar):
        char = uiInfo().getAssetFromRefSelection()
        if char:
            getAsset = comboChar.findText(char)
            if getAsset != -1:
                comboChar.setCurrentIndex(getAsset)

    def __saveClipCB_Info(self):
        gameInfo = uiInfo()
        clipLs   = gameInfo.getClipAttrLs()
        clipDict = {}
        for i in clipLs:
            cb = self.findChild(QtWidgets.QCheckBox,i)
            state = cb.isChecked()
            clipDict[i] = state
        gameNode = gameInfo.getGameInfo()
        gameInfo._nodeLock(gameNode,False)
        gameInfo._attrLock(gameNode,gameInfo.clipActive,False)
        mc.setAttr('%s.%s'%(gameNode,gameInfo.clipActive),clipDict,type='string',l=True)
        gameInfo._nodeLock(gameNode,True)
        
    def __loadClipCb_Info(self):
        gameInfo = uiInfo()
        gameNode = gameInfo.getGameInfo()
        clipCbInfo = mc.getAttr('%s.%s'%(gameNode,gameInfo.clipActive))
        if clipCbInfo:
            clipCbInfo = eval(clipCbInfo)
            for i in clipCbInfo.keys():
                cb = self.findChild(QtWidgets.QCheckBox,i)
                if cb:
                    cb.setChecked(clipCbInfo[i])

class gameFbxExporterAssetUi(QtWidgets.QMainWindow):
    '''gameFbxCamera ui'''
    def __init__(self,parent=uiInfo().getMayaWindow(),
        width=None,height=None,dev=False):
        QtWidgets.QMainWindow.__init__(self,parent)
        # init window settings
        self.__version__ = __version__
        self.windowName = 'sk_gameAssetEx   %s'%__version__
        uiInfo().removeWindow(self.windowName)

        if width:
          self.windowWidth = width
        else:
          self.windowWidth  = 200
        if height:
          self.windowHeight = height
        else:
          self.windowHeight = 150

        self.setWindowTitle(self.windowName)
        self.setObjectName (self.windowName)
        self.setGeometry(800,300,200,150)
        #winVal = [parent.width(),parent.height()]
        #self.move(winVal[0],winVal[1])
        
        self.resize(self.windowWidth,self.windowHeight)
        main = self.mainLayout(dev)
        self.setCentralWidget(main)

        #self.setMinimumWidth(self.windowWidth)
        #self.setMaximumWidth(self.windowWidth)
        #self.setMinimumHeight(400)
        self.setMaximumHeight(150)
        self.setMaximumWidth(200)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.__menuBar(self)

    def mainLayout(self,dev):
        mainLay = QtWidgets.QWidget(self)
        #construct layouts
        self.mainLay = QtWidgets.QVBoxLayout(mainLay)
        
        saveWin = QtWidgets.QWidget(mainLay)
        saveLay = QtWidgets.QVBoxLayout(saveWin)
        saveWin.setWindowModality(QtCore.Qt.ApplicationModal)
        
        hBoxWidTitle = QtWidgets.QWidget()
        hBoxLayTitle = QtWidgets.QGridLayout(hBoxWidTitle)

        self.mainLay.addWidget(saveWin)

        font      = QtGui.QFont() ; font.setBold(True) ; font.setPixelSize(14)
        textLbl   = QtWidgets.QLabel('Texure Export:') ; textLbl.setFont(font)
        charLbl   = QtWidgets.QLabel('Export Type:')  ; charLbl.setFont(font)
        subLbl    = QtWidgets.QLabel('Asset Name:')   ; subLbl.setFont(font)
        
        exportType = ['Mesh Scene','Mesh Batch','Mesh Selection','Skel Rig']

        gameInfo = uiInfo()

        textChk   = QtWidgets.QCheckBox()
        textChk.setChecked(False)


        charInput = QtWidgets.QComboBox()
        charInput.addItems(exportType)
        charInput.setEditable(False)  
        charInput.setMinimumWidth(100)
        
        subInput  = QtWidgets.QComboBox()
        subInput.setEditable(True)
        seqItems = gameInfo.getAssetInfo()
        subInput.addItems(seqItems)
        subInput.setEditable(False)
        subInput.setMinimumWidth(100)
        self.__comboContext(subInput)


        fileBut = QtWidgets.QPushButton('Game Export')
        fileBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #1D77A8;font-weight: bold")

        fileBut2 = QtWidgets.QPushButton('Asset Directory')
        fileBut2.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #1D77A8;font-weight: bold")

        hBoxLayTitle.addWidget(fileBut,0,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(fileBut2,0,1,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(textLbl,1,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(textChk,1,1,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(charLbl,2,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(charInput,2,1,QtCore.Qt.AlignLeft)
     
        hBoxLayTitle.addWidget(subLbl,3,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subInput,3,1,QtCore.Qt.AlignLeft)
       

        vBoxWid = QtWidgets.QWidget()
        vBoxLay = QtWidgets.QHBoxLayout(vBoxWid)
        saveBut = QtWidgets.QPushButton('EXPORT')
        saveBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #4D9A63;font-weight: bold")
        canBut  = QtWidgets.QPushButton('CANCEL')
        canBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #d6713b;font-weight: bold")
        vBoxLay.addWidget(saveBut)
        vBoxLay.addWidget(canBut)

        saveLay.addWidget(hBoxWidTitle)
        saveLay.addWidget(vBoxWid)

        self.__defaultSceneSettings(subInput,charInput)
 
        canBut.clicked.connect(lambda:self.__clipWinClose_Cb(self))
        saveBut.clicked.connect(lambda:self.__exportAsset_Cb(charInput,subInput,textChk))

        fileBut.clicked.connect(lambda:self.__openDirectoryGE())
        fileBut2.clicked.connect(lambda:self.__openDirectoryAsset(subInput))

        return mainLay

    def __menuBar(self,parent):
        
        menubar = QtWidgets.QMenuBar(parent)
        menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        menubar.setObjectName("menubar")
        menubar.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #7c7c7c;font-weight: bold")

        menuExtra = QtWidgets.QMenu(menubar)
        menuExtra.setTitle('Fbx Exporter')
        menuExtra.setObjectName("menuExtra")
        parent.setMenuBar(menubar)

        self.im= QtWidgets.QAction(parent)
        self.im.setObjectName("Camera")
        self.im.setText("Camera Export ")

        assetMenu = QtWidgets.QAction(parent)
        assetMenu.setObjectName("Anim")
        assetMenu.setText("Anim Export ")
  
        menuExtra.addAction(self.im)
        menuExtra.addAction(assetMenu)

        menubar.addAction(menuExtra.menuAction())


        self.im.triggered.connect(lambda:self.__menuFbxCamera_Cb(1))
        assetMenu.triggered.connect(lambda:self.__menuFbxCamera_Cb(2))

        #--/
        return menubar

    def __menuFbxCamera_Cb(self,call=1):
        if call == 1:
            callWindowCam()
        if call == 2:
            callWindowAnim()

    def __clipWinClose_Cb(self,window):
        window.close()

    def __initShotList_Cb(self):
        gameInfo  = uiInfo()
        seqItems  = gameInfo.listSequences()
        if seqItems:
            shotItems = gameInfo.listShots(seqItems[0])
            return shotItems
        return None

    def __openDirectoryGE(self):
        gameInfo  = uiInfo()
        os.startfile(gameInfo.gameDir)

    def __openDirectoryAsset(self,combo):
        gameInfo  = uiInfo()
        asset     = combo.currentText()
        assetPath = r'%s/%s'%(gameInfo.gameDir,asset)
        
        if os.path.exists(assetPath):
            os.startfile(assetPath)

    def __exportAsset_Cb(self,typeCombo,assetCombo,textChk):
        exType = typeCombo.currentIndex()
        asset  = assetCombo.currentText()
        exText = textChk.isChecked()

        if exType == 0:
            prodUtils().exportModelSetup(asset,True,incTexture=exText)

        if exType == 1:
            prodUtils().exportModelBatch(asset,incTexture=exText) 

        if exType == 2:
            prodUtils().exportModelSetup(asset,incTexture=exText)

        if exType == 3:
            prodUtils().exportCharSetup(asset,incTexture=exText)

    def __defaultSceneSettings(self,assetCombo,typeCombo):
        scene = mc.file(sn=True,q=True)
        fileName = scene.split('/')[-1]
        if '_' in fileName:
            assetName = fileName.split('_')[0]
            getAsset = assetCombo.findText(assetName)
            if getAsset != -1:
                assetCombo.setCurrentIndex(getAsset)
        if 'rig' in fileName:
            typeCombo.setCurrentIndex(3)

    def __comboContext(self,combo=None):
        combo.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        loadAction  = QtWidgets.QAction('Edit',self)
        loadAction.triggered.connect(lambda:self.__comboContextCallBack(combo))
        combo.addAction(loadAction)

    def __comboPressEnterCallBack(self,combo):
        line = combo.lineEdit()
        line.returnPressed.connect(lambda:self.__comboContextCallBack(combo))

    def __comboContextCallBack(self,combo):
        if combo.isEditable():
            items = [combo.itemText(i) for i in range(combo.count())]
            currentItem = combo.currentText()
            if not currentItem in items:
                items.append(currentItem)
            items.sort()
            combo.clear()
            combo.addItems(items)
            combo.setEditable(False)
            getAsset = combo.findText(currentItem)
            if getAsset != -1:
                combo.setCurrentIndex(getAsset)
        else:
            combo.setEditable(True)
            self.__comboPressEnterCallBack(combo)

class gameFbxExporterCamUi(QtWidgets.QMainWindow):
    '''gameFbxCamera ui'''
    def __init__(self,parent=uiInfo().getMayaWindow(),
        width=None,height=None,dev=False):
        QtWidgets.QMainWindow.__init__(self,parent)
        # init window settings
        self.__version__ = __version__
        self.windowName = 'sk_gameCamEx   %s'%__version__
        uiInfo().removeWindow(self.windowName)

        if width:
          self.windowWidth = width
        else:
          self.windowWidth  = 350
        if height:
          self.windowHeight = height
        else:
          self.windowHeight = 200

        self.setWindowTitle(self.windowName)
        self.setObjectName (self.windowName)
        self.setGeometry(800,300,200,150)
        #winVal = [parent.width(),parent.height()]
        #self.move(winVal[0],winVal[1])
        
        self.resize(self.windowWidth,self.windowHeight)
        main = self.mainLayout(dev)
        self.setCentralWidget(main)

        #self.setMinimumWidth(self.windowWidth)
        #self.setMaximumWidth(self.windowWidth)
        #self.setMinimumHeight(400)
        self.setMaximumHeight(200)
        self.setMaximumWidth(275)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


    def mainLayout(self,dev):
        mainLay = QtWidgets.QWidget(self)
        #construct layouts
        self.mainLay = QtWidgets.QVBoxLayout(mainLay)
        
        saveWin = QtWidgets.QWidget(mainLay)
        saveLay = QtWidgets.QVBoxLayout(saveWin)
        saveWin.setWindowModality(QtCore.Qt.ApplicationModal)
        
        hBoxWidTitle = QtWidgets.QWidget()
        hBoxLayTitle = QtWidgets.QGridLayout(hBoxWidTitle)

        self.mainLay.addWidget(saveWin)

        font      = QtGui.QFont() ; font.setBold(True) ; font.setPixelSize(14)
        charLbl   = QtWidgets.QLabel('Camera:')       ; charLbl.setFont(font)
        subLbl    = QtWidgets.QLabel('Sequence:')     ; subLbl.setFont(font)
        clipLbl   = QtWidgets.QLabel('Shot:')         ; clipLbl.setFont(font)
        infLbl    = QtWidgets.QLabel('Start Frame:')  ; infLbl.setFont(font)
        outfLbl   = QtWidgets.QLabel('End Frame:')    ; outfLbl.setFont(font)
        prefLbl   = QtWidgets.QLabel('File Prefix:')  ; prefLbl.setFont(font)
        yawLbl    = QtWidgets.QLabel('UE4 Yaw:')      ; yawLbl.setFont(font)
        keyLbl    = QtWidgets.QLabel('Redundant Keyframe Filter:') ; keyLbl.setFont(font)

        gameInfo  = uiInfo()
        gameInfo.getCameraShotgunInfo()
        
        charInput = QtWidgets.QComboBox()
        camItems  = gameInfo.getSceneCamera()
        charInput.addItems(camItems)
        charInput.setEditable(False)  
        charInput.setMinimumWidth(100)
        
        subInput  = QtWidgets.QComboBox()
        subInput.setEditable(True)
        seqItems = gameInfo.listSequences()
        subInput.addItems(seqItems)
        subInput.setEditable(False)
        subInput.setMinimumWidth(100)

        clipInput = QtWidgets.QComboBox()
        clipInput.setEditable(True)
        shotItems = self.__initShotList_Cb()
        if shotItems:
            clipInput.addItems(shotItems)
        clipInput.setEditable(False)
        clipInput.setMinimumWidth(100)

        infInput  = QtWidgets.QSpinBox()
        infInput.setMaximum(99999)
        infInput.setMinimum(-99999)
        outfInput = QtWidgets.QSpinBox()
        outfInput.setMaximum(99999)
        outfInput.setMinimum(-99999)

        prefInput = QtWidgets.QLineEdit()

        yawCheck = QtWidgets.QCheckBox()
        yawCheck.setChecked(True)
        if not dev:
            yawCheck.setEnabled(False)

        keyCheck = QtWidgets.QCheckBox()
        keyCheck.setChecked(True)


        fileBut = QtWidgets.QPushButton('Sequence Directory')
        fileBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #1D77A8;font-weight: bold")

        fileBut2 = QtWidgets.QPushButton('Shot Directory')
        fileBut2.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #1D77A8;font-weight: bold")

        hBoxLayTitle.addWidget(charLbl,1,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subLbl,2,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipLbl,3,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(infLbl,4,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outfLbl,5,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(prefLbl,6,0,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(charInput,1,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(subInput,2,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(clipInput,3,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(infInput,4,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(outfInput,5,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(prefInput,6,1,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(fileBut,0,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(fileBut2,0,1,QtCore.Qt.AlignLeft)

        hBoxLayTitle.addWidget(keyLbl,7,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(keyCheck,7,1,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(yawLbl,8,0,QtCore.Qt.AlignLeft)
        hBoxLayTitle.addWidget(yawCheck,8,1,QtCore.Qt.AlignLeft)
        
        vBoxWid = QtWidgets.QWidget()
        vBoxLay = QtWidgets.QHBoxLayout(vBoxWid)
        saveBut = QtWidgets.QPushButton('EXPORT')
        saveBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #4D9A63;font-weight: bold")
        canBut  = QtWidgets.QPushButton('CANCEL')
        canBut.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #d6713b;font-weight: bold")
        vBoxLay.addWidget(saveBut)
        vBoxLay.addWidget(canBut)

        saveLay.addWidget(hBoxWidTitle)
        saveLay.addWidget(vBoxWid)

        widInfo = [charInput,subInput,clipInput,infInput,outfInput]
        

        self.__defaultSceneSettings(clipInput,subInput,infInput,outfInput)

        subInput.currentIndexChanged.connect(lambda:self.__updateShotCombo_Cb(clipInput,subInput))
      
        canBut.clicked.connect(lambda:self.__clipWinClose_Cb(self))
        saveBut.clicked.connect(lambda:self.__exportCam_Cb(charInput,subInput,clipInput,infInput,\
            outfInput,prefInput,yawCheck,keyCheck))

        fileBut.clicked.connect(lambda:self.__openDirectorySeq(subInput))
        fileBut2.clicked.connect(lambda:self.__openDirectoryShot(subInput,clipInput))


        self.__menuBar(self,charInput)

        return mainLay

    def __menuBar(self,parent,camCombo):
        
        menubar = QtWidgets.QMenuBar(parent)
        menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        menubar.setObjectName("menubar")
        menubar.setStyleSheet("font-size: 14px; color: #ffffff;background-color:\
             #7c7c7c;font-weight: bold")

        menuExtra = QtWidgets.QMenu(menubar)
        menuExtra.setTitle('Fbx Exporter')
        menuExtra.setObjectName("menuExtra")
        parent.setMenuBar(menubar)

        self.im= QtWidgets.QAction(parent)
        self.im.setObjectName("Anim")
        self.im.setText("Anim Export ")

        assetMenu = QtWidgets.QAction(parent)
        assetMenu.setObjectName("Asset")
        assetMenu.setText("Asset Export ")
  
        menuExtra.addAction(self.im)
        menuExtra.addAction(assetMenu)

        menubar.addAction(menuExtra.menuAction())


        self.im.triggered.connect(lambda:self.__menuFbxCamera_Cb(1))
        assetMenu.triggered.connect(lambda:self.__menuFbxCamera_Cb(2))

        menuExtra2 = QtWidgets.QMenu(menubar)
        menuExtra2.setTitle('Render Status')
        menuExtra2.setObjectName("menuExtra2")
        parent.setMenuBar(menubar)

        toggleOn= QtWidgets.QAction(parent)
        toggleOn.setObjectName("ToggleOn")
        toggleOn.setText("On")

        toggleOff= QtWidgets.QAction(parent)
        toggleOff.setObjectName("ToggleOff")
        toggleOff.setText("Off")
  
        menuExtra2.addAction(toggleOn)
        menuExtra2.addAction(toggleOff)

        menubar.addAction(menuExtra2.menuAction())

        toggleOn.triggered.connect(lambda:self.__toggleRenderCamUpdate_Cb(camCombo,1))
        toggleOff.triggered.connect(lambda:self.__toggleRenderCamUpdate_Cb(camCombo,0))

        #--/
        return menubar

    def __menuFbxCamera_Cb(self,call=1):
        if call == 1:
            callWindowAnim()
        if call == 2:
            callWindowAsset()

    def __clipWinClose_Cb(self,window):
        window.close()

    def __initShotList_Cb(self):
        gameInfo  = uiInfo()
        seqItems  = gameInfo.listSequences()
        if seqItems:
            shotItems = gameInfo.listShots(seqItems[0])
            return shotItems
        return None

    def __defaultSceneSettings(self,shotCombo,seqCombo,sfSpin,efSpin):
        scene = mc.file(sn=True,q=True)
        gameInfo  = uiInfo()
    
        seqItems  = gameInfo.listSequences()
        sequence  = ''
        shot      = ''
        for i in seqItems:
            if '/%s/'%i in scene:
                sequence = i
        if sequence:
            shotItems = gameInfo.listShots(sequence)
            for x in shotItems:
                if '/%s/'%x in scene:
                    shot = x
        getSeq = seqCombo.findText(sequence)
        if getSeq != -1:
            seqCombo.setCurrentIndex(getSeq)

            self.__updateShotCombo_Cb(shotCombo,seqCombo)

            getShot = shotCombo.findText(shot)
            if getShot != -1:
                shotCombo.setCurrentIndex(getShot)

        min = mc.playbackOptions(q=True,min=True)
        max = mc.playbackOptions(q=True,max=True)

        sfSpin.setValue(min)
        efSpin.setValue(max)

    def __openDirectorySeq(self,seqCombo):
        gameInfo  = uiInfo()
        sequence = seqCombo.currentText()
        if not sequence:
            path = gameInfo.camDir
        else:
            path = r'%s/%s'%(gameInfo.camDir,sequence)
        os.startfile(path)

    def __openDirectoryShot(self,seqCombo,shotCombo):
        gameInfo  = uiInfo()
        sequence = seqCombo.currentText()
        shot     = shotCombo.currentText()
        if not sequence:
            path = gameInfo.camDir
        else:
            if not shot:
                path = r'%s/%s'%(gameInfo.camDir,sequence)
            else:
                path = r'%s/%s/%s'%(gameInfo.camDir,sequence,shot)
        os.startfile(path)

    def __updateShotCombo_Cb(self,shotCombo,seqCombo):
        gameInfo  = uiInfo()
        seq = seqCombo.currentText()
        seqItems  = gameInfo.listShots(seq)
        shotCombo.clear()
        if seqItems:
            shotCombo.addItems(seqItems)

    def __exportCam_Cb(self,cameraCombo,seqCombo,shotCombo,sfSpin,efSpin,prefixLine,yawCheck,keyCheck):
        gameInfo  = uiInfo()
        #camera = '%s:renderCam'%cameraCombo.currentText()
        camera =   cameraCombo.currentText()
        sequence = seqCombo.currentText()
        shot = shotCombo.currentText()
        sf = sfSpin.value()
        ef = efSpin.value()
        prefix = prefixLine.text()
        yaw = yawCheck.isChecked()
        
        path = r'%s/%s/%s'%(gameInfo.camDir,sequence,shot)

        if prefix:
            name = '%s_%s'%(prefix,shot) 
        else:
            name = shot

        if keyCheck.isChecked():
            keyRed = True
        else:
            keyRed = False

        cameraUtils().exportCamAnim(path,name,camera,[sf,ef],yaw,keyRed=keyRed)

    def __toggleRenderCamUpdate_Cb(self,cameraCombo,bIsRender):
        cameraUtils().toggleRender(bIsRender)
        cameraCombo.clear()
        gameInfo  = uiInfo()
        camItems  = gameInfo.getSceneCamera()
        cameraCombo.addItems(camItems)
 
def callWindowRig(dev=False):
    ui = gameRigToolsUi(dev=dev)
    ui.show()

def callWindowAnim(dev=False):
    ui = gameFbxExporterAnimUi(dev=dev)
    ui.show()

def callWindowAsset(dev=False):
    ui = gameFbxExporterAssetUi(dev=dev)
    ui.show()

def callWindowCam(dev=False):
    ui = gameFbxExporterCamUi(dev=dev)
    ui.show()

############################

class simpleExport(prodUtils):

    def __init__(self):
        super(simpleExport, self).__init__()

    def dialogPrompt(self):
        wid = QtWidgets.QWidget()
        gui = QtWidgets.QInputDialog()
        inputText,ok = gui.getText(wid,"FBX:Export","Enter Asset Name:")
        if ok:
            return inputText
        return None

    def simpleExport_Model(self):
        name = self.dialogPrompt()
        if name:
           self.exportModelSetup(name)

    def simpleExport_Model_Batch(self):
        char = self.dialogPrompt()
        self.exportModelBatch(char)

    def simpleExport_ModelScene(self):
        name = self.dialogPrompt()
        if name:
           self.exportModelSetup(name,True) 

    def simpleExport_Rig(self):
        name = self.dialogPrompt()
        if name:
           self.exportCharSetup(name) 
############################

assetUtils().__setupDir__()

# <

if __name__ == "__main__":
    pass
    
