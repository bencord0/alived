import sys
import os
toppath = os.path.join(__file__, '..', '..')
toppath = os.path.abspath(toppath)

print(toppath)
sys.path.insert(0, toppath)

import alived
