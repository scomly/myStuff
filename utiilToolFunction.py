
import maya.cmds as cmds
#import os
#import re
from mVray import vrayObjectProperties as vop
from mVray import vrayFrameBuffers as vfb
#import maya.mel as mel

class CreateAssetGroups(object):
    def __init__(self, mask, groupName, assetVOPName):
        
        self.mask = mask
        ## mask is the keyword used to filer thru the scn
        self.groupName = groupName
        ## group name in maya for the geometry
        self.assetVOPName = assetVOPName
        ## name of the vray object property associated with the group
      
        asset_mask_list = ['*:*%s' % (mask)]
        getAsset = cmds.ls(asset_mask_list, assemblies=True)
        
        if len(getAsset) > 0:
            if cmds.objExists(groupName):
                groupVariable = cmds.ls(groupName)
                cmds.parent(getAsset, groupVariable)
            else:
                groupVariable = cmds.group(getAsset, name=groupName)
                
            if not cmds.objExists(assetVOPName):
                assetVOPVariable =  vop.createObjectProperties(groupVariable, assetVOPName)
            else:
                assetVOPVariable = cmds.ls(assetVOPName)
                
                         
## example creation ##
## createArrows = CreateAssetGroups('arrow', 'ARROWS_GRP', 'ARROWS_VOP')


class CreateRGBLightMaterials(object):    
    def __init__(self, shaderName, R, G, B):
        
        self.shaderName = shaderName
        self.R = R
        self.G = G
        self.B = B
        
        if not cmds.objExists(shaderName):
            mtlName = cmds.shadingNode('VRayLightMtl', asShader=True, name=shaderName)
            cmds.setAttr('%s.color' % (mtlName), R,G,B, type='double3')
            cmds.setAttr('%s.emitOnBackSide' % (mtlName), 1)
        else:
            mtlName = cmds.ls(shaderName)[0]

## example creation ##    
## createRedShader = CreateRGBLightMaterials('RED',1,0,0)
## createRedShader = CreateRGBLightMaterials('GREEN',0,1,0)
## createRedShader = CreateRGBLightMaterials('BLUE',0,0,1)
## createRedShader = CreateRGBLightMaterials('WHITE',1,1,1)
## createRedShader = CreateRGBLightMaterials('BLACK',0,0,0)

class CreateCatchers(object):
    def __init__(self, type):
        self.type = type
        ## type meaning 'shadow' or 'reflection' catcher
        
        if type.lower() == 'shadow':
            if not cmds.objExists('SHADOW_CATCHER'):
                shdCatcher = cmds.shadingNode('VRayMtl', asShader=True, name='SHADOW_CATCHER')
                cmds.setAttr('%s.reflectionColorAmount' % (shdCatcher), 0)
                cmds.setAttr('%s.diffuseColorAmount' % (shdCatcher), 1)
                cmds.setAttr('%s.brdfType' % (shdCatcher), 0)
                cmds.setAttr('%s.useFresnel' % (shdCatcher), 0)
            ## creates shadow catching VRayMtl
            
            if not cmds.objExists('CONTACT_SHADOW_CATCHER'):
                contactShadCatcher = cmds.shadingNode('VRayDirt', asTexture=True, name='CONTACT_SHADOW_CATCHER')
                cmds.setAttr('%s.blackColor' % (contactShadCatcher), 1,1,1, type='double3')
                cmds.setAttr('%s.whiteColor' % (contactShadCatcher), 0,0,0, type='double3')
                cmds.setAttr('%s.radius' % (contactShadCatcher), 10)
                cmds.setAttr('%s.ignoreSelfOcclusion' % (contactShadCatcher), 1)
                cmds.setAttr('%s.resultAffectInclusive' % (contactShadCatcher), 0)
             ## creates VrayDirt used for ambient occlusion
        
        elif type.lower() == 'reflection':
                if not cmds.objExists('REFL_CATCHER'):
                    mirrorMtl = cmds.shadingNode('VRayMtl', asShader=True, name='REFL_CATCHER')
                    cmds.setAttr('%s.color' % (mirrorMtl), 0,0,0, type='double3')
                    cmds.setAttr('%s.reflectionColor' % (mirrorMtl), 1,1,1, type='double3')
                    cmds.setAttr('%s.reflectionColorAmount' % (mirrorMtl), 1)
                    cmds.setAttr('%s.diffuseColorAmount' % (mirrorMtl), 0)
                    cmds.setAttr('%s.useFresnel' % (mirrorMtl), 0)
                    mirrorOccl = cmds.shadingNode('VRayDirt', asTexture=True, name='MIRROR_REFLOCC')
                    cmds.setAttr('%s.blackColor' % (mirrorOccl), 1,1,1, type='double3')
                    cmds.setAttr('%s.whiteColor' % (mirrorOccl), 0,0,0, type='double3')
                    cmds.setAttr('%s.radius' % (mirrorOccl), 1000)
                    cmds.setAttr('%s.occlusionMode' % (mirrorOccl), 2)
                    cmds.connectAttr('%s.outColor' % (mirrorOccl), '%s.reflectionColor' % (mirrorMtl))
                    cmds.connectAttr('%s.reflectionGlossiness' % (mirrorMtl), '%s.glossiness' % (mirrorOccl))          
                    mkbrdfTypeOffset = cmds.shadingNode('plusMinusAverage', asUtility=True, name='brdfOffset')
                    cmds.connectAttr('%s.brdfType' % (mirrorMtl), '%s.input1D[0]' % (mkbrdfTypeOffset))
                    cmds.setAttr('%s.input1D[1]' % (mkbrdfTypeOffset), 1)
                    cmds.connectAttr('%s.output1D' % (mkbrdfTypeOffset), '%s.occlusionMode' % (mirrorOccl))
                    cmds.connectAttr('%s.reflectionSubdivs' % (mirrorMtl), '%s.subdivs' % (mirrorOccl))
                ## creates relfection catching VrayMtl and VRay dirt for an RO

