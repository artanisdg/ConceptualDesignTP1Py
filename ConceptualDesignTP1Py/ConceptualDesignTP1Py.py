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

TestPackage = MainF.PackageData

TestSession = MainF.Session(RTTest,TestAC,"TestRun")


while 1:
    
    
    TestSession.AeroAnalysis()

    STAB = TestSession.CGAnalysis()
    if STAB != 0:
        TestSession.resizeAC(STAB)

    if STAB == 0:
        TO = TestSession.TOAnalysis()

        if TO != 0:
            TestSession.resizeAC(TO)
            
        if TO == 0:
            CLB = TestSession.CLBAnalysis()

            if CLB != 0:
                TestSession.resizeAC(CLB)
            
            if CLB == 0:
                CRZ = TestSession.CRZAnalysis()
                
                if CRZ != 0:
                    TestSession.resizeAC(CRZ)
                    
                if CRZ == 0:
                    DES = TestSession.DESAnalysis()
                    
                    if DES != 0:
                        TestSession.resizeAC(DES)
                    
                    if DES == 0:
                        LDG = TestSession.LDGAnalysis()
                        
                        if LDG != 0:
                            TestSession.resizeAC(LDG)
                            
                        if LDG == 0:
                            Taxi = TestSession.TaxiAnalysis()
                            
                            if Taxi != 0:
                                0

                            if Taxi == 0:
                                break
                    


time.sleep(1000)