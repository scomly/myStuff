
import maya.cmds as cmds
import maya.mel as mel

def createVrayFramebuffer(node_name, framebuffer_type):
    if cmds.objExists(node_name): cmds.delete(node_name)
    command = 'vrayAddRenderElement %s;\n' % (framebuffer_type)
    node = mel.eval(command)
    node = cmds.rename(node, node_name)
    return node

def coverage(node_name):
    createVrayFramebuffer(node_name, "CoverageChannel")

def extraTex(node_name, texture, consider_aa=1, affect_matte=0, filter=1, explicit_channel=None, enabled=True):
    '''
    Texture: input texture
    consider_aa
    affect_matte
    filtering
    '''
    createVrayFramebuffer(node_name, "ExtraTexElement")
    out_attr = None
    if cmds.objExists("%s.outColor" % (texture)):
        out_attr = "%s.outColor" % (texture)
    elif cmds.objExists("%s.output" % (texture)):
        out_attr = "%s.output" % (texture)

    if out_attr:
        cmds.connectAttr(out_attr, "%s.vray_texture_extratex" % (node_name), force=True)
    cmds.setAttr("%s.vray_considerforaa_extratex" % (node_name), consider_aa)
    cmds.setAttr("%s.vray_affectmattes_extratex" % (node_name), affect_matte)
    cmds.setAttr("%s.vray_filtering_extratex" % (node_name), filter)
    if explicit_channel:
        cmds.setAttr("%s.vray_explicit_name_extratex" % (node_name), explicit_channel, type="string")
    cmds.setAttr("%s.enabled" % (node_name), enabled)

def extraTexIsolated(node_name, texture_geo_pair_list, **kwdict):
    switch_name = "%s_switch" % (node_name)
    if cmds.objExists(switch_name): cmds.delete(switch_name)
    cmds.shadingNode("tripleShadingSwitch", asUtility=True, name=switch_name)
    input = 0
    for [texture, geo] in texture_geo_pair_list:
        if cmds.nodeType(geo) == "transform":
            shape = cmds.listRelatives(geo, shapes=True)[0]
        else:
            shape = geo
        cmds.connectAttr("%s.instObjGroups[0]" % (shape), "%s.input[%d].inShape" % (switch_name, input), force=True)
        cmds.connectAttr("%s.outColor" % (texture), "%s.input[%d].inTriple" % (switch_name, input), force=True)
        input += 1
    # set default color to black
    cmds.setAttr("%s.default" % (switch_name), 0, 0, 0, type="double3")
    extraTex(node_name, switch_name, **kwdict)

def sss(node_name):
    createVrayFramebuffer(node_name, "FastSSS2Channel")

def lightSelect(node_name, light, select_type="normal"):
    LIGHT_NORMAL = 0
    LIGHT_RAW = 1
    LIGHT_DIFF = 2
    LIGHT_SPEC = 3
    createVrayFramebuffer(node_name, "LightSelectElement")
    if select_type.lower().startswith("diff"):
        cmds.setAttr("%s.vray_type_lightselect" % (node_name), LIGHT_DIFF)
    elif select_type.lower().startswith("spec"):
        cmds.setAttr("%s.vray_type_lightselect" % (node_name), LIGHT_SPEC)
    elif select_type.lower().startswith("raw"):
        cmds.setAttr("%s.vray_type_lightselect" % (node_name), LIGHT_RAW)
    elif select_type.lower().startswith("normal"):
        cmds.setAttr("%s.vray_type_lightselect" % (node_name), LIGHT_NORMAL)
    cmds.setAttr("%s.vray_name_lightselect" % (node_name), node_name, type="string")

def materialSelect(node_name):
    createVrayFramebuffer(node_name, "MaterialSelectElement")

