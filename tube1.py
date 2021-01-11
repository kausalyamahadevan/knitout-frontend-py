import knitout
import numpy as np
import math
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


#set carrier to one and bring in
wastecarrier = '1'
drawcarrier='2'
maincarrier='3'
k.ingripper(wastcarrier)
k.ingripper(drawcarrier)
k.ingripper(maincarrier)


#set sample size
waste = 50
width = 30
length = 15


#set miss repeat info
misses = 4
stiches = 1

repeat=misses+stitches
passes=repeat

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
for h in range(1,waste):
    if h%2 == 1:
        for s in range(width,0,-1):
            print('we neg', s)
            if s%2 == 0:
                k.knit('-',('f',s),wastecarrier)
            else:
                k.knit('-',('b',s),wastecarrier)
    else:
        for s in range(1,width+1):
            print('we pos', s)
            if s%2 == 1:
                k.knit('+',('f',s),wastecarrier)
            else:
                k.knit('+',('b',s),wastecarrier)

#add waste yarn




for b in range (1, passes+1):

#set the knit position for this row..
#accounts for the fact that sometimes more passes than total repeat
    knitPos=b%repeat
    if knitPos==0:
        knitPos=repeat

#create for positive direction
    if b%2==1:

        for z in range(1,numberRepeats+1):

            for m in range(1,repeat+1):
                if m!=knitPos:
                    k.miss('+',('f',(m*z)),maincarrier)
                else:
                    k.knit('+',('f',(m*z)),maincarrier)
#                k.miss(+,('f',m*z),maincarrier)
#
#            k.knit(+,('f',b*z),maincarrier)
#
#            for w in range(b+1,repeat+1):
#                k.miss(+,('f',w*z),maincarrier)

#create for negative direction
    else:
        for z in range(numberRepeats,0,-1):

            for m in range(repeat,0,-1):
                if m!=knitPos:
                    k.miss('-',('f',(m*z)),maincarrier)
                else:
                    k.knit('-',('f',(m*z)),maincarrier)


#            for w in range(repeat, b, -1):
#                k.miss(-,('f',w*z),maincarrier)
#
#            k.knit(-,('f'b*z),maincarrier)
#
#            for m in range(b-1,0,-1):
#                k.miss(-,('f',m*z),maincarrier)

for b in range (1,backpasses+1)
    if b%2==1:
        for z in range(width,0,-1):
            k.knit('-',('f',z),maincarrier)
    else:
        for z in range(1,width+1):
            k.knit('+',('f',z),maincarrier)





# Make the tube
#for i in range(1,length+1):
#    if i==1:
#        for k in range(1, passes+1):
#            if k%2==1:
#                for s in range(1,width+1):
#                    for z in range(1, numberRepeats+1):
#                        for w in range(1+z,)
#            else:
#                for s in range(width,0,-1):
