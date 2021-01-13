import knitout
import numpy as np
import math
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set carrier to one and bring in
carrier = '1'
k.ingripper('1')


#set sample size

width = 20
length= 10

#repeat informaiton
knits=3
misses=2
repeat=knits+misses

remainder=width%repeat #how many remaining stitches beyond unit cell

#setup the counter for negative passes
if remainder!=0:
    firstcounter=remainder
else:
    firstcounter=repeat


for h in range(1,length+1):

#if this is odd row go from right to left
    if h%2 == 1:
        counter=0
        for i in range(1,width+1):
            counter=counter+1
            if counter<=knits:
                k.knit('+',('f',i),carrier)
            else:
                k.miss('+',('f'i),carrier)

            if counter==repeat:
                counter=0

#if this is even row go from left to right
    else:
        counter=firstcounter

        for i in range(width,0,-1):
            if counter<=knits:
                k.knit('-',('f',i),carrier)
            else:
                k.miss('-',('f'i),carrier)

            counter=counter-1
            if counter==0:
                counter=repeat

k.outgripper(carrier)

for s in range(1,width+1):
    k.drop(('f',s))
    k.drop(('b',s))

k.write('misstrial.k')
