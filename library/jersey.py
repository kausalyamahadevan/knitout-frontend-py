
import math
import numpy as np

def jerseyKnit(k,width,length,c,side='l',bed='f'):

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(0, width):
                k.knit('+',(bed,w),c)
        else:
            for w in range(width-1,-1,-1):
                k.knit('-',(bed,w),c)

def jerseyRange(k,beg,end,length,c,side='l',bed='f'):

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(beg, end):
                k.knit('+',(bed,w),c)
        else:
            for w in range(end-1,beg-1,-1):
                k.knit('-',(bed,w),c)



def jerseySkip(k,width,length,c,skip=2,side='l',bed='f'):


    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(0, width,(skip)):
                k.knit('+',(bed,w),c)
        else:
            for w in range(width-1,-1,(-1*skip)):
                k.knit('-',(bed,w),c)


def jerseyArraySkipTransfer(k,width,c,array,bed='f'):

    #transfer stitches we kip to opposite bed
    for m in range(width):
        if array[m]==0:
            if bed=='f':
                k.xfer(('f',m),('b',m))
            else:
                k.xfer(('b',m),('f',m))

def jerseyArraySkipTransferRange(k,start,fin,c,array,bed='f'):

    #transfer stitches we kip to opposite bed
    for m in range(start,fin):
        if array[m]==0:
            if bed=='f':
                k.xfer(('f',m),('b',m))
            else:
                k.xfer(('b',m),('f',m))



def jerseyArraySkip(k,beg,end,length,c,stitcharray,side='l',bed='f'):
    '''makes knitout code where you miss rows of needles based upon a given array.
    In the array 1 means knit and 0 means miss. Arrays will be tiled based on width of sample.'''
    k.rack(0)
    repeatSize = len(stitcharray)
    totalRepeatsHoriz=int(math.ceil(float(beg-end)/repeatSize))
    array = np.tile(stitcharray,totalRepeatsHoriz+1)


    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(beg,end):
                if array[w]==1:
                    k.knit('+',(bed,w),c)
                else:
                    k.miss('+',(bed,w),c)

        else:
            for w in range(end-1,beg-1,-1):
                if array[w]==1:
                    k.knit('-',(bed,w),c)
                else:
                    k.miss('-',(bed,w),c)


def jerseyArrayTuck(k,width,length,c,array,side='l',bed='f'):
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(width):
                if array[w]==1:
                    k.knit('+',(bed,w),c)
                else:
                    k.tuck('+',(bed,w),c)

        else:
            for w in range(width-1,-1,-1):
                if array[w]==1:
                    k.knit('-',(bed,w),c)
                else:
                    k.tuck('-',(bed,w),c)
