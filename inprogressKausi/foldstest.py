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
knitroller = 450

draw = '1'
waste = '2'
main = '3'
# acr = '5'
# shrink = '6'
xrep = 1
yrep = 2
stitchsize = 4
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
# kwriter.ingripper(acr)
# kwriter.ingripper(shrink)
kwriter.stitchNumber(stitchsize)

# caston(kwriter,width,[draw,waste,main,acr,shrink])
caston(kwriter,width,[draw,waste,main])


# for yarn in [main,acr,shrink]:
for yarn in [main]:
    print(yarn)
    if yarn != main:
        circular(kwriter,width,2,draw,'r')
        interlock(kwriter,width,6,waste)
        circular(kwriter,width,4,waste)
        for s in range(width):
            kwriter.drop(('b',s))

        ribKnit(kwriter,[0],width,1,draw,'r')
        kwriter.rack(0.25)

        for s in range(width):
            kwriter.knit('+',('f',s),yarn)
            kwriter.knit('+',('b',s),yarn)

        circular(kwriter,width,3,yarn,'r')
    '''--- NEXT SAMPLE ---'''
    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)
    beginpleats(kwriter,refv,xrep)
    kwriter.stitchNumber(stitchsize)
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    pleatsrib(kwriter,refv,1,length,yarn)

    '''--- NEXT SAMPLE ---'''
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)
    circular(kwriter,width,2,draw)
    interlock(kwriter,width,6,waste)
    circular(kwriter,width,4,waste)
    for s in range(width):
        kwriter.drop(('b',s))

    ribKnit(kwriter,[0],width,1,draw)
    kwriter.rack(0.25)

    for s in range(width):
        kwriter.knit('+',('f',s),yarn)
        kwriter.knit('+',('b',s),yarn)

    circular(kwriter,width,3,yarn,'r')

    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)
    beginpleats(kwriter,refd[0],xrep)
    kwriter.stitchNumber(stitchsize)
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)
    pleatArray(kwriter,refd,1,1,yarn)

    '''--- NEXT SAMPLE ---'''
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)
    circular(kwriter,width,2,draw,'r')

    interlock(kwriter,width,6,waste)
    circular(kwriter,width,4,waste)
    for s in range(width):
        kwriter.drop(('b',s))

    circular(kwriter,width,1,draw,'r')
    kwriter.rack(0.25)

    for s in range(width):
        kwriter.knit('+',('f',s),yarn)
        kwriter.knit('+',('b',s),yarn)

    circular(kwriter,width,3,yarn,'r')

    # kwriter.speedNumber(100)
    # kwriter.rollerAdvance(0)
    # beginpleats(kwriter,refv,xrep)
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)
    kwriter.stitchNumber(4)
    pleatsrib(kwriter,ribonly,1,length,yarn)
    #
    '''--- NEXT SAMPLE ---'''
    circular(kwriter,width,2,draw)
    interlock(kwriter,width,6,waste)
    circular(kwriter,width,4,waste)
    for s in range(width):
        kwriter.drop(('b',s))

    ribKnit(kwriter,[0],width,1,draw)
    kwriter.rack(0.25)

    for s in range(width):
        kwriter.knit('+',('f',s),yarn)
        kwriter.knit('+',('b',s),yarn)

    circular(kwriter,width,3,yarn,'r')

    kwriter.speedNumber(xferspeed)
    kwriter.rollerAdvance(xferroller)
    xfertorib(kwriter,[0],width)
    kwriter.stitchNumber(stitchsize)
    kwriter.speedNumber(knitspeed)
    kwriter.rollerAdvance(knitroller)

    ribKnit(kwriter,[0],width,length,yarn)



'''--- NEXT SAMPLE ---'''

ribKnit(kwriter,[0],width,1,draw,'r')
ribKnit(kwriter,[0],width,20,waste)


for s in range(width):
    kwriter.drop(('f',s))
for s in range(width-1,-1,-1):
    kwriter.drop(('b',s))
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
# kwriter.outgripper(acr)
# kwriter.outgripper(shrink)
kwriter.write('knitting-files/samplesfold.k')
