import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.pleats import *
from library.ribbing import *
import numpy as npi
width = 42
length = 60
refv = np.zeros((width,))
refv[20] = 1
refd = np.identity(width)
ribonly = np.zeros((width,))
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')
xferspeed = 100
xferroller = 0
knitspeed = 450


draw = '1'
waste = '2'
main = '3'
shrink = '6'
xrep = 1
yrep = 2
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.ingripper(shrink)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main,shrink])
'''--- NEXT SAMPLE ---'''
kwriter.speedNumber(100)
kwriter.rollerAdvance(0)
beginpleats(kwriter,refv,xrep)
kwriter.speedNumber(450)
kwriter.rollerAdvance(450)
kwriter.stitchNumber(4)
pleatsrib(kwriter,refv,1,length,main)
#
# '''--- NEXT SAMPLE ---'''
# circular(kwriter,width,2,draw)
# interlock(kwriter,width,6,waste)
# circular(kwriter,width,4,waste)
# for s in range(width):
#     kwriter.drop(('b',s))
#
# circular(kwriter,width,1,draw,'r')
# kwriter.rack(0.25)
#
# for s in range(width):
#     kwriter.knit('+',('f',s),main)
#     kwriter.knit('+',('b',s),main)
#
# circular(kwriter,width,2,main,'r')
#
# kwriter.speedNumber(100)
# kwriter.rollerAdvance(0)
# beginpleats(kwriter,refv,xrep)
# kwriter.speedNumber(450)
# kwriter.rollerAdvance(450)
# kwriter.stitchNumber(4)
# pleatArray(kwriter,refd,1,1,main)
#
# '''--- NEXT SAMPLE ---'''
# circular(kwriter,width,2,draw)
# interlock(kwriter,width,6,waste)
# circular(kwriter,width,4,waste)
# for s in range(width):
#     kwriter.drop(('b',s))
#
# circular(kwriter,width,1,draw,'r')
# kwriter.rack(0.25)
#
# for s in range(width):
#     kwriter.knit('+',('f',s),main)
#     kwriter.knit('+',('b',s),main)
#
# circular(kwriter,width,2,main,'r')
#
# kwriter.speedNumber(100)
# kwriter.rollerAdvance(0)
# beginpleats(kwriter,refv,xrep)
# kwriter.speedNumber(450)
# kwriter.rollerAdvance(450)
# kwriter.stitchNumber(4)
# pleatsrib(kwriter,ribonly,1,length,main)
#
# '''--- NEXT SAMPLE ---'''
# circular(kwriter,width,2,draw)
# interlock(kwriter,width,6,waste)
# circular(kwriter,width,4,waste)
# for s in range(width):
#     kwriter.drop(('b',s))
#
# circular(kwriter,width,1,draw,'r')
# kwriter.rack(0.25)
#
# for s in range(width):
#     kwriter.knit('+',('f',s),main)
#     kwriter.knit('+',('b',s),main)
#
# circular(kwriter,width,2,main,'r')
#
# kwriter.speedNumber(100)
# kwriter.rollerAdvance(0)
# xfertorib(kwriter,[0],width)
# kwriter.speedNumber(450)
# kwriter.rollerAdvance(450)
# kwriter.stitchNumber(4)
# ribKnit(kwriter,[0],width,length,main)
#
# # '''--- NEXT SAMPLE ---'''
# #
# # ribKnit(kwriter,[0],width,1,draw)
# # ribKnit(kwriter,[0],width,5,waste,'r')
# # circular(kwriter,width,1,draw)


for s in range(width):
    kwriter.drop(('f',s))
for s in range(width-1,-1,-1):
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.outgripper(shrink)
kwriter.write('knitting-files/samplesfold.k')
