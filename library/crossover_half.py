

def crossoverHalf(k,width,length,c,side):

    #easy changeout for roller and speed params
    transferspeed=75
    transferroller=0
    jerseyspeed=400
    jerseyroller=400

    #make sure all stitches on front to start
    k.rollerAdvance(transferroller)
    k.speedNumber(transferspeed)
    for w in range(width):
        k.xfer(('b',w),('f',w))

    #account for starting position
    if side == 'l':
        start=1
    else:
        start=2
        length=length+1 #make sure we still get the full amount of passes desired

    for z in range(start,length+1):


        if z%2==1:
            k.stitchNumber(7)
            k.speedNumber(jerseyspeed)
            k.rollerAdvance(jerseyroller-100)
            #knit all stitches
            for w in range(0,width):
                k.knit('+',('f',w),c)


            k.speedNumber(transferspeed)
            k.rollerAdvance(transferroller)
            k.rack(0)
            #transfer all stitches to back
            for w in range(1,width-1):
                k.xfer(('f',w),('b',w))

            #rack +1 and transfer every other stitch
            k.rack(1)
            for w in range(1,width-1):
                if w%2==1:
                    k.xfer(('b',w),('f',w+1))

            # rack -1 and transfer
            k.rack(-1)
            for w in range(1,width-1):
                if w%2!=1:
                    k.xfer(('b',w),('f',w-1))


        else:
            k.speedNumber(jerseyspeed)
            k.rollerAdvance(jerseyroller)
            k.stitchNumber(5)
            for w in range(width-1,-1,-1):
                k.knit('-',('f',w),c)
