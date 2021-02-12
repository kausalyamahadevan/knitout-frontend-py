#get the necessary portions
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff

import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')


c1='1'
c2='2'

totalWidth=30;
c1Width=20;
cswidth=totalWidth-c1Width;
length=20;

stitchsize=4;

#Assume both start on the left (move second feeder to the right)

for z in range(totalWidth):
    k.knit('+',('f',z),c2)



for b in range(int(length/2)):
    for z in range(c1Width):
        k.knit('+',('f',z),c1)
    k.tuck('+',('b',c1Width),c1)

    for z in range(totalWidth-1,-1,c1Width-1):
        k.knit('-',('f',z),c2)
    k.tuck('-',('b',c1Width-1),c2)

    for z in range(c1Width-1,-1,-1):
        k.knit('-',('f',z),c1)

    for z in range(c1Width, totalWidth):
        k.knit('+',('f',z),c2)

    for z in range(c1Width+2,-1,c1Width-2):
        k.drop(('b',z))


for z in range(totalWidth):
    k.knit('+',('f',z),c1)

k.write('firstIntarsia.k')
