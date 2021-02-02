import knitout
import numpy as np
k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

#set carrier to one and bring in
carrier = '1'
k.ingripper('1')

#set sample size

waste=30
width = 20
length= waste+10

k.rack(0.5)

# cast on every needle
for s in range(1,width+1):
    k.tuck('+',('f',s),carrier)
    k.tuck('+',('b',s),carrier)

# interlock
k.rack(0)
for h in range(1,waste):
    if h%2 == 1:
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),carrier)
            else:
                k.knit('-',('b',s),carrier)
    else:
        for s in range(1,width+1):
            if s%2 == 1:
                k.knit('+',('f',s),carrier)
            else:
                k.knit('+',('b',s),carrier)

for h in range(waste, length+1):

#if we are an odd row move left to right
    if h%2 == 1:
        for s in range (width,0,-1):
            k.knit('-', ('f',s),carrier)
    else:
        for s in range (1,width+1):
            k.knit('+', ('b',s),carrier)

k.outgripper(carrier)

for s in range(1,width+1):
    k.drop(('f',s))
    k.drop(('b',s))

k.write('tubular.k')
