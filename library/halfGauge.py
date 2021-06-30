import math
import numpy as np


def knitSettings(k,size=4,roll=400,speed=400):
    '''helper to quickly set knit settings'''
    k.speedNumber(speed)
    k.stitchNumber(size)
    k.rollerAdvance(roll)

def xferSettings(k,size=2,roll=0,speed=100):
    '''helper to quickly set knit settings'''
    k.speedNumber(speed)
    k.stitchNumber(size)
    k.rollerAdvance(roll)

def knitSettingsArray(k,specs=[400,4,400]):
    '''helper to quickly set knit settings using an array defined as [stitch size,
    roller advance, speed]"'''
    k.speedNumber(specs[0])
    k.stitchNumber(specs[1])
    k.rollerAdvance(specs[2])

def xferSettingsArray(k,specs=[100,2,0]):
    '''helper to quickly set xfer settings using an array defined as [stitch size,
    roller advance, speed]. knitSettingsArray is the same thing with different
    default values'''
    k.speedNumber(specs[0])
    k.stitchNumber(specs[1])
    k.rollerAdvance(specs[2])



def jersey(k,beg,end,length,c,side='l',bed='f',gauge=1, gstart=0,knitArray=[400,4,400]):
    '''Jersey function to account for different gauge knititng
    k is knitout writer. beg is beginning needle, end is the final needle (**note: no longer 1 after final needle**)
    length is the number of courses knit. c is the carrier,
    side is the position of the carraige in the first row
    bed is the bed that we knit on
    gauge is the gauge, 1 is full needle, 2 is half gauge, 3 is 1/3 gauge and so on
    g start is the offset for the first needle of knitting going from left to right if you want to start after the first needle for some reason'''

    #adjust end here so that it value passed as argument more sense #new
    if end > beg:
        end += 1
    else:
        end -= 1

    #TODO: maybe remove 'side' parameter and just determined based on whether end > beg ?
    #figure out how to count back
    beg=beg+gstart;
    # tot=end-beg
    tot=end-beg + 1 #new
    r=tot%gauge;

    new_end=end-r;

    if r==0:
        new_end=new_end-gauge;


    #account for starting position and add first row of knitting
    if side == 'l':
        start=1

    else:
        start=2
        length=length+1

    knitSettingsArray(k,knitArray)
    for b in range(start,length+1):

        if b%2==1:
            for w in range(beg,end,gauge):
                k.knit('+',(bed,w),c)

        else:
            for w in range(new_end-1,beg-1,-1*gauge):
                k.knit('-',(bed,w),c)



def ribKnit(k,ribarray,beg,end,length,c,side='l',bed1='f',gauge=1,
    gstart=0,knitArray=[400,4,400]):

    #figure out how to count back
    beg=beg+gstart;
    # tot=fin-beg
    tot=end-beg + 1 #new +1
    r=tot%gauge;

    new_end=end-r;

    if r==0:
        new_end=new_end-gauge;

    #set beds for knitting
    if bed1=='f':
        bed0='b'
    else:
        bed0='f'

    repeatSize = len(ribarray)
    totalRepeatsHoriz=int(math.ceil(float(end-beg)/repeatSize))

    ref = np.tile(ribarray,totalRepeatsHoriz+2)

    #account for starting position and add first row of knitting
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    knitSettingsArray(k,knitArray)
    for h in range(start,length):
        if h%2 ==0:
            for s in range(beg,end,gauge):
                if ref[int(s/gauge)] == 1:
                    k.knit('+',(bed1,s),c)
                else:
                    k.knit('+',(bed0,s),c)
        else:
            for s in range(new_end+1,beg-1,-1*gauge):
                if ref[int(s/gauge)] == 1:
                    k.knit('-',(bed1,s),c)
                else:
                    k.knit('-',(bed0,s),c)

