import math
import numpy as np

def jerseyStitches(k,stitcharray,width,length,c,side):

    repeatSize = len(stitcharray)
    totalRepeats=int(math.ceil(float(width)/repeatSize))

    ref = np.tile(stitcharray,totalRepeats)

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(width):
                k.stitchNumber(ref[w])
                k.knit('+',('f',w),c)
        else:
            for w in range(width-1,-1,-1):
                k.stitchNumber(ref[w])
                k.knit('-',('f',w),c)

# def ribKnit(k,ribarray,repeats,length,c):
#     ribsize = len(ribarray)
#     w  = ribsize*repeats
#     ref = np.tile(ribarray,repeats)
#     for h in range(length):
#         if h%2 ==0:
#             for s in range(w):
#                 if ref[s] == 1:
#                     k.knit('+',('b',s),c)
#                 else:
#                     k.knit('+',('f',s),c)
#         else:
#             for s in range(w-1,-1,-1):
#                 if ref[s] == 1:
#                     k.knit('-',('b',s),c)
#                 else:
#                     k.knit('-',('f',s),c)
