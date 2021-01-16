#makes a two color fair isle to change knit stiffness
import math
import numpy as np

def stiffFairIsle(k,stitcharray,width,length,c1,c2,side):

    #offset the length
    offset=1

    #tells how much the checkerboard fair isle
    #to protect edge should be
    edgeProtect=4


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
