#get the necessary portions
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from library import ribbing
from library import jersey
from library import fairIsleStiffFxn

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


width=120; #horiz width
length=20; #vert length

#set what the left end right edges are
edgeProtect=4; #left edge
InterlockSegment=4; #right edge
stitcharray=[1,1,1,1,0,0,0,0]#repeat for the fair isle on back

interlockStart=width-InterlockSegment;


k.stitchNumber(4)
castonbindoff.caston(k,width,[c1,c2,c3])

k.stitchNumber(4)
k.rollerAdvance(300)
k.speedNumber(400)

castonbindoff.interlock(k,width,4,c3,'l')

k.outgripper(c1)
k.outgripper(c2)



backstitch=8
frontstitch=4

k.stitchNumber(frontstitch)
k.rollerAdvance(300)
k.speedNumber(400)

for x in range(length):


    jersey.jerseyKnit(k,interlockStart,1,c3,'l')

    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')


    # missArray(k,misses,stitches,start,finish,length,c1,side='l',bed='f',offset=1,current=0):

    fairIsleStiffFxn.missArray(k, 3, 1, edgeProtect, interlockStart, 1, c3,'r','b',1,0)
    jersey.jerseyRange(k,0,edgeProtect,2,c3,'r','b')
    fairIsleStiffFxn.missArray(k, 3, 1, edgeProtect, interlockStart, 3, c3,'l','b',1,1)

    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')

    jersey.jerseyKnit(k,interlockStart,1,c3,'r')


castonbindoff.interlock(k,width,6,c3,'l')

castonbindoff.bindoff(k,0,width,c3,'l',1)


k.outgripper(c3)



k.write('missAngleActuatorNew.k')
