#!/usr/bin/env python3
# python3
# see example() for usage
import sys
import re
validHeaders = ['Carriers', 'Machine', 'Position', 'Yarn', 'Gauge']
############### helpers ######################################################


reg = re.compile("([a-zA-Z]+)([\+\-]?[0-9]+)")
def shiftCarrierSet(args, carriers):
    if len(args) == 0:
        raise AssertionError("No carriers specified")
    for c in args:
        if not str(c) in carriers:
            raise ValueError("Carrier not specified in initial set", c)
    cs = ' '.join(str(c) for c in args)
    return cs

def shiftBedNeedle(args):
    if len(args) == 0:
        raise AssertionError("No needles specified")
    bn = args.pop(0)
    if  not (type(bn) == str or type(bn) == list or type(bn) == tuple):
        raise AssertionError("Invalid BedNeedle type")
    bed = None
    needle = None
    if type(bn) == str:
        m = reg.match(bn)
        if not m and (bn == 'f' or bn == 'b' or bn == 'fs' or bn == 'bs'):
            bed = bn
            if not len(args):
                raise ValueError("Needle not specified")
            if  isinstance(args[0],int) or args[0].isdgit():
                needle = int(args.pop(0))

        else:
            if (m.group(1) == 'f' or m.group(1) == 'b' or m.group(1) == 'fs' or m.group(1) == 'bs'):
                bed = m.group(1)
            else:
                raise ValueError("Invalid bed type. Must be 'f' 'b' 'fs' 'bs'.")
            if m.group(2):
                needle = m.group(2)
            else:
                raise ValueError("Invalid needle. Must be numeric.", m.group(2))
    else:
        if len(bn) != 2:
            raise ValueError("Bed and Needle need to be supplied.")
        if (bn[0] == 'f' or bn[0] == 'b' or bn[0] == 'fs' or bn[0] == 'bs'):
            bed = bn[0]
        else:
            raise ValueError("Invalid bed type. Must be 'f' 'b' 'fs' 'bs'.")
        if type(bn[1]) == int or bn[1].isdigit():
            needle = int(bn[1])
        else:
            raise ValueError("2.Invalid needle. Must be numeric.")

    return bed + str(needle)

def shiftDirection(args):
    if len(args) == 0:
        raise AssertionError("No direction specified")
    direction = args.pop(0)
    if direction != '+' and direction != '-':
        raise ValueError("Invalid direction: " + direction)
    return direction

##############################################################################


