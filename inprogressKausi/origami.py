import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.pleats import *
import numpy as np
pattern = np.array([0,0,0,1,0,0,0])
pattern2 = np.array([0,1,0,-1,0,1,0])
size = len(pattern)
totrepeats = 3
width  = size*totrepeats
length = 20
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(pattern,totrepeats) # "reference" tells us where pleats
ref2 = np.tile(pattern2,totrepeats)
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)
circular(kwriter,width,4,main)
beginpleats(kwriter,ref)
pleats(kwriter,ref,length,main)
xferpleats(kwriter,ref,ref2)
pleats(kwriter,ref2,length,main)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/pleats.k')
