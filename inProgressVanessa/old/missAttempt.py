#creates just a miss section of knit (no tube)
import knitout
from castonbindoff import *
import numpy as np
import math

#make knitout object
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set cariers
# draw = '1'
# waste = '2'
main = '3'
# k.ingripper(waste)
# k.ingripper(draw)
k.ingripper(main)


#set sample size
width = 30
passes = 30


#set miss repeat info
misses = 4
stitches = 1


repeat=misses+stitches

#make width so that it is a multiple of repeat size
if (width%repeat)!=0:
    width=width-(width%repeat)+repeat

numberRepeats=width/repeat



k.speedNumber(100)
k.stitchNumber(5)

#cast on every needle
k.rack(.5)
for s in range(1,width+1):
    k.tuck('+',('f',s),main)
    k.tuck('+',('b',s),main)

# add edge interlock
k.rack(0)
k.stitchNumber(5)
k.rollerAdvance(175)
k.speedNumber(300)
for h in range(1,80):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),main)
            else:
                k.knit('-',('b',s),main)
    else:
        for s in range(1,width+1):
            if s%2 == 1:
                k.knit('+',('f',s),main)
            else:
                k.knit('+',('b',s),main)

#transfer from back to front for all stitches
k.rollerAdvance(50)
k.stitchNumber(4)
k.speedNumber(150)
for q in range(1, width+1):
    k.xfer(('b',q),('f',q))

#add jersey
k.stitchNumber(5)
k.rollerAdvance(400)
k.speedNumber(300)
for h in range(2,6):
    if h%2 == 1:
        for s in range(width,0,-1):
            k.knit('-',('f',s),main)
    else:
        for s in range(1,width+1):
            k.knit('+',('f',s),main)

#begin knitting miss section
k.stitchNumber(4)
k.rollerAdvance(100)
k.speedNumber(300)
for b in range (1, passes+1):
#set the knit position for this row..
#accounts for the fact that sometimes more passes than total repeat
    knitPos=b%repeat
    if knitPos==0:
        knitPos=repeat

    # print('were in pass: '+ str(b))

#create for positive direction
    if b%2==1:

        for z in range(1,numberRepeats+1):

            for m in range(1,repeat+1):
                if (m==1 and z==1) or (z==numberRepeats and m==repeat) or (m==knitPos):
                    #print('knit:' + str((z*repeat)+m-repeat))
                    k.knit('+',('f',((z*repeat)+m-repeat)),main)

                else:
                    #print('miss:' + str((z*repeat)+m-repeat))
                    k.miss('+',('f',((z*repeat)+m-repeat)),main)


    else:
        for z in range(numberRepeats,0,-1):

            for m in range(repeat,0,-1):
                if (m==1 and z==1) or (z==numberRepeats and m==repeat) or m==knitPos:
                    #print('knit:' + str((z*repeat)+m-repeat))
                    k.knit('-',('f',((z*repeat)+m-repeat)),main)

                else:
                    #print('miss:' + str((z*repeat)+m-repeat))
                    k.miss('-',('f',((z*repeat)+m-repeat)),main)


#add edge jersey
k.stitchNumber(5)
k.rollerAdvance(400)
k.speedNumber(300)
for h in range(2,12):
    if h%2 == 1:
        for s in range(width,0,-1):
            k.knit('-',('f',s),main)
    else:
        for s in range(1,width+1):
            k.knit('+',('f',s),main)

k.speedNumber(100)
for s in range(1,width+1):
    k.drop(('f',s))
    k.drop(('b',s))

# k.outgripper(waste)
# k.outgripper(draw)
k.outgripper(main)



k.write('anewmissOnly.k')
