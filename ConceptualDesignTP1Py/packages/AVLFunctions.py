import math
import os
import signal
import string
import subprocess
import sys

if "darwin" in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))


def createAVLFile(name):
    0  # Do I really need this?


def createMassFile(name):
    0  # Do I really need this?


class runtime:
    def __init__(self, AVLnm, Massnm, Runnm):
        self.RunFileName = Runnm
        self.AVLFileName = AVLnm
        self.MassFileName = Massnm
        self.createRunFile()
        self.AVLSession = None

    def reStartAVL(self):
        self.AVLreturn()
        self.AVLreturn()

    def createRunFile(self):
        RunFile = open(self.RunFileName, "w")
        RunFile.write(
            " ---------------------------------------------\n Run case  1:  Empty"
        )
        RunFile.close()

    def readRunFile(self):
        RunFile = open(self.RunFileName)
        return RunFile.readlines()

    def appendRunFile(self, stuff: str):
        RunFile = open(self.RunFileName, "a")
        RunFile.write(str)
        RunFile.close()

    def overwriteRunFile(self, stuffs: list[str]):
        RunFile = open(self.RunFileName, "w")
        RunFile.writelines(stuffs)
        RunFile.close()

    def readRunFileName(self):
        return self.RunFileName

    def readAVLFileName(self):
        return self.AVLFileName

    def readMassFileName(self):
        return self.MassFileName

    def setRunFileName(self, input):
        self.RunFileName = input

    def setAVLFileName(self, input):
        self.AVLFileName = input

    def setMassFileName(self, input):
        self.MassFileName = input

    def AVLcommand(self, cmd: str):
        if self.AVLSession.poll() is not None:
            return
        print(f"\n{cmd}\n")
        print(cmd, file=self.AVLSession.stdin, flush=True)

    def AVLreturn(self):
        if self.AVLSession.poll() is not None:
            return
        print()
        print(file=self.AVLSession.stdin, flush=True)

    # --------------End of Class : runtime----------------------
