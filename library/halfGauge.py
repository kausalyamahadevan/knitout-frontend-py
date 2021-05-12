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

def knitSettingsArray(k,specs=[4,400,400]):
    '''helper to quickly set knit settings using an array defined as [stitch size,
    roller advance, speed]"'''
    k.speedNumber(specs[0])
    k.stitchNumber(specs[1])
    k.rollerAdvance(specs[2])

def xferSettingsArray(k,specs=[2,0,100]):
    '''helper to quickly set xfer settings using an array defined as [stitch size,
    roller advance, speed]. knitSettingsArray is the same thing with different
    default values'''
    k.speedNumber(specs[0])
    k.stitchNumber(specs[1])
    k.rollerAdvance(specs[2])



def jersey(k,beg,end,length,c,side='l',bed='f',gauge=1, gstart=0):
    '''Jersey function to account for different gauge knititng
    k is knitout writer. b is beginning needle, end is 1 after the final needl
    lenght is the number of courses knit. c is the carrier,
    side is the position of the carraige in the first row
    bed is the bed that we knit on
    gauge is the gauge, 1 is full needle, 2 is half gauge, 3 is 1/3 gauge and so on
    g start is the offse for the first needle of knitting going from left to right if you want to start after the first needle for some reason'''

    #figure out how to count back
    beg=beg+gstart;
    tot=end-beg
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

    for b in range(start,length+1):

        if b%2==1:
            for w in range(beg,end,gauge):
                k.knit('+',(bed,w),c)

        else:
            for w in range(new_end,beg-1,-1*gauge):
                k.knit('-',(bed,w),c)



def ribKnit(k,ribarray,beg,fin,length,c,side='l',bed1='f',gauge=1, gstart=0):

    #figure out how to count back
    beg=beg+gstart;
    tot=fin-beg
    r=tot%gauge;

    new_end=fin-r;

    if r==0:
        new_end=new_end-gauge;

    #set beds for knitting
    if bed1=='f':
        bed0='b'
    else:
        bed0='f'

    repeatSize = len(ribarray)
    totalRepeatsHoriz=int(math.ceil(float(fin-beg)/repeatSize))

    ref = np.tile(ribarray,totalRepeatsHoriz+2)

    #account for starting position and add first row of knitting
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    for h in range(start,length):
        if h%2 ==0:
            for s in range(beg,fin,gauge):
                if ref[int(s/gauge)] == 1:
                    k.knit('+',(bed1,s),c)
                else:
                    k.knit('+',(bed0,s),c)
        else:
            for s in range(new_end,beg-1,-1*gauge):
                if ref[int(s/gauge)] == 1:
                    k.knit('-',(bed1,s),c)
                else:
                    k.knit('-',(bed0,s),c)

def rib2ribXfer(k,ribarray1,ribarray2,start,finish,gauge=1,gstart=0):
    '''Transfer function for half gauge ribs etc to half or third gauge ribs
    of the same  gauge. Will ignore transferring all non-active needles.'''

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


def garter(k,garterNum,beg,end,length,c,side1='l',bed1='f',gauge=1, gstart=0):
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
        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)
        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart)
        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart)
        jersey(k,beg,end,garterNum,c,side2,bed2,gauge, gstart)


    if remainder<garterNum:
        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)
        jersey(k,beg,end,remainder,c,side1,bed1,gauge, gstart)
    else:
        rib2ribXfer(k,array2,array1,beg,end,gauge,gstart)
        jersey(k,beg,end,garterNum,c,side1,bed1,gauge, gstart)
        rib2ribXfer(k,array1,array2,beg,end,gauge,gstart)
        jersey(k,beg,end,remainder,c,side2,bed2,gauge, gstart)


def garterArray(k,garterarray,beg,end,length,c,side='l',gauge=1, gstart=0):
    '''Creates a garter that doesn't need to be balanced based on an input array.
    1 is front bed and 0 is back bed in the array.'''

    sz = len(garterarray)
    totalRepeatsvert=int(math.ceil(float(length)/sz))
    ref = np.tile(garterarray,totalRepeatsvert+1)

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

        if (i+1)<length and ref[i]!=ref[i+1] and ref[i]==1:
            rib2ribXfer(k,[1],[0],beg,end,gauge,gstart)
        elif (i+1)<length and ref[i]!=ref[i+1] and ref[i]==0:
            rib2ribXfer(k,[0],[1],beg,end,gauge,gstart)


def seed(k,beg,end,length,c,side1='l',gauge=1, gstart=0):

    if side1=='l':
        side2='r'
    else:
        side2='l'

    rib2ribXfer(k,[0],[1],beg,end,gauge,gstart)
    rib2ribXfer(k,[1,1],[0,1],beg,end,gauge,gstart)

    for i in range(int(math.floor(length/2))):
        ribKnit(k,[0,1],beg,end,1,c,side1,'f',gauge, gstart)
        rib2ribXfer(k,[0,1],[1,0],beg,end,gauge,gstart)
        ribKnit(k,[1,0],beg,end,1,c,side2,'f',gauge, gstart)
        rib2ribXfer(k,[1,0],[0,1],beg,end,gauge,gstart)

    if length%2==1:
        ribKnit(k,[0,1],beg,fin,length,c,side1,'f',gauge, gstart)

def gaugexfer(k,beg,end,bed='f',gauge=1,gstart=0,choice='l'):


    #first get every stitch onto side where we will not knit, aka "obed"
    if bed=='f':
        rib2ribXfer(k,[1],[0],beg,end,1,0)
        obed='b'

    else:
        rib2ribXfer(k,[0],[1],beg,end,1,0)
        obed='f'

    #next transfer every knit stitch back to the bed we will knit on
    for s in range(beg,end,gauge):
        k.xfer((obed,s),(bed,s))


    for m in range(gauge):

        if choice=='l' and m%2==0:
            k.rack()


        elif choice=='l' and m%2==1:





## eggo
