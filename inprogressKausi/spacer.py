import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
width  = 60
length = 70
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
front = '3'
middle = '5'
back = '6'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(front)
kwriter.ingripper(middle)
kwriter.ingripper(back)

kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,front,middle,back])

kwriter.speedNumber(400)
kwriter.rollerAdvance(250)
kwriter.stitchNumber(4)
for h in range(length):
    if h%2 ==1:
        for s in range(width-1,-1,-1):
            kwriter.knit('-',('f',s),front)
        for s in range(width-1,-1,-1):
            kwriter.knit('-',('b',s),back)
        for s in range(width-1,-1,-1):
            if s%2 ==0:
                kwriter.tuck('-',('b',s),middle)
            else:
                kwriter.tuck('-',('f',s),middle)
    else:
        for s in range(width):
            kwriter.knit('+',('f',s),front)
        for s in range(width):
            kwriter.knit('+',('b',s),back)
        for s in range(width):
            if s%2 ==1:
                kwriter.tuck('+',('b',s),middle)
            else:
                kwriter.tuck('+',('f',s),middle)
circular(kwriter,width,5,front,'l')
for s in range(width):
    kwriter.drop(('f',s))
for s in range(width-1,-1,-1):
    kwriter.drop(('b',s))

kwriter.outgripper(draw)
kwriter.outgripper(front)
kwriter.outgripper(middle)
kwriter.outgripper(back)
kwriter.outgripper(waste)
kwriter.write('knitting-files/spacer.k')
