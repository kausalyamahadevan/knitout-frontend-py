#makes a two color fair isle to change knit stiffness
import math
import numpy as np

#has an edge protect built into the function
def stiffFairIsle(k,stitcharray,width,length,c1,c2,side,offset=1,edgeProtect=4):

    repeatSize = len(stitcharray)
    totalRepeatsHoriz=int(math.ceil(float(width)/repeatSize))

    ref = np.tile(stitcharray,totalRepeatsHoriz+1)


    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    #set counter to make offset
    counter=0
    for b in range(start, length+1):

        if b%2==1:

            #first handle first carrier
            for w in range(0,edgeProtect):
                if w%2==1:
                    k.knit('+',('f',w),c1)
                else:
                    k.miss('+',('f',w),c1)


            for w in range(edgeProtect,width-edgeProtect):
                if ref[w+counter]==1:
                    k.knit('+',('f',w),c1)
                else:
                    k.miss('+',('f',w),c1)


            for w in range(width-edgeProtect,width):
                if w%2==1:
                    k.knit('+',('f',w),c1)
                else:
                    k.miss('+',('f',w),c1)

            #next handle second carrier
            for w in range(0,edgeProtect):
                if w%2==1:
                    k.miss('+',('f',w),c2)
                else:
                    k.knit('+',('f',w),c2)

            for w in range(edgeProtect,width-edgeProtect):
                if ref[w+counter]==1:
                    k.miss('+',('f',w),c2)
                else:
                    k.knit('+',('f',w),c2)

            for w in range(width-edgeProtect,width):
                if w%2==1:
                    k.miss('+',('f',w),c2)
                else:
                    k.knit('+',('f',w),c2)

        else:
            #first handle first carrier
            for w in range(width-1,width-edgeProtect-1,-1):
                if w%2==1:
                    k.miss('-',('f',w),c1)
                else:
                    k.knit('-',('f',w),c1)

            for w in range(width-edgeProtect-1,edgeProtect-1,-1):
                if ref[w+counter]==1:
                    k.knit('-',('f',w),c1)
                else:
                    k.miss('-',('f',w),c1)

            for w in range(edgeProtect-1,-1,-1):
                if w%2==1:
                    k.miss('-',('f',w),c1)
                else:
                    k.knit('-',('f',w),c1)


            #next handle second carrier
            for w in range(width-1,width-edgeProtect-1,-1):
                if w%2==1:
                    k.knit('-',('f',w),c2)
                else:
                    k.miss('-',('f',w),c2)

            for w in range(width-edgeProtect-1,edgeProtect-1,-1):
                if ref[w+counter]==1:
                    k.miss('-',('f',w),c2)
                else:
                    k.knit('-',('f',w),c2)

            for w in range(edgeProtect-1,-1,-1):
                if w%2==1:
                    k.knit('-',('f',w),c2)
                else:
                    k.miss('-',('f',w),c2)

        counter=counter+offset
        if counter>=repeatSize:
            counter=0


def stiffFairIsleArray(k,stitcharray,start,finish,length,c1,c2,side='l',bed='f',offset=1,current=0):

    #tells how much the checkerboard fair isle
    #to protect edge should be

    repeatSize = len(stitcharray)
    totalRepeatsHoriz=int(math.ceil(float(finish-start)/repeatSize))

    ref = np.tile(stitcharray,totalRepeatsHoriz+2)


    #account for starting position and add first row of knitting
    if side == 'l':
        beg=1

    else:
        beg=2
        length=length+1

    #set counter to make offset
    current=current%repeatSize
    counter=offset+current-1

    for b in range(beg, length+1):
        if counter>=repeatSize:
            counter=0

        if b%2==1:

            for w in range(start,finish):

                if ref[w+counter]==1:
                    k.knit('+',(bed,w),c1)
                else:
                    k.miss('+',(bed,w),c1)

            #next handle second carrier
            for w in range(start,finish):
                if ref[w+counter]==1:
                    k.miss('+',(bed,w),c2)
                else:
                    k.knit('+',(bed,w),c2)


        else:
            #first handle first carrier

            for w in range(finish-1,start-1,-1):
                if ref[w+counter]==1:
                    k.knit('-',(bed,w),c1)
                else:
                    k.miss('-',(bed,w),c1)

            #handle second carrier
            for w in range(finish-1,start-1,-1):
                if ref[w+counter]==1:
                    k.miss('-',(bed,w),c2)
                else:
                    k.knit('-',(bed,w),c2)


        counter=counter+offset



