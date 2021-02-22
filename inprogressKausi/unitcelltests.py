import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.pleats import *
import numpy as np

refarray = muira(6)
# print(refarray)

# refarray = np.array([[0,1,0,0,-1,0],[0,-1,0,0,1,0]])
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
y3 = '3'
y5 = '5'
y6 = '6'

allyarn = [draw,waste,y3,y5,y6]
xrep = 1
yrep = 1
width = len(refarray[0])*xrep

for i,c in enumerate(allyarn):
    kwriter.ingripper(c)

kwriter.stitchNumber(4)

startnowaste(kwriter,width,allyarn)

for i,c in enumerate([y3,y5,y6]):
    castonmiddle(kwriter,width,[draw,waste,c])
    kwriter.speedNumber(100)
    kwriter.rollerAdvance(0)
    beginpleats(kwriter,refarray[0],xrep)
    pleatArray(kwriter,refarray,xrep,yrep,c)
    scrapoffmiddle(kwriter,width,[draw,waste])
    circular(kwriter,width,2,draw)

dropeverything(kwriter,width,allyarn)
kwriter.write('knitting-files/unitcells.k')