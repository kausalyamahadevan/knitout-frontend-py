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


width=60; #horiz width
length=20; #vert length
numberMisses=1 #number misses between knits on back

#set what the left end right edges are
edgeProtect=4; #left edge
InterlockSegment=4; #right edge

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

for x in range(length):

    jersey.jerseyKnit(k,interlockStart,1,c3,'l')
    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')

    jersey.jerseyArraySkip(k,interlockStart,2,c3,ref,'r','b')

    castonbindoff.interlockRange(k,interlockStart,width,1,c3,'l')

    jersey.jerseyKnit(k,interlockStart,1,c3,'r')


castonbindoff.interlock(k,width,7,c3,'l')
castonbindoff.bindoff(k,0,width,c3,'r',1)

# for s in range(width):
#     k.drop(('f',s))
#     k.drop('b',s)

k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)


k.write('bigBend.k')
