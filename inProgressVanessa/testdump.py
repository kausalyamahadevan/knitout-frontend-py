#creates just a miss section of knit (no tube)
import knitout
from crossover_full import *
from crossover_half import*
import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c='1'

crossoverFull(k,20,20,c,'l')

k.write('aatestdump.k')
