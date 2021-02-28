import numpy as np
import math

def inlayKnit(k,beg,end,length,cRib,cInlay,siderib='l',bed1='f',roller=400,stitch=4,speed=400):
    '''can take in tuck array where 1s represent tucks and 0s represent misses
    or puts tucks only at edges'''

    #set beds
    if bed1=='f':
        bed2='b'
    else:
        bed2='f'

    # #make tuck array
    # if len(tuckarray)!=0:
    #     repeatSize = len(stitcharray)
    #     totalRepeatsHoriz=int(math.ceil(float(end-beg)/repeatSize))
    #     array = np.tile(stitcharray,totalRepeatsHoriz+2)


    tuckarray=np.zeros(end,int)

    for i in range(beg,end,4):
        tuckarray[i]=1

    if (end-beg)%2==0:
        tuckarray[end-1]=-1

    else:
        tuckarray[end-1]=1



    #set starting side
    if siderib == 'l':
        start=1

    else:
        start=2
        length=length+1


    for b in range(start,length+1):

        if b%2==1:
            k.rollerAdvance(roller)
            k.stitchNumber(stitch)
            k.speedNumber(speed)
            for w in range(beg,end):
                if w%2==0: #knits odds on front
                    k.knit('+',(bed1,w),cRib)
                else:
                    k.knit('+',(bed2,w),cRib)

            k.rollerAdvance(0)
            k.stitchNumber(2)
            k.speedNumber(speed)
            for w in range(beg,end):
                if tuckarray[w]==1:
                    k.drop((bed2,w))
                elif tuckarray[w]==-1:
                    k.drop((bed1,w))

            for w in range(beg,end):
                if tuckarray[w]==1:
                    k.tuck('+',(bed2,w),cInlay)
                elif tuckarray[w]==-1:
                    k.tuck('+',(bed1,w),cInlay)
                else:
                    k.miss('+',(bed2,w),cInlay)

        else:
            k.rollerAdvance(roller)
            k.stitchNumber(stitch)
            k.speedNumber(speed)
            for w in range(end-1,beg-1,-1):
                if w%2==0: #knits odds on front
                    k.knit('-',(bed1,w),cRib)
                else:
                    k.knit('-',(bed2,w),cRib)

            k.rollerAdvance(0)
            k.stitchNumber(stitch)
            k.speedNumber(speed)
            for w in range(end-1,beg-1,-1):
                if tuckarray[w]==1:
                    k.drop((bed2,w))
                elif tuckarray[w]==-1:
                    k.drop((bed1,w))

            for w in range(end-1,beg-1,-1):
                if tuckarray[w]==1:
                    k.tuck('-',(bed2,w),cInlay)
                elif tuckarray[w]==-1:
                    k.tuck('-',(bed1,w),cInlay)
                else:
                    k.miss('-',(bed2,w),cInlay)


def inlaySeed(k,beg,end,length,cRib,cInlay,inlayside='l',ribside='l',bed1='f',roller=400,stitch=4,speed=400):
    '''can take in tuck array where 1s represent tucks and 0s represent misses
    or puts tucks only at edges'''

    #set beds
    if bed1=='f':
        bed2='b'
    else:
        bed2='f'

    #set starting side
    if ribside == 'l':
        start=1

    else:
        start=2
        length=length+1


    for b in range(start,length+1):

        if b%2==1:
            k.rollerAdvance(roller)
            k.stitchNumber(stitch)
            k.speedNumber(speed)
            for w in range(beg,end):
                if w%2==0: #knits odds on front
                    k.knit('+',(bed1,w),cRib)
                else:
                    k.knit('+',(bed2,w),cRib)

            k.rollerAdvance(0)
            k.stitchNumber(stitch)
            k.speedNumber(speed)

            k.drop((bed2,end))
            k.drop((bed2,beg-1))


            if b!=length:
                if inlayside=='l':
                    k.tuck('+',(bed2,beg-1),cInlay)
                    k.tuck('+',(bed2,end),cInlay)
                else:
                    k.tuck('-',(bed2,end),cInlay)
                    k.tuck('-',(bed2,beg-1),cInlay)


                k.rollerAdvance(0)
                k.stitchNumber(2)
                k.speedNumber(100)
                for w in range(beg,end):
                    if w%2==0: #knits odds on front
                        k.xfer((bed1,w),(bed2,w))
                    else:
                        k.xfer((bed2,w),(bed1,w))



        else:
            k.rollerAdvance(roller)
            k.stitchNumber(stitch)
            k.speedNumber(speed)
            for w in range(end-1,beg-1,-1):
                if w%2==0: #knits odds on front
                    k.knit('-',(bed2,w),cRib)
                else:
                    k.knit('-',(bed1,w),cRib)

            k.rollerAdvance(0)
            k.stitchNumber(stitch)
            k.speedNumber(speed)

            k.drop((bed2,beg-1))
            k.drop((bed2,end))

            if b!=length:
                if inlayside=='l':
                    k.tuck('-',(bed2,end),cInlay)
                    k.tuck('-',(bed2,beg-1),cInlay)
                else:
                    k.tuck('+',(bed2,beg-1),cInlay)
                    k.tuck('+',(bed2,end),cInlay)


                k.rollerAdvance(0)
                k.stitchNumber(2)
                k.speedNumber(100)
                for w in range(beg,end):
                    if w%2==0: #knits odds on front
                        k.xfer((bed2,w),(bed1,w))
                    else:
                        k.xfer((bed1,w),(bed2,w))
