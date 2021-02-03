import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,1]) # 1 means knit on back bed
ribsize = len(ribpattern)
totrepeats = 20
width  = ribsize*totrepeats
samplelength = 30
wastelength = 20
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(ribpattern,totrepeats) # "reference" tells us where knit and purls go
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
y3 = '3'
y5 = '5'
y6 = '6'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(y3)
kwriter.ingripper(y5)
kwriter.ingripper(y6)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,waste,y3,y5,y6])
#TRANSFERS
kwriter.rack(0)
kwriter.stitchNumber(4)
kwriter.speedNumber(400)
# kwriter.rollerAdvance(400)

interlock(kwriter,width,wastelength,waste)
interlock(kwriter,width,samplelength,y3)
interlock(kwriter,width,wastelength,waste)

circular(kwriter,width,1,draw,'r')

interlock(kwriter,width,wastelength,waste)
interlock(kwriter,width,samplelength,y5)
interlock(kwriter,width,wastelength,waste)

circular(kwriter,width,1,draw)

interlock(kwriter,width,wastelength,waste)
interlock(kwriter,width,samplelength,y6)
interlock(kwriter,width,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,samplelength,y3)
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,1,draw)
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,samplelength,y5)
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,1,draw,'r')
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)
#
# ribKnit(kwriter,ribpattern,totrepeats,samplelength,y6)
#
# ribKnit(kwriter,ribpattern,totrepeats,wastelength,waste)

for s in range(width):
    kwriter.drop(('f',s))

for s in range(width):
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(y3)
kwriter.outgripper(waste)
kwriter.outgripper(y5)
kwriter.outgripper(y6)
kwriter.write('knitting-files/yarn_test.k')
