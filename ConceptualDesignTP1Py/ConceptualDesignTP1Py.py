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


RTTest = AVLF.runtime("TestRun/Test.avl","TestRun/Test.mass","T1/Test.run")
TestAC = Acft.Aircraft(1,"Test")

#MainF.runAVL(RTTest,"T1/Results.txt")

#RTTest.reStartAVL()

TestPackage = MainF.PackageData

TestSession = MainF.Session(RTTest,TestAC,"TestRun")


while 1:
    TestSession.AeroAnalysis()

    STAB = TestSession.CGAnalysis()
    if STAB != 0:
        MainF.resizeAC(TestAC,STAB)

    if STAB == 0:
        TO = TestSession.TOAnalysis()

        if TO != 0:
            MainF.resizeAC(TestAC,TO)
            
        if TO == 0:
            CLB = TestSession.CLBAnalysis()

            CRZ = TestSession.CRZAnalysis()


time.sleep(1000)
    

# MainF.CLBAnalysis()
# MainF.CRZAnalysis()
# MainF.DESAnalysis()
# MainF.LDGAnalysis()
# MainF.TaxiAnalysis()