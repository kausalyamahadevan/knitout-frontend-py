import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,0,0,0,1,1]) # 1 means knit on back bed
ribsize = len(ribpattern)
totrepeats = 10
width  = ribsize*totrepeats
length = 30
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

xfertorib(kwriter,ribpattern,totrepeats)
kwriter.stitchNumber(6)
kwriter.speedNumber(400)
kwriter.rollerAdvance(400)

ribKnit(kwriter,ribpattern,totrepeats,length,main)
# second to last repeat
for s in range(ribsize*(totrepeats-2),ribsize*(totrepeats-1)):
    if ref[s] == 0:
        kwriter.xfer(('f',s),('b',s))

#last repeat
for s in range(ribsize*(totrepeats-1),ribsize*totrepeats):
    if ref[s] == 1:
        kwriter.xfer(('b',s),('f',s))
''' now the second to last repeat is on the back bed and
    the last repeat on the front bed'''

kwriter.rack(2)
#ribsize*(totrepeats-1)-2 -> ribsize*(totrepeats-1)
#ribsize*(totrepeats-1)-1 -> ribsize*(totrepeats-1)+1
kwriter.xfer(('b',ribsize*(totrepeats-1)-2),('f',ribsize*(totrepeats-1)))
kwriter.xfer(('b',ribsize*(totrepeats-1)-1),('f',ribsize*(totrepeats-1)+1))

''' Last repeat totally on the front bed, second to last repeat (shortened) on the back bed'''
ref = np.delete(ref, [ribsize*(totrepeats-1)-2,ribsize*(totrepeats-1)-1])
kwriter.rack(0)
for s in range(ribsize*(totrepeats-2),ribsize*(totrepeats-1)-2):
    if ref[s] == 0:
        kwriter.xfer(('b',s),('f',s))

# ribKnit(kwriter,ref,1,1,main)
kwriter.write('knitting-files/ribdecrease.k')
