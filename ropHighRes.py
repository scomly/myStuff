sourceRop = hou.selectedNodes()[0]


sourceRop.parm('vm_samplesx').set(9)
sourceRop.parm('vm_samplesy').set(9)
sourceRop.parm('vm_variance').set(0.03)
sourceRop.parm('allowmotionblur').set(1)
sourceRop.parm('override_camerares').set(0)
