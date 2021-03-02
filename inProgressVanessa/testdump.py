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
c6='6'

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)
k.ingripper(c5)
k.ingripper(c6)

width=100
tablength=30
length=50

newx=np.array([[1,1,1,2,2,2,3,3,3],[1,1,2,2,2,3,3,3,1],[1,2,2,2,3,3,3,1,1],
    [2,2,2,3,3,3,1,1,1],[2,2,3,3,3,1,1,1,2],[2,3,3,3,1,1,1,2,2],[3,3,3,1,1,1,2,2,2],
    [3,3,1,1,1,2,2,2,3],[3,1,1,1,2,2,2,3,3],[1,1,1,2,2,2,3,3,3]], int)

newx=newx-1;

ribarray=[1,1,0,0]

k.stitchNumber(4)
castonbindoff.caston(k,width,[c1,c2,c3,c5,c6])

k.rack(0)
castonbindoff.interlock(k,width,tablength,c2,'l')

Ottoman.ottomanStitch(k,0,width,length,c3,6,2,'l','f')


k.rack(0)
castonbindoff.interlock(k,width,tablength,c2,'l')

Ottoman.realStriperPattern(k,0,width,length,[c3,c5,c6],newx)

castonbindoff.interlock(k,width,tablength,c2,'l')



for s in range(width):
    k.drop(('f',s))
for s in range(width):
    k.drop(('b',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)
k.outgripper(c6)

k.write('kniterateHW2.k')
