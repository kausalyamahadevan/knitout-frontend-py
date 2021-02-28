#creates just a miss section of knit (no tube)
import sys
sys.path.append('../knitout-frontend-py')
from library import knitout
from library import castonbindoff
from SensorTests import sensorSamples
from library import jersey
from library import ribbing
from library import fairIsleStiffFxn
from library import garter
from library import inlay



import numpy as np
import math

k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine','kniterate')

c1='1'
c2='2'
c6='6'
c5='5'
mainSampleYarn=c6;
secondYarn=c5

k.ingripper(c1)
k.ingripper(c2)
k.ingripper(mainSampleYarn)



sampleStitchsize=4
tabStitchsize=4
transferStitchSize=2




width=40
tablength=30
samplelength=40

'''important'''
numsamples=1

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


#2x2 garter
for z in range(numsamples):

    for i in range(int(samplelength/4)):
        k.speedNumber(100)
        k.rollerAdvance(0)
        k.stitchNumber(2)
        ribbing.rib2ribXferNoRoller(k, [1], [0], width)

        k.speedNumber(400)
        k.stitchNumber(4)
        k.rollerAdvance(400)
        jersey.jerseyKnit(k, width, 2, mainSampleYarn,'l','f')

        k.speedNumber(100)
        k.rollerAdvance(0)
        k.stitchNumber(2)
        ribbing.rib2ribXferNoRoller(k, [0], [1], width)

        k.speedNumber(400)
        k.stitchNumber(4)
        k.rollerAdvance(400)
        jersey.jerseyKnit(k, width, 2, mainSampleYarn,'l','b')


    k.speedNumber(400)
    k.stitchNumber(4)
    k.rollerAdvance(400)
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)

    counter=counter+1


#4x4 garter
for z in range(numsamples):

    for i in range(int(samplelength/8)):
        k.speedNumber(100)
        k.rollerAdvance(0)
        k.stitchNumber(2)
        ribbing.rib2ribXferNoRoller(k, [1], [0], width)

        k.speedNumber(400)
        k.stitchNumber(4)
        k.rollerAdvance(400)
        jersey.jerseyKnit(k, width, 4, mainSampleYarn,'l','f')

        k.speedNumber(100)
        k.rollerAdvance(0)
        k.stitchNumber(2)
        ribbing.rib2ribXferNoRoller(k, [0], [1], width)

        k.speedNumber(400)
        k.stitchNumber(4)
        k.rollerAdvance(400)
        jersey.jerseyKnit(k, width, 4, mainSampleYarn,'l','b')

    k.speedNumber(400)
    k.stitchNumber(4)
    k.rollerAdvance(400)
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)

    counter=counter+1



#3x1 miss array
for z in range(numsamples):

    k.speedNumber(100)
    k.rollerAdvance(0)
    k.stitchNumber(2)
    ribbing.rib2ribXfer(k, [1], [0], width)


    k.speedNumber(400)
    k.stitchNumber(4)
    k.rollerAdvance(400)
    fairIsleStiffFxn.missArray(k,3,1,0,width,int(samplelength*4),mainSampleYarn)

    k.speedNumber(400)
    k.rollerAdvance(400)
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)

    counter=counter+1

#4x1 miss array
for z in range(numsamples):

    k.speedNumber(100)
    k.rollerAdvance(0)
    k.stitchNumber(2)
    ribbing.rib2ribXfer(k, [1], [0], width)


    k.speedNumber(400)
    k.stitchNumber(4)
    k.rollerAdvance(400)
    fairIsleStiffFxn.missArray(k,4,1,0,width,int(samplelength*5),mainSampleYarn)

    k.speedNumber(400)
    k.rollerAdvance(400)
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)

    counter=counter+1

#5x1 miss array
for z in range(numsamples):

    k.speedNumber(100)
    k.rollerAdvance(0)
    k.stitchNumber(2)
    ribbing.rib2ribXfer(k, [1], [0], width)


    k.speedNumber(400)
    k.stitchNumber(4)
    k.rollerAdvance(400)
    fairIsleStiffFxn.missArray(k,5,1,0,width,int(samplelength*6),mainSampleYarn)

    k.speedNumber(400)
    k.rollerAdvance(400)
    k.stitchNumber(tabStitchsize)
    sensorSamples.maketabs(k,width,counter,c2,tablength)

    counter=counter+1









'''sample 1'''
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


''' Sample 2'''
# #seed structure
# for z in range(numsamples):
#
#     k.speedNumber(400)
#     k.rollerAdvance(400)
#     k.stitchNumber(4)
#     ribbing.seed(k, 0, width, samplelength, mainSampleYarn)
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#
# #Interlock 400 roller
# for z in range(numsamples):
#     k.speedNumber(400)
#     k.rollerAdvance(400)
#     k.stitchNumber(4)
#     castonbindoff.interlockRange(k, 0, width, samplelength, mainSampleYarn)
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#     counter=counter+1
# #

'''Sample 3'''
#
# #missing every other stitch Jersey
# for z in range(numsamples):
#
#     k.speedNumber(100)
#     k.stitchNumber(2)
#     k.rollerAdvance(0)
#     ribbing.rib2ribXfer(k, [1], [0], width)
#
#     jersey.jerseyArraySkipTransferSide(k,width,[1,0])
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     jersey.jerseyArraySkip(k,0,width-1,samplelength,mainSampleYarn,[1,0])
#
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#

'''Sample 4'''
#
#
# #gerter
# for z in range(numsamples):
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     garter.garterKnit(k, 0, width,samplelength,mainSampleYarn,'l',4,400,400)
#
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#

'''#### Not yet inlcudded#####'''
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

#not yet added
# #inlay on seed
# inlayside='l'
# for z in range(numsamples):
#     k.speedNumber(100)
#     k.rollerAdvance(0)
#     k.stitchNumber(2)
#     ribbing.xfertorib(k,[0,1],int(width/2))
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     inlay.inlaySeed(k,0,width,samplelength,mainSampleYarn,secondYarn,inlayside)
#
#     k.speedNumber(400)
#     k.rollerAdvance(400)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1
#     if inlayside=='l':
#         inlayside='r'
#     else:
#         inlayside='l'
# for z in range(numsamples):
#
#     k.speedNumber(100)
#     k.stitchNumber(2)
#     k.rollerAdvance(0)
#     ribbing.rib2ribXfer(k, [1,1], [1,0], width)
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     for k in range(samplelength):
#         ribbing.ribKnit(k, [1,0], int(width/2), 1 ,mainSampleYarn,'l')
#
#
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1


# #inlay on 1x1 rib
# for z in range(numsamples):
#     k.speedNumber(100)
#     k.rollerAdvance(0)
#     k.stitchNumber(2)
#     ribbing.xfertorib(k,[0,1],int(width/2))
#
#     inlay.inlayKnit(k,0,width,samplelength,mainSampleYarn,secondYarn)
#
#     k.speedNumber(400)
#     k.stitchNumber(4)
#     k.rollerAdvance(400)
#     k.stitchNumber(tabStitchsize)
#     sensorSamples.maketabs(k,width,counter,c2,tablength)
#
#     counter=counter+1




for s in range(width):
    k.drop(('f',s))
for s in range(width):
    k.drop(('b',s))


k.outgripper(c1)
k.outgripper(c2)
k.outgripper(mainSampleYarn)



k.write('structureSampler5.k')
