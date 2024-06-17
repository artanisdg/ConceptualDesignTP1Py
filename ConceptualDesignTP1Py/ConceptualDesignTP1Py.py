import os
import sys

if "darwin" in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import multiprocessing
import signal
import string
import subprocess
import time

import packages.AVLAircraft as Acft
import packages.AVLFunctions as AVLF
import packages.MainFunctions as MainF

OUTPUT_PATH = os.path.join(os.getcwd(), "TestRun_5")
RUN_PATH = os.path.join(os.getcwd(), "T1/Test.run")
AVL_PATH = os.path.join(OUTPUT_PATH, "Test.avl")
MASS_PATH = os.path.join(OUTPUT_PATH, "Test.mass")
MAX_WORKERS = 12


def run_avl_worker(config_queue, result_queue):
    def runSession(Alpha, Flap, Elev, resP: str):
        retval = MainF.operAVL(
            watcher_process_runtime, Alpha, Flap, Elev, OUTPUT_PATH + "/" + resP
        )
        return retval

    def quitAVL():
        watcher_process_runtime.AVLreturn()
        watcher_process_runtime.AVLreturn()
        watcher_process_runtime.AVLcommand("Quit")

    def preexec_function():
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    watcher_process_runtime = AVLF.runtime(AVL_PATH, MASS_PATH, RUN_PATH)
    if "darwin" in sys.platform:
        command = "../avl3.35"
    else:
        command = "avl.exe"
    avl_process = subprocess.Popen(
        command, stdin=subprocess.PIPE, text=True, preexec_fn=preexec_function
    )
    watcher_process_runtime.AVLSession = avl_process
    MainF.setupAVL(watcher_process_runtime)
    try:
        while True:
            config = config_queue.get()
            if config is None:
                quitAVL()
                break
            alpha, flap, elevation, result_path = config
            retval = runSession(alpha, flap, elevation, result_path)
            if retval:
                result_queue.put(config)
            else:
                config_queue.put(config)
            watcher_process_runtime.reStartAVL()
    except KeyboardInterrupt:
        quitAVL()

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    processes = []
    config_q = manager.Queue()
    result_q = manager.Queue()
    for idx in range(MAX_WORKERS):
        p = multiprocessing.Process(target=run_avl_worker, args=(config_q, result_q))
        p.start()
        processes.append(p)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    TestAC = Acft.Aircraft(1, "Test")

    TestPackage = MainF.PackageData
    RTTest = AVLF.runtime(AVL_PATH, MASS_PATH, RUN_PATH)
    TestSession = MainF.Session(RTTest, TestAC, OUTPUT_PATH)

    try:
        while True:
            TestSession.AeroAnalysis(config_q, result_q)
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
                                    if Taxi == 0:
                                        break
    except KeyboardInterrupt:
        ...
    else:
        for _ in range(MAX_WORKERS):
            config_q.put(None)
    finally:                    
        print("Cleaning")
        for p in processes:
            p.join()
