def garterKnit(k,beg,end,length,c,side='l',stitchsize=4,roller=400,speed=400):
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    for b in range(start,length+1):
        if b%2==1:

            k.stitchNumber(2)
            k.rollerAdvance(0)
            k.speedNumber(100)

            for w in range(beg,end):
                k.xfer(('b',w),('f',w))

            k.stitchNumber(stitchsize)
            k.rollerAdvance(roller)
            k.speedNumber(speed)
            for w in range(beg,end):
                k.knit('+',('f',w),c)

        else:
            k.stitchNumber(2)
            k.rollerAdvance(0)
            k.speedNumber(100)

            for w in range(end-1,beg-1,-1):
                k.xfer(('f',w),('b',w))

            k.stitchNumber(stitchsize)
            k.rollerAdvance(roller)
            k.speedNumber(speed)
            for w in range(end-1,beg-1,-1):
                k.knit('-',('b',w),c)