def rib2ribXfer(k,ribarray1,ribarray2,start,finish,
    gauge=1,gstart=0,settings=[100,2,0]):
    '''Transfer function for half gauge ribs etc to half or third gauge ribs
    of the same  gauge. Will ignore transferring all non-active needles.'''

    xferSettingsArray(k,settings)
    #add in offset
    start=start+gstart

    ribsize1 = len(ribarray1)
    ribsize2 = len(ribarray2)

    totalRepeatsHoriz1=int(math.ceil(float(finish-start)/ribsize1))
    totalRepeatsHoriz2=int(math.ceil(float(finish-start)/ribsize2))


    ref1 = np.tile(ribarray1,totalRepeatsHoriz1+1)
    ref2 = np.tile(ribarray2,totalRepeatsHoriz2+1)

    #need to make both reference arryas the same length to subrtact
    l1=len(ref1)
    l2=len(ref2)

    if l1>l2:
        diff=l1-l2
        extra=np.zeros((diff,), dtype=int)
        ref2=np.concatenate((ref2, extra), axis=None)

    elif l2>l1:
        diff=l2-l1
        extra=np.zeros((diff,), dtype=int)
        ref1=np.concatenate((ref1, extra), axis=None)



    #figure out transfer
    xferref = ref1-ref2 # 0: do not transfer. 1: back to front -1: front to back


    for s in range(start,finish,gauge):
        if xferref[int(s/gauge)] == -1:
            k.xfer(('b',s),('f',s))
        elif xferref[int(s/gauge)] == 1:
            k.xfer(('f',s),('b',s))




def garterPlain(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1,
    gstart=0,knitArray=[400,4,400],xferArray=[100,2,0]):
    '''Creates a balanced garter knit based on an input number. Bed is starting
    bed of knitting'''

    if bed1=='f':
        array1=[1]
        array2=[0]
        bed2='b'
    else:
        array1=[0]
        array2=[1]
        bed2='f'


    #if garter number is odd then we need to alternate knitting direction after switching
    if (garterNum%2)==1:
        if side1 == 'l':
            side2='r'
        else:
            side2='l'
    else:
        side2=side1

    remainder=length%(2*garterNum);

    fullcycles=math.floor(length/(2*garterNum));

    for i in range(fullcycles):

        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)


        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)


        jersey(k,beg,end,garterNum,c,side2,bed2,gauge, gstart,knitArray)

        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart,xferArray)



    if remainder<garterNum:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,remainder,c,side1,bed1,gauge, gstart,knitArray)



    else:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)


        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)


        jersey(k,beg,end,remainder,c,side2,bed2,gauge, gstart,knitArray)


