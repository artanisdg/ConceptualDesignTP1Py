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
        self.Wing()
        self.Fuselage()
        self.HStab()
        self.Vstab()
        self.MotorPod()
    
    class Wing:
        def __init__(self):
            self.AttachPos = [0,0,0]
            self.CoM = [0,0,0]
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
        Sweep = 0
        Airfoil = 2412
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