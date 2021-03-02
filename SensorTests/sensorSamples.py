from library.castonbindoff import *

'''Makes an edge with a draw thread of tablength in length'''
def maketabs(k,width,counter,c,tablength=30,draw='1',side='l'):

    interlock(k,width,tablength,c,side)

    circular(k,width,4,c,'l')

    for s in range(width):
        k.drop(('b',s))

    if counter%2!=1:
        for s in range(width):
            k.knit('+',('f',s),draw)
        k.miss('+',('f',s+5),draw) #move draw thread outta the way

    else:
        for s in range(width-1,-1,-1):
            k.knit('-',('f',s),draw)
        k.miss('-',('f',s-5),draw) #move draw thread outta the way

    #Cast on main yarn!
    k.rack(0.25)

    for s in range(width):
        k.knit('+',('f',s),c)
        k.knit('+',('b',s),c)


    circular(k,width,1,c,'r')

    interlock(k,width,tablength,c,'l')
