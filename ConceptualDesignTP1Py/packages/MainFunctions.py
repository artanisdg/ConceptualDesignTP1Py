import os, sys
import math
import string
import time
from tkinter import ROUND
import numpy

gAcc = 9.80665 #m/s**2

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft

def initSizing(avl:AVLF.runtime,ACFT:Acft.Aircraft,pth:string,res:int):
    ACFT.ReadFromTxt(pth)
    setBattery(ACFT,200,4000,0.66)
    ACFT.CalcCoM()
    Acft.WriteACtoFile(ACFT,avl,res,0.42)

def setBattery(ACFT:Acft.Aircraft,DensityWhkg,kWhReq,WingBatteryRatio:float):
    BattGW = kWhReq*1000/DensityWhkg
    BattWing = BattGW*WingBatteryRatio
    BattBody = BattGW*(1-WingBatteryRatio)
    ACFT.Battery.Mass.L = BattWing/2
    ACFT.Battery.Mass.R = BattWing/2
    ACFT.Battery.Mass.F = BattBody
    ACFT.Wing.Mass = ACFT.Wing.Mass + ACFT.Battery.Mass.F * 0.025
    
    ACFT.Battery.CoM.R[0] = ACFT.Wing.AttachPos[0] + ACFT.Wing.CoM[0]
    ACFT.Battery.CoM.R[1] = ACFT.Wing.AttachPos[1] + ACFT.Wing.CoM[1]
    ACFT.Battery.CoM.R[2] = ACFT.Wing.AttachPos[2] + ACFT.Wing.CoM[2]

    ACFT.Battery.CoM.L[0] = ACFT.Wing.AttachPos[0] + ACFT.Wing.CoM[0]
    ACFT.Battery.CoM.L[1] = (-1)*ACFT.Wing.AttachPos[1] - ACFT.Wing.CoM[1]
    ACFT.Battery.CoM.L[2] = ACFT.Wing.AttachPos[2] + ACFT.Wing.CoM[2]

    ACFT.Battery.CoM.F[0] = ACFT.Fuselage.CoM[0]
    ACFT.Battery.CoM.F[1] = ACFT.Fuselage.CoM[1]
    ACFT.Battery.CoM.F[2] = ACFT.Fuselage.CoM[2]
    print("Battery Calculation Complete")


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
        ACFT.Fuselage.CoM[0] = ACFT.Fuselage.CoM[0] + 0.10*0.5*(ACFT.Wing.RootChord+ACFT.Wing.TipChord)
    elif option == 5: #CG too aft, Shift Battery CoM
        ACFT.Battery.CoM.F[0] = ACFT.Battery.CoM.F[0] - 0.5
        ACFT.Fuselage.CoM[0] = ACFT.Fuselage.CoM[0] - 0.10*0.5*(ACFT.Wing.RootChord+ACFT.Wing.TipChord)
    elif option == 6: #Thrust insufficient
        0
    elif option == 11: #CL too low - increase chord
        ACFT.Wing.RootChord = ACFT.Wing.RootChord * 1.05
        ACFT.Wing.Mass = ACFT.Wing.Mass * 1.05 + ACFT.Wing.BattMass
    elif option == 12: #HStab ineffective -> Move Further Back
        ACFT.HStab.AttachPos[0] = ACFT.HStab.AttachPos[0] + 0.3
    elif option == 14: #trim too down, trim up
        ACFT.HStab.Ainc = ACFT.HStab.Ainc - 0.25
    elif option == 15: #trim too up, trim down
        ACFT.HStab.Ainc = ACFT.HStab.Ainc + 0.25
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
    
    if os.path.exists(resPath):
        os.remove(resPath)
    else:
        print("The Result file \""+resPath+"\" Does not yet exist")

    RTime.AVLcommand("st")
    RTime.AVLcommand(resPath)
    RTime.AVLreturn()
    RTime.AVLreturn()
    RTime.AVLcommand("Quit")

def analyzeAero():
    0 #tbd

def analyzePerf():
    0 #tbd
    
