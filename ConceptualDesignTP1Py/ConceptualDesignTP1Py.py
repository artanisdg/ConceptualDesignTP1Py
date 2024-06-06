import sys
import os
if 'darwin' in sys.platform:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

import math
import packages.MainFunctions

if 'Mac' in sys.platform:
    import packages.AVLFunctionsMac as AVLFunctionsMac
elif 'Windows' in sys.platform:
    import packages.AVLFunctions as AVLFunctions



Specs = open("Specs1.csv","a")
Specs.write("C, R, S, V")
Specs.close()