def garterEdgeProtect(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1,
    gstart=0,knitArray=[400,4,400],xferArray=[100,2,0],edgeprotect=0,offset=0):
    '''Creates a balanced garter knit based on an input number. Bed is starting
    bed of knitting'''

    if bed1=='f':
        array1=[1]
        array2=[0]
        bed2='b'
    else:
        array1=[0]
        array2=[1]
        bed2='f'


    #if garter number is odd then we need to alternate knitting direction after switching
    if (garterNum%2)==1:
        if side1 == 'l':
            side2='r'
        else:
            side2='l'
    else:
        side2=side1

    edgeprotect=int(edgeprotect*gauge)
    remainder=length%(2*garterNum);

    fullcycles=math.floor(length/(2*garterNum));


    for i in range(fullcycles):

        knitSettingsArray(k,knitArray)
        for q in range(garterNum):

            if ((side1=='l') and (q%2==0)) or (side1=='r' and (q%2==1)):
                for w in range(beg,beg+edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(beg+edgeprotect,end-edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(end-edgeprotect,end):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)


            else:
                for w in range(end-1,end-edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(end-edgeprotect-1,beg+edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(beg+edgeprotect-1,beg-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)


        #transfer to other bed
        xferSettingsArray(k,xferArray)
        for m in range(beg+edgeprotect,end-edgeprotect):
            if m%2==offset:
                k.xfer((bed1,m),(bed2,m))

        knitSettingsArray(k,knitArray)
        for q in range(garterNum):

            if ((side2=='l') and (q%2==0)) or (side2=='r' and (q%2==1)):

                for w in range(beg,beg+edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(beg+edgeprotect,end-edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed2,w),c)

                for w in range(end-edgeprotect,end):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)


            else:
                for w in range(end-1,end-edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(end-edgeprotect-1,beg+edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed2,w),c)

                for w in range(beg+edgeprotect-1,beg-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

        #transfer to other bed
        xferSettingsArray(k,xferArray)
        for m in range(beg+edgeprotect,end-edgeprotect):
            if m%2==offset:
                k.xfer((bed2,m),(bed1,m))


    if remainder<garterNum:

        for q in range(remainder):
            if ((side1=='l') and (q%2==0)) or (side1=='r' and (q%2==1)):
                for w in range(beg,beg+edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(beg+edgeprotect,end-edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(end-edgeprotect,end):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)


            else:
                for w in range(end-1,end-edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(end-edgeprotect-1,beg+edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(beg+edgeprotect-1,beg-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)



    else:
        knitSettingsArray(k,knitArray)
        for q in range(garterNum):

            if ((side1=='l') and (q%2==0)) or (side1=='r' and (q%2==1)):

                for w in range(beg,beg+edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(beg+edgeprotect,end-edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(end-edgeprotect,end):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)


            else:
                for w in range(end-1,end-edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(end-edgeprotect-1,beg+edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(beg+edgeprotect-1,beg-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

        #transfer
        xferSettingsArray(k,xferArray)
        for m in range(beg+edgeprotect,end-edgeprotect):
                if m%2==offset:
                    k.xfer((bed1,m),(bed2,m))

        knitSettingsArray(k,knitArray)
        for q in range(remainder):

            if ((side2=='l') and (q%2==0)) or (side2=='r' and (q%2==1)):
                for w in range(beg,beg+edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)

                for w in range(beg+edgeprotect,end-edgeprotect):
                    if w%2==offset:
                        k.knit('+',(bed2,w),c)

                for w in range(end-edgeprotect,end):
                    if w%2==offset:
                        k.knit('+',(bed1,w),c)


            else:
                for w in range(end-1,end-edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

                for w in range(end-edgeprotect-1,beg+edgeprotect-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed2,w),c)

                for w in range(beg+edgeprotect-1,beg-1,-1):
                    if w%2==offset:
                        k.knit('-',(bed1,w),c)

        #transfer to other bed
        xferSettingsArray(k,xferArray)
        for m in range(beg+edgeprotect,end-edgeprotect):
            if m%2==offset:
                k.xfer((bed2,m),(bed1,m))





# def garterEdgeProtect(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1,
#     gstart=0,knitArray=[400,4,400],xferArray=[100,2,0],edgeprotect=0):
#     '''Creates a balanced garter knit based on an input number. Bed is starting
#     bed of knitting'''
#
#     if bed1=='f':
#         array1=[1]
#         array2=[0]
#         bed2='b'
#     else:
#         array1=[0]
#         array2=[1]
#         bed2='f'
#
#
#     #if garter number is odd then we need to alternate knitting direction after switching
#     if (garterNum%2)==1:
#         if side1 == 'l':
#             side2='r'
#         else:
#             side2='l'
#     else:
#         side2=side1
#
#     remainder=length%(2*garterNum);
#
#     fullcycles=math.floor(length/(2*garterNum));
#
#     for i in range(fullcycles):
#
#         # jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)
#
#         for m in range(garterNum):
#             if (side1=='l'and garterNum%2==1) or (side1=='r' and garterNum%2==0):
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#             else:
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)
#
#
#         rib2ribXfer(k,array1,array2,beg+edgeprotect,end-edgeprotect,gauge,gstart,xferArray)
#
#
#         for m in range(garterNum):
#             if (side2=='r'and garterNum%2==0) or (side2=='l' and garterNum%2==1):
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#             else:
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)
#
#
#         rib2ribXfer(k,array2,array1,beg+edgeprotect,end-edgeprotect,gauge,gstart,xferArray)
#
#
#
#     if remainder<garterNum:
#         # xferSettingsArray(k,xferArray)
#         # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)
#
#         jersey(k,beg,end,remainder,c,side1,bed1,gauge, gstart,knitArray)
#
#
#
#     else:
#         # xferSettingsArray(k,xferArray)
#         # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)
#
#         jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)
#
#
#         rib2ribXfer(k,array1,array2,beg+edgeprotect,end-edgeprotect,gauge,gstart,xferArray)
#
#         for z in rage(remainder):
#             if (side2=='r'and remainder%2==0) or (side2=='l' and remainder%2==1):
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#             else:
#                 jersey(k,beg,edgeprotect,1,c,side2,bed1,gauge,gstart,knitArray)
#                 jersey(k,beg+edgeprotect,end-edgeprotect,1,c,side2,bed2,gauge, gstart,knitArray)
#                 jersey(k,end-edgeprotect,end,1,c,side2,bed1,gauge,gstart,knitArray)


def garter(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1,
    gstart=0,knitArray=[400,4,400],xferArray=[100,2,0]):
    '''Creates a balanced garter knit based on an input number. Bed is starting
    bed of knitting'''

    if bed1=='f':
        array1=[1]
        array2=[0]
        bed2='b'
    else:
        array1=[0]
        array2=[1]
        bed2='f'

    #if garter number is odd then we need to alternate knitting direction after switching
    if (garterNum%2)==1:
        if side1 == 'l':
            side2='r'
        else:
            side2='l'
    else:
        side2=side1

    remainder=length%(2*garterNum);

    fullcycles=math.floor(length/(2*garterNum));

    for i in range(fullcycles):


        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)

        if side2=='r' and gauge>1:
            k.tuck('+', (bed1,end), c)
            k.tuck('+', (bed2,end+1), c)

        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)

        if side2=='r' and gauge>1:
            k.drop((bed1, end))
            k.drop((bed2, end+1))


        jersey(k,beg,end,garterNum,c,side2,bed2,gauge, gstart,knitArray)


        if side1=='r' and gauge>1:
            k.tuck('+', (bed2,end), c)
            k.tuck('+', (bed1,end+1), c)

        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart,xferArray)

        if side1=='r' and gauge>1:
            k.drop((bed2, end))
            k.drop((bed1, end+1))



    if remainder<garterNum:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,remainder,c,side1,bed1,gauge, gstart,knitArray)



    else:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)

        if side2=='r' and gauge>1:
            k.tuck('+', (bed1,end), c)
            k.tuck('+', (bed2,end+1), c)

        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)

        if side2=='r' and gauge>1:
            k.drop((bed1, end))
            k.drop((bed2, end+1))


        jersey(k,beg,end,remainder,c,side2,bed2,gauge, gstart,knitArray)

def garterSecure(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1,
    gstart=0,knitArray=[400,4,400],xferArray=[100,2,0]):
    '''Creates a balanced garter knit based on an input number. Bed is starting
    bed of knitting'''

    if bed1=='f':
        array1=[1]
        array2=[0]
        bed2='b'
    else:
        array1=[0]
        array2=[1]
        bed2='f'

    #if garter number is odd then we need to alternate knitting direction after switching
    if (garterNum%2)==1:
        if side1 == 'l':
            side2='r'
        else:
            side2='l'
    else:
        side2=side1

    remainder=length%(garterNum);

    fullcycles=math.floor(length/(2*garterNum));

    for i in range(fullcycles):

        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)

        if side1=='r' and gauge>1:
            k.drop((bed2, end))

        if side2=='r' and gauge>1:
            k.tuck('+', (bed1,end), c)
            k.tuck('+', (bed2,end+1), c)

        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)

        if side2=='r' and gauge>1:
            k.drop((bed2, end+1))


        jersey(k,beg,end,garterNum,c,side2,bed2,gauge, gstart,knitArray)

        if side2=='r' and gauge>1:
            k.drop((bed1, end))


        if side1=='r' and gauge>1:
            k.tuck('+', (bed2,end), c)
            k.tuck('+', (bed1,end+1), c)

        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart,xferArray)

        if side1=='r' and gauge>1:
            k.drop((bed1, end+1))



    if remainder<garterNum:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,remainder,c,side1,bed1,gauge, gstart,knitArray)

        if side1=='r' and gauge>1:
            k.drop((bed2, end))



    else:
        # xferSettingsArray(k,xferArray)
        # rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)

        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart,knitArray)

        if side1=='r' and gauge>1:
            k.drop((bed2, end))

        if side2=='r' and gauge>1:
            k.tuck('+', (bed1,end), c)
            k.tuck('+', (bed2,end+1), c)

        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart,xferArray)

        if side2=='r' and gauge>1:
            k.drop((bed2, end+1))

        jersey(k,beg,end,remainder,c,side2,bed2,gauge, gstart,knitArray)

        if side2=='r' and gauge>1:
            k.drop((bed1, end))


