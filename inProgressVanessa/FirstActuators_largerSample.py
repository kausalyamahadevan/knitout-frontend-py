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


width=60; #horiz width
length=20; #vert length
numberMisses=1 #number misses between knits on back

#set what the left end right edges are
edgeProtect=4; #left edge
InterlockSegment=4; #right edge


#Create repeat array based on number missed stitches
repArray=np.zeros(numberMisses+1,int)
repArray[0]=1;

#create edge Array
edgeArray=np.ones(edgeProtect,int)

#interlock doesn't need array..
repeatSize = len(repArray)
totalRepeatsHoriz=int(math.ceil(float(width)/repeatSize))

ref = np.tile(repArray,totalRepeatsHoriz+1)

ref[0:edgeProtect]=edgeArray;


for x in range(length-1):

    jersey.jerseyknit(k,width,1,c3,'l')
