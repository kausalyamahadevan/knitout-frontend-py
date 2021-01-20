import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
# ribpattern = np.array([0,0,1,1]) # 1 means knit on back bed
seedpattern = np.array([[1,0],[0,1]])
ribsize = len(seedpattern[0])
totrepeats = 20
width  = ribsize*totrepeats
length = 20
kwriter = knitout.Writer('1 2 3 4 5 6')
# ref = np.tile(ribpattern,totrepeats) # "reference" tells us where knit and purls go
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

xfertorib(kwriter,seedpattern[0],totrepeats)
kwriter.stitchNumber(6)
kwriter.speedNumber(400)
kwriter.rollerAdvance(400)
#
# ribKnit(kwriter,ribpattern,totrepeats,length/2,main)
#
# rib2 = np.array([0,1,0,1])
#
# rib2ribXfer(kwriter,ribpattern,rib2,totrepeats)
#
# ribKnit(kwriter,rib2,totrepeats,length/2,main,'r')
knitArray(kwriter,seedpattern,totrepeats,length,main)
for s in range(width):
    kwriter.drop(('f',s))
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/seed.k')
