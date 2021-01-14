
#crossoverHalf_function
def crossoverHalf(k,width,length,c,side):

    #account for starting position
    if side == 'l':
        start=1
    else:
        start=2
        length=length+1 #make sure we still get the full amount of passes desired

    for z in range(start,length+1):

        if z%2==1:

            #knit all stitches
            for w in range(1,width+1):
                k.knit('+',('f',w-1),c)

            #transfer all stitches to back
            for w in range(1,width+1):
                k.xfer(('f',w-1),('b',w-1))

            #rack +1 and transfer every other stitch
            k.rack(1)
            for w in range(1,width+1):
                if w%2==1:
                    k.xfer(('b',w-1),('f',w))

            #rack -1 and transfer
            k.rack(-1)
            for w in range(1,width+1):
                if w%2!=1:
                    k.xfer(('b',w-1),('f',w-2))


        else:
            for w in range(width,0,-1):
                k.knit('-',('f',w-1),c)


k.write('across.k')
