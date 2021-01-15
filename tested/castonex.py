import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
## How to import from another folder (example)
# from inprogress.fnrib import *

kwriter = knitout.Writer('1 2 3 4 5 6')

kwriter.addHeader('Machine','kniterate')

width = 120
length = 150

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

for s in range(width):
    if s%2 == 0:
        kwriter.xfer(('f',s),('b',s))
for s in range(width-1,-1,-1):
    if s%2 ==1:
        kwriter.xfer(('f',s),('b',s))

kwriter.speedNumber(400)
kwriter.rollerAdvance(550)
for h in range(length):
    if h%2 ==1:
        for s in range(width-1,-1,-1):
            kwriter.knit('-',('b',s),main)
    else:
        for s in range(width):
            kwriter.knit('+',('b',s),main)

for s in range(width):
    kwriter.drop(('b',s))

kwriter.addRollerAdvance(1000)
kwriter.outgripper(draw)
kwriter.outgripper(main)
kwriter.outgripper(waste)
kwriter.write('aaJersey.k')
