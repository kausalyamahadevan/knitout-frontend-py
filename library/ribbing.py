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
def ribKnit(k,ribarray,repeats,length,c):
    ribsize = len(ribarray)
    w  = ribsize*repeats
    ref = np.tile(ribarray,repeats)
    for h in range(length):
        if h%2 ==0:
            for s in range(w):
                if ref[s] == 1:
                    k.knit('+',('b',s),c)
                else:
                    k.knit('+',('f',s),c)
        else:
            for s in range(w-1,-1,-1):
                if ref[s] == 1:
                    k.knit('-',('b',s),c)
                else:
                    k.knit('-',('f',s),c)

def rib2ribXfer(k,ribarray1,ribarray2,repeats):
    ribsize = len(ribarray1)
    w  = ribsize*repeats
    ref1 = np.tile(ribarray1,repeats)
    ref2 = np.tile(ribarray2,repeats)
    xferref = ref1-ref2 # 0: do not transfer. 1: back to front -1: front to back
    for s in range(w):
        if xferref[s] == 1:
            k.xfer(('b',s),('f',s))
        elif xferref[s] == -1:
            k.xfer(('f',s),('b',s))
