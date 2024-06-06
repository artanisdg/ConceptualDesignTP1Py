import os
import sys

if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import packages.MainFunctions as MainF

if 'darwin' in sys.platform:
    import packages.AVLFunctionsMac as AVLF
else:
    import packages.AVLFunctions as AVLF



Specs = open("Specs1.csv","a")
Specs.write("C, R, S, V")
Specs.close()


