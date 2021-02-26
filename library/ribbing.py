import numpy as np
'''
FOR ALL ARRAYS: 1 : knit on BACK bed
                0 : knit on FRONT bed
'''

'''
Transfers stitches from cast on configuration (on all needles f and b) to ribbing
k: knitout writer object
ribarray: numpy array/list of 0s and 1s to define rib pattern
repeats: integer, defines width of sample as a multiple of the ribarray length
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
k: knitout writer object
ribarray: numpy array/list of 0s and 1s to define rib pattern
repeats: integer, defines width of sample as a multiple of the ribarray length
length: number of rows knit
c: string defining yarn carrier
side: string defining which side the carrier starts on
n0: integer defining '0' needle. Defaults to 0
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


''' This function ribknitrange is likely a duplicate of the above
    for new scripts, use ribKnit.
    Leaving this uncommented for now, will eventually be "depreciated" (HEHE)'''
#
# def ribKnitRange(k,ribarray,start,finish,length,c,side='l',n0=0):
#     ribsize = len(ribarray)
#     w  = ribsize*repeats
#     ref = np.tile(ribarray,repeats)
#     if side == 'r':
#         start = 1
#         length = length+1
#     else:
#         start = 0
#     for h in range(start,length):
#         if h%2 ==0:
#             for s in range(w):
#                 if ref[s] == 1:
#                     k.knit('+',('b',s+n0),c)
#                 else:
#                     k.knit('+',('f',s+n0),c)
#         else:
#             for s in range(w-1,-1,-1):
#                 if ref[s] == 1:
#                     k.knit('-',('b',s+n0),c)
#                 else:
#                     k.knit('-',('f',s+n0),c)

''' must start in 1 x 1 configuration
k: knitout writer object
width: integer, sample width
length: number of rows knit
c: string defining yarn carrier
side: string defining which side the carrier starts on
n0: integer defining '0' needle. Defaults to 0
'''
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
ribarray: numpy array/list of 0s and 1s to define current needle configuration
ribarray: numpy array/list of 0s and 1s to define future needle configuration
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

''' Given an array and repeats, knits and purls
k: knitout writer object
array: numpy array of 0s and 1s to define rib pattern
xrepeats: integer, defines width of sample as a multiple of the ribarray dimension
xrepeats: integer, defines height of sample as a multiple of the ribarray dimension
c: string defining yarn carrier
side: string defining which side the carrier starts on'''

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


def seed(k,beg,end,length,c,side='l'):

    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start, length+1):

        if b%2==1:

            #make sure all stitches on correct needles
            for w in range(beg,end):
                if w%2==1:
                    k.xfer(('b',w),('f',w))
                else:
                    k.xfer(('f',w),('b',w))

            #knit all stitches
            for w in range(beg,end):
                if w%2==1:
                    k.knit('+',('f',w),c)
                else:
                    k.knit('+',('b',w),c)

        else:
            #make sure all stitches on correct needles
            for w in range(end-1,beg-1,-1):
                if w%2==1:
                    k.xfer(('f',w),('b',w))
                else:
                    k.xfer(('b',w),('f',w))

            #knit all stitches
            for w in range(end-1,beg-1,-1):
                if w%2==1:
                    k.knit('-',('b',w),c)
                else:
                    k.knit('-',('f',w),c)
