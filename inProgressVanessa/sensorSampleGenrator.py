#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from library import sensorSamples

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

sampleStitchsize=4
tabStitchsize=5
transferStitchSize=2

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(c3)
k.ingripper(c5)

width=30
tablength=30
samplelength=30

k.stitchNumber(tabStitchsize)
castonbindoff.caston(k,width,[c1,c2,c3,c5])

castonbindoff.interlock(k,width,tablength,c2,'l')
counter=1

for z in range(3):
    k.stitchNumber(sampleStitchsize)
    castonbindoff.interlock(k,width,samplelength,c5,'l')
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)
    counter=counter+1

for z in range(3):
    k.stitchNumber(sampleStitchsize)
    interlocktwoColorMix(k,width,samplelength,c5,c3,'l')
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)
    counter=counter+1

for z in range(3):
    k.stitchNumber(sampleStitchsize)
    interlocktwoColorStriped(k,width,samplelength,c5,c3,'l')
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)
    counter=counter+1


for z in range(3):
    k.speedNumber(100)
    k.stitchNumber(transferStitchSize)
    xfertorib(k,[0,1],15)
    k.rollerAdvance(400)
    k.speedNumber(400)
    k.stitchNumber(sampleStitchsize)
    ribKnit(k,[0,1],15,samplelength,c5,'l')
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)
    counter=counter+1

for z in range(3):
    k.speedNumber(100)
    k.stitchNumber(transferStitchSize)
    xfertorib(k,[0],30)
    k.rollerAdvance(400)
    k.speedNumber(400)
    k.stitchNumber(sampleStitchsize)
    jerseyKnit(k,width,samplelength,c5,'l')
    k.speedNumber(100)
    k.rollerAdvance(300)
    rib2ribXfer(k,[0,0],[0,1],15)

    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)
    counter=counter+1


for s in range(width):
    k.drop(('f',s))
    k.drop(('b',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(c3)
k.outgripper(c5)

k.write('sensorInterlock.k')
