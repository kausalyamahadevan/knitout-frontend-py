import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,0,1,1,1,1]) # 1 means knit on back bed
ribsize = len(ribpattern)
totrepeats = 10
width  = ribsize*totrepeats
length = 70
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(ribpattern,totrepeats) # "reference" tells us where knit and purls go
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main])
#TRANSFERS
kwriter.rack(0)
kwriter.speedNumber(100)
kwriter.rollerAdvance(100)

for s in range(width):
    if ref[s] == 1:
        kwriter.xfer(('f',s),('b',s))
    else:
        kwriter.xfer(('b',s),('f',s))

kwriter.speedNumber(400)
kwriter.rollerAdvance(400)
kwriter.stitchNumber(6)

for h in range(length):
    if h%2 ==0:
        for s in range(width):
            if ref[s] == 1:
                kwriter.knit('+',('b',s),main)
            else:
                kwriter.knit('+',('f',s),main)
    else:
        for s in range(width-1,-1,-1):
            if ref[s] == 1:
                kwriter.knit('-',('b',s),main)
            else:
                kwriter.knit('-',('f',s),main)

for s in range(width):
    kwriter.drop(('f',s))
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('Anewrib.k')
