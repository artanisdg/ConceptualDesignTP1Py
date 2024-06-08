import os, sys
import math
import string
import time
import numpy

gAcc = 9.80665 #m/s**2

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
        ACFT.HStab.Mass = ACFT.HStab.Mass * (1.05**2)
        ACFT.HStab.CoM[0] = ACFT.HStab.CoM[0] * 1.05
    elif option == 3: #VStab too small
        ACFT.VStab.Span = ACFT.VStab.Span * 1.05
        ACFT.VStab.RootChord = ACFT.VStab.Span * 1.05
        ACFT.VStab.TipChord = ACFT.VStab.Span * 1.05
        ACFT.VStab.Mass = ACFT.VStab.Mass * (1.05**2)
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
        self.CLArray = numpy.empty(shape=(17,4,18),dtype=float)
        self.CDArray = numpy.empty(shape=(17,4,18),dtype=float)
        self.CMArray = numpy.empty(shape=(17,4,18),dtype=float)
        self.NPArray = numpy.empty(shape=(17,4,18),dtype=float)
        cur_dir = os.getcwd()
        folder_path = os.path.join(cur_dir,fldr)
        if os.path.exists(folder_path):
            print("Session created, folder exists")
        else:
            try:
                os.mkdir(folder_path)
                print("Session created, folder made")
            except:    
                print("Session creation failed, folder not made")
                time.sleep(10)

    
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
    
    def readResult(self,Alpha,Flap,Elev,resP:str):
        try:
            resFile = open(self.Folder+"/"+resP,"r")
            resLines = resFile.readlines()
        except:
            print("file not found - a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
            time.sleep(2)
            return 1
            
        for line in resLines:
            line = line.strip()
            line = line.split('  ')
            k:list[str] = []
            for word in line:
                word = word.strip()
                word = word.strip('=')
                word = word.strip()
                if (word != '=') and (word != ''):
                    words = word.split('=')
                    k = k + words
            if k!=[]:
                line = k
            line = [word.strip() for word in line]
            l = len(line)
            if line[0] == "CLtot":
                self.CLArray[Alpha+2,round(Flap/2),5-Elev] = float(line[1])
                print("CLtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
            if line[0] == "CDtot":
                self.CDArray[Alpha+2,round(Flap/2),5-Elev] = float(line[1])
                print("CDtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
            if l > 2:
                if line[2] == "Cmtot":
                    self.CMArray[Alpha+2,round(Flap/2),5-Elev] = float(line[3])
                    print("Cmtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
                if line[1] == "Xnp":
                    self.NPArray[Alpha+2,round(Flap/2),5-Elev] = float(line[2])
                    print("XNP Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
        return 0
        
        
        

        
    def AeroAnalysis(self):#,CLArray:list[float],CDArray:list[float],):
        
    
        self.CreateFiles(self.ACFT.Name)

        for a in range(-2,15,1):
            for f in range(0,7,2):
                for e in range(5,-13,-1):
                    res:str = self.ACFT.Name+"-aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)
                    self.runSession(a,f,e,res)
                    time.sleep(0.5)
                    
            time.sleep(5)
        
        time.sleep(10)

        for a in range(-2,15,1):
            for f in range(0,7,2):
                for e in range(5,-13,-1):
                    res:str = self.ACFT.Name+"-Aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)
                    i = 0
                    while 1:
                        if self.readResult(a,f,e,res) == 0:
                            break
                        else:
                            if i>5:
                                print("file read abort - a:"+str(a)+" F:"+str(f)+" e:"+str(e))
                                break
                            else:
                                time.sleep(1.5)
                                i += 1
                            

    def TOAnalysis(self,ACFT:Acft.Aircraft,AVLrt:AVLF.runtime,resFolder:str):
        self.Mach = 0.212
        self.rho = self.rhoSet[0]
        
        Friction = ACFT.Mass*0.01.gAcc
        
        Cref = (Acft.Wing.RootChord+Acft.Wing.TipChord)/2
        Sref = Cref*ACFT.Wing.SpanHalf*2

        for f in range(0,7,2):
            #TO Speed Determination
            a = 12    
            CLv2 = self.CLArray[a+2,round(f/2),0]
            Lvsc = 0.5*CLv2*self.rho*Sref
                
            vs=numpy.sqrt(ACFT.Mass/Lvsc)
            v2 = 1.2*vs
            
            Lv2 = 0.5*CLv2*(v2**2)*self.rho*Sref

            #TO Run Analysis
            CL = self.CLArray[0,round(f/2),0]
            CD = self.CDArray[0,round(f/2),0]
            
            DragC = 0.5*CD*self.rho*Sref
            
            Thrust = 0
            
            F = Thrust - (DragC + Friction)
            
            TOEk = 0.5 * ACFT.Mass * (v2**2)
            
            TODR = TOEk / F
            
            if TODR > 

            V = numpy.sqrt((F*762)/(ACFT.Mass*0.5))

            #TO Rotation Analysis
            for a in range(0,10,1):
                ElevPull = 0
                for e in range(1,-13,-1):
                    if self.CMArray[a+2,round(f/2),5-e]:
                        

        MaxMach = 0.212
    
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
