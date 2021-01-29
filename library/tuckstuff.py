import math
import numpy as np


def tuckSingleSide(k, width,length,firstarray,secondarray,c1,side='l'):

    # width=20
    # length=20
    # c1='1'
    # side='l'

    firstarray=[1,0,1,0]
    secondarray=[0,1,0,1]

    tucklength=3
    tuckoffset=2
    edgeProtect=4

    transferroller=150
    knitroller=50
    transferspeed=100
    knitspeed=300

    RepeatSize = len(firstarray)
    totalRepeatsHoriz=int(math.ceil(float(width)/RepeatSize))

    refFirst = np.tile(firstarray,totalRepeatsHoriz+1)
    refSecond= np.tile(secondarray,totalRepeatsHoriz+1)

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    counter=0
    setting=0
    for b in range(start,length+1):
        k.rollerAdvance(knitroller)
        k.speedNumber(knitspeed)
        if b%2==1:
            if setting==0:
                for w in range(width):
                    if refFirst[w]==1:
                        k.knit('+',('f',w),c1)
                    else:
                        k.tuck('+',('b',w),c1)

                k.speedNumber(transferspeed)
                k.rollerAdvance(transferroller)
                for w in range(width-1,-1,-1):
                    if refFirst[w]==0:
                        k.xfer(('b',w),('f',w))

            else:
                for w in range(width):
                    if refSecond[w]==1:
                        k.knit('+',('f',w),c1)
                    else:
                        k.tuck('+',('b',w),c1)

                k.speedNumber(transferspeed)
                k.rollerAdvance(transferroller)
                for w in range(width-1,-1,-1):
                    if refSecond[w]==0:
                        k.xfer(('b',w),('f',w))

            counter=counter+1

        else:
            if setting==0:

                for w in range(width-1,-1,-1):
                    if refFirst[w]==1:
                        k.knit('-',('f',w),c1)
                    else:
                        k.tuck('-',('b',w),c1)

                k.speedNumber(transferspeed)
                k.rollerAdvance(transferroller)
                for w in range(width):
                    if refFirst[w]==0:
                        k.xfer(('b',w),('f',w))

            else:

                for w in range(width-1,-1,-1):
                    if refSecond[w]==1:
                        k.knit('-',('f',w),c1)
                    else:
                        k.tuck('-',('b',w),c1)

                k.speedNumber(transferspeed)
                k.rollerAdvance(transferroller)
                for w in range(width):
                    if refSecond[w]==0:
                        k.xfer(('b',w),('f',w))

            counter=counter+1

        if counter==tucklength-1:
            if setting==0:
                setting=1
            else:
                setting=0

            counter=0
