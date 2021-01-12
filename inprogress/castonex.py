import sys
sys.path.append('../knitout-frontend-py/')
from library.castonbindoff import *
kwriter = knitout.Writer('1 2 3 4 5 6')

kwriter.addHeader('Machine','kniterate')

width = 50
length = 75
ribwidth  = 4

draw = '1'
waste = '2'
main = '3'
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)
caston(kwriter,width,[draw,waste,main])
#JERSEY
kwriter.rack(0)
kwriter.speedNumber(100)
kwriter.rollerAdvance(100)

for s in range(1,width+1):
    if s%2 == 0:
        kwriter.xfer(('f',s),('b',s))
for s in range(width,0,-1):
    if s%2 ==1:
        kwriter.xfer(('f',s),('b',s))

kwriter.speedNumber(400)
kwriter.rollerAdvance(400)
for h in range(1,length):
    if h%2 ==1:
        for s in range(width,0,-1):
            kwriter.knit('-',('b',s),main)
    else:
        for s in range(1,width+1):
            kwriter.knit('+',('b',s),main)

for s in range(1,width+1):
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('jersey.k')
