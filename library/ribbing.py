import numpy as np

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