## example creation ##    
## createShadowCatcher = CreateCatchers('shadow') 
## createReflectionCatcher = CreateCatchers('reflection') 

class CreateRenderElements(object):
    def __init__(self,type):
        
        self.type = type
        
        if type.lower() == 'shadow':
            if not cmds.objExists('vrayRE_MatteShadow'):
                vfb.matteShadow('vrayRE_MatteShadow', enabled=False)
            ## creates cast shadow render element
            
        if type.lower() == 'contactshadow':
            if not cmds.objExists('vrayRE_ContactShadow'):
                if cmds.objExists('CONTACT_SHADOW_CATCHER'):
                    vfb.extraTex('vrayRE_ContactShadow', 'CONTACT_SHADOW_CATCHER', explicit_channel='contactShadow', enabled=False)
            ## creates contact shadow render element
            
        if type.lower() == 'fresnel':       
            if not cmds.objExists('vrayRE_Fresnel'):
                createFresnel = cmds.shadingNode('VRayFresnel', asTexture=True, name='VrayFresnel')
                createFresnelTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dFresnel')
                cmds.connectAttr('%s.outUV' % (createFresnelTwoD), '%s.uvCoord' % (createFresnel))
                cmds.connectAttr('%s.outUvFilterSize' % (createFresnelTwoD), '%s.uvFilterSize' % (createFresnel))
                vfb.extraTex('vrayRE_Fresnel', 'VrayFresnel', explicit_channel='fresnel', enabled=False)
            ## creates fresnel render element
        
        
