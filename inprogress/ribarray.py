import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,0,1,1,1,1])
ribsize = len(ribpattern)
totrepeats = 1
width  = ribsize*totrepeats
kwriter = knitout.Writer('1 2 3 4 5 6')

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
    kwriter.xfer(('f',s),('b',s))
