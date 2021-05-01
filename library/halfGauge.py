import math
import numpy as np



def jersey(k,beg,end,length,c,side='l',bed='f',gauge=1, gstart=0):
    '''jersey function to account for different gauge knititng
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
