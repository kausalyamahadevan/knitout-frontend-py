import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.spacer import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
width  = 60
length = 70
kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

frontsize = 4
backsize = 4
tucksize = 2

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
# kwriter.stitchNumber(4)
spacerFabric(kwriter,width,length,front,back,middle)

kwriter.stitchNumber(4)
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
