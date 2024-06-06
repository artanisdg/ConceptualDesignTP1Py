import os
import sys
import math

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import packages.AVLFunctions as AVLF


class AircraftData:
    def __init__(self,modType):
        self.ModelType = modType
    
    class Wing:
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
        Sweep = 0
        Airfoil = 2412
        AttachPos = [0,0,0]
        CoM = [0,0]
        Mass = 0

    class Fuselage:
        Length = 0
        Height = 0
        SlopeUpper = 0
        SlopeLower = 0
        SlopeSide = 0
        CoM = [0,0]
        Mass = 0

    class HStab:
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
        Sweep = 0
        Airfoil = 0
        AttachPos = [0,0,0]
        CoM = [0,0]
        Mass = 0

    class VStab:
        Num = 1
        RootChord = 0
        TipChord = 0
        Span = 0
        Sweep = 0
        AttachPos = [0,0,0]
        CoM = [0,0]
        Mass = 0

    class MotorPod:
        Num = 0
        AttachPos = [0,0,0]
        Radius = 0
        Length = 0
        CoM = [0,0]
        Mass = 0