import numpy as np
'''
FOR ALL ARRAYS: 1 : knit on BACK bed
                0 : knit on FRONT bed
'''
'''
Transfers stitches from cast on configuration (on all needles f and b) to ribbing
'''
def xfertorib(k,ribarray,repeats):
    ribsize = len(ribarray)
    w  = ribsize*repeats
    ref = np.tile(ribarray,repeats)
    for s in range(w):
        if ref[s] == 1:
            k.xfer(('f',s),('b',s))
        else:
            k.xfer(('b',s),('f',s))

'''
knits as many rows as you like of a given rib knit pattern.
Stitches must already be configured on the correct needles
'''
def ribKnit(k,ribarray,repeats,length,c,side='l',n0=0):
    ribsize = len(ribarray)
    w  = ribsize*repeats
    ref = np.tile(ribarray,repeats)
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0
    for h in range(start,length):
        if h%2 ==0:
            for s in range(w):
                if ref[s] == 1:
                    k.knit('+',('b',s+n0),c)
                else:
                    k.knit('+',('f',s+n0),c)
        else:
            for s in range(w-1,-1,-1):
                if ref[s] == 1:
                    k.knit('-',('b',s+n0),c)
                else:
                    k.knit('-',('f',s+n0),c)


def ribKnitRange(k,ribarray,start,finish,length,c,side='l',n0=0):
    ribsize = len(ribarray)
    w  = ribsize*repeats
    ref = np.tile(ribarray,repeats)
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0
    for h in range(start,length):
        if h%2 ==0:
            for s in range(w):
                if ref[s] == 1:
                    k.knit('+',('b',s+n0),c)
                else:
                    k.knit('+',('f',s+n0),c)
        else:
            for s in range(w-1,-1,-1):
                if ref[s] == 1:
                    k.knit('-',('b',s+n0),c)
                else:
                    k.knit('-',('f',s+n0),c)

def fishermansrib(k,width,length,c,side='l',n0=0):
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0
    for h in range(start,length):
        if h%2 ==0:
            for s in range(w):
                if ref[s] == 1:
                    k.knit('+',('b',s+n0),c)
                else:
                    k.tuck('+',('f',s+n0),c)
        else:
            for s in range(w-1,-1,-1):
                if ref[s] == 1:
                    k.tuck('-',('b',s+n0),c)
                else:
                    k.knit('-',('f',s+n0),c)
'''
Given two arrays of the same size, sets up for the
rib pattern given in ribarray2
'''

def rib2ribXfer(k,ribarray1,ribarray2,repeats):
    ribsize = len(ribarray1)
    w  = ribsize*repeats
    ref1 = np.tile(ribarray1,repeats)
    ref2 = np.tile(ribarray2,repeats)
    xferref = ref1-ref2 # 0: do not transfer. 1: back to front -1: front to back
    k.rollerAdvance(0)
    k.addRollerAdvance(-300)
    for s in range(w):
        if xferref[s] == 1:
            k.xfer(('b',s),('f',s))
        elif xferref[s] == -1:
            k.xfer(('f',s),('b',s))
    k.addRollerAdvance(300)
    k.rollerAdvance(400)

''' Given an array and repeats, knits and purls'''

def knitArray(k,array,xrepeats,yrepeats,c,side='l'):
    m, n = array.shape
    for i in range(yrepeats):
        for j in range(m):
            k.speedNumber(400)
            k.rollerAdvance(400)
            ribKnit(k,array[j],xrepeats,1,c,side)
            if side == 'l':
                side = 'r'
            else:
                side = 'l'
            k.speedNumber(100)
            k.rollerAdvance(100)
            if j !=m-1:
                rib2ribXfer(k,array[j],array[j+1],xrepeats)
            else:
                rib2ribXfer(k,array[j],array[0],xrepeats)
