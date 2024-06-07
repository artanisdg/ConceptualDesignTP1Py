import os
import sys
import math
import string

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF


class Aircraft:
    def __init__(self,modType,Nm):
        self.ModelType = modType
        self.Name = Nm
        self.CoM = [0,0,0]
        self.Wing = self.WingClass()
        self.Fuselage = self.FuselageClass()
        self.HStab = self.HStabClass()
        self.VStab = self.VStabClass()
        self.MotorPod = self.MotorPodClass()
        self.Battery = self.BatteryClass()
    
    CoM:list

    Name = None
    Mass = 0

    class WingClass:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
        Sweep = 0
        Airfoil = 2412
        Ainc = 0
        Mass = 0

        #--------End of SubClass : Wing--------

    class FuselageClass:
        def __init__(self):
            self.CoM = [0,0,0]
        Length = 0
        Height = 0
        Width = 0
        SlopeUpper = 0
        SlopeLower = 0
        SlopeSide = 0
        Mass = 0
        #--------End of SubClass : Fuselage--------

    class HStabClass:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
        Sweep = 0
        Airfoil = 0
        Ainc = 0
        Mass = 0
        #--------End of SubClass : HStab--------

    class VStabClass:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        Num = 1
        RootChord = 0
        TipChord = 0
        Span = 0
        Sweep = 0
        Mass = 0
        #--------End of SubClass : VStab--------

    class MotorPodClass:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        Num = 0
        Radius = 0
        Length = 0
        Mass = 0
        #--------End of SubClass : MotorPod--------
    
    class BatteryClass:
        def __init__(self):
            self.CoM = self.CoMBatClass()
            self.Mass = self.MassBatClass()
        class CoMBatClass:
            def __init__(self):
                self.L = [0,0,0]
                self.R = [0,0,0]
                self.F = [0,0,0]
            L:list
            R:list
            F:list
        class MassBatClass:
            L = 0
            R = 0
            F = 0
        #--------End of SubClass : Battery--------
        
    def ReadFromTxt(self,path:string):
        AcftTxt = open(path,"r")
        linesTemp = AcftTxt.readlines()
        Section:string
        Key:int = 0
        Tgt:int = 0
        G=None; W=None; F=None; HS=None; VS=None; 
        for line in linesTemp:
            line = line.strip()
            if line == "Generic":
                Section = "Generic"
                G:int = 0
                Tgt = Tgt+1
            elif line == "Wing":
                Section = "Wing"
                W:int = 0
                Tgt = Tgt+1
            elif line == "Fuselage":
                Section = "Fuselage"
                F:int = 0
                Tgt = Tgt+1
            elif line == "HStab":
                Section = "HStab"
                HS:int = 0
                Tgt = Tgt+1
            elif line == "VStab":
                Section = "VStab"
                VS:int = 0
                Tgt = Tgt+1

            elif line.isspace():
                0
            
            elif len(line) > 1:
                line=line.split('=')
                for val in line:
                    val = val.strip()
                
                if Section == "Generic":
                    if line[0] == "Name":
                        self.Name = line[1]
                        G=G+1
                    elif line[0] == "ModelType":
                        self.ModelType = int(line[1])
                        G=G+1
                    else:
                        print("Unrecognized Variable for Aircraft Generic")
                        G=0
                    
                elif Section == "Wing":
                    if line[0] == "AttachPos":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.Wing.AttachPos[i]=float(PosVec[i])
                        W=W+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.Wing.CoM[i]=float(PosVec[i])
                        W=W+1
                    elif line[0] == "RootChord":
                        self.Wing.RootChord = float(line[1])
                        W=W+1
                    elif line[0] == "TipChord":
                        self.Wing.TipChord = float(line[1])
                        W=W+1
                    elif line[0] == "SpanHalf":
                        self.Wing.SpanHalf = float(line[1])
                        W=W+1
                    elif line[0] == "Sweep":
                        self.Wing.Sweep = float(line[1])
                        W=W+1
                    elif line[0] == "Airfoil":
                        self.Wing.Airfoil = int(line[1])
                        W=W+1
                    elif line[0] == "Ainc":
                        self.Wing.Ainc = float(line[1])
                        W=W+1
                    elif line[0] == "Mass":
                        self.Wing.Mass = float(line[1])
                        W=W+1
                    else:
                        print("Unrecognized Variable for Aircraft Wing")
                        W=0

                elif Section == "Fuselage":
                    if line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.Fuselage.CoM[i]=float(PosVec[i])
                        F=F+1
                    elif line[0] == "Length":
                        self.Fuselage.Length = float(line[1])
                        F=F+1
                    elif line[0] == "Height":
                        self.Fuselage.Height = float(line[1])
                        F=F+1
                    elif line[0] == "Width":
                        self.Fuselage.Width = float(line[1])
                        F=F+1
                    elif line[0] == "SlopeUpper":
                        self.Fuselage.SlopeUpper = float(line[1])
                        F=F+1
                    elif line[0] == "SlopeLower":
                        self.Fuselage.SlopeLower = float(line[1])
                        F=F+1
                    elif line[0] == "SlopeSide":
                        self.Fuselage.SlopeSide = float(line[1])
                        F=F+1
                    elif line[0] == "Mass":
                        self.Fuselage.Mass = float(line[1])
                        F=F+1
                    else:
                        print("Unrecognized Variable for Aircraft Fuselage")
                        F=0

                elif Section == "HStab":
                    if line[0] == "AttachPos":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.HStab.AttachPos[i]=float(PosVec[i])
                        HS=HS+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.HStab.CoM[i]=float(PosVec[i])
                        HS=HS+1
                    elif line[0] == "RootChord":
                        self.HStab.RootChord = float(line[1])
                        HS=HS+1
                    elif line[0] == "TipChord":
                        self.HStab.TipChord = float(line[1])
                        HS=HS+1
                    elif line[0] == "SpanHalf":
                        self.HStab.SpanHalf = float(line[1])
                        HS=HS+1
                    elif line[0] == "Sweep":
                        self.HStab.Sweep = float(line[1])
                        HS=HS+1
                    elif line[0] == "Airfoil":
                        self.HStab.Airfoil = int(line[1])
                        HS=HS+1
                    elif line[0] == "Ainc":
                        self.HStab.Ainc = float(line[1])
                        HS=HS+1
                    elif line[0] == "Mass":
                        self.HStab.Mass = float(line[1])
                        HS=HS+1
                    else:
                        print("Unrecognized Variable for Aircraft Horizontal Stabilizer")
                        HS=0
                    
                elif Section == "VStab":
                    if line[0] == "AttachPos":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.VStab.AttachPos[i]=float(PosVec[i])
                        VS=VS+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.VStab.CoM[i]=float(PosVec[i])
                        VS=VS+1
                    elif line[0] == "Num":
                        self.VStab.Num = float(line[1])
                        VS=VS+1
                    elif line[0] == "RootChord":
                        self.VStab.RootChord = float(line[1])
                        VS=VS+1
                    elif line[0] == "TipChord":
                        self.VStab.TipChord = float(line[1])
                        VS=VS+1
                    elif line[0] == "Span":
                        self.VStab.Span = float(line[1])
                        VS=VS+1
                    elif line[0] == "Sweep":
                        self.VStab.Sweep = float(line[1])
                        VS=VS+1
                    elif line[0] == "Mass":
                        self.VStab.Mass = float(line[1])
                        VS=VS+1
                    else:
                        print("Unrecognized Variable for Aircraft Vertical Stabilizer")
                        VS=0
                
                else:
                    print("Unrecognized Section Name / TXT Format Not to Standard")
            if G == 2:
                print("Generic : Complete")
                Key = Key+1
            if W == 9:
                print("Wing    : Complete")
                Key = Key+1
            if F == 8:
                print("Fuselage: Complete")
                Key = Key+1
            if HS == 9:
                print("HStab   : Complete")
                Key = Key+1
            if VS == 8:
                print("VStab   : Complete")
                Key = Key+1
        if Key == Tgt:
            print("All Components Completely Loaded")
        
        self.Battery.CoM.R[0] = self.Wing.AttachPos[0] + self.Wing.CoM[0]
        self.Battery.CoM.R[1] = self.Wing.AttachPos[1] + self.Wing.CoM[1]
        self.Battery.CoM.R[2] = self.Wing.AttachPos[2] + self.Wing.CoM[2]

        self.Battery.CoM.L[0] = self.Wing.AttachPos[0] + self.Wing.CoM[0]
        self.Battery.CoM.L[1] = (-1)*self.Wing.AttachPos[1] - self.Wing.CoM[1]
        self.Battery.CoM.L[2] = self.Wing.AttachPos[2] + self.Wing.CoM[2]

        self.Battery.CoM.F[0] = self.Fuselage.CoM[0]
        self.Battery.CoM.F[1] = self.Fuselage.CoM[1]
        self.Battery.CoM.F[2] = self.Fuselage.CoM[2]
        #End of ReadFromTxt

        
    def CalcCoM(self):
        GW = 2*self.Wing.Mass+2*self.Fuselage.Mass+2*self.HStab.Mass+self.VStab.Num*self.VStab.Mass+self.MotorPod.Num*self.MotorPod.Mass+self.Battery.Mass.L+self.Battery.Mass.R+self.Battery.Mass.F
        
        xM = (2*self.Wing.Mass*(self.Wing.AttachPos[0]+self.Wing.CoM[0])
             +self.Fuselage.Mass*self.Fuselage.CoM[0]
             +2*self.HStab.Mass*(self.HStab.AttachPos[0]+self.HStab.CoM[0])
             +self.VStab.Num*self.VStab.Mass*(self.VStab.AttachPos[0]+self.VStab.CoM[0])
             +self.MotorPod.Num*self.MotorPod.Mass*(self.MotorPod.AttachPos[0]+self.MotorPod.CoM[0])
             +self.Battery.Mass.L*self.Battery.CoM.L[0]+self.Battery.Mass.R*self.Battery.CoM.R[0]+self.Battery.Mass.F*self.Battery.CoM.F[0])
        x = xM/GW

        yM = (self.Fuselage.Mass*self.Fuselage.CoM[1]
             +self.Battery.Mass.L*self.Battery.CoM.L[1]+self.Battery.Mass.R*self.Battery.CoM.R[1]+self.Battery.Mass.F*self.Battery.CoM.F[1])
        y = yM/GW
        
        zM = (2*self.Wing.Mass*(self.Wing.AttachPos[2]+self.Wing.CoM[2])
             +self.Fuselage.Mass*self.Fuselage.CoM[2]
             +2*self.HStab.Mass*(self.HStab.AttachPos[2]+self.HStab.CoM[2])
             +self.VStab.Num*self.VStab.Mass*(self.VStab.AttachPos[2]+self.VStab.CoM[2])
             +self.MotorPod.Num*self.MotorPod.Mass*(self.MotorPod.AttachPos[2]+self.MotorPod.CoM[2])
             +self.Battery.Mass.L*self.Battery.CoM.L[2]+self.Battery.Mass.R*self.Battery.CoM.R[2]+self.Battery.Mass.F*self.Battery.CoM.F[2])
        z = zM/GW
        
        self.CoM = [x,y,z]
        self.Mass = GW
        #End of CalcCoM

    #--------------End of Class : Aircraft----------------------
        

