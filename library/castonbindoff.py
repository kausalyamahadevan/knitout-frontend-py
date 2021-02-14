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
    k.rack(0)
    k.rollerAdvance(300)
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