def stiffFairIsleArraySided(k,stitcharray,start,finish,length,c1,c2,c1side='l',c2side='l',bed='f',offset=1):
    #allows the fair isle to be sided

    #tells how much the checkerboard fair isle
    #to protect edge should be

    repeatSize = len(stitcharray)
    totalRepeatsHoriz=int(math.ceil(float(finish-start)/repeatSize))

    ref = np.tile(stitcharray,totalRepeatsHoriz+2)


    #account for starting position and add first row of knitting
    if c1side == 'l':
        beg=1

    else:
        beg=2
        length=length+1

    #set counter to make offset
    counter=0
    for b in range(beg, length+1):

        if b%2==1:

            for w in range(start,finish):
                if ref[w+counter]==1:
                    k.knit('+',(bed,w),c1)
                else:
                    k.miss('+',(bed,w),c1)

            #next handle second carrier
            if c1side==c2side:
                for w in range(start,finish):
                    if ref[w+counter]==1:
                        k.miss('+',(bed,w),c2)
                    else:
                        k.knit('+',(bed,w),c2)
            else:
                for w in range(finish-1,start-1,-1):
                    if ref[w+counter]==1:
                        k.miss('-',(bed,w),c2)
                    else:
                        k.knit('-',(bed,w),c2)

        else:
            #first handle first carrier

            for w in range(finish-1,start-1,-1):
                if ref[w+counter]==1:
                    k.knit('-',(bed,w),c1)
                else:
                    k.miss('-',(bed,w),c1)

            #handle second carrier
            if c1side==c2side:
                for w in range(finish-1,start-1,-1):
                    if ref[w+counter]==1:
                        k.miss('-',(bed,w),c2)
                    else:
                        k.knit('-',(bed,w),c2)
            else:
                for w in range(start,finish):
                    if ref[w+counter]==1:
                        k.miss('+',(bed,w),c2)
                    else:
                        k.knit('+',(bed,w),c2)

        counter=counter+offset
        if counter>=repeatSize:
            counter=0


def missArray(k,misses,stitches,start,finish,length,c1,side='l',bed='f',offset=1,current=0):

    #make stitch array based on number of stitches and misses
    stitcharray=np.concatenate([np.ones(stitches,int),np.zeros(misses,int)])

    repeatSize = len(stitcharray)
    totalRepeatsHoriz=int(math.ceil(float(finish-start)/repeatSize))

    ref = np.tile(stitcharray,totalRepeatsHoriz+2)

    #account for starting position and add first row of knitting
    if side == 'l':
        beg=1

    else:
        beg=2
        length=length+1

    #set counter to make offset
    current=current%repeatSize
    counter=offset+current-1
    for b in range(beg, length+1):
        if counter>=repeatSize:
            counter=0

        if b%2==1:

            for w in range(start,finish):
                if w==start or w==finish-1:
                    k.knit('+',(bed,w),c1)

                elif ref[w+counter]==1:
                    k.knit('+',(bed,w),c1)
                else:
                    k.miss('+',(bed,w),c1)

        else:
            #first handle first carrier

            for w in range(finish-1,start-1,-1):
                if w==start or w==finish-1:
                    k.knit('-',(bed,w),c1)
                elif ref[w+counter]==1:
                    k.knit('-',(bed,w),c1)
                else:
                    k.miss('-',(bed,w),c1)


        counter=counter+offset


def ribKnitRange(k,ribarray,beg,fin,length,c,side='l',bed1='f',n0=0):

    if bed1=='f':
        bed0='b'
    else:
        bed0='f'


    repeatSize = len(ribarray)
    totalRepeatsHoriz=int(math.ceil(float(fin-beg)/repeatSize))

    ref = np.tile(ribarray,totalRepeatsHoriz+2)

    #account for starting position and add first row of knitting
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    for h in range(start,length):
        if h%2 ==0:
            for s in range(beg,fin):
                if ref[s] == 1:
                    k.knit('+',(bed1,s+n0),c)
                else:
                    k.knit('+',(bed0,s+n0),c)
        else:
            for s in range(fin-1,beg-1,-1):
                if ref[s] == 1:
                    k.knit('-',(bed1,s+n0),c)
                else:
                    k.knit('-',(bed0,s+n0),c)

def rib2ribXferRange(k,ribarray1,ribarray2,start,finish,repeats=1):
    ribsize = len(ribarray1)
    w  = ribsize*repeats
    ref1 = np.tile(ribarray1,repeats)
    ref2 = np.tile(ribarray2,repeats)
    xferref = ref1-ref2 # 0: do not transfer. 1: back to front -1: front to back
    for s in range(start,finish):
        if xferref[s] == 1:
            k.xfer(('b',s),('f',s))
        elif xferref[s] == -1:
            k.xfer(('f',s),('b',s))
