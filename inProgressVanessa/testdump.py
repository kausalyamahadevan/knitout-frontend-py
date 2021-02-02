#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff

# from crossover_full import *
# from library.crossover_half import *
# from library.crossover_full import *

# from seedKnit import*
from library.jersey import*
from library.tuckstuff import*
from library.twocolorinterlock import*
# from library.fairIsleStiffFxn import*
# from library.jerseyVariedStitches import*
from library.ribbing import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c3='3'
c5='5'


k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)
k.ingripper(c5)

width=30

k.stitchNumber(5)
castonbindoff.caston(k,width,[c1,c2,c3,c5])

interlocktwoColorStriped(k,width,30,c1,c2)

for s in range(width):
    k.drop(('f',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)

k.write('twoColorInterlock.k')
