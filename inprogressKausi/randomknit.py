import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library.castonbindoff import *
from library.ribbing import *
import numpy as np

width = 61
length = 90
N = width*length
frac = 0.5

K = int(frac*N) # K zeros, N-K ones
arr = np.array([0] * K + [1] * (N-K))

kwriter = knitout.Writer('1 2 3 4 5 6')
kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
y3 = '6'
# y5 = '5'
# y6 = '6'

allyarn = [draw,waste,y3]
xrep = 1
yrep = 1

for i,c in enumerate(allyarn):
    kwriter.ingripper(c)

kwriter.stitchNumber(4)

startnowaste(kwriter,width,allyarn)

for i in range(3):
    np.random.shuffle(arr)
    ref = np.reshape(arr,(length,width))

    castonmiddle(kwriter,width,[draw,waste,y3])
    kwriter.speedNumber(100)
    kwriter.rollerAdvance(0)
    xfertorib(kwriter,ref[0],xrep)
    kwriter.speedNumber(400)
    kwriter.rollerAdvance(450)
    knitArray(kwriter,ref,1,1,c)
    kwriter.stitchNumber(4)
    kwriter.speedNumber(400)
    scrapoffmiddle(kwriter,width,[draw,waste])
    circular(kwriter,width,2,draw)

frac = 0.25
K = int(frac*N) # K zeros, N-K ones
arr = np.array([0] * K + [1] * (N-K))

for i in range(3):
    np.random.shuffle(arr)
    ref = np.reshape(arr,(length,width))

    castonmiddle(kwriter,width,[draw,waste,y3])
    kwriter.speedNumber(100)
    kwriter.rollerAdvance(0)
    xfertorib(kwriter,ref[0],xrep)
    kwriter.speedNumber(400)
    kwriter.rollerAdvance(450)
    knitArray(kwriter,ref,1,1,c)
    kwriter.stitchNumber(4)
    kwriter.speedNumber(400)
    scrapoffmiddle(kwriter,width,[draw,waste])
    circular(kwriter,width,2,draw)

dropeverything(kwriter,width,allyarn)
kwriter.write('knitting-files/random.k')
