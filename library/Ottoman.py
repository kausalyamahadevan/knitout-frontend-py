import numpy as np

def ottomanStitch(k,beg,fin,length,c,passes1,passesBoth=1,side='l',bed1='f'):
    k.rack(0.25)
    if bed1=='f':
        bed0='b'
    else:
        bed0='f'

    #account for starting position and add first row of knitting
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    totalpasses=passes1+passesBoth

    counter=passes1
    for h in range(length):

        if counter<passes1:

            if h%2 ==0:
                for s in range(beg,fin):
                    k.knit('+',(bed1,s),c)

            else:
                for s in range(fin-1,beg-1,-1):
                    k.knit('-',(bed1,s),c)

            counter=counter+1

        else:
            if h%2 == 0:
                for s in range(beg,fin):
                    k.knit('+',(bed1,s),c)
                    k.knit('+',(bed0,s),c)

            else:
                for s in range(fin-1,beg-1,-1):
                    k.knit('-',(bed0,s),c)
                    k.knit('-',(bed1,s),c)
            counter=counter+1

            if counter==totalpasses:
                counter=0

def striperPattern(k,beg,fin,length,carriers,matrix,side='l',bed1='f'):
    k.rack(0.25)
    if bed1=='f':
        bed0='b'
    else:
        bed0='f'

    #account for starting position and add first row of knitting
    if side == 'r':
        start = 1
        length = length+1
    else:
        start = 0

    matrixL=np.shape(matrix)[0]
    matrixW=np.shape(matrix)[1]

    numCarriers=len(carriers)
    # print(numCarriers)

    for h in range(length):

        for b in range(numCarriers):
            if h%2 ==0:
                for s in range(beg,fin):
                    if matrix[h%matrixL,s%matrixW]==b:
                        k.knit('+',(bed1,s),carriers[b])
                    k.knit('+',(bed0,s),carriers[b])

            else:
                for s in range(fin-1,beg-1,-1):
                    k.knit('-',(bed0,s),carriers[b])
                    if matrix[h%matrixL,s%matrixW]==b:
                        k.knit('-',(bed1,s),carriers[b])

def realStriperPattern(k,beg,fin,length,carriers,matrix,bed1='f'):
    k.rack(0.25)
    if bed1=='f':
        bed0='b'
    else:
        bed0='f'

    matrixL=np.shape(matrix)[0]
    matrixW=np.shape(matrix)[1]

    numCarriers=len(carriers)

    for h in range(int(length/2)):

        for b in range(numCarriers):
                for s in range(beg,fin):
                    if matrix[h%matrixL,s%matrixW]==b:
                        k.knit('+',(bed1,s),carriers[b])
                    k.knit('+',(bed0,s),carriers[b])

                for s in range(fin-1,beg-1,-1):
                    k.knit('-',(bed0,s),carriers[b])
                    if matrix[h%matrixL,s%matrixW]==b:
                        k.knit('-',(bed1,s),carriers[b])
