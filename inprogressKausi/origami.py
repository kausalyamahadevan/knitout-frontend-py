import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.pleats import *
import numpy as np
pattern = np.array([0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,1])
pattern2 = np.array([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,-1])
size = len(pattern)
totrepeats = 5
# width  = size*totrepeats
length = 50
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(pattern,totrepeats) # "reference" tells us where pleats
ref2 = np.tile(pattern2,totrepeats)
ref = np.append(ref, [0,0,0,0,0,0,0])
ref2 = np.append(ref2, [0,0,0,0,0,0,0])
width  = len(ref)
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main])

kwriter.speedNumber(100)
kwriter.addRollerAdvance(-200)
kwriter.rollerAdvance(0)
beginpleats(kwriter,ref)
kwriter.speedNumber(400)
kwriter.addRollerAdvance(200)
kwriter.stitchNumber(4)

pleatsrib(kwriter,ref,length,main)

kwriter.speedNumber(100)
kwriter.addRollerAdvance(-200)
kwriter.rollerAdvance(0)
xferpleats(kwriter,ref,ref2)

kwriter.stitchNumber(4)
kwriter.speedNumber(400)
kwriter.addRollerAdvance(200)
kwriter.stitchNumber(4)
pleatsrib(kwriter,ref2,length,main)

for s in range(width):
    kwriter.drop(('f',s))
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/pleats.k')
