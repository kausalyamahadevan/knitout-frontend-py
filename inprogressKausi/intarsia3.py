import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
from library.jersey import *
import numpy as np
start = 0
length = 50
refarray = np.hstack((np.zeros((30,)),np.ones((30,))))
# refarray = np.array([[0,1,0,0,-1,0],[0,-1,0,0,1,0]])
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')
draw = '1'
waste = '2'
c1 = '3'
c2 = '5'
xrep = 4
yrep = 2
width = len(refarray)
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(c1)
kwriter.ingripper(c2)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,c1,c2])
xfertorib(kwriter,[0],width)
jerseyKnit(kwriter,width, 4, c1)

for h in range(start,length):
    if h%2 ==0:
        for s in range(width):
            if refarray[s]==0:
                kwriter.knit('+',('f',s),c1)
            elif refarray[s-1]==0:
                kwriter.tuck('+',('b',s),c1)
            # else:
            #     kwriter.miss('+',('f',s),c1)
        for s in range(width):
            # if refarray[s]==0:
            #     kwriter.miss('+',('f',s),c2)
            if refarray[s]==1:
                kwriter.knit('+',('f',s),c2)
    else:
        for s in range(width-1,-1,-1):
            # if refarray[s]==0:
            #     kwriter.miss('-',('f',s),c2)
            if refarray[s]==1:
                kwriter.knit('-',('f',s),c2)
        for s in range(width-1,-1,-1):
            # if refarray[s]==1:
            #     kwriter.miss('-',('f',s),c1)


            if refarray[s]==0:
                kwriter.knit('-',('f',s),c1)
                if refarray[s+1]==1:
                    kwriter.drop(('b',s+1))
jerseyKnit(kwriter,width, 10, c2)
for s in range(width):
    kwriter.drop(('f',s))
for s in range(width-1,-1,-1):
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(waste)
kwriter.outgripper(c1)
kwriter.outgripper(c2)
kwriter.write('knitting-files/intarsia3.k')
