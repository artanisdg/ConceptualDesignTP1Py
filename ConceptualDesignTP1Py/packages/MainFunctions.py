import os
import sys
import math
import string
import time
import numpy

gAcc = 9.80665 #m/s^2

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft

def initSizing(avl:AVLF.runtime,ACFT:Acft.Aircraft,pth:string,res:int):
    ACFT.ReadFromTxt(pth)
    setBattery(ACFT,200,5000,0.66)
    ACFT.CalcCoM()
    Acft.WriteACtoFile(ACFT,avl,res,0.42)

def setBattery(ACFT:Acft.Aircraft,DensityWhkg,WhReq,WingBatteryRatio:float):
    BattGW = WhReq/DensityWhkg
    BattWing = BattGW*WingBatteryRatio
    BattBody = BattGW*(1-WingBatteryRatio)
    ACFT.Battery.Mass.L = BattWing/2
    ACFT.Battery.Mass.R = BattWing/2
    ACFT.Battery.Mass.F = BattBody
    ACFT.Wing.Mass = ACFT.Wing.Mass + ACFT.Battery.Mass.F * 0.025

def resizeAC(ACFT:Acft.Aircraft,option:int):
    if   option == 1: #CL too low
        ACFT.Wing.SpanHalf = ACFT.Wing.SpanHalf * 1.05
        ACFT.Wing.Mass = ACFT.Wing.Mass * 1.08
    #elif option == 99: #CL excessive
    #    0#tbd
    elif option == 2: #HStab too small
        ACFT.HStab.SpanHalf = ACFT.HStab.SpanHalf * 1.05
        ACFT.HStab.RootChord = ACFT.HStab.RootChord * 1.05
        ACFT.HStab.TipChord = ACFT.HStab.TipChord * 1.05
        ACFT.HStab.Mass = ACFT.HStab.Mass * (1.05^2)
        ACFT.HStab.CoM[0] = ACFT.HStab.CoM[0] * 1.05
    elif option == 3: #VStab too small
        ACFT.VStab.Span = ACFT.VStab.Span * 1.05
        ACFT.VStab.RootChord = ACFT.VStab.Span * 1.05
        ACFT.VStab.TipChord = ACFT.VStab.Span * 1.05
        ACFT.VStab.Mass = ACFT.VStab.Mass * (1.05^2)
        ACFT.VStab.CoM[0] = ACFT.VStab.CoM[0] * 1.05
    elif option == 4: #CG too fwd, Shift Battery CoM
        ACFT.Battery.CoM.F[0] = ACFT.Battery.CoM.F[0] + 0.5
    elif option == 5: #CG too aft, Shift Battery CoM
        ACFT.Battery.CoM.F[0] = ACFT.Battery.CoM.F[0] - 0.5
    elif option == 11: #CL too low - increase chord
        ACFT.Wing.RootChord = ACFT.Wing.RootChord * 1.05
        ACFT.Wing.Mass = ACFT.Wing.Mass * 1.05 + ACFT.Wing.BattMass
    elif option == 12: #HStab ineffective -> Move Further Back
        ACFT.HStab.AttachPos[0] = ACFT.HStab.AttachPos[0] + 0.3
    else:
        print("resizeAC Function Call Error")
    ACFT.CalcCoM()
    

def setupAVL(RTime:AVLF.runtime):
    avlF = RTime.readAVLFileName()
    masF = RTime.readMassFileName()
    runF = RTime.readRunFileName()

    RTime.AVLcommand(("LOAD "+avlF))
    RTime.AVLcommand(("MASS "+masF))
    RTime.AVLcommand(("MSET 0"))

def operAVL(RTime:AVLF.runtime,Alpha,Flap,Elevator,resPath:str):
    RTime.AVLcommand("OPER")
    RTime.AVLcommand("O")
    RTime.AVLcommand("V")
    RTime.AVLreturn()
    if Alpha != 0:
        RTime.AVLcommand("A A "+str(Alpha))
    if Flap != 0:
        RTime.AVLcommand("D1 D1 "+str(Flap))
    if Elevator != 0:
        RTime.AVLcommand("D3 D3 "+str(Elevator))
    RTime.AVLcommand("X")
    RTime.AVLcommand("st")
    RTime.AVLcommand(resPath)
    RTime.AVLreturn()
    RTime.AVLreturn()
    RTime.AVLcommand("Quit")

