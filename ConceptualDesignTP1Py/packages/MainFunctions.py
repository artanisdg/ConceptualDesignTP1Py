import os
import sys
import math
import string

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft

def initSizing(avl:AVLF.runtime,ACFT:Acft.Aircraft,pth:string,res:int):
    ACFT.ReadFromTxt(pth)
    Acft.WriteACtoFile(ACFT,avl,res)
    0 #tbd

def resizeAC(ACFT:Acft.Aircraft,option:int):
    if   option == 1: #CL too low
        ACFT.Wing.SpanHalf = ACFT.Wing.SpanHalf * 1.05
        ACFT.Wing.Mass = (ACFT.Wing.Mass - ACFT.Battery.Mass.R) * 1.08 + ACFT.Battery
    elif option == 99: #CL excessive
        0#tbd
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
        ACFT.Wing.Mass = (ACFT.Wing.Mass - ACFT.Wing.BattMass) * 1.05 + ACFT.Wing.BattMass
    elif option == 12: #HStab ineffective -> Move Further Back
        ACFT.HStab.AttachPos[0] = ACFT.HStab.AttachPos[0] + 0.3
    else:
        print("resizeAC Function Call Error")

def runAVL():
    0 #tbd

def analyzeAero():
    0 #tbd

def analyzePerf():
    0 #tbd