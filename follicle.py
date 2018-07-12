def prFollicleOnFace():
    # create follicle on selected face(s)
    import pymel.core as pm
    import maya.mel as mm
    
    sel = pm.ls(sl=1, fl=1)
    fols = []
    for eachFace in sel:
    # errorcheck
        if( not eachFace.hasUVs() ):
            mm.eval( 'warning "this face has no uvs: '+eachFace+'"' )
        # get geom
        meshName = str(eachFace)[:eachFace.find('.')]
        faceIndex = str(eachFace)[ eachFace.find('[')+1 : eachFace.find(']') ]
        geoMesh = pm.PyNode( meshName )
        # average UV
        uvs = eachFace.getUVs()
        averageU = float(sum(uvs[0])) / len(uvs[0])
        averageV = float(sum(uvs[1])) / len(uvs[1])
        # creat follicle
        fol = pm.createNode( 'follicle' )
        fol.parameterU.set( averageU )
        fol.parameterV.set( averageV )
        folP = fol.getParent()
        folP.rename( 'fol_'+geoMesh.getParent()+'_'+faceIndex )
        # connect
        geoMesh.outMesh >> fol.inputMesh
        geoMesh.worldMatrix[0] >> fol.inputWorldMatrix
        fol.outTranslate >> folP.translate
        fol.outRotate >> folP.rotate
        # save
        fols.append( folP )
        # select all created follicles
        pm.select( fols )
        # call def
prFollicleOnFace()
