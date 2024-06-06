import os
import sys
import math
import string
import subprocess

def RunAVL():0

if 'darwin' in sys.platform:
    AVLSession = subprocess.Popen(["/Users/dong-gunjung/Desktop/CDTP1/ConceptualDesignTP1Py/ConceptualDesignTP1Py/avl335"],stdin=subprocess.PIPE, text=True)
else:
    AVLSession = subprocess.Popen(["avl.exe"],stdin=subprocess.PIPE, text=True)

def createAVLFile(name): 0

def createMassFile(name): 0

class runtime:
    def __init__(self,AVLnm,Massnm,Runnm):
        self.createRunFile(Runnm)
        AVLFileName = AVLnm
        MassFileName = Massnm
    
    def createRunFile(self): 0

    def modifyRunFile(self,var,value): 0
    
    def readAVLFileName(self):
        return self.AVLFileName
    
    def readMassFileName(self):
        return self.MassFileName
    



# print("PLOP",file=avl.stdin)
# print("G",file=avl.stdin)
# print(file=avl.stdin)
# print("Quit",file=avl.stdin)