class Writer:

    def __init__(self, cs):
        # array of carrier names, front-to-back
        self.carriers = list()
        # array of operations, strings
        self.operations = list()
        # array of headers, strings
        self.headers = list()

        self.carriers = cs.split()
        self.addHeader('Carriers', cs);
    def addHeader(self, name, value):
        if not name in validHeaders:
            raise ValueError("Unknown header, must be " + ' '.join(validHeaders) + "; " + name)
        self.headers.append(';;' + name + ': ' + value)

    def addRawOperation(self, op):
        self.operations.append(op)

    def ingripper(self, *args):
        argl = list(args)
        self.operations.append('in ' +  shiftCarrierSet(argl, self.carriers))


    def inhook(self, *args):
        argl = list(args)
        self.operations.append('inhook ' + shiftCarrierSet(argl, self.carriers))

    def incarrier(self, *args):
        argl = list(args)
        self.operations.append('in ' + shiftCarrierSet(argl, self.carriers))

    def outgripper(self, *args):
        argl = list(args)
        self.operations.append('out ' + shiftCarrierSet(argl, self.carriers))


    def outhook(self, *args):
        argl = list(args)
        self.operations.append('outhook ' + shiftCarrierSet(argl, self.carriers))

    def outcarrier(self, *args):
        argl = list(args)
        self.operations.append('out ' + shiftCarrierSet(argl, self.carriers))

    def releasehook(self, *args):
        argl = list(args)
        self.operations.append('releasehook ' + shiftCarrierSet(argl, self.carriers))


    def rack(self, r):
        if not (type(r) == int or type(r) == float or (type(r) == str and r.isdigit())):
            raise ValueError("Rack is not an integer or fraction")
        #TODO only certain values make sense
        self.operations.append('rack ' + str(r))


    def knit(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('knit ' + direction + ' ' + bn + ' ' + cs)

    def tuck(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('tuck ' + direction + ' ' + bn + ' ' + cs)


    def xfer(self, *args):
        argl = list(args)
        bn_from = shiftBedNeedle(argl)
        bn_to = shiftBedNeedle(argl)
        self.operations.append('xfer ' + bn_from + ' ' + bn_to)


    def split(self, *args):
        argl = list(args)
        direction  = shiftDirection(argl)
        bn_from = shiftBedNeedle(argl)
        bn_to = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('split '+ direction + ' '  + bn_from + ' ' + bn_to + ' ' + cs)


    def miss(self, *args):
        argl = list(args)
        direction = shiftDirection(argl)
        bn = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)
        self.operations.append('miss ' + direction + ' ' + bn + ' ' + cs)

    def drop(self, *args):
        argl = list(args)
        bn = shiftBedNeedle(argl)
        self.operations.append('drop ' + bn)

    def amiss(self, *args):
        argl = list(args)
        bn = shiftBedNeedle(argl)
        self.operations.append('amiss ' + bn)

    def pause(self, message=''):
        self.operations.append(f'pause {message}')

    def comment(self, commentString):
        if type(commentString) != str:
            raise ValueError('comment has to be string')
        self.operations.append(';' + commentString)

    def kcodecomment(self, commentString):
        if type(commentString) != str:
            raise ValueError('comment has to be string')
        self.operations.append(';kniterate ' + commentString)

    #Extensions

    def stitchNumber(self, val):
        self.operations.append('x-stitch-number ' + str(val))

    def speedNumber(self, val):
        self.operations.append('x-speed-number ' + str(val))

    def rollerAdvance(self, val):
        self.operations.append('x-roller-advance ' + str(val))

    def addRollerAdvance(self,val):
        self.operations.append('x-add-roller-advance ' + str(val))

    def stoppingDistance(self,val):
        self.operations.append('x-carrier-stopping-distance ' + str(val))

    def fabricPresser(self, mode):
        if not (mode == 'auto' or mode == 'on' or mode == 'off'):
            raise ValueError("Mode must be one of 'auto','on','off' : "+ str(mode))
        self.operations.append('x-presser-mode ' + mode)

    #function for going back to make a twisted stitch
    def twist(self, bedNeedle_s, rollerAdvanceOffset=None): #bedNeedle_s can be just a single bed-needle, or a list to go through multiple
        if type(bedNeedle_s) == str: bedNeedle_s = [bedNeedle_s]

        if rollerAdvanceOffset is not None: rollerAdvanceOffset = f'x-add-roller-advance {rollerAdvanceOffset}'
        
        leftovers = []

        for bn in bedNeedle_s:
            for o in range (len(self.operations)-1, 0, -1):
                if f'xfer {bn}' in self.operations[o]: #new #check #v
                    leftovers.append(bn) 
                    break #^
                if 'knit' in self.operations[o] and bn in self.operations[o]:
                    line = self.operations[o]
                    originalDir = line.split()[1]
                    if originalDir == '-': twistDir = '+'
                    else: twistDir = '-'
                    missLine = line.replace('knit', 'miss')
                    twistLine = line.replace(originalDir, twistDir)
                    if rollerAdvanceOffset is not None: self.operations[o:o+1] = ';twisted stitch', rollerAdvanceOffset, missLine, rollerAdvanceOffset, twistLine
                    else: self.operations[o:o+1] = ';twisted stitch', missLine, twistLine
                    break
        
        return leftovers


    #function for going back to make a split stitch
    def switchToSplit(self, *args):
        argl = list(args)
        direction  = shiftDirection(argl)
        bn_from = shiftBedNeedle(argl)
        bn_to = shiftBedNeedle(argl)
        cs = shiftCarrierSet(argl, self.carriers)

        for o in range (len(self.operations)-1, 0, -1):
            if 'knit' in self.operations[o] and bn_from in self.operations[o]:
                self.operations[o] = f'split {direction} {bn_from} {bn_to} {cs}'
                break
    

    def tuckOverSplit(self, tuckCarrier, tuckDirection, *args):
        '''
        *args: if no argument is passed, will just tuck over most recent split. if one argument, assumes that argument is the number of splits that should be skipped over to find the split that is meant to be tucked over. if two arguments, assumes the argument 1 == bn_from and argument 2 == bn_to
        '''
        # direction = None
        bn_from = None
        bn_to = None
        otherDir = None

        if len(args) <= 1:
            if len(args) == 0: splitSkipCount = 0
            else: splitSkipCount = args[0]
            splitCount = -1
            for op in reversed(self.operations):
                info = op.split()
                if info[0] == 'split':
                    splitCount += 1
                    if splitCount == splitSkipCount:
                        # direction = info[1]
                        otherDir = info[1]
                        bn_from = info[2]
                        bn_to = info[3]
                        break
                    else: continue
            # info = self.operations[len(self.operations)-1]
            # if 'split ' in info:
            #     info = info.split()
            #     direction = info[1]
            #     bn_from = info[2]
            #     bn_to = info[3]
            #     # bed = bn_to[0]
            #     # needle = int(bn_to[1:])
            if bn_from is None: raise ValueError(f"Couldn't find a split.")
        else: 
            info = list(args)
            # direction = info[0]
            # bn_from = info[1]
            # bn_to = info[2]
            bn_from = info[0]
            bn_to = info[1]

        bed_from = bn_from[0]
        needle_from = int(bn_from[1:])
        bed_to = bn_to[0]
        needle_to = int(bn_to[1:])

        if otherDir is None:
            if tuckDirection == '+': otherDir = '-'
            else: otherDir = '+'

        if otherDir == '-': outNeedle = needle_to-2
        else: outNeedle = needle_to+2
        
        # if tuckDirection == '+':
        #     otherDir = '-'
        #     outNeedle = needle_to-2
        # else:
        #     otherDir = '+'
        #     outNeedle = needle_to+2

        
        for op in reversed(self.operations):
            if op.split()[0] == 'rack':
                currentRack = int(op.split()[1])
                if bed_from == 'b' and needle_from+currentRack == needle_to:
                    if currentRack == 0 and tuckDirection == '+': self.operations.append('rack -0.25') #check
                    else: self.operations.append('rack 0.25')
                elif bed_from == 'f' and needle_to+currentRack == needle_from:
                    if currentRack == 0 and tuckDirection == '-': self.operations.append('rack -0.25')
                    else: self.operations.append('rack 0.25')
                else: currentRack is None
                # if (bed_from == 'b' and needle_from+rack == needle_to) or (bed_from == 'f' and needle_to+rack == needle_from):
                #     if currentRack == 0: self.operations.append('rack 0.25')
                #     else: self.operations.append()
                # else: currentRack is None
                break

        self.operations.append(f'tuck {tuckDirection} {bed_from}{needle_to} {tuckCarrier}')
        self.operations.append(f'tuck {tuckDirection} {bed_to}{needle_from} {tuckCarrier}')
        self.operations.append(f'tuck {otherDir} {bed_from}{outNeedle} {tuckCarrier}')
        if currentRack is not None: self.operations.append(f'rack {currentRack}')

        return [f'{bed_from}{outNeedle}', f'{bed_from}{needle_to}', f'{bed_to}{needle_from}'] #to drop

    def deleteLastOp(self, kwd=None, breakCondition=None):
    # def deleteLastOp(self, kwd=None, searchRange=None, breakCondition=None):
        if kwd is None: self.operations.pop()
        else:
            # if searchRange is None: stop = 0
            # else:
            #     stop = len(self.operations)-2-searchRange
            #     if stop < 0: stop = 0
            
            found = False
            # for o in range(len(self.operations)-1, stop, -1):
            for o in range(len(self.operations)-1, 0, -1):
                if breakCondition is not None and breakCondition(self.operations[o]): break

                if kwd in self.operations[o]:
                    del self.operations[o]
                    found = True
                    break

            if not found: print(f"WARNING: Couldn't find operation matching keyword: {kwd}, so didn't delete anything.") #remove #?


    def clear(self):
        #clear buffers
        self.headers = list()
        self.operations = list()

    def write(self, filename):
        version = ';!knitout-2\n'
        content = version + '\n'.join(self.headers) + '\n' +  '\n'.join(self.operations)
        try:
            # with open(filename, "w") as out:
            #     print(content, file=out)
            #     print('wrote file ' + filename)
            # # with open(filename, "w") as out:
            # #     sys.stdout = out
            # #     print(content)
            ''' ----- '''
            out = open(filename,'w')
            sys.stdout = out
            print(content)
            out.close()
        except IOError as error:
            print('Could not write to file ' + filename)

def example():
    stockinette_rectangle()
    garter_rectangle()
    rib_rectangle()
    cable_rectangle()
    stockinette_band()

def stockinette_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)
    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            for i in range(0, width):
                writer.knit('+', ('f', i), carrier)

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('stockinette-'+str(width)+'x'+str(height)+'.k')

