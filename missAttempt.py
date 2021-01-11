#creates just a miss section of knit (no tube)
import knitout
from castonbindoff import *
import numpy as np
import math

#make knitout object
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set cariers
draw = '1'
waste = '2'
main = '3'
k.ingripper(waste)
k.ingripper(draw)
k.ingripper(main)


#set sample size
width = 50
passes = 30


#set miss repeat info
misses = 4
stitches = 1


repeat=misses+stitches

#make width so that it is a multiple of repeat size
if (width%repeat)!=0:
    width=width-(width%repeat)+repeat

numberRepeats=width/repeat

xsize=width
# cast on every needle
catchyarns(xsize,[draw,waste,main])
#Move draw thread to the right side.
for s in range(1,xsize+1):
    k.knit('+',('f',s),draw)

k.rack(0.5)
for s in range(1,xsize+1):
    k.knit('+',('f',s),waste)
    k.knit('+',('b',s),waste)


#interlock / waste yarn
interlock(xsize,16,waste,'r')
#circular / waste Yarn
circular(xsize,4,waste,'r')

for s in range(1,xsize+1):
    k.drop(('b',s))

for s in range(xsize,0,-1):
    k.knit('-',('f',s),draw)

#Case on main yarn!
k.rack(0.5)
for s in range(1,xsize+1):
    k.knit('+',('f',s),main)
    k.knit('+',('b',s),main)


''' making'''




# add edge interlock
k.rack(0)
k.rollerAdvance(150)
for h in range(1,6):
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

for q in range(1, width+1):
    k.xfer(('b',q),('f',q))

for h in range(2,12):
    if h%2 == 1:
        for s in range(width,0,-1):
            k.knit('-',('f',s),main)
    else:
        for s in range(1,width+1):
            k.knit('+',('f',s),main)

#begin knitting miss section
k.stitchNumber(4)
k.rollerAdvance(75)
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
                if (m==1 and z==1) or (z==numberRepeats and m==repeat) or m==knitPos:
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
k.rollerAdvance(150)
for h in range(2,12):
    if h%2 == 1:
        for s in range(width,0,-1):
            k.knit('-',('f',s),main)
    else:
        for s in range(1,width+1):
            k.knit('+',('f',s),main)

k.outgripper(waste)
k.outgripper(draw)
k.outgripper(main)

# for s in range(1,width+1):
#     k.drop(('f',s))
#     k.drop(('b',s))

k.write('newmissOnly.k')
