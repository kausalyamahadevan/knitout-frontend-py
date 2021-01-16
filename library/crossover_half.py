
#crossoverHalf_function
def crossoverHalf(k,width,length,c,side):

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
            k.speedNumber(400)
            k.rollerAdvance(400)
            #knit all stitches
            for w in range(0,width):
                k.knit('+',('f',w),c)


            k.speedNumber(100)
            k.rollerAdvance(50)
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
            k.speedNumber(400)
            k.rollerAdvance(400)
            for w in range(width-1,-1,-1):
                k.knit('-',('f',w),c)
