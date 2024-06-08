import os, sys

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import string
import time
import packages.AVLFunctions as AVLF
import packages.AVLAircraft as Acft
import packages.MainFunctions as MainF


RTTest = AVLF.runtime("T1/Test.avl","T1/Test.mass","T1/Test.run")
TestAC = Acft.Aircraft(1,"Test")

MainF.initSizing(RTTest,TestAC,"Test.txt",20)

#MainF.runAVL(RTTest,"T1/Results.txt")

#RTTest.reStartAVL()

TestSession = MainF.Session(RTTest,TestAC,"TestSession")


while 1:
    TestSession.AeroAnalysis()

while 1:
    TO = TestSession.TOAnalysis()

    if TO != 0:
        0 #tbd
        
    else:
        break
    

# MainF.CLBAnalysis()
# MainF.CRZAnalysis()
# MainF.DESAnalysis()
# MainF.LDGAnalysis()
# MainF.TaxiAnalysis()