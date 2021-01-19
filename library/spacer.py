def spacerFabric(k,width,length,cfront,cback,cmiddle, frontsize = 4,backsize = 4,tucksize = 2):
    for h in range(length):
        if h%2 ==1:
            k.stitchNumber(frontsize)
            for s in range(width-1,-1,-1):
                k.knit('-',('f',s),cfront)
            k.stitchNumber(backsize)
            for s in range(width-1,-1,-1):
                k.knit('-',('b',s),cback)
            k.stitchNumber(tucksize)
            for s in range(width-1,-1,-1):
                if s%2 ==0:
                    k.tuck('-',('b',s),cmiddle)
                else:
                    k.tuck('-',('f',s),cmiddle)
        else:
            k.stitchNumber(frontsize)
            for s in range(width):
                k.knit('+',('f',s),cfront)
            k.stitchNumber(backsize)
            for s in range(width):
                k.knit('+',('b',s),cback)
            k.stitchNumber(tucksize)
            for s in range(width):
                if s%2 ==1:
                    k.tuck('+',('b',s),cmiddle)
                else:
                    k.tuck('+',('f',s),cmiddle)
