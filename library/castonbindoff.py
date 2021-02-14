# import library.knitout as knitout

'''Functions to knit a section. Can be stacked.
   Should always end with the carriage and yarn feeder on the left
   However, "side" tells us what side the carriage (and yarn feeder) is on at the beginning'''

def catchyarns(k,width,carriers):
    k.rack(0)
    for i,c in enumerate(carriers):
        for h in range(1,5):
            if h%2 ==1:
                # k.knit('+',('f',i),c)
                for s in range(width-i):
                    if s%10 == 0:
                        k.knit('+',('f',s+i),c)
                    elif s%10 == 5:
                        k.knit('+',('b',s+i),c)
            else:
                for s in range(width-i-1,-1,-1):
                    if s%10 == 0:
                        k.knit('-',('b',s+i),c)
                    elif s%10 == 5:
                        k.knit('-',('f',s+i),c)
                # k.knit('-',('b',i+1),c)
        if i !=0:
            k.miss('-',('f',0),c) #moves carriers to the edge, maybe not necessary?

def interlock(k,width,length,c,side='l'):
    k.rack(0)
    k.rollerAdvance(300)
    if side == 'r':
        for s in range(width-1,-1,-1):
            if s%2 == 0:
                k.knit('-',('f',s),c)
            else:
                k.knit('-',('b',s),c)

    for h in range(length*2):
        if h%2 ==1:
            for s in range(width-1,-1,-1):
                if s%2 == 0:
                    k.knit('-',('f',s),c)
                else:
                    k.knit('-',('b',s),c)
        else:
            for s in range(width):
                if s%2 == 1:
                    k.knit('+',('f',s),c)
                else:
                    k.knit('+',('b',s),c)

def interlockRange(k,start,end,length,c,side='l'):

    if side == 'r':
        for s in range(end-1,start-1,-1):
            if s%2 == 0:
                k.knit('-',('f',s),c)
            else:
                k.knit('-',('b',s),c)

    for h in range(length*2):
        if h%2 ==1:
            for s in range(end-1,start-1,-1):
                if s%2 == 0:
                    k.knit('-',('f',s),c)
                else:
                    k.knit('-',('b',s),c)
        else:
            for s in range(start,end):
                if s%2 == 1:
                    k.knit('+',('f',s),c)
                else:
                    k.knit('+',('b',s),c)

def circular(k,width,length,c,side='l'):
    k.rack(0)
    k.rollerAdvance(300)
    if side == 'r':
        for s in range(width-1,-1,-1):
            k.knit('-',('f',s),c)

    for h in range(int(length*2)):
        if h%2 ==1:
            for s in range(width-1,-1,-1):
                k.knit('-',('f',s),c)
        else:
            for s in range(width):
                k.knit('+',('b',s),c)

# cast on every needle
def caston(k,width,carriers):
    #carriers is a list like ['1','2','3']
    k.speedNumber(200)
    catchyarns(k,width,carriers)
    # draw,waste,main, = carriers
    #Move draw thread to the right side.
    for s in range(width):
        k.knit('+',('f',s),carriers[0])

    # k.rack(0.25)
    # for s in range(1,width+1):
    #     k.knit('+',('f',s),waste)
    #     k.knit('+',('b',s),waste)
    #interlock / waste yarn
    k.speedNumber(400)
    interlock(k,width,36,carriers[1],'l')
    #circular / waste Yarn
    circular(k,width,4,carriers[1],'l')

    for s in range(width):
        k.drop(('b',s))

    for s in range(width-1,-1,-1):
        k.knit('-',('f',s),carriers[0])

    #Cast on main yarn!
    k.rack(0.25)
    for s in range(width):
        k.knit('+',('f',s),carriers[2])
        k.knit('+',('b',s),carriers[2])
    circular(k,width,1,carriers[2],'r')

''' Bind off function - note from now only goes from left to right
and doesn't correct if  yarn in wrong place'''

def bindoff(k, start,width,c,side='l',onfront=1):

    k.rack(0)

    #prob not always needed.. unsure if I should reduce roller
    if onfront:
        for z in range(width):
            k.xfer(('f',z),('b',z))

    k.rollerAdvance(50)
    k.addRollerAdvance(-50)

    #first stitches start
    k.tuck('-',('b',start-1),c)
    k.knit('+',('b',start),c)
    k.xfer(('b',start)),('f',start))
    k.rack(-1)
    k.xfer(('f',start)),('b',start+1))
    k.rack(0)
    k.knit('+',('b',start+1),c)

    k.tuck('-',('b',start),c)
    k.drop('b',0)
    k.xfer(('b',start+1)),('f',start+1))
    k.rack(-1)
    k.xfer(('f',start+1)),('b',start+2))
    k.rack(0)
    k.addRollerAdvance(-50)
    k.drop('b',start)
    k.knit('+',('b',start+2),c)


    for s in range(start+2,width):

        k.tuck('-',('b',s-1),c)
        k.xfer(('b',s),('f',s))
        k.rack(-1)
        k.xfer(('f',s),('b',s+1))
        k.rack(0)
        k.addRollerAdvance(-50)
        k.drop('b',s-1)
        k.knit('+',('b',s+1),c)

    #make the chain
    k.rollerAdvance(200)
    for m in range(8):
        k.miss('+',('b',s+1),c)
        k.knit('-',('b',s),c)
        k.miss('-',('b',-1),c)
        k.knit('+',('b',s),c)

    #drop the last stitch
    k.addRollerAdvance(200)
    k.drop('b',s)