## example creation ##   
## createShadowRE = CreateRenderElements('shadow')
## createShadowRE = CreateRenderElements('contactShadow')
## createFresnelRE = CreateRenderElements('fresnel')  

   
class PlateProject(object):
    
    def __init__(self):
    
        projectCam = 'shotcam1:shot_camera'
        if not cmds.objExists('plateProject'):
            projShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='plateProject')
            cmds.setAttr('%s.emitOnBackSide' % (projShader), 1)
            ## creates shader
            
            plateTexture = cmds.shadingNode('file', asTexture=True, name='plateTexture')
            cmds.setAttr('%s.defaultColor' % (plateTexture), 0,0,0, type='double3')
            cmds.setAttr('%s.useFrameExtension' % (plateTexture), 1)
            ## creates texture node
            
            fileProject = cmds.shadingNode('projection', asTexture=True, name='projectNodePlate') 
            cmds.setAttr('%s.projType' % (fileProject), 8)
            cmds.setAttr('%s.fitType' % (fileProject), 0)
            cmds.setAttr('%s.fitFill' % (fileProject), 1)
            cmds.setAttr('%s.defaultColor' % (fileProject), 0,0,0, type='double3')
            ## creates projection node
            
            twoD = cmds.shadingNode('place2dTexture', asUtility=True, name='PlatePlace2d')
            cmds.setAttr('%s.wrapU' % (twoD), 0)
            cmds.setAttr('%s.wrapV' % (twoD), 0)
            ## creates place2D for plate texture
            
            threeD = cmds.shadingNode('place3dTexture', asUtility=True, name='PlatePlace3d')
            ## creates place3D for camera
            
            cmds.connectAttr('%s.outColor' % (fileProject), '%s.color' % (projShader))
            cmds.connectAttr('%s.outColor' % (plateTexture), '%s.image' % (fileProject))
            cmds.connectAttr('%s.worldInverseMatrix' % (threeD), '%s.placementMatrix' % (fileProject))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityR' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityG' % (projShader))
            cmds.connectAttr('%s.outAlpha' % (fileProject), '%s.opacity.opacityB' % (projShader))
            ## connects texture, alpha, shader, projection, and 3D placement
                
            place2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in place2DConnections:
                cmds.connectAttr('%s.%s' % (twoD, x), '%s.%s' % (plateTexture, x))               
            cmds.connectAttr('%s.outUV' % (twoD), '%s.uv' % (plateTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (twoD), '%s.uvFilterSize' % (plateTexture))
            ## connects place2D for plate texture
                
            if cmds.objExists(projectCam):
                cmds.connectAttr('%s' % (projectCam) + 'Shape.message', '%s.linkedCamera' % (fileProject), f=True)
            ## connects shotcam to the proj cam if it exists

## example creation ##   
## createPlateProject = PlateProject()  
    
    
class CreateRefSphere(object):
    
    def __init__(self):
        
        if not cmds.objExists('greyBall'):
            diffBall = cmds.polySphere(name='greyBall', r=2.5)
            cmds.setAttr('%s.translateY' % (diffBall[0]), 6)
            cmds.delete(diffBall, ch=True)
            ## creates grey ball geo
        
        if not cmds.objExists('greyBallShader'):
            diffShader = cmds.shadingNode('VRayMtl', asShader=True, name='greyBallShader')
            diffShaderSG = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (diffShader) ,'%s.surfaceShader' % (diffShaderSG))
            cmds.setAttr('%s.useFresnel' % (diffShader), 0)
            cmds.setAttr('%s.color' % (diffShader),  0.18,0.18,0.18, type='double3')
            ## creates and assigns grey ball shader    
        
            cmds.sets(diffBall[0], e=True, forceElement=diffShaderSG)
            ## assigns  grey ball shader to geo
        
        if not cmds.objExists('chromeBall'):    
            refBall = cmds.polySphere(name='chromeBall', r=2.5)
            cmds.delete(refBall, ch=True)
            ## creates chrome ball geo
        
        if not cmds.objExists('chromeBallShader'):
            refShader = cmds.shadingNode('VRayMtl', asShader=True, name='chromeBallShader')
            refShaderSG = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (refShader) ,'%s.surfaceShader' % (refShaderSG))
            cmds.setAttr('%s.useFresnel' % (refShader), 0)
            cmds.setAttr('%s.color' % (refShader),  0, 0, 0, type='double3')
            cmds.setAttr('%s.reflectionColor' % (refShader),  1, 1, 1, type='double3')
            cmds.setAttr('%s.diffuseColorAmount' % (refShader),  0)
            cmds.setAttr('%s.reflectionsMaxDepth' % (refShader),  2)
            ## creates chrome ball shader
        
            cmds.sets(refBall[0], e=True, forceElement=refShaderSG)
            ## assigns chrome ball shader to geo
    
        colorChartTexturePath = '/jobs/asset_library/sequences/assets/common/pub/hdr_library/ColorChecker_linear_from_Avg_16bit.exr'
        ## color chart texture path
        
        if not cmds.objExists('colorChart'):    
            colorChart =  cmds.polyPlane(name='colorChart', h=5,w=5,sx=1,sy=1)
            cmds.setAttr('%s.translate' % (colorChart[0]), 7,3,0)
            cmds.setAttr('%s.rotateX' % (colorChart[0]), 90)
            ## creates color chart geo
        
        if not cmds.objExists('colorChartShader'):
            chartShader = cmds.shadingNode('VRayLightMtl', asShader=True, name='colorChartShader')
            chartShaderSG = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
            cmds.connectAttr('%s.outColor' % (chartShader) ,'%s.surfaceShader' % (chartShaderSG))
            cmds.setAttr('%s.emitOnBackSide' % (chartShader), 1)
            cmds.sets(colorChart[0], e=True, forceElement=chartShaderSG)
            ## creates color chart VrayLightMtl
        
        if not cmds.objExists('chartTexture'):
            chartTexture = cmds.shadingNode('file', asTexture=True, name='chartTexture')
            chartTwoD = cmds.shadingNode('place2dTexture', asUtility=True, name='chartPlace2d')    
            chart2DConnections = ('coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV',
                                  'offset', 'rotateUV', 'noiseUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne')                          
            for x in chart2DConnections:
                cmds.connectAttr('%s.%s' % (chartTwoD, x), '%s.%s' % (chartTexture, x))               
            cmds.connectAttr('%s.outUV' % (chartTwoD), '%s.uv' % (chartTexture))
            cmds.connectAttr('%s.outUvFilterSize' % (chartTwoD), '%s.uvFilterSize' % (chartTexture))
            cmds.connectAttr('%s.outColor' % (chartTexture), '%s.color' % (chartShader))
            ## creates and connects file texture node
            
            cmds.setAttr('%s.fileTextureName' % (chartTexture), colorChartTexturePath, type='string')
            ############ So dumb but I can't get the file tetxture path to fully eval without selecting the file node ###################
            cmds.select(chartTexture, r=True)
            ## feeds in colro chart texture path
        
        if not cmds.objExists('RefSphere_GRP'):
            refSetupGroupName = 'RefSphere_GRP'
            refSetupTransGroup = 'TranslateThis'
            refSetupGroupMembers = (colorChart[0], refBall[0], diffBall[0])
            translateGroup = cmds.group(refSetupGroupMembers, name=refSetupTransGroup)
            cmds.setAttr('%s.translate' % (translateGroup), -50, -25, -150)
            refSetupGroup = cmds.group(translateGroup, name=refSetupGroupName)
            shotCam = 'shotcam1:shot_camera'
            if cmds.objExists(shotCam):
                cmds.parentConstraint(shotCam, refSetupGroup, mo=False)
            ## creates groups and constrains to camera

## example creation ##   
## createRefSpheres = CreateRefSphere()


































   
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
