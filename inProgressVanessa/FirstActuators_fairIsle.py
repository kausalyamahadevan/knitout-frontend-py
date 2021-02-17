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


width=100; #horiz width
length=20; #vert length
numberMisses=2 #number misses between knits on back

#set what the left end right edges are
edgeProtect=4; #left edge
InterlockSegment=4; #right edge
stitcharray=[1,1,1,1,0,0,0,0]

interlockStart=width-InterlockSegment;

#Create repeat array based on number missed stitches
repArray=np.zeros(numberMisses+1,int)
repArray[0]=1;

#create edge Array
edgeArray=np.ones(edgeProtect,int)

#interlock doesn't need array..

#make final array to represent back sttich pattern where 1 is knit and 0 is miss
repeatSize = len(repArray)
totalRepeatsHoriz=int(math.ceil(float(width)/repeatSize))

ref = np.tile(repArray,totalRepeatsHoriz)

ref[0:edgeProtect]=edgeArray;


k.stitchNumber(4)
castonbindoff.caston(k,width,[c1,c2,c3])

k.stitchNumber(4)
k.rollerAdvance(300)
k.speedNumber(400)

castonbindoff.interlock(k,width,4,c3,'l')


# k.stitchNumber(2)
# k.rollerAdvance(0)
# k.speedNumber(200)
# jersey.jerseyArraySkipTransfer(k,width,c3,ref,'b')

k.stitchNumber(4)
k.rollerAdvance(300)
k.speedNumber(400)
print(edgeProtect)
for x in range(length):

    jersey.jerseyKnit(k,interlockStart,1,c3,'l')

    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')

    fairIsleStiffFxn.stiffFairIsleArray(k,stitcharray,edgeProtect,interlockStart,1,c3,c5,'r','b')

    jersey.jerseyRange(k,0,edgeProtect,2,c3,'r','b')

    fairIsleStiffFxn.stiffFairIsleArray(k,stitcharray,edgeProtect,interlockStart,1,c3,c5,'l','b')

    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')

    jersey.jerseyKnit(k,interlockStart,1,c3,'r')


castonbindoff.interlock(k,width,6,c3,'l')

k.outgripper(c1)
k.outgripper(c2)

castonbindoff.bindoff(k,0,width,c3,'l',1)



k.outgripper(c3)



k.write('fairIsleBend.k')
