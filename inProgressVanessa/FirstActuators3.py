#get the necessary portions
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from library import ribbing
from library import jersey

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
length=10


k.stitchNumber(4)
castonbindoff.caston(k,width,[c1,c2,c3,c5])


k.stitchNumber(4)
k.rollerAdvance(400)
k.speedNumber(400)

castonbindoff.interlock(k,width,4,c3,'l')



for x in range(length):

    k.stitchNumber(4)
    k.rollerAdvance(300)

    jersey.jerseyKnit(k,width,1,c3,'l')

    k.stitchNumber(7)
    k.rollerAdvance(300)
    jersey.jerseyKnit(k,width,2,c3,'r','b')

    k.stitchNumber(4)
    k.rollerAdvance(300)
    jersey.jerseyKnit(k,width,1,c3,'r')


k.rollerAdvance(400)
k.speedNumber(400)
k.stitchNumber(4)
castonbindoff.interlock(k,width,6,c3,'l')



for s in range(width):
    k.drop(('f',s))
    k.drop('b',s)

k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)

k.write('InflatableActuator3.k')
