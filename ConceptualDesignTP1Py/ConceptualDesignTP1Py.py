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

RTTest = AVLF.runtime("Test.avl","Test.mass","Test.run")
TestAC = Acft.Aircraft(1,"Test")

MainF.initSizing(RTTest,TestAC,"Test.txt",10)

MainF.runAVL(RTTest,"Results.txt")