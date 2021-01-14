import knitout
from castonbindoff import *
import numpy as np

xrepeats = 2
yrepeats = 2

xpatternsize = 20
ypatternsize = 60 #?

xsize = xrepeats*xpatternsize
ysize = yrepeats*ypatternsize

def pleats(width,length,space,c,side):
    k.rack(0)
    # transfer
    for s in range(1,width+1):
        if s%xpatternsize==0:
            k.xfer(('f',s),('b',s))
        elif s%xpatternsize == xpatternsize/2:
            k.xfer(('b',s),('f',s))
    k.rack(0.5)
    #full needle rib without those needles

k = knitout.Writer('1 2 3 4 5 6')

k.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'
k.ingripper(waste)
k.ingripper(draw)
k.ingripper(main)

# cast on every needle
catchyarns(xsize,['1','2','3'])
k.rack(0.5)
for s in range(1,xsize+1):
    k.knit('+',('f',s),waste)
    k.knit('+',('b',s),waste)


#interlock / waste yarn
interlock(xsize,18,waste,'r')
#circular / waste Yarn
circular(xsize,2,waste,'l')
k.outgripper(waste)

# draw thread
circular(xsize,2,draw,'l')
k.outgripper(draw)

# # cast on every needle
# k.rack(0.5)
# for s in range(1,xsize+1):
#     k.knit('+',('f',s),main)
#     k.knit('+',('b',s),main)

k.write('muiraori.k')
