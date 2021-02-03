import numpy as np
''' ARRAY KEY
    0 : knit both beds
    1 : knit back bed only
    -1: knit front bed only '''

def pleats(k,refarray,length,c,side='l'):
    width = len(refarray)
    k.rack(0)
    k.rollerAdvance(300)
    if side == 'r':
        for s in range(width-1,-1,-1):
            if s%2 == 0:
                k.knit('-',('f',s),c)
            else:
                k.knit('-',('b',s),c)
        length = length-1

    for h in range(length):
        if h%2 ==1:
            for s in range(width-1,-1,-1):
                if (s%2 == 0) and refarray[s] !=1:
                    k.knit('-',('f',s),c)
                elif refarray[s] != -1 and s%2 ==1:
                    k.knit('-',('b',s),c)
        else:
            for s in range(width):
                if s%2 == 1 and refarray[s] !=1:
                    k.knit('+',('f',s),c)
                elif refarray[s] != -1 and s%2 == 0:
                    k.knit('+',('b',s),c)

def beginpleats(k,refarray):
    w = len(refarray)
    for s in range(w):
        if refarray[s] == 1:
            k.xfer(('f',s),('b',s))
        elif refarray[s] == -1:
            k.xfer(('b',s),('f',s))

def xferpleats(k,ref1,ref2):
    w = len(ref2)
    xferref = ref1-ref2
    for s in range(w):
        if ref2[s] !=0:
            if xferref[s] == -1 or xferref[s] == -2:
                k.xfer(('f',s),('b',s))
            elif xferref[s] == 1 or xferref[s] == 2:
                k.xfer(('b',s),('f',s))
