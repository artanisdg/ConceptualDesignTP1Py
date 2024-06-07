import os, sys, signal
import math
import string
import subprocess


if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

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
        self.AVLSession = self.StartAVL()
    
    def StartAVL(self):
        if 'darwin' in sys.platform:
            return subprocess.Popen(["/Users/dong-gunjung/Desktop/CDTP1/ConceptualDesignTP1Py/ConceptualDesignTP1Py/avl335"],stdin=subprocess.PIPE, text=True)
        else:
            return subprocess.Popen(["avl.exe"],stdin=subprocess.PIPE, text=True)

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
        
    def AVLcommand(self,cmd:str):
        print(cmd,file=self.AVLSession.stdin)
    
    def AVLreturn(self):
        print(file=self.AVLSession.stdin)
        
    #--------------End of Class : runtime----------------------
