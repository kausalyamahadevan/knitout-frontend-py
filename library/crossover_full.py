
# crossover portion of the code
def crossoverFull(k,width,length,c,side):

    #account for starting position and add first row of knitting
    if side == 'l':
        for w in range (width):
            k.knit('+',('f',w),c)
        start=2
        length=length+1 #make sure we still get the full amount of passes desired


    else:
        for w in range(width-1,-1,-1):
            k.knit('-',('f',w),c)

        start=1


    for z in range(start,length+1):

        if z%2==1:

            #knit all stitches
            for w in range(width):
                k.knit('+',('f',w),c)

            #transfer all stitches to back
            for w in range(width):
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
                    k.xfer(('b',w),('f',w+1))


        else:
            for w in range(width-1,-1,-1):
                k.knit('-',('f',w),c)

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
            for w in range(width,0,-1):
                if w%2!=1:
                    k.xfer(('b',w),('f',w-1))

    # make sure last line is knitting
    if length%2==1:
        for w in range (width):
            k.knit('+',('f',w),c)

    else:
        for w in range(width-1-1,-1):
            k.knit('-',('f',w),c)