def WriteACtoFile(Acft : Aircraft,runtm : AVLF.runtime, slices : int):
    AVLpath = runtm.readAVLFileName()
    MassPath = runtm.readMassFileName()
    
    AVLFile = open(AVLpath,"w")
    
    AVLFile.write(Acft.Name+"\n")
    AVLFile.write("\n")
    AVLFile.write("#Mach\n")
    AVLFile.write(" 0.42\n")
    AVLFile.write("\n")
    AVLFile.write("#IYsym   IZsym   Zsym\n")
    AVLFile.write(" 0       0       0.0\n")
    AVLFile.write("\n")
    AVLFile.write("#Sref    Cref    Bref\n")
    AVLFile.write("1260.0   11.0    113.0\n")
    AVLFile.write("\n")
    AVLFile.write("#Xref    Yref    Zref\n")
    AVLFile.write(str(round(Acft.CoM[0],2))+"     "+str(round(Acft.CoM[1],2))+"     "+str(round(Acft.CoM[2],2))+"\n")
    AVLFile.write("#--------------------------------------------------\n")


    #Write Wing
    AVLFile.write("SURFACE\nWing\n")
    AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write(str(round(slices,2))+"           "+"1.0"+"     "+str(round(2*slices,2))+"         1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(str(round(Acft.Wing.AttachPos[0],2))+"  "+str(round(Acft.Wing.AttachPos[1],2))+"  "+str(round(Acft.Wing.AttachPos[2],2))+"\n\n\n")

    intervalWing:float = Acft.Wing.SpanHalf/slices*2
    for i in range(0,round((slices/2)-1)):
        Chord:float = (Acft.Wing.RootChord*(slices/2-i-1)+Acft.Wing.TipChord*i)/(slices/2-1)
        LEx:float = intervalWing*i*math.tan(Acft.Wing.Sweep/180*math.pi)
        LEy:float = intervalWing*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(str(round(LEx,2))+"    "+str(round(LEy,2))+"    "+"0.0"+"     "+str(round(Chord,2))+"    "+str(round(Acft.Wing.Ainc,2))+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(str(round(Acft.Wing.Airfoil,2))+"\n")
        if i < slices/4:
            AVLFile.write("CONTROL\n")
            AVLFile.write("flap     1.0  0.70  0. 0. 0.  +1\n")
        if i > 3*slices/8:
            AVLFile.write("CONTROL\n")
            AVLFile.write("aileron  1.0  0.80  0. 0. 0.  -1\n")
        AVLFile.write("\n")


    #Write FuselageH
    AVLFile.write("SURFACE\nFuselage Horizontal\n")
    AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseH:float = Acft.Fuselage.Width/5
    for i in range(0,4):
        Chord:float = Acft.Fuselage.Length-i*(Acft.Fuselage.Width*math.tan(Acft.Fuselage.SlopeSide/180*math.pi))
        LEx:float = i*(Acft.Fuselage.Width*math.tan(Acft.Fuselage.SlopeSide/180*math.pi))
        LEy:float = intervalFuseH*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(str(round(LEx,2))+"    "+str(round(LEy,2))+"    "+"0.0"+"     "+str(round(Chord,2))+"   0.    1          0.\n")
        AVLFile.write("\n")

    #Write FuselageVU
    AVLFile.write("SURFACE\nFuselage V Upper\n")
    AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseV:float = Acft.Fuselage.Height/10
    for i in range(0,4):
        Chord:float = Acft.Fuselage.Length-i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeUpper/180*math.pi))
        LEx:float = i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeUpper/180*math.pi))
        LEz:float = intervalFuseV*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(str(round(LEx,2))+"    "+"0.0"+"    "+str(round(LEz,2))+"     "+str(round(Chord,2))+"   0.    1          0.\n")
        AVLFile.write("\n")

    #Write FuselageVL
    AVLFile.write("SURFACE\nFuselage V Lower\n")
    AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseV:float = Acft.Fuselage.Height/10
    for i in range(0,4):
        Chord:float = Acft.Fuselage.Length-i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeLower/180*math.pi))
        LEx:float = i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeLower/180*math.pi))
        LEz:float = -intervalFuseV*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(str(round(LEx,2))+"    "+"0.0"+"    "+str(round(LEz,2))+"     "+str(round(Chord,2))+"   0.    1          0.\n")
        AVLFile.write("\n")


    StabSlices:int = 10

    #Write Hstab
    AVLFile.write("SURFACE\nHorizontal Stabilizer\n")
    AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write(str(round(StabSlices,2))+"           "+"1.0"+"     "+str(round(2*StabSlices,2))+"         1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(str(round(Acft.HStab.AttachPos[0],2))+"  "+str(round(Acft.HStab.AttachPos[1],2))+"  "+str(round(Acft.HStab.AttachPos[2],2))+"\n\n\n")

    intervalHStab:float = Acft.HStab.SpanHalf/StabSlices*2
    for i in range(0,round((StabSlices/2)-1)):
        Chord:float = (Acft.HStab.RootChord*(StabSlices/2-i-1)+Acft.HStab.TipChord*i)/(StabSlices/2-1)
        LEx:float = intervalHStab*i*math.tan(Acft.HStab.Sweep/180*math.pi)
        LEy:float = intervalHStab*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(str(round(LEx,2))+"    "+str(round(LEy,2))+"    "+"0.0"+"     "+str(round(Chord,2))+"    "+str(round(Acft.HStab.Ainc,2))+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(str(round(Acft.HStab.Airfoil,2))+"\n")
        AVLFile.write("CONTROL\n")
        AVLFile.write("elevator 1.0  0.70  0. 0. 0.  +1\n")
        AVLFile.write("\n")

    #Write Vstab
    if Acft.VStab.Num == 1:
        AVLFile.write("SURFACE\nVertical Stabilizer\n")
        AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
        AVLFile.write(str(round(StabSlices,2))+"           "+"1.0"+"     "+str(round(2*StabSlices,2))+"         1.0\n")
        AVLFile.write("\n")
        AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
        AVLFile.write("\n")
        AVLFile.write("TRANSLATE\n")
        AVLFile.write(str(round(Acft.VStab.AttachPos[0],2))+"  "+str(round(Acft.VStab.AttachPos[1],2))+"  "+str(round(Acft.VStab.AttachPos[2],2))+"\n\n\n")

        intervalVStab:float = Acft.VStab.Span/StabSlices*2
        for i in range(0,round((StabSlices-1)/2)):
            Chord:float = (Acft.VStab.RootChord*(StabSlices/2-i-1)+Acft.VStab.TipChord*i)/(StabSlices/2-1)
            LEx:float = intervalVStab*i*math.tan(Acft.VStab.Sweep/180*math.pi)
            LEz:float = intervalVStab*i
            AVLFile.write("SECTION\n")
            AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
            AVLFile.write(str(round(LEx,2))+"    "+"0.0"+"    "+str(round(LEz,2))+"     "+str(round(Chord,2))+"    0.\n")
            AVLFile.write("CONTROL\n")
            AVLFile.write("rudder 1.0  0.70  0. 0. 0.  +1\n")
            AVLFile.write("\n")

    elif Acft.VStab.Num ==2:
        AVLFile.write("SURFACE\nVertical Stabilizer\n")
        AVLFile.write("#Nchordwise  Cspace  Nspanwise  Sspace\n") 
        AVLFile.write(str(round(StabSlices,2))+"           "+"1.0"+"     "+str(round(2*StabSlices,2))+"         1.0\n")
        AVLFile.write("\n")
        AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
        AVLFile.write("\n")
        AVLFile.write("TRANSLATE\n")
        AVLFile.write(str(round(Acft.VStab.AttachPos[0],2))+"  "+str(round(Acft.VStab.AttachPos[1],2))+"  "+str(round(Acft.VStab.AttachPos[2],2))+"\n\n\n")

        intervalVStab:float = Acft.VStab.Span/StabSlices*2
        for i in range(0,round((StabSlices-1)/2)):
            Chord:float = (Acft.VStab.RootChord*(StabSlices-i)+Acft.VStab.TipChord*i)/StabSlices
            LEx:float = intervalVStab*i*math.tan(Acft.VStab.Sweep/180*math.pi)
            LEz:float = intervalVStab*i
            AVLFile.write("SECTION\n")
            AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
            AVLFile.write(str(round(LEx,2))+"    "+"0.0"+"    "+str(round(LEz,2))+"     "+str(round(Chord,2))+"    0.\n")
            AVLFile.write("CONTROL\n")
            AVLFile.write("rudder 1.0  0.70  0. 0. 0.  +1\n")
            AVLFile.write("\n")

    #Write MotorPod
    #tbd

    AVLFile.close()
    #End of Writing to AVLFile

    #Write to MassFile
    MassFile = open(MassPath,"w")

    MassFile.write("#  "+Acft.Name+"\n#\n#  Dimensional unit and parameter data.\n#  Mass & Inertia breakdown.\n")
    MassFile.write("\n")

    MassFile.write("Lunit = 1.0000 m\nMunit = 1.000  kg\nTunit = 1.0    s\n")
    MassFile.write("#-------------------------\n")
    MassFile.write("g   = 9.81\nrho = 1.225\n\n\n")
    MassFile.write("#-------------------------\n")

    MassFile.write("#  mass   x     y     z    [ Ixx     Iyy    Izz     Ixy   Ixz   Iyz ]\n")
    MassFile.write("*   1.    1.    1.    1.     1.     1.      1.      1.    1.    1.\n")
    MassFile.write("+   0.    0.    0.    0.     0.     0.      0.      0.    0.    0.\n")

    WingCoM = [0,0,0]
    for i in range(0,2):
        WingCoM[i] = Acft.Wing.AttachPos[i]+Acft.Wing.CoM[i]
    WingAvgChord = (Acft.Wing.RootChord+Acft.Wing.TipChord)/2
    IxxWing = Acft.Wing.Mass*(Acft.Wing.SpanHalf**3)*WingAvgChord/12
    IyyWing = Acft.Wing.Mass*Acft.Wing.SpanHalf*(WingAvgChord**3)/12
    IzzWing = Acft.Wing.Mass*Acft.Wing.SpanHalf*(WingAvgChord**3)/12
    MassFile.write("   "+str(round(Acft.Wing.Mass,2))+"   "+str(round(WingCoM[0],2))+"   "+str(round(WingCoM[1],2))+"   "+str(round(WingCoM[2],2))+"    "+str(round(IxxWing,2))+"    "+str(round(IyyWing,2))+"    "+str(round(IzzWing,2))+"     ! Wing\n")

    IxxFuse = Acft.Fuselage.Mass*(Acft.Fuselage.Height**3)*Acft.Fuselage.Length/12
    IyyFuse = Acft.Fuselage.Mass*Acft.Fuselage.Height*(Acft.Fuselage.Length**3)/12
    IzzFuse = Acft.Fuselage.Mass*Acft.Fuselage.Width*(Acft.Fuselage.Length**3)/12
    MassFile.write("   "+str(round(Acft.Fuselage.Mass,2))+"   "+str(round(Acft.Fuselage.CoM[0],2))+"   "+str(round(Acft.Fuselage.CoM[1],2))+"   "+str(round(Acft.Fuselage.CoM[2],2))+"    "+str(round(IxxFuse,2))+"    "+str(round(IyyFuse,2))+"    "+str(round(IzzFuse,2))+"     ! Fuselage\n")
    
    HStabCoM = [0,0,0]
    for i in range(0,2):
        HStabCoM[i] = Acft.HStab.AttachPos[i]+Acft.HStab.CoM[i]
    HStabAvgChord = (Acft.HStab.RootChord+Acft.HStab.TipChord)/2
    IxxHStab = Acft.HStab.Mass*(Acft.HStab.SpanHalf**3)*HStabAvgChord/12
    IyyHStab = Acft.HStab.Mass*Acft.HStab.SpanHalf*(HStabAvgChord**3)/12
    IzzHStab = Acft.HStab.Mass*Acft.HStab.SpanHalf*(HStabAvgChord**3)/12
    MassFile.write("   "+str(round(Acft.HStab.Mass,2))+"   "+str(round(HStabCoM[0],2))+"   "+str(round(HStabCoM[1],2))+"   "+str(round(HStabCoM[2],2))+"     "+str(round(IxxHStab,2))+"    "+str(round(IyyHStab,2))+"    "+str(round(IzzHStab,2))+"     ! HStab\n")

    VStabCoM = [0,0,0]
    for i in range(0,2):
        VStabCoM[i] = Acft.VStab.AttachPos[i]+Acft.VStab.CoM[i]
    VStabAvgChord = (Acft.VStab.RootChord+Acft.VStab.TipChord)/2
    IxxVStab = Acft.VStab.Mass*(Acft.VStab.Span**3)*VStabAvgChord/12
    IyyVStab = Acft.VStab.Mass*Acft.VStab.Span*(VStabAvgChord**3)/12
    IzzVStab = Acft.VStab.Mass*Acft.VStab.Span*(VStabAvgChord**3)/12
    MassFile.write("   "+str(round(Acft.VStab.Mass,2))+"   "+str(round(VStabCoM[0],2))+"   "+str(round(VStabCoM[1],2))+"   "+str(round(VStabCoM[2],2))+"     "+str(round(IxxVStab,2))+"    "+str(round(IyyVStab,2))+"    "+str(round(IzzVStab,2))+"     ! VStab\n")
    
    IxxBatL = 0
    IyyBatL = 0
    IzzBatL = 0
    MassFile.write("   "+str(round(Acft.Battery.Mass.L,2))+"   "+str(round(Acft.Battery.CoM.L[0],2))+"   "+str(round(Acft.Battery.CoM.L[1],2))+"   "+str(round(Acft.Battery.CoM.L[2],2))+"     "+str(round(IxxBatL,2))+"    "+str(round(IyyBatL,2))+"    "+str(round(IzzBatL,2))+"     ! BatL\n")

    IxxBatR = 0
    IyyBatR = 0
    IzzBatR = 0
    MassFile.write("   "+str(round(Acft.Battery.Mass.R,2))+"   "+str(round(Acft.Battery.CoM.R[0],2))+"   "+str(round(Acft.Battery.CoM.R[1],2))+"   "+str(round(Acft.Battery.CoM.R[2],2))+"     "+str(round(IxxBatR,2))+"    "+str(round(IyyBatR,2))+"    "+str(round(IzzBatR,2))+"     ! BatR\n")

    IxxBatF = 0
    IyyBatF = 0
    IzzBatF = 0
    MassFile.write("   "+str(round(Acft.Battery.Mass.F,2))+"   "+str(round(Acft.Battery.CoM.F[0],2))+"   "+str(round(Acft.Battery.CoM.F[1],2))+"   "+str(round(Acft.Battery.CoM.F[2],2))+"     "+str(round(IxxBatF,2))+"    "+str(round(IyyBatF,2))+"    "+str(round(IzzBatF,2))+"     ! BatF\n")

    MassFile.close()

    #End of WriteACtoFile