def garterArray(k,garterarray,beg,end,length,c,side='l',gauge=1, gstart=0,
    knitArray=[400,4,400],xferArray=[100,2,0]):
    '''Creates a garter that doesn't need to be balanced based on an input array.
    1 is front bed and 0 is back bed in the array.'''

    sz = len(garterarray)
    totalRepeatsvert=int(math.ceil(float(length)/sz))
    ref = np.tile(garterarray,totalRepeatsvert+1)

    xferSettingsArray(k,xferArray)
    if ref[0]==1:
        rib2ribXfer(k,[0],[1],beg,end,gauge,gstart)
    else:
        rib2ribXfer(k,[1],[0],beg,end,gauge,gstart)

    #account for starting position and add first row of knitting
    if side == 'l':
        start=0

    else:
        start=1
        length=length+1
        ref=np.concatenate(([0], ref), axis=None)

    for i in range(start,length):
        knitSettingsArray(k,knitArray)
        if i%2 ==0:
            if ref[i]==1:
                jersey(k,beg,end,1,c,'l','f',gauge, gstart)
            else:
                jersey(k,beg,end,1,c,'l','b',gauge, gstart)
        else:
            if ref[i]==1:
                jersey(k,beg,end,1,c,'r','f',gauge, gstart)
            else:
                jersey(k,beg,end,1,c,'r','b',gauge, gstart)

        xferSettingsArray(k,xferArray)
        if (i+1)<length and ref[i]!=ref[i+1] and ref[i]==1:
            rib2ribXfer(k,[1],[0],beg,end,gauge,gstart)
        elif (i+1)<length and ref[i]!=ref[i+1] and ref[i]==0:
            rib2ribXfer(k,[0],[1],beg,end,gauge,gstart)