def multiMatte(node_name, matte_name, red=0, blue=0, green=0, consider_for_aa=1, affect_matte=0, material_ids=0):
    createVrayFramebuffer(node_name, "MultiMatteElement")
    cmds.setAttr("%s.vray_redid_multimatte" % (node_name), red)
    cmds.setAttr("%s.vray_greenid_multimatte" % (node_name), green)
    cmds.setAttr("%s.vray_blueid_multimatte" % (node_name), blue)
    cmds.setAttr("%s.vray_name_multimatte" % (node_name), matte_name, type="string")
    cmds.setAttr("%s.vray_affectmattes_multimatte" % (node_name), affect_matte)
    cmds.setAttr("%s.vray_usematid_multimatte" % (node_name), material_ids)
    cmds.setAttr("%s.vray_considerforaa_multimatte" % (node_name), consider_for_aa)

def atmosphere(node_name):
    createVrayFramebuffer(node_name, "atmosphereChannel")

def background(node_name):
    createVrayFramebuffer(node_name, "backgroundChannel")

def bumpNormals(node_name):
    createVrayFramebuffer(node_name, "bumpNormalsChannel")

def caustics(node_name):
    createVrayFramebuffer(node_name, "causticsChannel")

def diffuse(node_name):
    createVrayFramebuffer(node_name, "diffuseChannel")

def drBucker(node_name):
    createVrayFramebuffer(node_name, "drBucketChannel")

def gi(node_name):
    createVrayFramebuffer(node_name, "giChannel")

def lighting(node_name):
    createVrayFramebuffer(node_name, "lightingChannel")

def materialID(node_name, suffix=None):
    createVrayFramebuffer(node_name, "materialIDChannel")
    if suffix:
        cmds.setAttr("%s.vray_filename_mtlid" % (node_name), suffix)

def matteShadow(node_name):
    createVrayFramebuffer(node_name, "matteShadowChannel")

def nodeId(node_name):
    createVrayFramebuffer(node_name, "nodeIDChannel")

def normals(node_name):
    createVrayFramebuffer(node_name, "normalsChannel")

def rawGi(node_name):
    createVrayFramebuffer(node_name, "rawGiChannel")

def rawLight(node_name):
    createVrayFramebuffer(node_name, "rawLightChannel")

def rawReflection(node_name):
    createVrayFramebuffer(node_name, "rawReflectionChannel")

def rawRefraction(node_name):
    createVrayFramebuffer(node_name, "rawRefractionChannel")

def rawShadow(node_name):
    createVrayFramebuffer(node_name, "rawShadowChannel")

def rawTotalLight(node_name):
    createVrayFramebuffer(node_name, "rawTotalLightChannel")

def reflect(node_name):
    createVrayFramebuffer(node_name, "reflectChannel")

def reflectionFilter(node_name):
    createVrayFramebuffer(node_name, "reflectionFilterChannel")

def refract(node_name):
    createVrayFramebuffer(node_name, "refractChannel")

def refractionFilter(node_name):
    createVrayFramebuffer(node_name, "refractionFilterChannel")

def renderId(node_name):
    createVrayFramebuffer(node_name, "renderIDChannel")

def sampleRate(node_name):
    createVrayFramebuffer(node_name, "sampleRateChannel")

def selfIllum(node_name):
    createVrayFramebuffer(node_name, "selfIllumChannel")

def shadow(node_name):
    createVrayFramebuffer(node_name, "shadowChannel")

def specular(node_name):
    createVrayFramebuffer(node_name, "specularChannel")

def totalLight(node_name):
    createVrayFramebuffer(node_name, "totalLightChannel")

def velocity(node_name):
    createVrayFramebuffer(node_name, "velocityChannel")

def depth(node_name="vrayRE_Depth"):
    createVrayFramebuffer(node_name, "zdepthChannel")
    cmds.setAttr("%s.vray_filtering_zdepth" % (node_name), 1)
    cmds.setAttr("%s.vray_depthClamp" % (node_name), 0)
    cmds.setAttr("%s.vray_depthWhite" % (node_name), 1)
    cmds.setAttr("%s.vray_depthBlack" % (node_name), 0)
    cmds.setAttr("%s.vray_depthFromCamera_zdepth" % (node_name), 0)

'''
import sys
sys.path.insert(0, "/home/bsweeney/SRC/atlas/lib/maya/scripts/py")
import vrayFrameBuffers as vfb
reload(vfb)

vfb.extraTex("ramp_extra_tex", "ramp1")
'''

