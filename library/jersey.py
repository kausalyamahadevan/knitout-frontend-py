#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout

def jerseyKnit(k,width,length,c,side):

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):

        if b%2==1:
            for w in range(0, width):
                k.knit('+',('f',w),c)
        else:
            for w in range(width-1,-1,-1):
                k.knit('-',('f',w),c)