def garter_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)
    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            for i in range(0, width):
                writer.xfer(('f',i), ('b',i))
            for i in range(0, width):
                writer.knit('+', ('b', i), carrier)
            for i in range(0, width):
                writer.xfer(('b',i), ('f',i))

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('garter-'+str(width)+'x'+str(height)+'.k')

def rib_rectangle(width=10, height=20):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        bed = 'f'
        if i%2:
            bed = 'b'
        writer.tuck('-', (bed,i), carrier)

    writer.releasehook(carrier)

    for i in range(0, width, 2):
        bed = 'f'
        if i%2:
            bed = 'b'

        writer.tuck('+', (bed, i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                bed = 'f'
                if (i-1)%2:
                    bed = 'b'
                writer.knit('-', (bed, i-1), carrier)
        else:
            for i in range(0, width):
                bed = 'f'
                if i%2:
                    bed = 'b'
                writer.knit('+', (bed, i), carrier)

    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))
        writer.drop(('b', i))

    writer.write('rib-'+str(width)+'x'+str(height)+'.k')

#to test xfers, rack:
def cable_rectangle(width=30, height=40):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    mid = int(width/2)
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)

    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)
    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            for i in range(0, width):
                writer.knit('+', ('f', i), carrier)
        if j > 2 and j < height-2 and j%4==0: #every 4th row
            writer.comment("cable op at row " + str(j))
            writer.xfer('f', mid-2, 'b', mid-2)
            writer.xfer('f', mid-1, 'b', mid-1)
            writer.xfer('f', mid, 'b', mid)
            writer.xfer('f', mid+1, 'b', mid+1)
            writer.rack(2)
            writer.xfer('b',mid-2, 'f', mid)
            writer.xfer('b',mid-1, 'f', mid+1)
            writer.rack(-2)
            writer.xfer('b',mid, 'f', mid-2)
            writer.xfer('b',mid+1, 'f', mid-1)
            writer.rack(0)
    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('cable-'+str(width)+'x'+str(height)+'.k')

