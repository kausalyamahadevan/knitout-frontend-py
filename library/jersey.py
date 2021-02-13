#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout

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


def jerseyArraySkip(k,width,length,c,array,side='l',bed='f'):
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
                    k.miss('+',(bed,w),c)

        else:
            for w in range(width-1,-1,-1):
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
