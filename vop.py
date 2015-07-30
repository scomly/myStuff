#!/usr/bin/env python

"""
Library to create vrayObjectProperties
"""

import maya.cmds as cmds
import maya.mel as mel

def createObjectProperties(nodes_match, vray_obj_prop_name, object_id=0, recreate=False):
    mel.eval("vrayCreateVRaySettingsNode;")
    nodes = cmds.ls(nodes_match)
    if recreate and cmds.objExists(vray_obj_prop_name):
        cmds.delete(vray_obj_prop_name)
    if not nodes:
        print "No nodes match '%s'" % (nodes_match)
        return
    if not cmds.objExists(vray_obj_prop_name):
        vray_obj_prop_name = cmds.createNode("VRayObjectProperties", name=vray_obj_prop_name)
        cmds.connectAttr("%s.outConnect" % (vray_obj_prop_name), "vraySettings.vray_nodes_connect", nextAvailable=True)
    cmds.sets(nodes, add=vray_obj_prop_name)

    if object_id != 0:
        cmds.setAttr("%s.objectIDEnabled" % (vray_obj_prop_name), 1)
        cmds.setAttr("%s.objectID" % (vray_obj_prop_name), object_id)

    return vray_obj_prop_name

'''
import sys
sys.path.insert(0, "/home/bsweeney/python")
import vrayObjectProperties as vop
reload(vop)

node = "pSphere1"
vray_obj_prop_name = "sphere_props"
vop.createObjectProperties(node, vray_obj_prop_name)
'''

