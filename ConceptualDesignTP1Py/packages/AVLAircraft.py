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
        self.Wing()
        self.Fuselage()
        self.HStab()
        self.VStab()
        self.MotorPod()
    
    Name = None
    Mass = 0

    class Wing:
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

    class Fuselage:
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

    class HStab:
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

    class VStab:
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

    class MotorPod:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        Num = 0
        Radius = 0
        Length = 0
        Mass = 0
        #--------End of SubClass : MotorPod--------
    
    class Battery:
        class CoM:
            def __init__(self):
                self.L = [0,0,0]
                self.R = [0,0,0]
                self.F = [0,0,0]
        class Mass:
            L = 0
            R = 0
            F = 0
        #--------End of SubClass : Battery--------
        
    def ReadFromTxt(self,path:string):
        AcftTxt = open(path,"r")
        linesTemp = AcftTxt.readlines()
        Section:string = None
        Key:int = 0
        Tgt:int = 0
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
            
            else:
                line.split('=')
                for val in line:
                    val = val.strip()
                
                if Section == "Generic":
                    if line[0] == "Name":
                        self.Name = line[1]
                        G=G+1
                    elif line[0] == "ModelType":
                        self.ModelType = line[1]
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
                            self.Wing.AttachPos[i]=PosVec
                        W=W+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.Wing.CoM[i]=PosVec
                        W=W+1
                    elif line[0] == "RootChord":
                        self.Wing.RootChord = line[1]
                        W=W+1
                    elif line[0] == "TipChord":
                        self.Wing.TipChord = line[1]
                        W=W+1
                    elif line[0] == "SpanHalf":
                        self.Wing.SpanHalf = line[1]
                        W=W+1
                    elif line[0] == "Sweep":
                        self.Wing.Sweep = line[1]
                        W=W+1
                    elif line[0] == "Airfoil":
                        self.Wing.Airfoil = line[1]
                        W=W+1
                    elif line[0] == "Ainc":
                        self.Wing.Ainc = line[1]
                        W=W+1
                    elif line[0] == "Mass":
                        self.Wing.Mass = line[1]
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
                            self.Fuselage.CoM[i]=PosVec
                        F=F+1
                    elif line[0] == "Length":
                        self.Fuselage.Length = line[1]
                        F=F+1
                    elif line[0] == "Height":
                        self.Fuselage.Height = line[1]
                        F=F+1
                    elif line[0] == "Width":
                        self.Fuselage.Width = line[1]
                        F=F+1
                    elif line[0] == "SlopeUpper":
                        self.Fuselage.SlopeUpper = line[1]
                        F=F+1
                    elif line[0] == "SlopeLower":
                        self.Fuselage.SlopeLower = line[1]
                        F=F+1
                    elif line[0] == "SlopeSide":
                        self.Fuselage.SlopeSide = line[1]
                        F=F+1
                    elif line[0] == "Mass":
                        self.Fuselage.Mass = line[1]
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
                            self.HStab.AttachPos[i]=PosVec
                        HS=HS+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.HStab.CoM[i]=PosVec
                        HS=HS+1
                    elif line[0] == "RootChord":
                        self.HStab.RootChord = line[1]
                        HS=HS+1
                    elif line[0] == "TipChord":
                        self.HStab.TipChord = line[1]
                        HS=HS+1
                    elif line[0] == "SpanHalf":
                        self.HStab.SpanHalf = line[1]
                        HS=HS+1
                    elif line[0] == "Sweep":
                        self.HStab.Sweep = line[1]
                        HS=HS+1
                    elif line[0] == "Airfoil":
                        self.HStab.Airfoil = line[1]
                        HS=HS+1
                    elif line[0] == "Ainc":
                        self.HStab.Ainc = line[1]
                        HS=HS+1
                    elif line[0] == "Mass":
                        self.HStab.Mass = line[1]
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
                            self.VStab.AttachPos[i]=PosVec
                        VS=VS+1
                    elif line[0] == "CoM":
                        PosVec = line[1].split(',')
                        for Val in PosVec:
                            Val.strip()
                        for i in [0,1,2]:
                            self.VStab.CoM[i]=PosVec
                        VS=VS+1
                    elif line[0] == "Num":
                        self.VStab.Num = line[1]
                        VS=VS+1
                    elif line[0] == "RootChord":
                        self.VStab.RootChord = line[1]
                        VS=VS+1
                    elif line[0] == "TipChord":
                        self.VStab.TipChord = line[1]
                        VS=VS+1
                    elif line[0] == "Span":
                        self.VStab.Span = line[1]
                        VS=VS+1
                    elif line[0] == "Sweep":
                        self.VStab.Sweep = line[1]
                        VS=VS+1
                    elif line[0] == "Mass":
                        self.VStab.Mass = line[1]
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
        
        self.Battery.CoM.R[0] = self.Wing.AttachPoint[0] + self.Wing.CoM[0]
        self.Battery.CoM.R[1] = self.Wing.AttachPoint[1] + self.Wing.CoM[1]
        self.Battery.CoM.R[2] = self.Wing.AttachPoint[2] + self.Wing.CoM[2]

        self.Battery.CoM.L[0] = self.Wing.AttachPoint[0] + self.Wing.CoM[0]
        self.Battery.CoM.L[1] = -self.Wing.AttachPoint[1] - self.Wing.CoM[1]
        self.Battery.CoM.L[2] = self.Wing.AttachPoint[2] + self.Wing.CoM[2]
        #End of ReadFromTxt

        
    def CalcCoM(self):
        GW = 2*self.Wing.Mass+2*self.Fuselage.Mass+2*self.HStab.Mass+self.VStab.Num*self.VStab.Mass+self.MotorPod.Num*self.MotorPod.Mass
        
        xM = (2*self.Wing.Mass*(self.Wing.AttachPos[0]+self.Wing.CoM[0])
             +self.Fuselage.Mass*self.Fuselage.CoM[0]
             +2*self.HStab.Mass*(self.HStab.AttachPos[0]+self.HStab.CoM[0])
             +self.VStab.Num*self.VStab.Mass*(self.VStab.AttachPos[0]+self.VStab.CoM[0])
             +self.MotorPod.Num*self.MotorPod.Mass*(self.MotorPod.AttachPos[0]+self.MotorPod.CoM[0]))
        x = xM/GW

        yM = self.Fuselage.Mass*self.Fuselage.CoM[1]
        y = yM/GW
        
        zM = (2*self.Wing.Mass*(self.Wing.AttachPos[2]+self.Wing.CoM[2])
             +self.Fuselage.Mass*self.Fuselage.CoM[2]
             +2*self.HStab.Mass*(self.HStab.AttachPos[2]+self.HStab.CoM[2])
             +self.VStab.Num*self.VStab.Mass*(self.VStab.AttachPos[2]+self.VStab.CoM[2])
             +self.MotorPod.Num*self.MotorPod.Mass*(self.MotorPod.AttachPos[2]+self.MotorPod.CoM[2]))
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
    AVLFile.write(Acft.CoM[0]+"     "+Acft.CoM[1]+"     "+Acft.CoM[2]+"\n")
    AVLFile.write("#--------------------------------------------------\n")


    #Write Wing
    AVLFile.write("SURFACE\nWing\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write(slices+"           "+"1.0"+"     "+2*slices+"         1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(Acft.Wing.AttachPos[0]+"  "+Acft.Wing.AttachPos[1]+"  "+Acft.Wing.AttachPos[2]+"\n\n\n")

    intervalWing:float = Acft.Wing.SpanHalf/slices
    for i in range(0,slices-1):
        Chord:float = (Acft.Wing.RootChord*(slices-i)+Acft.Wing.TipChord*i)/slices
        LEx:float = intervalWing*i*math.tan(Acft.Wing.Sweep/180*math.pi)
        LEy:float = intervalWing*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"    "+Acft.Wing.Ainc+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(Acft.Wing.Airfoil+"\n")
        if i < slices/2:
            AVLFile.write("CONTROL\n")
            AVLFile.write("flap     1.0  0.70  0. 0. 0.  +1\n")
        if i > 3*slices/4:
            AVLFile.write("CONTROL\n")
            AVLFile.write("aileron  1.0  0.80  0. 0. 0.  -1\n")
        AVLFile.write("\n")


    #Write FuselageH
    AVLFile.write("SURFACE\nFuselage Horizontal\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseH:float = Acft.Fuselage.Width/10
    for i in range(0,10):
        Chord:float = Acft.Fuselage.Length-i*(Acft.Fuselage.Width*math.tan(Acft.Fuselage.SlopeSide/180*math.pi))
        LEx:float = i*(Acft.Fuselage.Width*math.tan(Acft.Fuselage.SlopeSide/180*math.pi))
        LEy:float = intervalFuseH*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"   0.    1          0.\n")
        AVLFile.write("\n")

    #Write FuselageVU
    AVLFile.write("SURFACE\nFuselage V Upper\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseV:float = Acft.Fuselage.Height/20
    for i in range(0,10):
        Chord:float = Acft.Fuselage.Length-i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeUpper/180*math.pi))
        LEx:float = i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeUpper/180*math.pi))
        LEz:float = intervalFuseV*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(LEx+"    "+"0.0"+"    "+LEz+"     "+Chord+"   0.    1          0.\n")
        AVLFile.write("\n")

    #Write FuselageVL
    AVLFile.write("SURFACE\nFuselage V Lower\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write("10           1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    intervalFuseV:float = Acft.Fuselage.Height/20
    for i in range(0,10):
        Chord:float = Acft.Fuselage.Length-i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeLower/180*math.pi))
        LEx:float = i*((Acft.Fuselage.Height/2)*math.tan(Acft.Fuselage.SlopeLower/180*math.pi))
        LEz:float = intervalFuseV*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(LEx+"    "+"0.0"+"    "+LEz+"     "+Chord+"   0.    1          0.\n")
        AVLFile.write("\n")


    StabSlices:int = 10

    #Write Hstab
    AVLFile.write("SURFACE\nHorizontal Stabilizer\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
    AVLFile.write(StabSlices+"           "+"1.0"+"     "+2*StabSlices+"         1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(Acft.HStab.AttachPos[0]+"  "+Acft.HStab.AttachPos[1]+"  "+Acft.HStab.AttachPos[2]+"\n\n\n")

    intervalHStab:float = Acft.HStab.SpanHalf/StabSlices
    for i in range(0,StabSlices-1):
        Chord:float = (Acft.HStab.RootChord*(StabSlices-i)+Acft.HStab.TipChord*i)/StabSlices
        LEx:float = intervalHStab*i*math.tan(Acft.HStab.Sweep/180*math.pi)
        LEy:float = intervalHStab*i
        AVLFile.write("SECTION\n")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"    "+Acft.HStab.Ainc+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(Acft.HStab.Airfoil+"\n")
        AVLFile.write("CONTROL\n")
        AVLFile.write("elevator 1.0  0.70  0. 0. 0.  +1\n")
        AVLFile.write("\n")

    #Write Vstab
    if Acft.VStab.Num == 1:
        AVLFile.write("SURFACE\nVertical Stabilizer\n")
        AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
        AVLFile.write(StabSlices+"           "+"1.0"+"     "+2*StabSlices+"         1.0\n")
        AVLFile.write("\n")
        AVLFile.write("COMPONENT \n1\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
        AVLFile.write("\n")
        AVLFile.write("TRANSLATE\n")
        AVLFile.write(Acft.VStab.AttachPos[0]+"  "+Acft.VStab.AttachPos[1]+"  "+Acft.VStab.AttachPos[2]+"\n\n\n")

        intervalVStab:float = Acft.VStab.Span/StabSlices
        for i in range(0,StabSlices-1):
            Chord:float = (Acft.VStab.RootChord*(StabSlices-i)+Acft.VStab.TipChord*i)/StabSlices
            LEx:float = intervalVStab*i*math.tan(Acft.VStab.Sweep/180*math.pi)
            LEz:float = intervalVStab*i
            AVLFile.write("SECTION\n")
            AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
            AVLFile.write(LEx+"    "+"0.0"+"    "+LEz+"     "+Chord+"    0.\n")
            AVLFile.write("CONTROL\n")
            AVLFile.write("rudder 1.0  0.70  0. 0. 0.  +1\n")
            AVLFile.write("\n")

    elif Acft.VStab.Num ==2:
        AVLFile.write("SURFACE\nVertical Stabilizer\n")
        AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace\n") 
        AVLFile.write(StabSlices+"           "+"1.0"+"     "+2*StabSlices+"         1.0\n")
        AVLFile.write("\n")
        AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
        AVLFile.write("\n")
        AVLFile.write("TRANSLATE\n")
        AVLFile.write(Acft.VStab.AttachPos[0]+"  "+Acft.VStab.AttachPos[1]+"  "+Acft.VStab.AttachPos[2]+"\n\n\n")

        intervalVStab:float = Acft.VStab.Span/StabSlices
        for i in range(0,StabSlices-1):
            Chord:float = (Acft.VStab.RootChord*(StabSlices-i)+Acft.VStab.TipChord*i)/StabSlices
            LEx:float = intervalVStab*i*math.tan(Acft.VStab.Sweep/180*math.pi)
            LEz:float = intervalVStab*i
            AVLFile.write("SECTION\n")
            AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n")
            AVLFile.write(LEx+"    "+"0.0"+"    "+LEz+"     "+Chord+"    0.\n")
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

    WingCoM = None
    for i in range(0,2):
        WingCoM[i] = Acft.Wing.AttachPoint[i]+Acft.Wing.CoM[i]
    WingAvgChord = (Acft.Wing.RootChord+Acft.Wing.TipChord)/2
    IxxWing = Acft.Wing.Mass*(Acft.Wing.SpanHalf^3)*WingAvgChord/12
    IyyWing = Acft.Wing.Mass*Acft.Wing.SpanHalf*(WingAvgChord^3)/12
    IzzWing = Acft.Wing.Mass*Acft.Wing.SpanHalf*(WingAvgChord^3)/12
    MassFile.write("   "+Acft.Wing.Mass+"   "+WingCoM[0]+"   "+WingCoM[1]+"   "+WingCoM[2]+"    "+IxxWing+"    "+IyyWing+"    "+IzzWing+"     ! Wing\n")

    IxxFuse = Acft.Fuselage.Mass*(Acft.Fuselage.Height^3)*Acft.Fuselage.Length/12
    IyyFuse = Acft.Fuselage.Mass*Acft.Fuselage.Height*(Acft.Fuselage.Length^3)/12
    IzzFuse = Acft.Fuselage.Mass*Acft.Fuselage.Width*(Acft.Fuselage.Length^3)/12
    MassFile.write("   "+Acft.Fuselage.Mass+"   "+Acft.Fuselage.CoM[0]+"   "+Acft.Fuselage.CoM[1]+"   "+Acft.Fuselage.CoM[2]+"    "+IxxFuse+"    "+IyyFuse+"    "+IzzFuse+"     ! Fuselage\n")
    
    HStabCoM = None
    for i in range(0,2):
        HStabCoM[i] = Acft.HStab.AttachPoint[i]+Acft.HStab.CoM[i]
    HStabAvgChord = (Acft.HStab.RootChord+Acft.HStab.TipChord)/2
    IxxHStab = Acft.HStab.Mass*(Acft.HStab.SpanHalf^3)*HStabAvgChord/12
    IyyHStab = Acft.HStab.Mass*Acft.HStab.SpanHalf*(HStabAvgChord^3)/12
    IzzHStab = Acft.HStab.Mass*Acft.HStab.SpanHalf*(HStabAvgChord^3)/12
    MassFile.write("   "+Acft.HStab.Mass+"   "+HStabCoM[0]+"   "+HStabCoM[1]+"   "+HStabCoM[2]+"     "+IxxHStab+"    "+IyyHStab+"    "+IzzHStab+"     ! HStab\n")

    VStabCoM = None
    for i in range(0,2):
        VStabCoM[i] = Acft.VStab.AttachPoint[i]+Acft.VStab.CoM[i]
    VStabAvgChord = (Acft.VStab.RootChord+Acft.VStab.TipChord)/2
    IxxVStab = Acft.VStab.Mass*(Acft.VStab.Span^3)*VStabAvgChord/12
    IyyVStab = Acft.VStab.Mass*Acft.VStab.Span*(VStabAvgChord^3)/12
    IzzVStab = Acft.VStab.Mass*Acft.VStab.Span*(VStabAvgChord^3)/12
    MassFile.write("   "+Acft.VStab.Mass+"   "+VStabCoM[0]+"   "+VStabCoM[1]+"   "+VStabCoM[2]+"     "+IxxVStab+"    "+IyyVStab+"    "+IzzVStab+"     ! VStab\n")

    MassFile.close()

    #End of WriteACtoFile