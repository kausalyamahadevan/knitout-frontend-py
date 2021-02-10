import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.pleats import *
import numpy as np
# print(np.zeros((8,4)))
a = np.vstack((np.zeros((8,4)),np.identity(4),np.zeros((4,4))))
c = np.vstack((np.zeros((4,8)),np.rot90(np.identity(8)),np.zeros((4,8))))
e = np.vstack((np.zeros((4,4)),np.identity(4),np.zeros((8,4))))
b = np.vstack((np.ones((12,1)),-np.ones((4,1))))
d = np.vstack((-np.ones((4,1)),np.ones((12,1))))
block = np.hstack((a,b,c,d,e))

refarray = np.vstack((block,-block))
# refarray = np.array([[0,1,0,0,-1,0],[0,-1,0,0,1,0]])
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'
xrep = 4
yrep = 4
width = len(refarray[0])*xrep

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(2)

caston(kwriter,width,[draw,waste,main])

kwriter.speedNumber(100)
kwriter.addRollerAdvance(-200)
kwriter.rollerAdvance(0)
beginpleats(kwriter,refarray[0],xrep)

pleatArray(kwriter,refarray,xrep,yrep,main)

for s in range(width):
    kwriter.drop(('f',s))
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/origami.k')
