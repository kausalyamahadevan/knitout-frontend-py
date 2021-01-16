#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff

# from crossover_full import *
from library.crossover_half import *
from library.crossover_full import *

# from seedKnit import*
from library.jersey import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c='3'
k.ingripper('1')
k.ingripper('2')
k.ingripper('3')

width=20

k.stitchNumber(5)
castonbindoff.caston(k,width,['1','2','3'])
#

for w in range(width):
    k.xfer(('b',w),('f',w))

k.stitchNumber(6)
k.speedNumber(300)
k.rollerAdvance(400)
jerseyKnit(k,width,4,c,'l')

k.stitchNumber(5)
crossoverHalf(k,width,20,c,'l')
#
k.stitchNumber(6)
k.speedNumber(300)
k.rollerAdvance(400)
jerseyKnit(k,width,10,c,'l')

k.stitchNumber(5)
crossoverFull(k,width,20,c,'l')

k.stitchNumber(6)
k.speedNumber(300)
k.rollerAdvance(400)
jerseyKnit(k,width,10,c,'l')

for s in range(20):
    k.drop(('f',s))

k.outgripper('1')
k.outgripper('2')
k.outgripper('3')

k.write('racktest.k')
