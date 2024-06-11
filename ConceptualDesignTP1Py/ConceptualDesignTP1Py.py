import os
import sys

if "darwin" in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import string
import subprocess
import time

import packages.AVLAircraft as Acft
import packages.AVLFunctions as AVLF
import packages.MainFunctions as MainF

AVL_PATH = os.path.join(os.getcwd(), "TestRun_2/Test.avl")
MASS_PATH = os.path.join(os.getcwd(), "TestRun_2/Test.mass")
RUN_PATH = os.path.join(os.getcwd(), "T1/Test.run")

RTTest = AVLF.runtime(AVL_PATH, MASS_PATH, RUN_PATH)
print(RTTest.AVLSession.pid)
TestAC = Acft.Aircraft(1, "Test")

# MainF.runAVL(RTTest,"T1/Results.txt")

# RTTest.reStartAVL()

TestPackage = MainF.PackageData


if __name__ == "__main__":
    TestSession = MainF.Session(RTTest, TestAC, "TestRun_2")
    TestSession.AeroAnalysis()

    STAB = TestSession.CGAnalysis()
    if STAB != 0:
        MainF.resizeAC(TestAC, STAB)

    if STAB == 0:
        TO = TestSession.TOAnalysis()

        if TO != 0:
            MainF.resizeAC(TestAC, TO)

        if TO == 0:
            CLB = TestSession.CLBAnalysis()

            CRZ = TestSession.CRZAnalysis()


# MainF.CLBAnalysis()
# MainF.CRZAnalysis()
# MainF.DESAnalysis()
# MainF.LDGAnalysis()
# MainF.TaxiAnalysis()