#to test split
def stockinette_band(width=20, height=40):
    writer = Writer('1 2 3 4')
    writer.addHeader('Machine', 'swg')
    carrier = '1'
    writer.inhook(carrier)
    for i in range(width-1, 0, -2):
        writer.tuck('-', ('f',i), carrier)

    writer.releasehook(carrier)
    for i in range(0, width, 2):
        writer.tuck('+', ('f', i), carrier)

    for j in range(0, height):
        if j%2 == 0:
            for i in range(width, 0,-1):
                writer.knit('-', ('f', i-1), carrier)
        else:
            if j == 1:
                for i in range(0, width):
                    writer.split('+','f',i,'b',i, carrier)
            else:
                for i in range(0, width):
                    writer.knit('+', ('f', i), carrier)


    for i in range(0, width):
        writer.xfer('b',i,'f',i)

    if height%2 == 0:
        for i in range(width, 0,-1):
            writer.knit('-', ('f', i-1), carrier)
        for i in range(0, width):
            writer.knit('+', ('f', i), carrier)


    else:
        for i in range(0, width):
            writer.knit('+', ('f', i), carrier)
        for i in range(width, 0,-1):
            writer.knit('-', ('f', i-1), carrier)

    #todo bindoff
    writer.outhook(carrier)
    for i in range(0, width):
        writer.drop(('f', i))

    writer.write('band-'+str(width)+'x'+str(height)+'.k')

#todo tubes, castons, bindoffs
