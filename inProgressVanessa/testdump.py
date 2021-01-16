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
from library.fairIsleStiffFxn import*
from library.jerseyVariedStitches import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c3='3'


k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)

width=60

k.stitchNumber(5)
castonbindoff.caston(k,width,[c1,c2,c3])
#

for w in range(width):
    k.xfer(('b',w),('f',w))

# jerseyarray= [3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,6,6,6,5,5,5,4,4,4]
# jerseyStitches(k,jerseyarray,width,20,c3,'l')

k.stitchNumber(6)
k.speedNumber(400)
k.rollerAdvance(400)
jerseyKnit(k,width,4,c3,'l')

k.stitchNumber(5)
k.speedNumber(300)
k.rollerAdvance(200)
fairArray=[1,1,1,1,2,2,2,2]
stiffFairIsle(k,fairArray,width,20,c3,c2,'l')

k.stitchNumber(6)
k.speedNumber(400)
k.rollerAdvance(400)
jerseyKnit(k,width,10,c3,'l')

# k.stitchNumber(5)
# crossoverFull(k,width,20,c,'l')
# #
# k.stitchNumber(6)
# k.speedNumber(300)
# k.rollerAdvance(400)
# jerseyKnit(k,width,10,c,'l')
#



for s in range(width):
    k.drop(('f',s))

k.outgripper('1')
k.outgripper('2')
k.outgripper('3')

k.write('fairIsleStiff.k')
