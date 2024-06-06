import os
import sys
import math

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

if 'darwin' in sys.platform:
    import packages.AVLFunctionsMac as AVLF
else:
    import packages.AVLFunctions as AVLF




class AircraftData:
    ModelType = 0
    
    class Wing:
        RootChord = 0
        TipChord = 0
        SpanHalf = 0
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
        Airfoil = 0
        AttachPos = [0,0,0]
        CoM = [0,0]
        Mass = 0

    class VStab:
        Num = 1
        RootChord = 0
        TipChord = 0
        Span = 0
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