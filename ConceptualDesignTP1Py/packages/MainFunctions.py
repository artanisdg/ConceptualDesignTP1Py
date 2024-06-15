import os, sys
import math
import string
from telnetlib import GA
import time
from tkinter import ROUND
import numpy

gAcc = 9.80665 #m/s**2

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft

def setBattery(ACFT:Acft.Aircraft,DensityWhkg,WhReq,WingBatteryRatio:float):
    BattGW = WhReq/DensityWhkg
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
            if line[0] == "BatteryDensity":
                self.BattDensity = float(line[1])
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
    BattDensity:float = 200 #in Wh/kg
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
    CLBAngle:float = 0 #in deg
    CLBAoA:float = 0 #in deg
    CLBDist:float = 0 #in m
    
    DESRate:float = 5.588 #in m/s (1100fpm)
    DESDist:float = 0 #in m

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
        self.DATA = PackageData(self.Folder+"/"+Ac.Name+"_DATA.txt")
        self.CLArray = numpy.empty(shape=(self.DATA.AoAMax-self.DATA.AoAmin+1,round((self.DATA.FlapMax-self.DATA.Flapmin)/2+1),self.DATA.ElevFD-self.DATA.ElevFU+1),dtype=float)
        self.CDArray = numpy.empty(shape=(self.DATA.AoAMax-self.DATA.AoAmin+1,round((self.DATA.FlapMax-self.DATA.Flapmin)/2+1),self.DATA.ElevFD-self.DATA.ElevFU+1),dtype=float)
        self.CMArray = numpy.empty(shape=(self.DATA.AoAMax-self.DATA.AoAmin+1,round((self.DATA.FlapMax-self.DATA.Flapmin)/2+1),self.DATA.ElevFD-self.DATA.ElevFU+1),dtype=float)
        self.NPArray = numpy.empty(shape=(self.DATA.AoAMax-self.DATA.AoAmin+1,round((self.DATA.FlapMax-self.DATA.Flapmin)/2+1),self.DATA.ElevFD-self.DATA.ElevFU+1),dtype=float)
        self.TrimArray = numpy.empty(shape=(round((self.DATA.FlapMax-self.DATA.Flapmin)/2+1)),dtype=float)
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
                
        self.initSizing(self.Folder+"/"+Ac.Name+"_AC.txt",20)

        for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
            self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
        
        self.iteration = 0


    def initSizing(self,pth:string,res:int):
        self.ACFT.ReadFromTxt(pth)
        Ereq = self.DATA.ReqEnergy[0] + self.DATA.ReqEnergy[1] + self.DATA.ReqEnergy[2] + self.DATA.ReqEnergy[3] + self.DATA.ReqEnergy[4]
        Ebat = Ereq
        setBattery(self.ACFT,200,Ebat,0.66)
        self.ACFT.CalcCoM()
        Acft.WriteACtoFile(self.ACFT,self.AVLrt,res,0.42)
    
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
            time.sleep(1)
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
        
        
    def writeLogMessage(self,message:list[str]):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / LOG Message\n")
        file.write("----------------------------------------------------\n")

        file.writelines(message)
        
        file.close()        

    def writeTOData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / TO\n")
        file.write("----------------------------------------------------\n")

        lines:list[str] = []
        lines = ["TO Flap : "+str(self.DATA.TOFlap)]
        lines = ["VsTO : "+str(self.DATA.VsTO)+"m/s\n"]
        lines = lines + ["V2 : "+str(self.DATA.V2)+"m/s\n"]
        lines = lines + ["TODR : "+str(self.DATA.TODR)+"m\n"]
        
        file.writelines(lines)
        
        file.close()

    def writeCLBData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / CLB\n")
        file.write("----------------------------------------------------\n")

        lines:list[str] = []
        lines = ["CLB Rate : "+str(self.DATA.CLBRate)+"m/s\n"]
        lines = lines + ["CLB Angle : "+str(self.DATA.CLBAngle)+" deg\n"]
        lines = lines + ["CLB AoA : "+str(self.DATA.CLBAoA)+" deg\n"]
        lines = lines + ["CLB Distance : "+str(self.DATA.CLBDist)+" m\n"]
        
        file.writelines(lines)
        
        file.close
    
    def writeCRZData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / CRZ\n")
        file.write("----------------------------------------------------\n")

        crzSpeed = 245/1.94384
        crzDist = 926000-self.DATA.CLBDist-self.DATA.DESDist
        crzTime = crzDist/crzSpeed

        BattMass = self.ACFT.Battery.Mass.L+self.ACFT.Battery.Mass.F+self.ACFT.Battery.Mass.R
        BattE = self.DATA.BattDensity * BattMass

        lines:list[str] = []
        lines = ["CRZ Speed : 245kts\n"]
        lines = lines + ["TO/CLB/CRZ Req Energy : "+str(round(self.DATA.ReqEnergy[0]))+"/"+str(round(self.DATA.ReqEnergy[1]))+"/"+str(round(self.DATA.ReqEnergy[2]))+" (Wh)\n"]
        lines = lines + ["Total Batt Energy : "+str(round(BattE))+"Wh\n"]
        lines = lines + ["CRZ Time : "+str(round(crzTime))+"sec\n"]
        lines = lines + ["CRZ Distance : "+str(crzDist/1852)+" nm\n"]

        file.writelines(lines)
        
        file.close

    def writeDESData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / DES\n")
        file.write("----------------------------------------------------\n")

        desDist = self.DATA.DESDist

        BattMass = self.ACFT.Battery.Mass.L+self.ACFT.Battery.Mass.F+self.ACFT.Battery.Mass.R
        BattE = self.DATA.BattDensity * BattMass

        lines = ["DES Req Energy : "+str(round(self.DATA.ReqEnergy[3]))+" (Wh)\n"]
        lines = lines + ["Total Batt Energy : "+str(round(BattE))+"Wh\n"]
        lines = lines + ["DES Rate : -1100fpm\n"]
        lines = lines + ["DES Distance : "+str(desDist/1852)+"nm\n"]
        
        file.writelines(lines)
        
        file.close

    def writeLDGData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / LDG\n")
        file.write("----------------------------------------------------\n")

        lines = [""]
        
        file.writelines(lines)
        
        file.close

    def writeTaxiData(self):
        file = open(self.Folder+"/Output/Log-"+self.ACFT.Name,'a')
        
        file.write("----------------------------------------------------\n")
        file.write("  iteration : "+str(self.iteration)+" / Taxi\n")
        file.write("----------------------------------------------------\n")

        lines = ["Taxi Req Energy : "+str(round(self.DATA.ReqEnergy[4]))+" (Wh)\n"]
        
        file.writelines(lines)
        
        file.close

    def resizeAC(self,option:int):
        if   option == 1: #CL too low
            msg = ["CL Too Low\n"+"Wing Span * 1.05\n"]
            self.ACFT.Wing.SpanHalf = self.ACFT.Wing.SpanHalf * 1.05
            self.ACFT.Wing.Mass = self.ACFT.Wing.Mass * 1.08
            msg = msg + ["Span : "+str(self.ACFT.Wing.SpanHalf)+"  Mass : "+str(self.ACFT.Wing.Mass)+"\n"]
            print(msg)
            self.writeLogMessage(msg)


        #elif option == 99: #CL excessive
        #    0#tbd
        elif option == 2: #HStab too small
            msg = ["HStab too small\n"+"HStab Geom * 1.05\n"]
            self.ACFT.HStab.SpanHalf = self.ACFT.HStab.SpanHalf * 1.05
            self.ACFT.HStab.RootChord = self.ACFT.HStab.RootChord * 1.05
            self.ACFT.HStab.TipChord = self.ACFT.HStab.TipChord * 1.05
            self.ACFT.HStab.Mass = self.ACFT.HStab.Mass * (1.05**2)
            self.ACFT.HStab.CoM[0] = self.ACFT.HStab.CoM[0] * 1.05
            msg = msg + ["HStab Span : "+str(self.ACFT.HStab.SpanHalf)+"  Mass : "+str(self.ACFT.HStab.Mass)+"\n"]
            msg = msg + ["HStab Root Chord : "+str(self.ACFT.HStab.RootChord)+"  Tip Chord : "+str(self.ACFT.HStab.TipChord)+"\n"]
            print(msg)
            self.writeLogMessage(msg)


        elif option == 3: #VStab too small
            self.ACFT.VStab.Span = self.ACFT.VStab.Span * 1.05
            self.ACFT.VStab.RootChord = self.ACFT.VStab.Span * 1.05
            self.ACFT.VStab.TipChord = self.ACFT.VStab.Span * 1.05
            self.ACFT.VStab.Mass = self.ACFT.VStab.Mass * (1.05**2)
            self.ACFT.VStab.CoM[0] = self.ACFT.VStab.CoM[0] * 1.05

        elif option == 4: #CG too fwd, Shift Battery CoM
            self.ACFT.Battery.CoM.F[0] = self.ACFT.Battery.CoM.F[0] + 0.5
            self.ACFT.Fuselage.CoM[0] = self.ACFT.Fuselage.CoM[0] + 0.10*0.5*(self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)

        elif option == 5: #CG too aft, Shift Battery CoM
            self.ACFT.Battery.CoM.F[0] = self.ACFT.Battery.CoM.F[0] - 0.5
            self.ACFT.Fuselage.CoM[0] = self.ACFT.Fuselage.CoM[0] - 0.10*0.5*(self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)

        elif option == 6: #Thrust insufficient
            0

        elif option == 11: #CL too low - increase chord
            self.ACFT.Wing.RootChord = self.ACFT.Wing.RootChord * 1.05
            self.ACFT.Wing.Mass = self.ACFT.Wing.Mass * 1.05 + self.ACFT.Wing.BattMass

        elif option == 12: #HStab ineffective -> Move Further Back
            self.ACFT.HStab.AttachPos[0] = self.ACFT.HStab.AttachPos[0] + 0.3

        elif option == 14: #trim too down, trim up
            msg = ["Trim too down\n"+"HStab Trim -0.1deg\n"]
            self.ACFT.HStab.Ainc = self.ACFT.HStab.Ainc - 0.1
            msg = msg + ["HStab Trim : "+str(self.ACFT.HStab.Ainc)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

        elif option == 15: #trim too up, trim down
            msg = ["Trim too up\n"+"HStab Trim +0.1deg\n"]
            self.ACFT.HStab.Ainc = self.ACFT.HStab.Ainc + 0.1
            msg = msg + ["HStab Trim : "+str(self.ACFT.HStab.Ainc)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

        elif option == 24: #trim too down, trim up a lot
            msg = ["Trim too down\n"+"HStab Trim -0.5deg\n"]
            self.ACFT.HStab.Ainc = self.ACFT.HStab.Ainc - 0.5
            msg = msg + ["HStab Trim : "+str(self.ACFT.HStab.Ainc)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

        elif option == 25: #trim too up, trim down a lot
            msg = ["Trim too up\n"+"HStab Trim +0.5deg\n"]
            self.ACFT.HStab.Ainc = self.ACFT.HStab.Ainc + 0.5
            msg = msg + ["HStab Trim : "+str(self.ACFT.HStab.Ainc)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

        else:
            self.print("resizeAC Function Call Error")
            self.writeLogMessage("resizeAC Function Call Error")
            
        self.ACFT.CalcCoM()

        
    def AeroAnalysis(self):
        
        Hung:list[str] = []

        self.CreateFiles(self.ACFT.Name)
        
        AeroFolder = self.Folder + "/Output"

        if os.path.exists(AeroFolder):
            print("Output folder exists")
        else:
            try:
                os.mkdir(AeroFolder)
                print("Output folder made")
            except:    
                print("Output folder creation failed")

        for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
            while 1:
                self.CreateFiles(self.ACFT.Name)
                res:str = self.ACFT.Name+"-aero_stab_f"+str(f)
                self.runSession(0,f,0,res)
                time.sleep(3)
                i = 0
                while 1:
                    if self.readResult(0,f,0,res) == 0:
                        break
                    else:
                        if i>3:
                            print("file read abort - aero_stab_f"+str(f))
                            break
                        else:
                            time.sleep(0.5)
                            i += 1
                if self.CMArray[0-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]<-0.1:
                    self.resizeAC(24)
                    self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
                elif self.CMArray[0-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]>0.1:
                    self.resizeAC(25)
                    self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
                elif self.CMArray[0-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]<-0.01:
                    self.resizeAC(14)
                    self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
                elif self.CMArray[0-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]>0.01:
                    self.resizeAC(15)
                    self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
                elif i<=3 :
                    self.TrimArray[round(f/2)] = self.ACFT.HStab.Ainc
                    msg = ["Trim Set\n"]+["Alpha : 0, Flaps : "+str(f)+", Trim : "+str(round(self.ACFT.HStab.Ainc,2))+"\n"]+["Saved Trim Value = "+str(round(self.TrimArray[round(f/2)],2))+"\n"]+["Cm = "+str(self.CMArray[0-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0])+"\n"]
                    print(msg)
                    self.writeLogMessage(msg)
                    for a in range(self.DATA.AoAmin,self.DATA.AoAMax+1,1):
                        for e in range(self.DATA.ElevFD,self.DATA.ElevFU-1,-1):
                            res:str = self.ACFT.Name+"-aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)+"_t"+str(self.TrimArray[round(f/2)])
                            self.runSession(a,f,e,res)
                            time.sleep(0.5)    
                        time.sleep(3)
                    time.sleep(3)
                    break
                time.sleep(1)
            time.sleep(5)

            for a in range(self.DATA.AoAmin,self.DATA.AoAMax+1,1):
                for e in range(self.DATA.ElevFD,self.DATA.ElevFU-1,-1):
                    res:str = self.ACFT.Name+"-Aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)+"_t"+str(self.TrimArray[round(f/2)])
                    i = 0
                    while 1:
                        if self.readResult(a,f,e,res) == 0:
                            break
                        else:
                            if i>3:
                                print("file read abort - a:"+str(a)+" F:"+str(f)+" e:"+str(e)+"_t"+str(self.TrimArray[round(f/2)]))
                                Hung.append([a,f,e])
                                break
                            else:
                                time.sleep(1)
                                i += 1
        while 1:
            V = Hung.pop()
            a = V[0]; f = V[1]; e = V[2]
            res:str = self.ACFT.Name+"-Aero_a"+str(a)+"_f"+str(f)+"_e"+str(e)+"_t"+str(self.TrimArray[round(f/2)])

            self.ACFT.HStab.Ainc=self.TrimArray[round(f/2)]
            self.CreateFiles(self.ACFT.Name)
            self.runSession(a,f,e,res)

            i = 0
            while 1:
                if self.readResult(a,f,e,res) == 0:
                    break
                else:
                    if i>3:
                        print("file read abort - a:"+str(a)+" F:"+str(f)+" e:"+str(e)+"_t"+str(self.TrimArray[round(f/2)]))
                        Hung.append([a,f,e])
                        break
                    else:
                        time.sleep(1)
                        i += 1
            if Hung == []:
                print("Hung File Stack Empty")
                break
        
        self.iteration += 1                                
    
    def CGAnalysis(self):
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
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-3]>0.1:
                    msg = ["CG Too Far Back\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0])+"\n"]
                    print(msg)
                    self.writeLogMessage(msg)

                    return 5
                
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-5)]<-0.1:
                    msg = ["CG Too Far Forward\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-(-5)])+"\n"]
                    print(msg)
                    self.writeLogMessage(msg)
                    
                    return 4
                
        for a in range(4,self.DATA.AoAMax+1,1):
            for f in range(self.DATA.Flapmin,self.DATA.FlapMax+1,2):
                if self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0]>0:
                    msg = ["CG Too Far Back\n"]+["Alpha : "+str(a)+", Flaps : "+str(f)+"\n"]+["Cm = "+str(self.CMArray[a-self.DATA.AoAmin,round(f/2),self.DATA.ElevFD-0])+"\n"]
                    print(msg)
                    self.writeLogMessage(msg)

                    return 5

        self.writeLogMessage("CG in Range\n")
        return 0

        
        

    def TOAnalysis(self):
        self.Mach = 0.212
        self.rho = self.rhoSet[0]
        
        Friction = self.ACFT.Mass*0.01*gAcc
        
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2

        f = 6
        #TO Speed Determination
        a = 12    
        CLv2 = self.CLArray[a-self.DATA.AoAmin,round(f/2),0]
        Lvsc = 0.5*CLv2*self.rho*Sref
            
        self.DATA.VsTO=numpy.sqrt((self.ACFT.Mass*gAcc)/Lvsc)
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
                    msg = ["TODR > TODA(762m)(marginal)\n"+"Alpha : "+0+", Flaps : "+str(f)+"\n"+"TODR = "+str(d)+"\n"]
                    print(msg)
                    self.writeLogMessage(msg)

                    return 1
            elif d>762:
                msg = ["TO Failed : TODR > TODA(762m)\nV2 unachievable\n"+"Alpha : 0, Flaps : "+str(f)+"\n"]
                print(msg)
                self.writeLogMessage(msg)

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
        self.rho = self.rhoSet[3]
        
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2
        
        Vclb = self.VmpsT
        VVref = 900/196.85
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
            for e in range(4,-10,-1):
                CL = self.CLArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                CD = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                CM = self.CMArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-e]
                
                if e > -12:
                    CMm1 = self.CMArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-(e-1)]
                else:
                    CMm1 = CM
                if e < 5:
                    CMp1 = self.CMArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-(e+1)]
                else:
                    CMp1 = CM
                    
                if (CMm1 > 0) and (CMp1 < 0):
                    elev = e
                    L = 0.5*CL*(Vclb**2)*self.rho*Sref
                
                    if L > (self.ACFT.Mass*gAcc):
                        VVclb2 = Vclb*numpy.sin(numpy.arccos((self.ACFT.Mass*gAcc)/L))
                        VVangle = numpy.arccos((self.ACFT.Mass*gAcc)/L)

                        if VVclb2 > VVclb:
                            VVclb = VVclb2
                            if VVclb >= VVref:
                                Drag = 0.5*CD*(Vclb**2)*self.rho*Sref
                            
                                if Thrust > Drag:
                                    self.DATA.CLBAoA = a
                                    self.DATA.CLBAngle = 180*VVangle/numpy.pi
                                    self.DATA.CLBRate = VVclb
        
        CD0 = self.CDArray[self.DATA.CLBAoA-self.DATA.AoAmin,0,self.DATA.ElevFD-elev]
        Drag = 0.5*CD0*(Vclb**2)*self.rho*Sref

        if Drag > Thrust:
            msg = ["Thrust insufficient\n"]+["Alpha : "+str(self.DATA.CLBAoA)+"\n"]+["Max Thrust : "+str(Thrust)+",  Drag : "+str(Drag)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

            return 6
                        
        elif VVclb < VVref:
            msg = ["Climbrate insufficient\n"]+["Alpha : "+str(self.DATA.CLBAoA)+"\n"]+["VV Req : "+str(VVref)+",  VV Act : "+str(VVclb)+"\n"]
            print(msg)
            self.writeLogMessage(msg)

            return 1
        

        #CLB Energy Analysis
        AltTgt = 9144 #meters, 30000ft
        ClbTime = AltTgt/self.DATA.CLBRate
        
        Ep = self.ACFT.Mass * gAcc * AltTgt
        Efric = Drag*Vclb*ClbTime / self.DATA.ThrustEfficiency
        
        self.DATA.ReqEnergy[1] = (Ep + Efric)/3600
        self.DATA.CLBDist = ClbTime * Vclb
        
        #CLB Result Output
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
        self.writeCLBData()
        return 0
    

    def CRZAnalysis(self):
        self.Mach = 0.42
        self.VmpsT = 245/1.94384
        self.rho = self.rhoSet[3]
        
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2

        CL = self.CLArray[0-self.DATA.AoAmin,0,self.DATA.ElevFD-0]
        CD = self.CDArray[0-self.DATA.AoAmin,0,self.DATA.ElevFD-0]

        DESSpeed = 220/1.94384 
        DEStime = 30000/1100 * 60
        self.DATA.DESDist = DESSpeed * DEStime

        Dist = 926000 - self.DATA.CLBDist - self.DATA.DESDist #500nm to meters
        Drag = 0.5*CD*(self.VmpsT**2)*self.rho*Sref
        
        self.DATA.ReqEnergy[2] = Dist* (Drag / self.DATA.ThrustEfficiency) / 3600
        
        BattMass = self.ACFT.Battery.Mass.L+self.ACFT.Battery.Mass.F+self.ACFT.Battery.Mass.R
        
        BattE = self.DATA.BattDensity * BattMass
        Ereq = self.DATA.ReqEnergy[0] + self.DATA.ReqEnergy[1] + self.DATA.ReqEnergy[2] + self.DATA.ReqEnergy[3] + self.DATA.ReqEnergy[4]

        if Ereq > BattE:
            Eadd = Ereq + 45 * 60 * self.VmpsT * Drag / 3600
            setBattery(self.ACFT,self.DATA.BattDensity,Eadd,0.8)
            msg = ["Battery Energy Insufficient\n"+"Required Energy : "+str(round(Ereq))+"   Battery Energy : "+str(round(BattE))+"   (Battery Mass : "+str(round(BattMass))+")\n"]
            print(msg)
            self.writeLogMessage(msg)
            return 1

        self.writeCRZData()
        return 0
    
    def DESAnalysis(self):
        self.Mach = 0.42
        self.VmpsT = 220/1.94384
        self.rho = self.rhoSet[1]

        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2

        a = 0

        while 1:
            
            CL = self.CLArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-0]
            CD = self.CDArray[a-self.DATA.AoAmin,0,self.DATA.ElevFD-0]

            Lift = 0.5*CL*(self.VmpsT**2)*self.rho*Sref
            Drag = 0.5*CD*(self.VmpsT**2)*self.rho*Sref

            DEStime = 30000/1100 * 60

            if (Lift > (self.ACFT.Mass * gAcc)) or (a > -2):
                a -= 1
            else:
                DESdist = DEStime * self.VmpsT
                self.DATA.DESDist = DESdist
                break

        # Descent Energy Analysis
        self.DATA.ReqEnergy[3] = self.DATA.DESDist*(Drag / self.DATA.ThrustEfficiency) / 3600
        
        BattMass = self.ACFT.Battery.Mass.L+self.ACFT.Battery.Mass.F+self.ACFT.Battery.Mass.R
        
        BattE = self.DATA.BattDensity * BattMass
        Ereq = self.DATA.ReqEnergy[0] + self.DATA.ReqEnergy[1] + self.DATA.ReqEnergy[2] + self.DATA.ReqEnergy[3] + self.DATA.ReqEnergy[4]

        if Ereq > BattE:
            Eadd = Ereq + 45 * 60 * self.VmpsT * Drag / 3600
            setBattery(self.ACFT,self.DATA.BattDensity,Eadd,0.8)
            msg = ["Battery Energy Insufficient\n"+"Required Energy : "+str(round(Ereq))+"   Battery Energy : "+str(round(BattE))+"   (Battery Mass : "+str(round(BattMass))+")\n"]
            print(msg)
            self.writeLogMessage(msg)
            return 1

        self.writeDESData()
        return 0
    
    def LDGAnalysis(self):
        self.Mach = 0.212
        self.VmpsT = 190/1.94384
        self.rho = self.rhoSet[0]

        self.writeLDGData()
        return 0

    def TaxiAnalysis(self):
        self.Mach = 0.212
        self.VmpsT = 220/1.94384
        self.rho = self.rhoSet[0]
        
        Friction = self.ACFT.Mass*0.01*gAcc
        Vtaxi = 5.15 #m/s (10kts)
        
        Power = Friction * Vtaxi

        CD = self.CDArray[0-self.DATA.AoAmin,0,self.DATA.ElevFD-0]
        Cref = (self.ACFT.Wing.RootChord+self.ACFT.Wing.TipChord)/2
        Sref = Cref*self.ACFT.Wing.SpanHalf*2

        Drag = 0.5*CD*(self.VmpsT**2)*self.rho*Sref
        
        Tout = 240 #seconds
        Tin = 240 #seconds
        
        Energy = Power*(Tout + Tin)

        self.DATA.ReqEnergy[4] = Energy / 3600

        BattMass = self.ACFT.Battery.Mass.L+self.ACFT.Battery.Mass.F+self.ACFT.Battery.Mass.R
        BattE = self.DATA.BattDensity * BattMass
        Ereq = self.DATA.ReqEnergy[0] + self.DATA.ReqEnergy[1] + self.DATA.ReqEnergy[2] + self.DATA.ReqEnergy[3] + self.DATA.ReqEnergy[4]

        if Ereq > BattE:
            Eadd = Ereq + 45 * 60 * self.VmpsT * Drag
            setBattery(self.ACFT,self.DATA.BattDensity,Eadd,0.8)
            msg = ["Battery Energy Insufficient\n"+"Required Energy : "+str(round(Ereq))+"   Battery Energy : "+str(round(BattE))+"   (Battery Mass : "+str(round(BattMass))+")\n"]
            print(msg)
            self.writeLogMessage(msg)
            return 1
        
        self.writeTaxiData()
        return 0
        