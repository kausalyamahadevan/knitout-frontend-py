#creates just a miss section of knit (no tube)

import knitout
import numpy as np
import math
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set carrier to one and bring in
wastecarrier = '1'
drawcarrier='2'
maincarrier='3'
k.ingripper(wastecarrier)
k.ingripper(drawcarrier)
k.ingripper(maincarrier)


#set sample size
waste = 50
width = 30
length = 15
widthamt= 10


#set miss repeat info
misses = 4
stitches = 1

passes=30

repeat=misses+stitches


backpasses=2

if (width%repeat)!=0:
    width=width-(width%repeat)+repeat

numberRepeats=width/repeat

# cast on every needle
k.rack(0.5)
for s in range(1,width+1):
    k.tuck('+',('f',s),wastecarrier)
    k.tuck('+',('b',s),wastecarrier)

# interlock
k.rack(0)
k.speedNumber(300)
k.rollerAdvance(150)
k.stitchNumber(5)
for h in range(1,waste):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),wastecarrier)
            else:
                k.knit('-',('b',s),wastecarrier)
    else:
        for s in range(1,width+1):
            if s%2 == 1:
                k.knit('+',('f',s),wastecarrier)
            else:
                k.knit('+',('b',s),wastecarrier)

#add tube
for h in range(1,3):
    if h%2 == 1:
        k.knit('-',('f',s),wastecarrier)
    else:
        k.knit('+',('b',s),wastecarrier)


# drop back



#add draw thread

for s in range(1,width+1):
    k.knit('+',('f',s),drawcarrier)
    k.knit('+',('b',s),drawcarrier)

for s in range(1,width+1):
    k.tuck('+',('f',s),maincarrier)
    k.tuck('+',('b',s),maincarrier)



# add edge interlock
k.rack(0)
k.rollerAdvance(150)
for h in range(1,6):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),maincarrier)
            else:
                k.knit('-',('b',s),maincarrier)
    else:
        for s in range(1,width+1):
            if s%2 == 1:
                k.knit('+',('f',s),maincarrier)
            else:
                k.knit('+',('b',s),maincarrier)

#begin knitting miss section
k.stitchNumber(4)
k.rollerAdvance(75)
for b in range (1, passes+1):
#set the knit position for this row..
#accounts for the fact that sometimes more passes than total repeat
    knitPos=b%repeat
    if knitPos==0:
        knitPos=repeat

    print('were in pass: '+ str(b))

#create for positive direction
    if b%2==1:

        for z in range(1,numberRepeats+1):

            for m in range(1,repeat+1):
                if (m==1 and z==1) or (z==numberRepeats and m==repeat) or m==knitPos:
                    #print('knit:' + str((z*repeat)+m-repeat))
                    k.knit('+',('f',((z*repeat)+m-repeat)),maincarrier)

                else:
                    #print('miss:' + str((z*repeat)+m-repeat))
                    k.miss('+',('f',((z*repeat)+m-repeat)),maincarrier)


    else:
        for z in range(numberRepeats,0,-1):

            for m in range(repeat,0,-1):
                if (m==1 and z==1) or (z==numberRepeats and m==repeat) or m==knitPos:
                    #print('knit:' + str((z*repeat)+m-repeat))
                    k.knit('-',('f',((z*repeat)+m-repeat)),maincarrier)

                else:
                    #print('miss:' + str((z*repeat)+m-repeat))
                    k.miss('-',('f',((z*repeat)+m-repeat)),maincarrier)


#add edge interlock
k.stitchNumber(5)
k.rollerAdvance(150)
for h in range(2,8):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),maincarrier)
            else:
                k.knit('-',('b',s),maincarrier)
    else:
        for s in range(1,width+1):
            if s%2 == 1:
                k.knit('+',('f',s),maincarrier)
            else:
                k.knit('+',('b',s),maincarrier)

k.outgripper(wastecarrier)
k.outgripper(drawcarrier)
k.outgripper(maincarrier)

# for s in range(1,width+1):
#     k.drop(('f',s))
#     k.drop(('b',s))

k.write('missOnly.k')