def analyzeAero():
    0 #tbd

def analyzePerf():
    0 #tbd
    
class LimitationData:
    ReqEnergy:float #in Wh
    MaxThrust:float #in N
    MaxPower:float #in W
    ThrustEfficiency:float #in floating point (Eprop * Emotor)

class Session:
    AVLrt:AVLF.runtime
    ACFT:Acft.Aircraft
    Folder:str
    Mach = 0.42
    VmpsT = 245/1.94384 #245KTAS in m/s
    Alt = 30000/3.28084 #inMeters
    rhoSet = [1.225,0.90464,0.65269,0.45831]
    
    rhoAlt = Alt*3.28084/10000
    rho = float(rhoSet[3])
    
    CLArray = numpy.empty(shape=(17,4,18),dtype=float)
    CDArray = numpy.empty(shape=(17,4,18),dtype=float)
    CMArray = numpy.empty(shape=(17,4,18),dtype=float)
    NPArray = numpy.empty(shape=(17,4,18),dtype=float)
    
    def __init__(self,avl:AVLF.runtime,Ac:Acft.Aircraft,fldr:str):
        self.AVLrt = avl
        self.ACFT = Ac
        self.Folder = fldr
    
    def ChangeFolder(self,fldr:str):
        self.Folder = fldr
        self.AVLrt.setAVLFileName(fldr+self.AVLrt.readAVLFileName())
        self.AVLrt.setMassFileName(fldr+self.AVLrt.readMassFileName())
    
    def CreateFiles(self,name:str):
        self.AVLrt.setAVLFileName(self.Folder+"/"+name+".avl")
        self.AVLrt.setMassFileName(self.Folder+"/"+name+".mass")
        Acft.WriteACtoFile(self.ACFT,self.AVLrt,20,self.Mach)
        
    def runSession(self,Alpha,Flap,Elev,resP:str):
        self.AVLrt.reStartAVL()
        setupAVL(self.AVLrt)
        operAVL(self.AVLrt,Alpha,Flap,Elev,self.Folder+"/"+resP)
        
    def AeroAnalysis(self):#,CLArray:list[float],CDArray:list[float],):
        
    
        self.CreateFiles(self.ACFT.Name)

        for a in range(-2,15,1):
            for f in range(0,7,2):
                for e in range(5,-13,-1):
                    res:str = self.ACFT.Name+"-Aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)
                    self.runSession(a,f,e,res)
                    time.sleep(0.5)
            time.sleep(5)
                

def TOAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resFolder:str):
    MaxMach = 0.212
    TOSession = Session(MaxMach,140,0,AVLrt,ACFT,resFolder)
    
    Friction = ACFT.Mass*0.01*gAcc
    

    
def CLBAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resPath:str):
    CLBSession = Session(0.42,170,10000)
    
    for i in range(0,20):
        0 #tbd
    
    AVLrt.reStartAVL()
    operAVL(AVLrt,resPath)


def CRZAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resPath:str):
    CRZSession = Session(0.42,245,30000)
    
    AVLrt.reStartAVL()
    operAVL(AVLrt,resPath)
    
    
def DESAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resPath:str):
    DESSession = Session(0.42,220,30000)
    
    for i in range(0,20):
        0 #tbd
        
    AVLrt.reStartAVL()
    operAVL(AVLrt,resPath)
    
def LDGAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resPath:str):
    LDGSession = Session(0.42,135,0)
    
    Friction = ACFT.Mass*0.01*gAcc
    
    for i in range(0,20):
        0 #tbd
    
    AVLrt.reStartAVL()
    operAVL(AVLrt,resPath)


def TaxiAnalysis(ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resPath:str):
    Friction = ACFT.Mass*0.01*gAcc

    AVLrt.reStartAVL()
    operAVL(AVLrt,resPath)
