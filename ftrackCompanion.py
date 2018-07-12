from PySide import QtGui
from PySide import QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken
import os
import shadow

########################################################################
############################### GUI ####################################
########################################################################

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
    
class FTrackCompanion(QtGui.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(FTrackCompanion, self).__init__(parent)
                
        self.setWindowTitle("FTrack Companion")
        self.setWindowFlags(QtCore.Qt.Tool) # makes it a tool window so it will stay on top of maya
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # deletes UI when closed    
      
        ############################################################################
        self.getTaskListFunc()
        self.createLayout() # runs function below
                
    ################################################################################    
    ##################### Layout Creation ##########################################    
    ################################################################################
        
    def createLayout(self):
        
        layout = QtGui.QVBoxLayout() # main layout
        #self.setMinimumHeight(650)
        #self.setMinimumWidth(750)
        #layout.setSpacing(0)
        
        self.comboBox = QtGui.QComboBox()
        
        for task in self.taskDict.keys():
            self.comboBox.addItem(task)
        self.comboBox.currentIndexChanged.connect(self.getFunction)
        layout.addWidget(self.comboBox)
        
        ########### Output Window #################
        
        self.outWindow = QtGui.QTextEdit()
        self.outWindow.setReadOnly(True)
        layout.addWidget(self.outWindow)
        self.outWindow.setMaximumHeight(25)
        self.getFunction()
        
        #######################################################################################        
                
        self.setLayout(layout)
        
    ################################ MATTE SHADER OVERRIDE #########################################################
    
    def getFunction(self):
        self.comboBoxText = str(self.comboBox.currentText())
        getUserFromTask = self.taskDict[self.comboBoxText]
        self.outWindow.setText(getUserFromTask)
        #print self.taskDict[self.comboBoxText]
        
    ######################## FTrack Stuff ############################################################################
    
    def getTaskListFunc(self):       
        job = os.environ['MILL_EPISODE']
        scene = os.environ['MILL_SCENE']
        shot = os.environ['MILL_SHOT']
        #print job, scene, shot
        
        session = shadow.get_session(session_options={'cache':None})
        
        ft_shot = session.query('Shot where name is {shot_name} and parent.name is {scene_name} and project.name is {proj_name}'.format(shot_name=shot, scene_name=scene, proj_name=job)).first()        
        #print ft_shot
        
        shotLevelChildren = ft_shot["children"]
        
        self.taskDict = {}
        
        for a in shotLevelChildren:
            #print a.keys()
            taskName = a['name']
            #print taskName
            self.taskDict[taskName]= 'This task is unassigned'
            for i in a['assignments']:
                resource = i['resource']     
                #print resource.keys()
                userName = resource['username']
                #print userName
                firstName = resource['first_name']
                lastName = resource['last_name']
                if firstName:
                    wholeName = (firstName + ' ' + lastName + ' (' + userName + ')')
                    self.taskDict[taskName]= wholeName

    ######################## Close Event ############################################################
            
    def closeEvent(self,event):
        session.close()                
        
def launchUI():
    global FTrackCompanion
    
    # will try and close the ui if it exists
    try: FTrackCompanion.close()
    except: pass
    
    FTrackCompanion = FTrackCompanion()
    FTrackCompanion.show()
    FTrackCompanion.raise_()   
        
################## Show Window #######################################            
 
if __name__ == "__main__": 
    launchUI()
