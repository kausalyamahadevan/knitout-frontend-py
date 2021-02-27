import numpy as np
import math

def inlayKnit(k,beg,end,length,cRib,cInlay,side='l',bed1='f',roller=400,stitch=4,speed=400):
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


    tuckarray=np.zeros(end+1,int)
    tuckarray[beg]=1
    if (end-beg)%2==0:
        tuckarray[end-1]=-1
        print(tuckarray)
    else:
        tuckarray[end-1]=1

    print(tuckarray)

    #set starting side
    if side == 'l':
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
