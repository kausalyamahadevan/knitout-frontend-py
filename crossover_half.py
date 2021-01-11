
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

k.rack(0)


for z in range(1,5):

    if z%2==1:
        for w in range(1,width+1):
            k.knit('+',('f',w),maincarrier)

    else:
        for w in range(width,0,-1):
            k.knit('-',('f',w),maincarrier)


for z in range(1,length+1):

    if z%2==1:

        #knit all stitches
        for w in range(1,width+1):
            k.knit('+',('f',w),maincarrier)

        #transfer all stitches to back
        for w in range(1,width+1):
            k.xfer(('f',w),('b',w))

        #rack +1 and transfer every other stitch
        k.rack(1)
        for w in range(1,width+1):
            if w%2==1:
                k.xfer(('b',w),('f',w+1))

        #rack -1 and transfer
        k.rack(-1)
        for w in range(1,width+1):
            if w%2!=1:
                k.xfer(('b',w),('f',w-1))


    else:
        for w in range(width,0,-1):
            k.knit('-',('f',w),maincarrier)


k.write('across.k')
