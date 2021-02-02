#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff

# from crossover_full import *
# from library.crossover_half import *
# from library.crossover_full import *

# from seedKnit import*
from library.jersey import*
from library.tuckstuff import*
# from library.fairIsleStiffFxn import*
# from library.jerseyVariedStitches import*
from library.ribbing import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c3='3'
c5='5'


k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)
k.ingripper(c5)

width=30

k.stitchNumber(5)
castonbindoff.caston(k,width,[c1,c2,c3,c5])
#

for w in range(width):
    k.xfer(('b',w),('f',w))

k.stitchNumber(4)
k.speedNumber(400)
k.rollerAdvance(400)
jerseyKnit(k,width,30,c3,'l')

k.stitchNumber(4)
k.speedNumber(400)
k.rollerAdvance(400)
jerseyKnit(k,width,30,c5,'l')


k.stitchNumber(4)
k.speedNumber(400)
k.rollerAdvance(400)
jerseyKnit(k,width,10,c2,'l')

# # # jerseyarray = [4,4,4,4,4,4,8,8,8,8,8,8,8,8,8,8,4,4,4,4,4,4,4]
# # # # k.rollerAdvance(300)
# # # k.speedNumber(300)
# # # jerseyStitches(k,jerseyarray,width,6,c3,'l')
# #
# #
# # k.stitchNumber(5)
# # k.speedNumber(300)
# # k.rollerAdvance(250)
# # fairArray=[1,1,1,1,2,2,2,2]
# # stiffFairIsle(k,fairArray,width,50,c2,c3,'l')
# # # k.rack(0)
# # # crossoverHalf(k,width,6,c3,'l')
#
#
# # k.rack(0)
# # crossoverFull(k,width,50,c3,'l')
# #
# # k.rack(0)
# # k.stitchNumber(6)
# # k.speedNumber(400)
# # k.rollerAdvance(400)
# # jerseyKnit(k,width,20,c3,'l')
#

for s in range(width):
    k.drop(('f',s))

k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)

k.write('jerseySensor.k')
