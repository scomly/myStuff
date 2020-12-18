import maya.cmds as mc
import maya.mel  as mel

__version__ = '1.0.0'


class fbxUtils(object):
    def __init__(self):
        self.baseRoot = 'root'
        self.baseGeo  = 'GEO'
        self.fbxSettings = [
                    'FBXExportUpAxis z;',
                    'FBXExportFileVersion -v FBX201800;',
                    'FBXExportSmoothingGroups -v true;',
                    'FBXExportSmoothMesh -v true;',
                    'FBXExportTangents -v true;',
                    'FBXExportSkins -v true',
                    'FBXExportShapes -v true',
                    'FBXExportEmbeddedTextures -v false',
                    'FBXExportApplyConstantKeyReducer -v true',
                    'FBXExportSplitAnimationIntoTakes -c']

    def __fbxSettings(self):
        for i in self.fbxSettings:
            mel.eval(i)

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

    def exportFbxRig(self,path,name):
        self.__fbxSettings()
        filePath = r'%s/%s_unreal_rig.fbx'%(path,name)
        self.checkPlugin('fbxmaya')
        
        #prep for export
        base = mc.listRelatives(self.baseGeo,parent=True)[0]
        mc.parent(self.baseRoot,w=True)
        jntHi = mc.listRelatives(self.baseRoot,ad=True,type='constraint',f=True)
        if jntHi:
            mc.delete(jntHi)
        jntLs = [self.baseRoot]
        jntLs.extend(mc.listRelatives(self.baseRoot,ad=True))
        for i in jntLs:
            for x in ['tx','ty','tz','rx','ry','rz']:
                conn = mc.listConnections('%s.%s'%(i,x),s=True,p=True)
                if conn:
                    mc.disconnectAttr(conn[0],'%s.%s'%(i,x))

        mc.parent(self.baseGeo,w=True)
        mc.delete(base)

        mc.select(self.baseRoot,r=True)
        mc.select(self.baseGeo,tgl=True)
        
        if mc.objExists('MESH'):
            mc.delete('MESH')
        mc.setAttr('%s.v'%self.baseRoot,1)
    
        #export 
        filePath = filePath.replace('\\','/')
        mel.eval('FBXExport -f "%s" -s;'%filePath)
         
        mc.file(filePath,o=True,f=True)
 

#ex = fbxUtils()
#ex.exportFbxRig(r'F:TEST\Testing','charName')
