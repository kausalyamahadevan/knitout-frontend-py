#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from library import fairIsleStiffFxn
from library import Ottoman


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
tablength=30
length=30

k.stitchNumber(5)
castonbindoff.caston(k,width,[c1,c2,c3,c5])

castonbindoff.interlock(k,width,tablength,c2,'l')

for s in range(width):
    k.drop(('b',s))

fairIsleStiffFxn.missArray(k,4,1,0,width,length,c3,'l','f')
Ottoman.ottomanStitch(k,0,width,length,c3,4,'l','f')

for s in range(width):
    k.drop(('f',s))
    k.drop(('b',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)

k.write('sensorInterlock.k')
