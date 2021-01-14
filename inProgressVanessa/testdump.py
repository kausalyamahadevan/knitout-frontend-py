#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff

from crossover_full import *
from crossover_half import *
from seedKnit import*
from jersey import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c='3'

k.stitchNumber(5)
castonbindoff.caston(k,20,['1','2','3'])
#crossoverFull(k,20,20,c,'l')
k.stitchNumber(6)
k.speedNumber(300)
k.rollerAdvance(400)
jerseyKnit(k,20,5,c,'l')




k.write('aatestdump.k')
