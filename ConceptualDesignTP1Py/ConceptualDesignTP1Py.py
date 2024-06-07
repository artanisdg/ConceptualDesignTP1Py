import os
import sys

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import string
import time
import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft
import packages.MainFunctions as MainF



# Specs = open("Specs1.csv","a")
# Specs.write("C, R, S, V")
# Specs.close()

RTTest = AVLF.runtime("T1/Test.avl","T1/Test.mass","T1/Test.run")
TestAC = Acft.Aircraft(1,"Test")

MainF.initSizing(RTTest,TestAC,"Test.txt",20)

MainF.runAVL(RTTest,"T1/Results.txt")