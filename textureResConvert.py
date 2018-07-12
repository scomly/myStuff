
import glob
import os
import re
import subprocess

texturePath = '/jobs/ads/3d_library_J400233/build/resources/m_textures/SETS/megascans/'
getTextureFolderPath = os.listdir(texturePath)
setTexturePath = os.chdir(texturePath)

getFolders = glob.glob('*8K*')

for x in getFolders:
    textureFolder = texturePath + x
    getPath = os.listdir(textureFolder)
    chdir = os.chdir(textureFolder)
    getJpeg = glob.glob('*jpg*')
    print x

    for x in getJpeg:
        newName = x.replace('8','4')
        subprocess.call(["convert", x, "-resize", "4096x4096", newName])
        print x
