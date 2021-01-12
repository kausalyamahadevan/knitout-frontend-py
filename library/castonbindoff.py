import knitout
import numpy as np

'''Functions to knit a section. Can be stacked.
   Should always end with the carriage and yarn feeder on the left
   However, "side" tells us what side the carriage (and yarn feeder) is on at the beginning'''

def catchyarns(k,width,carriers):
    k.rack(0)
    for i,c in enumerate(carriers):
        for h in range(1,5):
            if h%2 ==1:
                k.knit('+',('f',i+1),c)
                for s in range(1,width+1-i):
                    if s%8 == 0:
                        k.knit('+',('f',s+i),c)
                    elif s%8 == 4:
                        k.knit('+',('b',s+i),c)
            else:
                for s in range(width-i,0,-1):
                    if s%8 == 0:
                        k.knit('-',('b',s+i),c)
                    elif s%8 == 4:
                        k.knit('-',('f',s+i),c)
                k.knit('-',('b',i+1),c)
            if i !=0:
                k.miss('-',('f',1),c) #moves carriers to the edge, maybe not necessary?

def interlock(k,width,length,c,side):
    k.rack(0)
    k.rollerAdvance(200)
    if side == 'r':
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),c)
            else:
                k.knit('-',('b',s),c)

    for h in range(1,length*2+1):
        if h%2 ==0:
            for s in range(width,0,-1):
                if s%2 == 0:
                    k.knit('-',('f',s),c)
                else:
                    k.knit('-',('b',s),c)
        else:
            for s in range(1,width+1):
                if s%2 == 1:
                    k.knit('+',('f',s),c)
                else:
                    k.knit('+',('b',s),c)

def circular(k,width,length,c,side):
    k.rack(0)
    k.rollerAdvance(200)
    if side == 'r':
        for s in range(width,0,-1):
            k.knit('-',('f',s),c)

    for h in range(1,int(length*2+1)):
        if h%2 ==0:
            for s in range(width,0,-1):
                k.knit('-',('f',s),c)
        else:
            for s in range(1,width+1):
                k.knit('+',('b',s),c)

# cast on every needle
def caston(k,width,carriers):
    #carriers is a list like ['1','2','3']
    k.speedNumber(200)
    catchyarns(k,width,carriers)
    draw,waste,main = carriers
    #Move draw thread to the right side.
    for s in range(1,width+1):
        k.knit('+',('f',s),draw)

    # k.rack(0.25)
    # for s in range(1,width+1):
    #     k.knit('+',('f',s),waste)
    #     k.knit('+',('b',s),waste)
    #interlock / waste yarn
    k.speedNumber(400)
    interlock(k,width,36,waste,'l')
    #circular / waste Yarn
    circular(k,width,4,waste,'l')

    for s in range(1,width+1):
        k.drop(('b',s))

    for s in range(width,0,-1):
        k.knit('-',('f',s),draw)

    #Cast on main yarn!
    k.rack(0.25)
    for s in range(1,width+1):
        k.knit('+',('f',s),main)
        k.knit('+',('b',s),main)
    circular(k,width,0.5,main,'r')