def seed(k,beg,end,length,c,side1='l',gauge=1, gstart=0,
    knitArray=[400,4,400],xferArray=[100,2,0]):

    if side1=='l':
        side2='r'
    else:
        side2='l'

    xferSettingsArray(k,xferArray)
    rib2ribXfer(k,[0],[1],beg,end,gauge,gstart)
    rib2ribXfer(k,[1,1],[0,1],beg,end,gauge,gstart)


    for i in range(int(math.floor(length/2))):
        knitSettingsArray(k,knitArray)
        ribKnit(k,[0,1],beg,end,1,c,side1,'f',gauge, gstart)

        xferSettingsArray(k,xferArray)
        rib2ribXfer(k,[0,1],[1,0],beg,end,gauge,gstart)

        knitSettingsArray(k,knitArray)
        ribKnit(k,[1,0],beg,end,1,c,side2,'f',gauge, gstart)

        xferSettingsArray(k,xferArray)
        rib2ribXfer(k,[1,0],[0,1],beg,end,gauge,gstart)

    if length%2==1:
        knitSettingsArray(k,knitArray)
        ribKnit(k,[0,1],beg,end,length,c,side1,'f',gauge, gstart) #TODO: maybe change all 'fin' / 'finish' to 'end' so parameter names are consistent; and 'beginning' to 'beg'


def xferhelper(k,beg,end,gauge,have,receive):
    for s in range(beg,end,gauge):
        k.xfer((have,s),(receive,s))



#not anywhere near done...needz halp
def gaugexfer(k,beg,end,bed='f',gauge=1,gstart=0):

    beg=beg+gstart

    #first get every stitch onto side where we will not knit, aka "obed"
    if bed=='f':
        rib2ribXfer(k,[1],[0],beg,end,1,0)
        obed='b'
        modify=-1;


    else:
        rib2ribXfer(k,[0],[1],beg,end,1,0)
        obed='f'
        modify=1;

    #next transfer every knit stitch back to the bed we will knit on
    xferhelper(k,beg,end,gauge,obed,bed)


    for m in range(gauge):

        if m%2==0:
            k.rack((m+1)*modify)
            xferhelper(k,beg+m+1,end,gauge,obed,bed)

        else:
            k.rack(m*-1*modify)
            xferhelper(k,beg+m,end,gauge,obed,bed)



## eggo
