import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np

rib1 = np.hstack((np.ones((4,)),np.zeros((4,))))
rib2 = np.hstack((np.zeros((4,)),np.ones((4,))))
knitpart = np.ones(8,)
purlpart = np.zeros(8,)

ribsize = len(rib1)
totrepeats = 10
width  = ribsize*totrepeats
yrepeats = 4
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')
knitheight = 10
ribheight = 20

xferspeed = 100
xferroller = 100
knitspeed = 400
knitroller = 400

draw = '1'
waste = '2'
main = '5'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main])
#TRANSFERS
kwriter.rack(0)
kwriter.speedNumber(xferspeed)
kwriter.rollerAdvance(xferroller)

xfertorib(kwriter,rib1,totrepeats)

# kwriter.stitchNumber(6)
''' --------- '''
for i in range(yrepeats):
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    ribKnit(kwriter,rib1,totrepeats,ribheight,main)
    ''' ------------- '''
    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)

    rib2ribXfer(kwriter,rib1,knitpart,totrepeats)

    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    ribKnit(kwriter,knitpart,totrepeats,knitheight,main)
    ''' ------------- '''
    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)

    rib2ribXfer(kwriter,knitpart,rib2,totrepeats)

    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    ribKnit(kwriter,rib2,totrepeats,ribheight,main)
    ''' ------------- '''
    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)

    rib2ribXfer(kwriter,rib2,purlpart,totrepeats)

    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    ribKnit(kwriter,purlpart,totrepeats,knitheight,main)
    ''' ----------------- '''
    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)

    rib2ribXfer(kwriter,purlpart,rib1,totrepeats)

for s in range(width):
    kwriter.drop(('f',s))
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('knitting-files/bistable.k')
