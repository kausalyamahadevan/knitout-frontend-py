import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np

n = 5
knitheight = 12
ribheight = 10
rib1 = np.hstack((np.ones((ribheight,n)),np.zeros((ribheight,n))))
rib2 = np.hstack((np.zeros((ribheight,n)),np.ones((ribheight,n))))
knitpart = np.ones((knitheight,2*n))
purlpart = np.zeros((knitheight,2*n))
block = np.vstack((rib1,knitpart,rib2,purlpart))
ribsize = len(rib1)
totrepeats = 10
width  = ribsize*totrepeats
yrepeats = 2
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')
kwriter.addHeader('Position','Left')


xferspeed = 100
xferroller = 0
knitspeed = 400
knitroller = 450

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
kwriter.speedNumber(xferspeed)
kwriter.rollerAdvance(xferroller)

xfertorib(kwriter,block[0],totrepeats)

# kwriter.stitchNumber(6)
''' --------- '''
knitArray(kwriter,block,totrepeats,yrepeats,main)
kwriter.speedNumber(knitspeed)
kwriter.rollerAdvance(knitroller)
kwriter.stitchNumber(4)
ribKnit(kwriter,block[0],totrepeats,10,main)
ribKnit(kwriter,block[0],totrepeats,1,draw)
ribKnit(kwriter,block[0],totrepeats,36,waste)
# for i in range(yrepeats):
#     kwriter.speedNumber(knitspeed)
#     kwriter.rollerAdvance(knitroller)

    # ribKnit(kwriter,rib1,totrepeats,ribheight,main)
    # ''' ------------- '''
    # kwriter.speedNumber(xferspeed)
    # kwriter.rollerAdvance(xferroller)
    #
    # rib2ribXfer(kwriter,rib1,knitpart,totrepeats)
    #
    # kwriter.speedNumber(knitspeed)
    # kwriter.rollerAdvance(knitroller)
    #
    # ribKnit(kwriter,knitpart,totrepeats,knitheight,main)
    # ''' ------------- '''
    # kwriter.speedNumber(xferspeed)
    # kwriter.rollerAdvance(xferroller)
    #
    # rib2ribXfer(kwriter,knitpart,rib2,totrepeats)
    #
    # kwriter.speedNumber(knitspeed)
    # kwriter.rollerAdvance(knitroller)
    #
    # ribKnit(kwriter,rib2,totrepeats,ribheight,main)
    # ''' ------------- '''
    # kwriter.speedNumber(xferspeed)
    # kwriter.rollerAdvance(xferroller)
    #
    # rib2ribXfer(kwriter,rib2,purlpart,totrepeats)
    #
    # kwriter.speedNumber(knitspeed)
    # kwriter.rollerAdvance(knitroller)
    #
    # ribKnit(kwriter,purlpart,totrepeats,knitheight,main)
    # ''' ----------------- '''
    # kwriter.speedNumber(xferspeed)
    # kwriter.rollerAdvance(xferroller)
    #
    # rib2ribXfer(kwriter,purlpart,rib1,totrepeats)


for s in range(width):
    kwriter.drop(('f',s))
for s in range(width):
    kwriter.drop(('b',s))

kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/bistable.k')
