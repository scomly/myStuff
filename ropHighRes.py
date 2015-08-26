sourceRop = hou.selectedNodes()

for x in sourceRop:
    x.parm('vm_samplesx').set(9)
    x.parm('vm_samplesy').set(9)
    x.parm('vm_maxraysamples').set(9)
    x.parm('vm_variance').set(0.03)
    x.parm('allowmotionblur').set(1)
    x.parm('override_camerares').set(0)