class PackageData:
    def __init__(self,file:str):
        file = open(file,'r')
        linesTemp = file.readlines()
        for line in linesTemp:
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
            k = []
            for word in line:
                word = word.strip()
                word = word.strip('=')
                word = word.strip()
                if (word != ',') and (word != ''):
                    words = word.split(',')
                    k = k + words
            if k!=[]:
                line = k
            line = [word.strip() for word in line]
            l = len(line)
            if line[0] == "ReqEnergyTO":
                self.ReqEnergy[0] = float(line[1])
            if line[0] == "ReqEnergyCLB":
                self.ReqEnergy[1] = float(line[1])
            if line[0] == "ReqEnergyCRZ":
                self.ReqEnergy[2] = float(line[1])
            if line[0] == "ReqEnergyDES":
                self.ReqEnergy[3] = float(line[1])
            if line[0] == "ReqEnergyTAXI":
                self.ReqEnergy[4] = float(line[1])
            if line[0] == "MaxThrust":
                self.MaxThrust = float(line[1])
            if line[0] == "MaxPower":
                self.MaxPower = float(line[1])
            if line[0] == "ThrustEfficiency":
                self.ThrustEfficiency = float(line[1])
            if line[0] == "AoARange":
                self.AoAmin = int(line[1])
                self.AoAMax = int(line[2])
            if line[0] == "FlapRange":
                self.Flapmin = int(line[1])
                self.FlapMax = int(line[2])
            if line[0] == "ElevRange":
                self.ElevFU = int(line[1])
                self.ElevFD = int(line[2])
        

    ReqEnergy:list[float] = numpy.empty(shape=(5),dtype=float) #in Wh
    MaxThrust:float = 0 #in N
    MaxPower:float = 0 #in W
    ThrustEfficiency:float = 0 #in floating point (Eprop * Emotor)

    AoAmin:int
    AoAMax:int
    Flapmin:int
    FlapMax:int
    ElevFU:int
    ElevFD:int
    
    TOFlap:float = 0 #in deg
    VsTO:float = 0 #in m/s
    V2:float = 0 #in m/s
    TODR:float = 0 #in m

    CLBRate:float = 0 #in m/s
    CLBAoA:float = 0 #in deg
       
    Vref:float = 0 #in m/s
    LDR:float = 0 #in m
    



