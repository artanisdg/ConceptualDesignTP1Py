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

    class MotorPod:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        Num = 0
        Radius = 0
        Length = 0
        Mass = 0
        
    def readFromTxt(self):
        0 #tbd
        
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