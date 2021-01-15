import sys
sys.path.append('../knitout-frontend-py')
from library import knitout

import numpy as np
import math
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set carrier to one and bring in
carrier = '3'
castonCarrier=1
k.ingripper('3')
k.ingripper('1')


#set sample size

width = 20
length= 10

#repeat informaiton
knits=3
purls=4
repeat=knits+purls

#numRepeats=math.floor(width/repeat) #how many times we fully repeat

remainder=width%repeat #how many remaining stitches beyond unit cell

#setup the counter for negative passes
if remainder!=0:
    firstcounter=remainder
else:
    firstcounter=repeat

k.rack(.5)
k.speedNumber(100)
for z in range(1, length+1):
    # cast on every needle
    for s in range(1,width+1):
        k.tuck('+',('f',s),carrier)
        k.tuck('+',('b',s),carrier)

# interlock
k.rack(0)
k.speedNumber(300)
k.stitchNumber(5)
k.rollerAdvance(150)
for h in range(1,60):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),carrier)
            else:
                k.knit('-',('b',s),carrier)
    else:
        for s in range(1,width+1):

            if s%2 == 1:
                k.knit('+',('f',s),carrier)
            else:
                k.knit('+',('b',s),carrier)


counter=0
for i in range(1,width+1):
    counter=counter+1
    if counter<=knits:
        k.xfer(('b',h),('f',h))
    else:
        k.xfer(('f',h),('b',h))

    if counter==repeat:
        counter=0

for h in range(1,length+1):

#if this is odd row go from right to left
    if h%2 == 1:
        counter=0
        for i in range(1,width+1):
            counter=counter+1
            if counter<=knits:
                k.knit('+',('f',i),carrier)
            else:
                k.knit('+',('b',i),carrier)

            if counter==repeat:
                counter=0

#if this is even row go from left to right
    else:
        counter=firstcounter

        for i in range(width,0,-1):
            if counter<=knits:
                k.knit('-',('f',i),carrier)
            else:
                k.knit('-',('b',i),carrier)

            counter=counter-1
            if counter==0:
                counter=repeat

k.outgripper(carrier)

for s in range(1,width+1):
    k.drop(('f',s))
    k.drop(('b',s))

k.write('Aribtrial.k')
