import numpy as np
''' ARRAY KEY
    0 : knit both beds
    1 : knit back bed only
    -1: knit front bed only '''

def pleatsrib(k,refarray,repeats,length,c,side='l'):
    ref = np.tile(refarray,repeats)
    width = len(ref)
    k.rack(0.25)
    k.rollerAdvance(450)
    if side =='r':
        for s in range(width-1,-1,-1):
            if ref[s] !=-1:
                k.knit('-',('b',s),c)
            if ref[s] != 1:
                k.knit('-',('f',s),c)
        length = length-1
    for h in range(length):
        if h%2 ==0:
            for s in range(width):
                if ref[s] !=1:
                    k.knit('+',('f',s),c)
                if ref[s] !=-1:
                    k.knit('+',('b',s),c)
        else:
            for s in range(width-1,-1,-1):
                if ref[s] !=-1:
                    k.knit('-',('b',s),c)
                if ref[s] != 1:
                    k.knit('-',('f',s),c)

def pleats(k,refarray,repeats,length,c,side='l'):
    ref = np.tile(refarray,repeats)
    width = len(ref)
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
                if (s%2 == 0) and ref[s] !=1:
                    k.knit('-',('f',s),c)
                elif ref[s] != -1 and s%2 ==1:
                    k.knit('-',('b',s),c)
        else:
            for s in range(width):
                if s%2 == 1 and ref[s] !=1:
                    k.knit('+',('f',s),c)
                elif ref[s] != -1 and s%2 == 0:
                    k.knit('+',('b',s),c)

def beginpleats(k,refarray,repeats):
    ref = np.tile(refarray,repeats)
    w = len(ref)
    k.rack(0)
    k.stitchNumber(2)
    for s in range(w):
        if ref[s] == 1:
            k.xfer(('f',s),('b',s))
        elif ref[s] == -1:
            k.xfer(('b',s),('f',s))

def xferpleats(k,refarray1,refarray2,repeats):
    size = len(refarray1)
    w  = size*repeats
    ref1 = np.tile(refarray1,repeats)
    ref2 = np.tile(refarray2,repeats)
    k.rack(0)
    k.stitchNumber(2)
    w = len(ref2)
    xferref = ref1-ref2
    for s in range(w):
        if ref2[s] !=0:
            if xferref[s] == -1 or xferref[s] == -2:
                k.xfer(('f',s),('b',s))
            elif xferref[s] == 1 or xferref[s] == 2:
                k.xfer(('b',s),('f',s))

def pleatArray(k,array,xrepeats,yrepeats,c,side='l'):
    m, n = array.shape
    for i in range(yrepeats):
        for j in range(m):
            k.speedNumber(450)
            k.rollerAdvance(450)
            k.stitchNumber(2)
            pleatsrib(k,array[j],xrepeats,2,c,side)
            # if side == 'l':
            #     side = 'r'
            # else:
            #     side = 'l'
            k.speedNumber(100)
            k.addRollerAdvance(-200)
            k.rollerAdvance(0)
            k.stitchNumber(2)
            if j !=m-1:
                xferpleats(k,array[j],array[j+1],xrepeats)
            else:
                xferpleats(k,array[j],array[0],xrepeats)
