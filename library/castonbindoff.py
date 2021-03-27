# import library.knitout as knitout

'''Functions to knit a section. Can be stacked.
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
    '''Knits an every needle interlock designated side.
    In this function length is the number of total courses knit so if you want an interlock segment
    is 20 courses long on each side set length to 20.
    k is knitout Writer
    width is width of tube (same on both sides)
    length is total courses knit
    c is carrier
    side is starting position of carraige'''
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
    '''Knits an every needle interlock designated side at designated needle range.
    In this function length is the number of total passes knit so if you want an interlock segment
    is 20 courses long on each side set length to 40. Useful if you want to have odd amounts of interlock.
    k is knitout Writer
    start is the starting needle to knit on
    end is the needle after the last needle to knit on
    length is total passes knit
    c is carrier
    side is starting position of carraige'''
    if side == 'l':
        beg=0

    else:
        beg=1
        length=length+1

    for h in range(beg,length*2):
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

def interlockRangeHalved(k,start,end,length,c,side='l'):
    '''Knits an every needle interlock designated side.
    In this function length is the number of total passes knit so if you want an interlock segment
    is 20 courses long on each side set length to 40. Useful if you want to have odd amounts of interlock.
    k is knitout Writer
    width is width of tube (same on both sides)
    length is total passes knit
    c is carrier
    side is starting position of carraige'''

    if side == 'l':
        beg=0

    else:
        beg=1
        length=length+1

    for h in range(beg,length):
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
    '''Knits an every needle circular tube starting on designated side.
    In this function length is the number of total passes knit so if you want a tube that
    is 20 courses long on each side set length to 40.
    k is knitout Writer
    width is width of tube (same on both sides)
    length is total passes knit
    c is carrier
    side is starting position of carraige'''
    k.rack(0)
    k.rollerAdvance(500)
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    for h in range(start,length):
        if h%2 ==0:
            for s in range(width):
                k.knit('+',('b',s),c)
        else:
            for s in range(width-1,-1,-1):
                k.knit('-',('f',s),c)

def circularEON(k,width,length,c,side='l'):
    '''Knits an every needle circular tube starting on designated side.
    In this function length is the number of total passes knit so if you want a tube that
    is 20 courses long on each side set length to 40.
    k is knitout Writer
    width is width of tube (same on both sides)
    length is total passes knit
    c is carrier
    side is starting position of carraige'''
    k.rack(0)
    k.rollerAdvance(500)
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    for h in range(start,length):
        if h%2 ==0:
            for s in range(width):
                if s%2==0:
                    k.knit('+',('b',s),c)
                else:
                    k.miss('+',('b',s),c)
        else:
            for s in range(width-1,-1,-1):
                if s%2==0:
                    k.miss('-',('f',s),c)
                else:
                    k.knit('-',('f',s),c)

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
    circular(k,width,8,carriers[1],'l')

    for s in range(width):
        k.drop(('b',s))

    for s in range(width-1,-1,-1):
        k.knit('-',('f',s),carriers[0])

    #Cast on main yarn!
    k.rack(0.25)
    for s in range(width):
        k.knit('+',('f',s),carriers[2])
        k.knit('+',('b',s),carriers[2])
    circular(k,width,3,carriers[2],'r')


def bindoff(k, start,width,c,side='l',onfront=1):

    k.rack(0)

    #prob not always needed.. unsure if I should reduce roller
    if onfront:
        for z in range(width):
            k.xfer(('f',z),('b',z))

    k.rollerAdvance(50)
    k.addRollerAdvance(-50)

    if side=='l':
        #first stitches start
        k.tuck('-',('b',start-1),c)
        k.knit('+',('b',start),c)
        k.xfer(('b',start),('f',start))
        k.rack(-1)
        k.xfer(('f',start),('b',start+1))
        k.rack(0)
        k.knit('+',('b',start+1),c)

        k.tuck('-',('b',start),c)
        k.drop('b',start-1)
        k.xfer(('b',start+1),('f',start+1))
        k.rack(-1)
        k.xfer(('f',start+1),('b',start+2))
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
            k.miss('-',('b',s-1),c)
            k.knit('+',('b',s),c)

        #drop the last stitch
        k.addRollerAdvance(200)
        k.drop('b',s)

    else:
        k.tuck('+',('b',width),c)
        k.knit('-',('b',width-1),c)
        k.xfer(('b',width-1),('f',width-1))
        k.rack(1)
        k.xfer(('f',width-1),('b',width-2))
        k.rack(0)
        k.knit('-',('b',width-2),c)

        k.tuck('+',('b',width-1),c)
        k.drop('b',width)
        k.xfer(('b',width-2),('f',width-2))
        k.rack(1)
        k.xfer(('f',width-2),('b',width-3))
        k.rack(0)
        k.addRollerAdvance(-50)
        k.drop('b',width-1)
        k.knit('-',('b',width-3),c)


        for s in range(width-3,-1,-1):

            k.tuck('+',('b',s+1),c)
            k.xfer(('b',s),('f',s))
            k.rack(1)
            k.xfer(('f',s),('b',s-1))
            k.rack(0)
            k.addRollerAdvance(-50)
            k.drop('b',s+1)
            k.knit('-',('b',s-1),c)

        print(s)

        #make the chain
        k.rollerAdvance(200)
        for m in range(8):
            k.miss('-',('b',s-1),c)
            k.knit('+',('b',s),c)
            k.miss('+',('b',s+1),c)
            k.knit('-',('b',s),c)


        #drop the last stitch
        k.addRollerAdvance(200)
        k.drop(('b',s))

# cast on every needle
def castonmiddle(k,width,carriers,knitsize = 4):
    #carriers is a list like ['1','2','3']
    # draw,waste,main, = carriers

    k.speedNumber(400)
    interlock(k,width,24,carriers[1],'l')
    #circular / waste Yarn
    circular(k,width,8,carriers[1],'l')

    k.speedNumber(200)
    for s in range(width):
        k.xfer(('b',s),('f',s))
    k.speedNumber(400)
    # for s in range(width-1,-1,-1):
    #     k.knit('-',('f',s),carriers[0])
    for s in range(width):
        k.knit('+',('f',s),carriers[0])
    #Cast on main yarn!
    k.rack(0.25)
    k.stitchNumber(knitsize)
    for s in range(width):
        k.knit('+',('f',s),carriers[2])
        k.knit('+',('b',s),carriers[2])
    circular(k,width,3,carriers[2],'r')

def scrapoff(k,width,carriers,side = 'l'):
    #carriers is a list like ['1','2','3']
    # draw,waste,main, = carriers
    k.speedNumber(400)
    circular(k,width,2,carriers[0],side)
    for i,c in enumerate(carriers):
        if i!=1:
            k.outgripper(c)
    if side =='r':
        h = 37
    else:
        h = 36
    interlock(k,width,h,carriers[1],side)
    #circular / waste Yarn
    for s in range(width):
        k.drop(('f',s))
    for s in range(width-1,-1,-1):
        k.drop(('b',s))
    k.outgripper(carriers[1])

def scrapoffmiddle(k,width,carriers,side = 'l'):
    #carriers is a list like ['1','2','3']
    # draw,waste,main, = carriers
    k.speedNumber(200)
    for s in range(width):
        k.xfer(('b',s),('f',s))
    k.speedNumber(400)
    circular(k,width,1,carriers[0],'r')

    if side =='r':
        h = 25
    else:
        h = 24
    interlock(k,width,h,carriers[1],side)

# cast on every needle
def startnowaste(k,width,carriers):
    #carriers is a list like ['1','2','3']
    k.speedNumber(200)
    catchyarns(k,width,carriers)
    # draw,waste,main, = carriers

    k.speedNumber(400)
    interlock(k,width,8,carriers[1],'l')

def dropeverything(k,width,carriers):
    for i,c in enumerate(carriers):
            k.outgripper(c)
    for s in range(width):
        k.drop(('f',s))
    for s in range(width-1,-1,-1):
        k.drop(('b',s))
