import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np
# 0 -> knit on front bed, 1 -> knit on back bed
ribpattern = np.array([0,0,1,1,1,1]) # 1 means knit on back bed
ribsize = len(ribpattern)
totrepeats = 10
width  = ribsize*totrepeats
length = 70
kwriter = knitout.Writer('1 2 3 4 5 6')
ref = np.tile(ribpattern,totrepeats) # "reference" tells us where knit and purls go
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
