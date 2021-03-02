import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,0,0,0,1,1,0,0,0,0,1,1]) # 1 means knit on back bed
ribsize = len(ribpattern)
totrepeats = 8
width  = ribsize*totrepeats
length = 30
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(ribpattern,totrepeats) # "reference" tells us where knit and purls go
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '6'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main])
#TRANSFERS
kwriter.rack(0)
kwriter.speedNumber(100)
kwriter.rollerAdvance(0)

xfertorib(kwriter,ribpattern,totrepeats)
kwriter.speedNumber(400)
kwriter.rollerAdvance(400)

ribKnit(kwriter,ribpattern,totrepeats,length,main)
''' decrease 1 repeate on RIGHT'''
stitchesleft = ribsize
reflen = len(ref)
reps = int(stitchesleft/4)
# second to last repeat
kwriter.rollerAdvance(0)
for i in range(reps):
    for s in range(reflen-ribsize-2,reflen-ribsize):
        if ref[s] == 1:
            kwriter.xfer(('b',s),('f',s))

    #last repeat
    for s in range(reflen-ribsize,reflen):
        if ref[s] == 0:
            kwriter.xfer(('f',s),('b',s))
    ''' now the second to last repeat is on the front bed and
        the last repeat on the back bed'''

    kwriter.rack(-2)
    for s in range(reflen-ribsize,reflen):
        kwriter.xfer(('b',s),('f',s-2))

    ''' everything on the front bed now '''
    kwriter.rack(0)
    ref = np.delete(ref, [ribsize*(totrepeats-1)-2,ribsize*(totrepeats-1)-1])
    reflen = len(ref)
    for s in range(reflen-ribsize,reflen):
        if ref[s] == 1:
            kwriter.xfer(('f',s),('b',s))
    kwriter.rollerAdvance(400)
    ribKnit(kwriter,ref,1,2,main)
    stitchesleft = stitchesleft-2

''' -----------------------
    DECREASE 1 REPEAT ON LEFT '''
kwriter.rollerAdvance(400)
ribKnit(kwriter,ref,1,1,main)

stitchesleft = ribsize
reflen = len(ref)
reps = int(stitchesleft/4)
# second to last repeat
startn = 0
kwriter.rollerAdvance(0)
for i in range(reps):
    for s in range(ribsize+1,ribsize+3):
        if ref[s] == 1:
            kwriter.xfer(('b',s+startn),('f',s+startn))

    #last repeat
    for s in range(0,ribsize):
        if ref[s] == 0:
            kwriter.xfer(('f',s+startn),('b',s+startn))
    ''' now the second to last repeat is on the front bed and
        the last repeat on the back bed'''

    kwriter.rack(2)
    for s in range(0,ribsize):
        kwriter.xfer(('b',s+startn),('f',s+2+startn))

    ''' everything on the front bed now '''
    kwriter.rack(0)
    ref = np.delete(ref, [ribsize+1,ribsize+2])
    reflen = len(ref)
    startn +=2
    for s in range(0,ribsize*2):
        if ref[s] == 1:
            kwriter.xfer(('f',s+startn),('b',s+startn))
    kwriter.rollerAdvance(400)
    ribKnit(kwriter,ref,1,2,main,n0=startn,side = 'r')
    stitchesleft = stitchesleft-2

''' --------------------------- '''
kwriter.rollerAdvance(400)
ribKnit(kwriter,ref,1,15,main,n0=startn,side = 'r')
ribKnit(kwriter,ref,1,25,waste,n0=startn,side = 'l')
rib2ribXfer(kwriter,ribpattern,[0,1,0,1,0,1,0,1,0,1,0,1],10)
fishermansrib(kwriter,84,100,main,side='l',n0=startn)

dropeverything(kwriter,width,[draw,waste,main])
kwriter.write('knitting-files/ribdecrease.k')
