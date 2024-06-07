import os
import sys
import math
import string
import subprocess


if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

if 'darwin' in sys.platform:
    AVLSession = subprocess.Popen(["/Users/dong-gunjung/Desktop/CDTP1/ConceptualDesignTP1Py/ConceptualDesignTP1Py/avl335"],stdin=subprocess.PIPE, text=True)
else:
    AVLSession = subprocess.Popen(["avl.exe"],stdin=subprocess.PIPE, text=True)

def createAVLFile(name):
    0 #Do I really need this?

def createMassFile(name):
    0 #Do I really need this?

class runtime:
    def __init__(self,AVLnm,Massnm,Runnm):
        self.RunFileName = Runnm
        self.AVLFileName = AVLnm
        self.MassFileName = Massnm
        self.createRunFile()
    
    def createRunFile(self):
        RunFile = open(self.RunFileName,"w")
        #tbd
        RunFile.close()

    def modifyRunFile(self,var,value):
        RunFile = open(self.RunFileName,"r")
        #tbd
        RunFile.close()

        RunFile = open(self.RunFileName,"w")
        #tbd
        RunFile.close()


    def readRunFileName(self):
        return self.RunFileName
    
    def readAVLFileName(self):
        return self.AVLFileName
    
    def readMassFileName(self):
        return self.MassFileName
    
    def setRunFileName(self,input):
        self.RunFileName=input
    
    def setAVLFileName(self,input):
        self.AVLFileName=input
    
    def setMassFileName(self,input):
        self.MassFileName=input
    
    #--------------End of Class : runtime----------------------


# print("PLOP",file=avl.stdin)
# print("G",file=avl.stdin)
# print(file=avl.stdin)
# print("Quit",file=avl.stdin)


