import knitout
import numpy as np
k = knitout.Writer('1 2 3 4 5 6')

width = 50
length = 300
k.addHeader('Machine','kniterate')
#x-stitch-number 5
#x-speed-number 600
k.rack(0.5)

carrier = '1'
k.ingripper(carrier)
# cast on every needle
for s in range(1,width+1):
    k.tuck('+',('f',s),carrier)
    k.tuck('+',('b',s),carrier)

# interlock
k.rack(0)
for h in range(1,length/3):
    if h%2 ==1:
        for s in range(width+1,1,-1):
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

#full needle rib
k.rack(0.5)
for h in range(length/3,length+1):
    if h%2 ==1:
        for s in range(width+1,1,-1):
            k.knit('-',('b',s),carrier)
            k.knit('-',('f',s),carrier)
    else:
        for s in range(1,width+1):
            k.knit('+',('f',s),carrier)
            k.knit('+',('b',s),carrier)

k.outgripper(carrier)

for s in range(1,width+1):
    k.drop(('f',s))
    k.drop(('b',s))

k.write('fnrib.k')
