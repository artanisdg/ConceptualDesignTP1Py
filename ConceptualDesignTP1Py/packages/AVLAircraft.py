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
    
    AVLFile = open(AVLpath,"a")
    
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
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace") 
    AVLFile.write(slices+"           "+"1.0"+"     "+2*slices+"         1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(Acft.Wing.AttachPos[0]+"  "+Acft.Wing.AttachPos[1]+"  "+Acft.Wing.AttachPos[2]+"\n\n\n")

    interval:float = Acft.Wing.SpanHalf/slices
    for i in range(1,slices-1):
        Chord:float = (Acft.Wing.RootChord*(slices-i)+Acft.Wing.TipChord*i)/slices
        LEx:float = interval*i*math.tan(Acft.Wing.Sweep/180*math.pi)
        LEy:float = interval*i
        AVLFile.write("SECTION")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"    "+Acft.Wing.Ainc+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(Acft.Wing.Airfoil+"\n")
        if i < slices/2:
            AVLFile.write("CONTROL\n")
            AVLFile.write("flap     1.0  0.7  0. 0. 0.  +1\n")
        if i > 3*slices/4:
            AVLFile.write("CONTROL\n")
            AVLFile.write("aileron  1.0  0.8  0. 0. 0.  -1\n")
        AVLFile.write("\n")


    #Write FuselageH
    AVLFile.write("SURFACE\nFuselageH\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace") 
    AVLFile.write(30+"           "+"1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write("0.0  0.0  0.0\n\n\n")

    interval:float = Acft.Wing.SpanHalf/slices
    for i in range(1,slices-1):
        Chord:float = (Acft.Wing.RootChord*(slices-i)+Acft.Wing.TipChord*i)/slices
        LEx:float = interval*i*math.tan(Acft.Wing.Sweep/180*math.pi)
        LEy:float = interval*i
        AVLFile.write("SECTION")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"    "+Acft.Wing.Ainc+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(Acft.Wing.Airfoil+"\n")
        if i < slices/2:
            AVLFile.write("CONTROL\n")
            AVLFile.write("flap     1.0  0.7  0. 0. 0.  +1\n")
        if i > 3*slices/4:
            AVLFile.write("CONTROL\n")
            AVLFile.write("aileron  1.0  0.8  0. 0. 0.  -1\n")
        AVLFile.write("\n")


    #Write FuselageV
    AVLFile.write("SURFACE\nFuselageH\n")
    AVLFile.write("!Nchordwise  Cspace  Nspanwise  Sspace") 
    AVLFile.write(30+"           "+"1.0\n")
    AVLFile.write("\n")
    AVLFile.write("COMPONENT \n1\n\nYDUPLICATE \n0.0\n\nANGLE\n0.0\n\nSCALE\n1.0   1.0   1.0\n")
    AVLFile.write("\n")
    AVLFile.write("TRANSLATE\n")
    AVLFile.write(Acft.Wing.AttachPos[0]+"  "+Acft.Wing.AttachPos[1]+"  "+Acft.Wing.AttachPos[2]+"\n\n\n")

    interval:float = Acft.Wing.SpanHalf/slices
    for i in range(1,slices-1):
        Chord:float = (Acft.Wing.RootChord*(slices-i)+Acft.Wing.TipChord*i)/slices
        LEx:float = interval*i*math.tan(Acft.Wing.Sweep/180*math.pi)
        LEy:float = interval*i
        AVLFile.write("SECTION")
        AVLFile.write("#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace")
        AVLFile.write(LEx+"    "+LEy+"    "+"0.0"+"     "+Chord+"    "+Acft.Wing.Ainc+"\n")
        AVLFile.write("NACA\n")
        AVLFile.write(Acft.Wing.Airfoil+"\n")
        if i < slices/2:
            AVLFile.write("CONTROL\n")
            AVLFile.write("flap     1.0  0.7  0. 0. 0.  +1\n")
        if i > 3*slices/4:
            AVLFile.write("CONTROL\n")
            AVLFile.write("aileron  1.0  0.8  0. 0. 0.  -1\n")
        AVLFile.write("\n")


  

# SECTION
# #Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
# -0.5    6.0    0.0     21.0    5.0  
# NACA
# 2412
# CONTROL
# slat    -1.0 -0.05  0. 0. 0.  +1
# CONTROL
# flap     1.0  0.81  0. 0. 0.  +1