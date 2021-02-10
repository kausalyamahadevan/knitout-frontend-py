

def interlocktwoColorMix(k,width,length,c1,c2,side='l'):
    k.rack(0)
    k.rollerAdvance(300)


    if side == 'l':
        start=2
        length=length+1

    else:
        start=1

    for h in range(start, length+1):

        if h%2 ==1:
            for s in range(width-1,-1,-1):
                if s%2 == 0:
                    k.knit('-',('f',s),c1)
                else:
                    k.knit('-',('b',s),c1)

            for s in range(width-1,-1,-1):
                if s%2 == 0:
                    k.knit('-',('b',s),c2)
                else:
                    k.knit('-',('f',s),c2)

        else:
            for s in range(width):
                if s%2 == 1:
                    k.knit('+',('f',s),c1)
                else:
                    k.knit('+',('b',s),c1)

            for s in range(width):
                if s%2 == 1:
                    k.knit('+',('b',s),c2)
                else:
                    k.knit('+',('f',s),c2)


def interlocktwoColorStriped(k,width,length,c1,c2,side='l'):
    k.rack(0)
    k.rollerAdvance(300)


    if side == 'l':
        start=2
        length=length+1

    else:
        start=1

    for h in range(start, length+1):

        if h%2 ==1:
            for s in range(width-1,-1,-1):
                if s%2 == 0:
                    k.knit('-',('f',s),c1)
                else:
                    k.knit('-',('b',s),c1)

            for s in range(width-1,-1,-1):
                if s%2 == 0:
                    k.knit('-',('b',s),c2)
                else:
                    k.knit('-',('f',s),c2)

        else:
            for s in range(width):
                if s%2 == 1:
                    k.knit('+',('b',s),c1)
                else:
                    k.knit('+',('f',s),c1)

            for s in range(width):
                if s%2 == 1:
                    k.knit('+',('f',s),c2)
                else:
                    k.knit('+',('b',s),c2)
