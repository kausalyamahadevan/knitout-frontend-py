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
print(block)
refarray = np.vstack((block,-block))
# refarray = np.array([[0,1,0,0,-1,0],[0,-1,0,0,1,0]])
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'
mono = '6'
xrep = 4
yrep = 2
width = len(refarray[0])*xrep
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.ingripper(mono)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main,mono])

kwriter.kcodecomment('first transfers')
kwriter.speedNumber(100)
#i thought add roller advance only added for one pass but actually does it for all transfwer passes
kwriter.rollerAdvance(0)
# kwriter.addRollerAdvance(-50)
beginpleats(kwriter,refarray[0],xrep)

pleatArray(kwriter,refarray,xrep,yrep,mono)
kwriter.rollerAdvance(300)
kwriter.speedNumber(450)
circular(kwriter,width,6,main)
circular(kwriter,width,2,draw)
interlock(kwriter,width,14,waste)

for s in range(width):
    kwriter.drop(('f',s))
for s in range(width-1,-1,-1):
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.outgripper(mono)
kwriter.write('knitting-files/origami.k')
