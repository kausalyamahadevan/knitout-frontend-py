#get the necessary portions
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from library import ribbing
from library import jersey

import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


c1='1'
c2='2'
c3='3'
c5='5'

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)
k.ingripper(c5)



totalWidth=30;
c1Width=20;
length=20;
width=totalWidth;

stitchsize=4;
tuckstitchsize=2;
transfersize=2;
standardKnitSpeed=400;
standardRoller=400






k.stitchNumber(stitchsize)
castonbindoff.caston(k,width,[c1,c2,c3,c5])

k.speedNumber(100)
k.stitchNumber(transfersize)
k.rollerAdvance(0)
ribbing.rib2ribXfer(k,[1],[0],width)


k.rollerAdvance(standardRoller)
k.speedNumber(standardKnitSpeed)
k.stitchNumber(stitchsize)

jersey.jerseyKnit(k, width, 4, c3)


#Assume both start on the left (move second feeder to the right)
for z in range(totalWidth):
    k.knit('+',('f',z),c5)

#because we have two colors per row,,, change roller to roller/2
k.rollerAdvance(int(standardRoller/2))

for b in range(int(length/2)):
    for z in range(c1Width-1):
        k.knit('+',('f',z),c3)

    #add one tuck at the end of each row - will count as extra pass
    k.rollerAdvance(0)
    k.stitchNumber(tuckstitchsize)

    k.tuck('+',('f',c1Width-1),c3)

    k.stitchNumber(stitchsize)
    k.rollerAdvance(int(standardRoller/2))


    for z in range(c1Width-1,-1,-1):
        k.knit('-',('f',z),c3)

    for z in range(totalWidth-1,c1Width-1,-1):
        k.knit('-',('f',z),c5)

    #add one tuck at the end of each row - will count as extra pass
    k.rollerAdvance(0)
    k.stitchNumber(tuckstitchsize)

    k.tuck('-',('f',c1Width-1),c5)

    k.stitchNumber(stitchsize)
    k.rollerAdvance(int(standardRoller/2))

    for z in range(c1Width-1,totalWidth):
        k.knit('+',('f',z),c5)


k.rollerAdvance(standardRoller)

jersey.jerseyKnit(k, width, 10, c3)

for s in range(width):
    k.drop(('f',s))

k.write('cmuIntarsia.k')
