#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
import sensorSamples
from library import jersey
from library import ribbing
from library import fairIsleStiffFxn
from library import garter
from library import inlay



import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c6='6'
c5='5'
mainSampleYarn=c6;
secondYarn=c5

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(mainSampleYarn)



sampleStitchsize=4
tabStitchsize=4
transferStitchSize=2




width=40
tablength=30
samplelength=40


k.speedNumber(400)
k.rollerAdvance(400)
k.stitchNumber(4)

#make first tab
castonbindoff.interlock(k,39,30,c5,'r')

for s in range(width):
    if s%2==1 or s>11:
        k.drop(('f',s))
for s in range(width):
    if s%2==0 or s>11:
        k.drop(('b',s))



k.outgripper(c1)
k.outgripper(c2)
k.outgripper(mainSampleYarn)



k.write('interlockSeg.k')
