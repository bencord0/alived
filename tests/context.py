import sys
import os
from functools import reduce

toppath = os.path.abspath('..')
sys.path.insert(0, toppath)

import alived

def bsjoin(iterable):
    return reduce(lambda x,y: x+y, iterable).decode()
