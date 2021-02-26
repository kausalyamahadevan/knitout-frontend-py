#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from SensorTests import sensorSamples
from library import jersey
from library import ribbing
from library import fairIsleStiffFxn



import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c6='6'
mainSampleYarn=c6;

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(mainSampleYarn)


sampleStitchsize=4
tabStitchsize=4
transferStitchSize=2




width=40
tablength=30
samplelength=40
numsamples=6

k.stitchNumber(tabStitchsize)
k.speedNumber(400)
k.rollerAdvance(300)
castonbindoff.caston(k,width,[c1,c2,c2,mainSampleYarn])


k.speedNumber(400)
k.rollerAdvance(300)

#make first tab
castonbindoff.interlock(k,width,tablength,c2,'l')

#set counter which tells side that feeder for
counter=0




# #Jersey structure stitch size 6
# for z in range(3):
#
#     k.stitchNumber(6)
#     jersey.jerseyKnit(k,width,samplelength,c3)
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#
# #Jersey structure stitch size 8
# for z in range(3):
#
#     k.stitchNumber(8)
#     jersey.jerseyKnit(k,width,samplelength,c3)
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1

#
# #structure sampler 1 code:
# #Jersey structure stitch size 4
# for z in range(numsamples):
#
#     k.speedNumber(100)
#     k.stitchNumber(2)
#     k.rollerAdvance(0)
#     ribbing.rib2ribXfer(k, [1], [0], width)
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     jersey.jerseyKnit(k,width,samplelength,c6)
#
#     k.rollerAdvance(300)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#
#
# #interlock structure
# for z in range(numsamples):
#
#     k.rollerAdvance(400)
#     k.stitchNumber(sampleStitchsize)
#     castonbindoff.interlock(k,width,samplelength,mainSampleYarn,'l')
#
#     k.rollerAdvance(300)
#     k.stitchNumber(tabStitchsize)
#     k.rollerAdvance(400)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#
#
# #ribbing structure 1x1 rib
# for z in range(numsamples):
#     k.speedNumber(100)
#     k.rollerAdvance(0)
#     k.stitchNumber(transferStitchSize)
#
#     ribbing.xfertorib(k,[0,1],int(width/2))
#
#     k.speedNumber(400)
#     k.stitchNumber(sampleStitchsize)
#     k.rollerAdvance(400)
#     ribbing.ribKnit(k,[0,1],int(width/2),samplelength,mainSampleYarn)
#
#     k.rollerAdvance(300)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#     counter=counter+1
#
# #ribbing structure 2x2 rib
# for z in range(numsamples):
#     k.speedNumber(100)
#     k.rollerAdvance(0)
#     k.stitchNumber(transferStitchSize)
#
#     ribbing.xfertorib(k,[0,0,1,1],int(width/4))
#
#     k.speedNumber(400)
#     k.stitchNumber(sampleStitchsize)
#     k.rollerAdvance(400)
#     ribbing.ribKnit(k,[0,0,1,1],int(width/4),samplelength,mainSampleYarn)
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#     counter=counter+1
#
# #ribbing structure 4x4 rib
# for z in range(numsamples):
#     k.speedNumber(100)
#     k.rollerAdvance(0)
#     k.stitchNumber(transferStitchSize)
#
#     ribbing.xfertorib(k,[0,0,0,0,1,1,1,1],int(width/8))
#
#     k.speedNumber(400)
#     k.stitchNumber(sampleStitchsize)
#     k.rollerAdvance(400)
#     ribbing.ribKnit(k,[0,0,0,0,1,1,1,1],int(width/8),samplelength,mainSampleYarn)
#
#     k.rollerAdvance(300)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#     counter=counter+1
#


for s in range(width):
    k.drop(('f',s))
for s in range(width):
    k.drop(('b',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(mainSampleYarn)


k.write('structureSampler.k')
