
# crossover portion of the code
def crossoverFull(k,width,length,c,side):

    #easy changeout for roller and speed params
    transferspeed=100
    transferroller=50
    jerseyspeed=400
    jerseyroller=400

    #make sure all stitches on front to start
    k.speedNumber(transferspeed)
    for w in range(width):
        k.xfer(('b',w),('f',w))


    k.speedNumber(jerseyspeed)
    k.rollerAdvance(jerseyroller)
    #account for starting position and add first row of knitting
    if side == 'l':
        for w in range (width):
            k.knit('+',('f',w),c)
        start=2

    else:
        for w in range(width-1,-1,-1):
            k.knit('-',('f',w),c)

        start=3
        length=length+1 #make sure we still get the full amount of passes desired


    for z in range(start,length+1):

        k.speedNumber(jerseyspeed)
        k.rollerAdvance(jerseyroller)
        k.rack(0)
        if z%2==1:


            #knit all stitches
            for w in range(width):
                k.knit('+',('f',w),c)

            #transfers section
            k.speedNumber(transferspeed)
            k.rollerAdvance(transferroller)
            #transfer all stitches to back
            for w in range(1,width-1):
                k.xfer(('f',w),('b',w))

            #rack +1 and transfer every other stitch
            k.rack(1)
            for w in range(1,width-1):
                if w%2==1:
                    k.xfer(('b',w),('f',w+1))

            #rack -1 and transfer
            k.rack(-1)
            for w in range(1,width-1):
                if w%2!=1:
                    k.xfer(('b',w),('f',w-1))


        else:

            #knits section
            for w in range(width-1,-1,-1):
                k.knit('-',('f',w),c)

            #transfers section
            k.speedNumber(transferspeed)
            k.rollerAdvance(transferroller)
            #transfer all stitches to back
            for w in range(width-2,0,-1):
                k.xfer(('f',w),('b',w))

            #rack +1 and transfer every other stitch
            k.rack(1)
            for w in range(width-2,0,-1):
                if w%2==1:
                    k.xfer(('b',w),('f',w+1))

            #rack -1 and transfer
            k.rack(-1)
            for w in range(width-2,0,-1):
                if w%2!=1:
                    k.xfer(('b',w),('f',w-1))


    k.rack(0)
    k.speedNumber(jerseyspeed)
    k.rollerAdvance(jerseyroller)
    # make sure last line is knitting
    if length%2==1:
        for w in range (width):
            k.knit('+',('f',w),c)

    else:
        for w in range(width-1-1,-1):
            k.knit('-',('f',w),c)
