import knitout
import numpy as np

xsize = 5
'''Functions to knit a section. Can be stacked.
   Should always end with the carriage and yarn feeder on the left
   However, "side" tells us what side the carriage (and yarn feeder) is on at the beginning'''

def catchyarns(width,carriers):
    k.rack(0)
    for c in carriers:
        for h in range(1,7):
            if h%2 ==0:
                for s in range(1,width+1):
                    if s%8 == 0:
                        k.tuck('+',('f',s),c)
                    elif s%8 == 4:
                        k.tuck('+',('b',s),c)
            else:
                for s in range(1,width+1):
                    if s%8 == 0:
                        k.tuck('-',('b',s),c)
                    elif s%8 == 4:
                        k.tuck('-',('f',s),c)
            k.miss('+',('f',width),c) #moves carriers to the edge, maybe not necessary?

def interlock(width,length,c,side):
    k.rack(0)
    k.rollerAdvance(150)
    if side == 'r':
        for s in range(width,0,-1):
            if s%2 == 0:
                k.knit('-',('f',s),c)
            else:
                k.knit('-',('b',s),c)

    for h in range(1,length*2):
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

def circular(width,length,c,side):
    k.rack(0)
    k.rollerAdvance(150)
    if side == 'r':
        for s in range(width,0,-1):
            k.knit('-',('f',s),c)

    for h in range(1,length*2):
        if h%2 ==0:
            for s in range(width,0,-1):
                k.knit('-',('f',s),c)
        else:
            for s in range(1,width+1):
                k.knit('+',('b',s),c)

k = knitout.Writer('1 2 3 4 5 6')

k.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'
k.ingripper(waste)
k.ingripper(draw)
k.ingripper(main)

# cast on every needle
catchyarns(xsize,['1','2','3'])
#Move draw thread to the right side.
for s in range(1,xsize+1):
    k.knit('+',('f',s),draw)

k.rack(0.5)
for s in range(1,xsize+1):
    k.knit('+',('f',s),waste)
    k.knit('+',('b',s),waste)


#interlock / waste yarn
interlock(xsize,16,waste,'r')
#circular / waste Yarn
circular(xsize,4,waste,'r')

for s in range(1,xsize+1):
    k.drop(('b',s))

for s in range(xsize,0,-1):
    k.knit('-',('f',s),draw)

#Case on main yarn!
k.rack(0.5)
for s in range(1,xsize+1):
    k.knit('+',('f',s),main)
    k.knit('+',('b',s),main)

k.write('caston.k')
