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
k.ingripper(c5)


width=100; #horiz width
length=20; #vert length

#set what the left end right edges are
edgeProtect=4; #left edge
InterlockSegment=4; #right edge

interlockStart=width-InterlockSegment;

repArray=[1,1,0,0]

#make final array to represent back sttich pattern where 1 is knit and 0 is miss
repeatSize = len(repArray)
totalRepeatsHoriz=int(math.ceil(float(width)/repeatSize))

ref = np.tile(repArray,totalRepeatsHoriz)


allback=np.ones(len(ref))

rib=c5;
shrink=c3;

k.stitchNumber(4)
castonbindoff.caston(k,width,[c1,c2,rib,shrink])

k.stitchNumber(4)
k.rollerAdvance(300)
k.speedNumber(400)

castonbindoff.interlock(k,width,4,rib,'l')
jersey.jerseyKnit(k,width,1,rib,'l','f')

k.outgripper(c1)
k.outgripper(c2)


k.stitchNumber(2)
k.rollerAdvance(0)
k.speedNumber(200)
jersey.jerseyArraySkipTransferRange(k,edgeProtect,interlockStart,rib,ref,'b')

k.stitchNumber(4)
k.rollerAdvance(300)
k.speedNumber(400)
for x in range(length):

    jersey.jerseyKnit(k,edgeProtect,1,shrink,'l')

    jersey.jerseyArraySkip(k,edgeProtect,interlockStart,1,shrink,ref)

    castonbindoff.interlockRangeHalved(k,interlockStart,width,1,shrink,'l')

    k.stitchNumber(2)
    k.rollerAdvance(0)
    k.speedNumber(150)

    fairIsleStiffFxn.rib2ribXferRange(k,allback,ref,edgeProtect,interlockStart)

    k.stitchNumber(4)
    k.rollerAdvance(300)
    k.speedNumber(400)

    castonbindoff.interlockRangeHalved(k,interlockStart,width,1,rib,'r')

    fairIsleStiffFxn.ribKnitRange(k,ref,edgeProtect,interlockStart,1,rib,'r','b')

    jersey.jerseyKnit(k,edgeProtect,2,rib,'r','b')

    fairIsleStiffFxn.ribKnitRange(k,ref,edgeProtect,interlockStart,1,rib,'l','b')

    castonbindoff.interlockRangeHalved(k,interlockStart,width,1,rib,'l')

    k.stitchNumber(2)
    k.rollerAdvance(0)
    k.speedNumber(150)

    fairIsleStiffFxn.rib2ribXferRange(k,ref,allback,edgeProtect,interlockStart)

    k.stitchNumber(4)
    k.rollerAdvance(5000)
    k.speedNumber(400)

    castonbindoff.interlockRangeHalved(k,interlockStart,width,1,shrink,'r')

    jersey.jerseyArraySkip(k,edgeProtect,interlockStart,1,shrink,ref,'r')

    jersey.jerseyKnit(k,edgeProtect,1,shrink,'r')


k.miss('+',('f',-10),shrink)

castonbindoff.interlock(k,width,6,rib,'r')



castonbindoff.bindoff(k,0,width,rib,'l',1)



k.outgripper(shrink)
k.outgripper(rib)



k.write('bendingRibShrink.k')