class Session:
    AVLrt:AVLF.runtime
    ACFT:Acft.Aircraft
    DATA:PackageData
    Folder:str
    

    iteration = 0

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
                
        self.DATA = PackageData(self.Folder+"/"+Ac.Name+"_DATA.txt")
        initSizing(avl,Ac,self.Folder+"/"+Ac.Name+"_AC.txt",20)
        
        self.iteration = 0

    
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
                self.CLArray[Alpha-self.DATA.AoAmin,round(Flap/2),self.DATA.ElevFD-Elev] = float(line[1])
                print("CLtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
            if line[0] == "CDtot":
                self.CDArray[Alpha-self.DATA.AoAmin,round(Flap/2),self.DATA.ElevFD-Elev] = float(line[1])
                print("CDtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
            if l > 2:
                if line[2] == "Cmtot":
                    self.CMArray[Alpha-self.DATA.AoAmin,round(Flap/2),self.DATA.ElevFD-Elev] = float(line[3])
                    print("Cmtot Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
                if line[1] == "Xnp":
                    self.NPArray[Alpha-self.DATA.AoAmin,round(Flap/2),self.DATA.ElevFD-Elev] = float(line[2])
                    print("XNP Read"+" a:"+str(Alpha)+" F:"+str(Flap)+" e:"+str(Elev))
        return 0
        
        
    def writeSTABMessage(self,message:list[str]):
        file = open(self.Folder+"/Output/STABData-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / STAB\n")
        file.write("----------------------------------------------------\n")

        file.writelines(message)
        
        file.close()        

    def writeTOData(self):
        file = open(self.Folder+"/Output/TOData-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / TO\n")
        file.write("----------------------------------------------------\n")

        lines:list[str] = []
        lines = ["TO Flap : "+str(self.DATA.TOFlap)]
        lines = ["VsTO : "+str(self.DATA.VsTO)+"\n"]
        lines = lines + ["V2 : "+str(self.DATA.V2)+"\n"]
        lines = lines + ["TODR : "+str(self.DATA.TODR)+"\n"]
        
        file.writelines(lines)
        
        file.close()


    def writeTOMessage(self,message:list[str]):
        file = open(self.Folder+"/Output/TOData-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / TO\n")
        file.write("----------------------------------------------------\n")

        file.writelines(message)
        
        file.close()

    def writeCLBData(self):
        file = open(self.Folder+"/Output/CLBData-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / CLB\n")
        file.write("----------------------------------------------------\n")

        lines:list[str] = []
        lines = ["CLB Rate : "+str(self.DATA.CLBRate)+"\n"]
        lines = lines + ["CLB AoA : "+str(self.DATA.CLBAoA)+"\n"]
        
        file.writelines(lines)
        
        file.close

        
    def AeroAnalysis(self):
        
    
        self.CreateFiles(self.ACFT.Name)

        for a in range(self.DATA.AoAmin,self.DATA.AoAMax+1,1):
            for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
                for e in range(self.DATA.ElevFD,self.DATA.ElevFU-1,-1):
                    res:str = self.ACFT.Name+"-aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)
                    self.runSession(a,f,e,res)
                    time.sleep(0.5)
                    
            time.sleep(5)
        
        time.sleep(10)

        for a in range(self.DATA.AoAmin,self.DATA.AoAMax+1,1):
            for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
                for e in range(self.DATA.ElevFD,self.DATA.ElevFU-1,-1):
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
        self.iteration += 1                                
    
    def StabAnalysis(self):
        STABFolder = self.Folder + "/Output"
        if os.path.exists(STABFolder):
            print("STABDATA folder exists")
        else:
            try:
                os.mkdir(STABFolder)
                print("STABDATA folder made")
            except:    
                print("STABDATA folder creation failed")

        for a in range(self.DATA.AoAmin,3+1,1):
            for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-3]>0:
                    msg = ["CG Too Far Back\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0])+"\n"]
                    print(msg)
                    self.writeSTABMessage(msg)

                    return 5
                
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-5)]<-0:
                    msg = ["CG Too Far Forward\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-5)])+"\n"]
                    print(msg)
                    self.writeSTABMessage(msg)
                    
                    return 4

                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-2]>0.1:
                    msg = ["trim down required\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-2])+"\n"]
                    print(msg)
                    self.writeSTABMessage(msg)
                    
                    return 15
                
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-2)]<-0.1:
                    msg = ["trim up required\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-2)])+"\n"]
                    print(msg)
                    self.writeSTABMessage(msg)

                    return 14
                
        for a in range(4,self.DATA.AoAMax+1,1):
            for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]>0:
                    msg = ["CG Too Far Back\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0])+"\n"]
                    print(msg)
                    self.writeSTABMessage(msg)

                    return 5


        return 0

        
        

    def TOAnalysis(self):
        self.Mach = 0.212
        self.rho = self.rhoSet[0]
        
        Friction = self.ACFT.Mass*0.01*gAcc
        
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2

        for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
            #TO Speed Determination
            a = 12    
            CLv2 = self.CLArray[a-self.DATA.AoAMin,round(f/2),0]
            Lvsc = 0.5*CLv2*self.rho*Sref
                
            self.DATA.VsTO=numpy.sqrt(self.ACFT.Mass/Lvsc)
            self.DATA.V2 = 1.2*self.DATA.VsTO
            
            Lv2 = 0.5*CLv2*(self.DATA.V2**2)*self.rho*Sref

            #TO Run Analysis
            CL = self.CLArray[0,round(f/2),0]
            CD = self.CDArray[0,round(f/2),0]
            v = 0
            t = 0
            d = 0
            while 1:
                Drag = 0.5*CD*(v**2)*self.rho*Sref
                F = self.DATA.MaxThrust - (Friction + Drag)
                v = v + F/self.ACFT.Mass
                t = t + 1
                d = d + v
                if v > self.DATA.V2:
                    if d<762:
                        self.DATA.TODR = d
                        break
                    else:
                        print("TODR > TODA")

                        return 1
                elif d>762:
                    print("TO Failed : Thrust Insufficient")

                    return 6
                    
            
            #TO Energy Analysis            
            self.DATA.ReqEnergy[0] = self.DATA.MaxThrust*self.DATA.TODR/self.DATA.ThrustEfficiency/3600
            

            TOFolder = self.Folder + "/Output"
            if os.path.exists(TOFolder):
                print("TODATA folder exists")
            else:
                try:
                    os.mkdir(TOFolder)
                    print("TODATA folder made")
                except:    
                    print("TODATA folder creation failed")

            self.writeTOData()
            return 0
            

    def CLBAnalysis(self):
        self.Mach = 0.42
        self.VmpsT = 170/1.94384
        self.rho = self.rhoSet[1]
        
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2
        
        Vclb = self.VmpsT
        VVref = 900*0.00508
        VVclb = 0
        elev = 0
        
        Thrust = 0
        Thrust1 = self.DATA.MaxThrust
        Thrust2 = self.DATA.MaxPower*3600/Vclb
        
        if(Thrust1 < Thrust2):
            Thrust = Thrust1
        else:
            Thrust = Thrust2
        
        for a in range(10,-1,-1):
            for e in range(5,-13,-1):
                CL = self.CLArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                CD = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                CM = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                
                if e > -12:
                    CMm1 = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-(e-1)]
                else:
                    CMm1 = CM
                if e < 5:
                    CMp1 = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-(e+1)]
                else:
                    CMp1 = CM
                    
                if (CMm1 > 0) and (CMp1 < 0):
                    elev = e
                    L = 0.5*CL*(Vclb**2)*self.rho*Sref
                
                    if L > self.ACFT.Mass:
                        VVclb2 = Vclb*numpy.sin(numpy.arccos(self.ACFT.Mass/L))
                        VVangle = numpy.arccos(self.ACFT.Mass/L)

                        if VVclb2 > VVclb:
                            VVclb = VVclb2
                            if VVclb >= VVref:
                                Drag = 0.5*CD*(Vclb**2)*self.rho*Sref
                            
                                if Thrust > Drag:
                                    self.DATA.CLBAoA = a
        
        CD0 = self.CDArray[self.DATA.CLBAoA-self.DATA.AoAmin,0,self.DATA.ElevFD-elev]
        Drag = 0.5*CD0*(Vclb**2)*self.rho*Sref

        if Drag > Thrust:
            print("Thrust insufficient")

            return 6
                        
        elif VVclb < VVref:
            print("Climbrate insufficient")

            return 1
        else:
            CLBFolder = self.Folder + "/Output"
            self.DATA.CLBRate = VVclb


            if os.path.exists(CLBFolder):
                print("CLBDATA folder exists")
            else:
                try:
                    os.mkdir(CLBFolder)
                    print("CLBDATA folder made")
                except:    
                    print("CLBDATA folder creation failed")
            self.DATA.writeCLBData(CLBFolder,self.ACFT.Name+"-a"+str(self.DATA.CLBAoA))
            return 0
    

    def CRZAnalysis(self):
        0

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
