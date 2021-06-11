import numpy as np

from skimage import io
# from skimage import data

#NOTE: for gauge > 1: decided baseBed should consistently be front so as to make things less complicated (because doesn't really matter) --- so translation would be fn -> f(gauge*n) bn -> b((gauge*n)+1)

#-------------------------------------------------------------------------------
#--- FUNCTION FOR KNITTING ON ALT NEEDLES, PARITY SWITCHING FOR FRONT & BACK ---
#-------------------------------------------------------------------------------
def interlockRange(k, startN, endN, length, c, gauge=1):
	'''Knits on every needle interlock starting on side indicated by which needle value is greater.
	In this function length is the number of total passes knit so if you want an interlock segment that is 20 courses long on each side set length to 40. Useful if you want to have odd amounts of interlock.
	k is knitout Writer
	startN is the starting needle to knit on
	endN is the last needle to knit on (***note: no longer needs to be +1)
	length is total passes knit
	c is carrier
	gauge is the... well, gauge'''

	if endN > startN: #first pass is pos
		beg = 0
		leftN = startN
		rightN = endN
	else: #first pass is neg
		beg = 1
		length += 1
		leftN = endN
		rightN = startN

	for h in range(beg, length*2):
		if h%2 == 0:
			for s in range(leftN, rightN+1):
				if s % gauge == 0 and (((s/gauge) % 2) == 0):
					k.knit('+',('f',s),c)
				elif s % gauge != 0 and ((((s-1)/gauge) % 2) == 0):
					k.knit('+',('b',s),c)
		else:
			for s in range(rightN, leftN-1, -1):
				if s % gauge == 0 and (((s/gauge) % 2) != 0):
					k.knit('-',('f',s),c)
				elif s % gauge != 0 and ((((s-1)/gauge) % 2) != 0):
					k.knit('-',('b',s),c)


#-------------------------------------
#--- KNITTING CIRCULAR, OPEN TUBES ---
#-------------------------------------

#--- FUNCTION FOR DOING THE MAIN KNITTING OF TUBE ---
def circular(k, startN, endN, length, c, gauge=1):
	'''Knits on every needle circular tube starting on side indicated by which needle value is greater.
	In this function length is the number of total passes knit so if you want a tube that
	is 20 courses long on each side set length to 40.
	k is knitout Writer
	startN is the starting needle to knit on
	endN is the last needle to knit on
	length is total passes knit
	c is carrier
	gauge is... gauge'''

	# width = abs(endN-startN) + 1 #width is width of tube (same on both sides)

	if endN > startN: #first pass is pos
		beg = 0
		leftN = startN
		rightN = endN
	else: #first pass is neg
		beg = 1
		length += 1
		leftN = endN
		rightN = startN

	k.rollerAdvance(500)

	for h in range(beg, length):
		if h % 2 == 0:
			for s in range(leftN, rightN+1):
				if gauge == 1 or s % gauge != 0: k.knit('+',('b',s),c)
		else:
			for s in range(rightN, leftN-1, -1):
				if s % gauge == 0: k.knit('-',('f',s),c)


#--------------------------
#--- PREPARING KNITTING ---
#--------------------------

#--- FUNCTION FOR BRINGING IN CARRIERS ---
def catchyarns(k, leftN, rightN, carriers, gauge=1, endOnRight=[], missNeedles={}):
	for i,c in enumerate(carriers):
		k.incarrier(c)

		toggleF = True
		toggleB = True

		passes = range(0, 4)
		if c in endOnRight: passes = range(0, 5)
		# for h in range(0,4):
		for h in passes:
			if h % 2 == 0:
				needleRange = range(leftN, rightN+1)
				direction = '+'
			else:
				needleRange = range(rightN, leftN-1, -1)
				direction = '-'
			
			for s in needleRange:
					if s % gauge == 0 and (((s/gauge) % len(carriers)) == i):
						if toggleF: k.knit(direction, ('f', s), c)
						elif (direction == '+' and s == rightN) or (direction == '-' and s == leftN): k.miss(direction, ('f', s), c) #check
						toggleF = not toggleF
					elif s % gauge != 0 and ((((s-1)/gauge) % len(carriers)) == i):
						if toggleB: k.knit(direction, ('b', s), c)
						elif (direction == '+' and s == rightN) or (direction == '-' and s == leftN): k.miss(direction, ('f', s), c) #check
						toggleB = not toggleB
					elif (direction == '+' and s == rightN) or (direction == '-' and s == leftN): k.miss(direction, ('f', s), c)
		if c in missNeedles: k.miss(direction, f'f{missNeedles[c]}', c) #check


#--- FUNCTION FOR DOING ALL THINGS BEFORE CAST-ON (catch/initialize yarns, waste yarn, draw thread) ---
def wasteSection(k, leftN, rightN, wasteC='1', drawC='2', otherCs = [], gauge=1, endOnRight=[], firstNeedles={}):

	# width = rightN - leftN + 1

	carriers = [wasteC, drawC]
	carriers.extend(otherCs)
	carriers = list(set(carriers))
	catchEndOnRight = endOnRight.copy()

	missWaste = None
	missDraw = None
	missOtherCs = {}
	if len(firstNeedles):
		if wasteC in firstNeedles:
			if wasteC in endOnRight: missWaste = firstNeedles[wasteC][1]
			else: missWaste = firstNeedles[wasteC][0]
		if drawC in firstNeedles:
			if drawC in endOnRight: missDraw = firstNeedles[drawC][1]
			else: missDraw = firstNeedles[drawC][0]
		if len(otherCs):
			for c in range(0, len(otherCs)):
				if otherCs[c] in firstNeedles:
					if otherCs[c] in endOnRight: missOtherCs[otherCs[c]] = firstNeedles[otherCs[c]][1]
					else: missOtherCs[otherCs[c]] = firstNeedles[otherCs[c]][0]

	if len(endOnRight):
		if drawC in endOnRight: catchEndOnRight.remove(drawC)
		else: catchEndOnRight.append(drawC)

	catchyarns(k, leftN, rightN, carriers, gauge, catchEndOnRight, missOtherCs)

	k.comment('waste section')
	k.speedNumber(400)

	if wasteC in endOnRight:
		interlockRange(k, rightN, leftN, 36, wasteC, gauge)
		circular(k, rightN, leftN, 8, wasteC, gauge)
		if missWaste is not None: k.miss('+', f'f{missWaste}', wasteC) #check
	else:
		interlockRange(k, leftN, rightN, 36, wasteC, gauge)
		circular(k, leftN, rightN, 8, wasteC, gauge)
		if missWaste is not None: k.miss('-', f'f{missWaste}', wasteC) #check

	for s in range(leftN, rightN+1):
		if (s + 1) % gauge == 0: k.drop(('b',s))

	k.comment('draw thread')
	if len(endOnRight) == 0 or drawC in endOnRight:
		for s in range(leftN, rightN+1):
			if s % gauge == 0: k.knit('+',('f',s),drawC)
		if missDraw is not None: k.miss('+', f'f{missDraw}', drawC) #check
	else:
		for s in range(rightN, leftN-1, -1):
			if s % gauge == 0: k.knit('-',('f',s),drawC)
		if missDraw is not None: k.miss('-', f'f{missDraw}', drawC) #check
	

#--------------------------
#--- CASTONS / BINDOFFS ---
#--------------------------

#--- FUNCTION FOR CASTING ON OPEN TUBES ---
def tubeCaston(k, startN, endN, c, gauge=1):
	k.comment('tube cast-on')
	k.rollerAdvance(500)

	if endN > startN: #first pass is pos
		dir1 = '+'
		dir2 = '-'
		needleRange1 = range(startN, endN+1)
		needleRange2 = range(endN, startN-1, -1)
	else: #first pass is neg
		dir1 = '-'
		dir2 = '+'
		needleRange1 = range(startN, endN-1, -1)
		needleRange2 = range(endN, startN+1)

	for s in needleRange1:
		if s % gauge == 0 and (((s/gauge) % 2) == 0):
			k.knit(dir1,('f',s),c)
		elif s == endN: k.miss(dir1,('f',s),c)
	for s in needleRange2:
		if (gauge == 1 or s % gauge != 0) and ((((s-1)/gauge) % 2) == 0):
			k.knit(dir2,('b',s),c)
		elif s == startN: k.miss(dir2,('b',s),c)

	for s in needleRange1:
		if s % gauge == 0 and (((s/gauge) % 2) != 0):
			k.knit(dir1,('f',s),c)
		elif s == endN: k.miss(dir1,('f',s),c)
	for s in needleRange2:
		if (gauge == 1 or s % gauge != 0) and ((((s-1)/gauge) % 2) != 0):
			k.knit(dir2,('b',s),c)
		elif s == startN: k.miss(dir2,('b',s),c)
	
	#two final passes now that loops are secure
	for s in needleRange1:
		if s % gauge == 0: k.knit(dir1, ('f',s),c)
		elif s == endN: k.miss(dir1,('f',s),c)
	for s in needleRange2:
		if (s-1) % gauge == 0: k.knit(dir2, ('b',s),c)
		elif s == startN: k.miss(dir2,('b',s),c)

	k.comment('begin main piece')


#--- SECURE BINDOFF FUNCTION (can also be used for decreasing large number of stitches) ---
def bindoff(k, count, xferNeedle, c, side='l', doubleBed=True, asDecMethod=False):
	def posLoop(op=None, bed=None):
		for x in range(xferNeedle, xferNeedle+count):
			if op == 'knit': k.knit('+', f'{bed}{x}', c)
			elif op == 'xfer':
				receive = 'b'
				if bed == 'b': receive = 'f'
				k.xfer(f'{bed}{x}', f'{receive}{x}')
			else:
				if x == xferNeedle + count - 1 and not asDecMethod: break

				k.xfer(f'b{x}', f'f{x}')
				k.rack(-1)
				k.xfer(f'f{x}', f'b{x+1}')
				k.rack(0)
				if x != xferNeedle:
					if x > xferNeedle+3: k.addRollerAdvance(-50)
					k.drop(f'b{x-1}')
				k.knit('+', f'b{x+1}', c)

				if x < xferNeedle+count-2: k.tuck('-', f'b{x}', c)
				if not asDecMethod and x == xferNeedle+3: k.drop(f'b{xferNeedle-1}')

	def negLoop(op=None, bed=None):
		for x in range(xferNeedle+count-1, xferNeedle-1, -1):
			if op == 'knit': k.knit('-', f'{bed}{x}', c)
			elif op == 'xfer':
				receive = 'b'
				if bed == 'b': receive = 'f'
				k.xfer(f'{bed}{x}', f'{receive}{x}')
			else:
				if x == xferNeedle and not asDecMethod: break

				k.xfer(f'b{x}', f'f{x}')
				k.rack(1)
				k.xfer(f'f{x}', f'b{x-1}')
				k.rack(0)
				if x != xferNeedle+count-1:
					if x < xferNeedle+count-4: k.addRollerAdvance(-50)
					k.drop(f'b{x+1}')
				k.knit('-', f'b{x-1}', c)
				
				if x > xferNeedle+1: k.tuck('+', f'b{x}', c)
				if not asDecMethod and x == xferNeedle+count-4: k.drop(f'b{xferNeedle+count}')
	
	def tail(lastNeedle, dir, shortrowing=False):
		otherDir = '-'
		miss1 = lastNeedle+1
		miss2 = lastNeedle-1
		if dir == '-':
			otherDir = '+'
			miss1 = lastNeedle-1
			miss2 = lastNeedle+1
		
		k.comment(';tail')
		if shortrowing: k.rollerAdvance(100)
		else: k.rollerAdvance(200)

		k.miss(dir, f'b{miss1}', c)

		for i in range(0, 6):
			k.knit(otherDir, f'b{lastNeedle}', c)
			k.miss(otherDir, f'b{miss2}', c)
			k.knit(dir, f'b{lastNeedle}', c)
			k.miss(dir, f'b{miss1}', c)
		
		k.addRollerAdvance(200)
		k.drop(f'b{lastNeedle}')

	if side == 'l':
		if not asDecMethod:
			posLoop('knit', 'f')
			if doubleBed: negLoop('knit', 'b')
		posLoop('xfer', 'f')
		k.rollerAdvance(50)
		k.addRollerAdvance(-50)
		if not asDecMethod: k.tuck('-', f'b{xferNeedle-1}', c)
		k.knit('+', f'b{xferNeedle}', c)
		posLoop()

		if not asDecMethod: tail(xferNeedle+count-1, '+')
	else:
		xferNeedle = xferNeedle-count + 1

		if not asDecMethod:
			negLoop('knit', 'f')
			if doubleBed: posLoop('knit', 'b')
		negLoop('xfer', 'f')
		k.rollerAdvance(50)
		k.addRollerAdvance(-50)
		if not asDecMethod: k.tuck('+', f'b{xferNeedle+count}', c)
		k.knit('-', f'b{xferNeedle+count-1}', c)
		negLoop()

		if not asDecMethod: tail(xferNeedle, '-')


#--- FINISH BY DROP FUNCTION ---
def dropFinish(k, frontNeedleRanges=[], backNeedleRanges=[], carriers=[], rollOut=True):
	'''
	*k is knitout Writer
	*frontNeedleRanges is a list of [leftN, rightN] pairs for needles to drop on the front bed; if multiple sections, can have sub-lists as so: [[leftN1, rightN1], [leftN2, rightN2], ...], or just [leftN, rightN] if only one section
	*backNeedleRanges is same as above, but for back bed
	*carriers is list of carriers to take out (optional, only if you want to take them out using this function)
	*rollOut is an optional boolean parameter indicating whether extra roller advance should be added to roll the piece out
	'''
	def dropOnBed(needleRanges, bed):
		if type(needleRanges[0]) == int: #just one range (one section)
			if rollOut and (needleRanges is backNeedleRanges or not len(backNeedleRanges)): k.addRollerAdvance(2000) #TODO: determine what max roller advance is
			for n in range(needleRanges[0], needleRanges[1]+1):
				k.drop(f'{bed}{n}')
		else: #multiple ranges (multiple sections, likely shortrowing)
			for nr in needleRanges:
				if rollOut and needleRanges.index(nr) == len(needleRanges)-1 and (needleRanges is backNeedleRanges or not len(backNeedleRanges)): k.addRollerAdvance(2000) #TODO: determine what max roller advance is
				for n in range(nr[0], nr[1]+1):
					k.drop(f'f{n}')
	
	if len(frontNeedleRanges): dropOnBed(frontNeedleRanges, 'f')
	if len(backNeedleRanges): dropOnBed(backNeedleRanges, 'b')
	
	if len(carriers):
		for c in carriers: k.outcarrier(c)


#----------------------------------
#--- SHAPING (INC/DEC) & BINDOFF---
#----------------------------------

def decDoubleBed(k, count, decNeedle, c=None, side='l', emptyNeedles=[]):
	'''
	*k in knitout Writer
	*count is number of needles to dec
	*decNeedle is edge-most needle being decreased
	*c is carrier (optional, but necessary if dec > 2, so worth including anyway)
	*side is side to dec on
	*emptyNeedles is an optional list of needles that are not currently holding loops (e.g. if using stitch pattern), so don't waste time xferring them

	returns new edge-needle on given side based on decrease count, so should be called as so (e.g.):
	leftneedle = decDoubleBed(...)
	'''
	newEdgeNeedle = decNeedle
	if side == 'l':
		k.comment(f'dec {count} on left')
		newEdgeNeedle += count
	else:
		k.comment(f'dec {count} on right')
		newEdgeNeedle -= count

	if count == 1:
		if len(emptyNeedles): k.stoppingDistance(3.5)
		if side == 'l': #left side
			k.rack(1)
			if f'b{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(150)
				k.xfer(f'b{decNeedle}', f'f{decNeedle+1}')
			if f'b{decNeedle+1}' not in emptyNeedles:
				k.xfer(f'b{decNeedle+1}', f'f{decNeedle+2}')
			if f'f{decNeedle}' not in emptyNeedles:
				k.rack(-1)
				k.addRollerAdvance(100)
				k.xfer(f'f{decNeedle}', f'b{decNeedle+1}')
		else: #right side
			k.rack(-1)
			if f'b{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(150)
				k.xfer(f'b{decNeedle}', f'f{decNeedle-1}')
			if f'b{decNeedle-1}' not in emptyNeedles:
				k.xfer(f'b{decNeedle-1}', f'f{decNeedle-2}')
			if f'f{decNeedle}' not in emptyNeedles:
				k.rack(1)
				k.addRollerAdvance(100)
				k.xfer(f'f{decNeedle}', f'b{decNeedle-1}')
		k.rack(0)
		if len(emptyNeedles): k.stoppingDistance(2.5)
	elif count == 2:
		if len(emptyNeedles): k.stoppingDistance(3.5)
		if side == 'l':
			if f'b{decNeedle + 2}' not in emptyNeedles:
				k.addRollerAdvance(100)
				k.xfer(f'b{decNeedle+2}', f'f{decNeedle+2}')
			if f'b{decNeedle + 3}' not in emptyNeedles:
				k.xfer(f'b{decNeedle+3}', f'f{decNeedle+3}')
			k.rack(-1)
			if f'f{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(150)
				k.xfer(f'f{decNeedle}', f'b{decNeedle+1}')
			if f'f{decNeedle + 1}' not in emptyNeedles:
				k.xfer(f'f{decNeedle+1}', f'b{decNeedle+2}')
			if f'f{decNeedle + 2}' not in emptyNeedles or f'b{decNeedle + 2}' not in emptyNeedles: #note: it is *not* an accident that these needles don't match those referenced below 
				k.xfer(f'f{decNeedle+2}', f'b{decNeedle+3}')
			k.rack(1)
			if f'b{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(100)
				k.xfer(f'b{decNeedle}', f'f{decNeedle+1}')
			if f'b{decNeedle+1}' not in emptyNeedles or f'f{decNeedle}' not in emptyNeedles: #note: it is *not* an accident that these needles don't match those referenced below 
				k.xfer(f'b{decNeedle+1}', f'f{decNeedle+2}')
			k.rack(-1)
			if f'b{decNeedle}' not in emptyNeedles: #note: it is *not* an accident that this needle doesn't match those referenced below 
				k.addRollerAdvance(50)
				k.xfer(f'f{decNeedle+1}', f'b{decNeedle+2}')
		else:
			if f'b{decNeedle-2}' not in emptyNeedles:
				k.addRollerAdvance(100)
				k.xfer(f'b{decNeedle-2}', f'f{decNeedle-2}')
			if f'b{decNeedle - 3}' not in emptyNeedles:
				k.xfer(f'b{decNeedle-3}', f'f{decNeedle-3}')
			k.rack(1)
			if f'f{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(150)
				k.xfer(f'f{decNeedle}', f'b{decNeedle-1}')
			if f'f{decNeedle - 1}' not in emptyNeedles:
				k.xfer(f'f{decNeedle-1}', f'b{decNeedle-2}')
			if f'f{decNeedle - 2}' not in emptyNeedles or f'b{decNeedle - 2}' not in emptyNeedles: #note: it is *not* an accident that these needles don't match those referenced below 
				k.xfer(f'f{decNeedle-2}', f'b{decNeedle-3}')
			k.rack(-1)
			if f'b{decNeedle}' not in emptyNeedles:
				k.addRollerAdvance(100)
				k.xfer(f'b{decNeedle}', f'f{decNeedle-1}')
			if f'b{decNeedle-1}' not in emptyNeedles or f'f{decNeedle}' not in emptyNeedles: #note: it is *not* an accident that these needles don't match those referenced below 
				k.xfer(f'b{decNeedle-1}', f'f{decNeedle-2}')
			k.rack(1)
			if f'b{decNeedle}' not in emptyNeedles: #note: it is *not* an accident that this needle doesn't match those referenced below 
				k.addRollerAdvance(50)
				k.xfer(f'f{decNeedle-1}', f'b{decNeedle-2}')
		k.rack(0)
		if len(emptyNeedles): k.stoppingDistance(2.5)
	else: #dec by more than 2
		bindoff(k, count, decNeedle, c, side, True, True)
	
	return newEdgeNeedle


def incDoubleBed(k, count, edgeNeedle, c, side='l', emptyNeedles=[], incMethod='xfer'):
	'''
	*k in knitout Writer
	*count is number of needles to inc
	*edgeNeedle is *current* edge-most needle before inc occurs (so reference point for increasing)
	*c is carrier
	*side is side to inc on
	*emptyNeedles is an optional list of needles that are not currently holding loops (e.g. if using stitch pattern), so don't place loops on those
	*incMethod is the chosen method for increasing, options are: 'xfer', 'zig-zag', and 'twist'

	returns 1) new edge-needle on given side based on inc count and 2) list of now-empty needles to perform twisted stitches on, so should be called as so (e.g.):
	leftneedle, twistedStitches = incDoubleBed(...)
	'''
	newEdgeNeedle = edgeNeedle
	if side == 'l':
		k.comment(f'inc {count} on left')
		newEdgeNeedle -= count
	else:
		k.comment(f'inc {count} on right')
		newEdgeNeedle += count

	if len(emptyNeedles): incMethod='twist' #TODO: make sure increasing doesn't occur on empty needles for incMethod='xfer' ... for now, makes it so incMethod='twist' so don't have to worry about issue (but should have it be possible to use xfer method for e.g. half-gauge)

	if count > 2: incMethod='zig-zag'

	twistedStitches = []
	if incMethod == 'xfer':
		shift = 1
		if side == 'r': shift = -1
		if f'b{edgeNeedle}' not in emptyNeedles: twistedStitches.append(f'b{edgeNeedle-(shift*count)+shift}')
		if f'f{edgeNeedle}' not in emptyNeedles: twistedStitches.append(f'f{edgeNeedle-(shift*count)+shift}')
		if count == 1:
			if side == 'l': #left side #TODO: make sure correct empty needle
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
				k.rack(0)
				k.addRollerAdvance(-100)
				k.miss('+', f'f{edgeNeedle}', c) #ensures order of xfers that is least likely to drop stitches (edge-most needle first)
				k.xfer(f'f{edgeNeedle}', f'b{edgeNeedle}')
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle-1}')
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
			else: #right side
				k.rack(1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle+1}')
				k.rack(0)
				k.addRollerAdvance(-100)
				k.miss('+', f'f{edgeNeedle}', c)
				k.xfer(f'f{edgeNeedle}', f'b{edgeNeedle}')
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle-1}')
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
		elif count == 2:
			if side == 'l': #left side
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
				k.rack(1)
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle-2}')
				k.xfer(f'f{edgeNeedle+1}', f'b{edgeNeedle}')
				k.rack(0)
				k.xfer(f'b{edgeNeedle-2}', f'f{edgeNeedle-2}')
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
				k.rack(0)
				k.xfer(f'b{edgeNeedle+1}', f'f{edgeNeedle+1}')
				k.rack(1)
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle-2}')
				k.xfer(f'f{edgeNeedle+1}', f'b{edgeNeedle}')
			else: #right side
				k.rack(1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle+1}')
				k.rack(-1)
				k.xfer(f'f{edgeNeedle+1}', f'b{edgeNeedle+2}') #TODO: determine which order is better
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle}')
				k.rack(0)
				k.xfer(f'b{edgeNeedle+2}', f'f{edgeNeedle+2}')
				k.rack(1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle+1}')
				k.rack(0)
				k.xfer(f'b{edgeNeedle-1}', f'f{edgeNeedle-1}')
				k.rack(-1)
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle}')
				k.xfer(f'f{edgeNeedle+1}', f'b{edgeNeedle+2}')
		k.rack(0)
	elif incMethod == 'zig-zag':
		k.rack(0.25) #half-rack for knitout (note: could do true half rack for kniterate - 0.5 - but then wouldn't look right in visualizer)
		if side == 'l':
			for x in range(edgeNeedle-1, edgeNeedle-count-1, -1): #check
				k.knit('-', f'b{x}', c)
				k.knit('-', f'f{x}', c)
		else:
			for x in range(edgeNeedle+1, edgeNeedle+count+1):
				k.knit('+', f'f{x}', c)
				k.knit('+', f'b{x}', c)
		k.rack(0)
	else:
		if side == 'l': #left side
			for n in range(edgeNeedle-1, edgeNeedle-count-1, -1):
				if f'f{n}' not in emptyNeedles: twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles: twistedStitches.append(f'b{n}')
		else: #right side
			for n in range(edgeNeedle+1, edgeNeedle+count+1):
				if f'f{n}' not in emptyNeedles: twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles: twistedStitches.append(f'b{n}')
	
	return newEdgeNeedle, twistedStitches


#------------------------------------------------------------------------
#--- IMAGE PROCESSING / KNITTING WITH KNITOUT FOR CACTUS-ESQUE THINGS ---
#------------------------------------------------------------------------

def wasteYarnWeights(k, leftN, rightN, c, side='l', gauge=1, drawC=None):
	'''
	*k is knitout Writer
	*leftN is left-most needle
	*rightN is right-most needle
	*c is carrier
	*side is the side that the carrier should start and end on
	*gauge is gauge
	*drawC is the carrier that would be used for the draw thread if it's time to do that

	- adds waste yarn as 'weights' prior to new sections / large increases to make sure the stitches are stable
	'''
	#TODO: #come back!
	if drawC is not None:
		k.comment('draw thread')
		if side == 'l':
			for s in range(leftN, rightN+1):
				if s % gauge == 0: k.knit('+',('f',s),drawC)
			# if missDraw is not None: k.miss('+', f'f{missDraw}', drawC) #check
		else:
			for s in range(rightN, leftN-1, -1):
				if s % gauge == 0: k.knit('-',('f',s),drawC)
			# if missDraw is not None: k.miss('-', f'f{missDraw}', drawC) #check



#--- FUNCTION TO PROCESS/ANALYZE IMAGE AND OUTPUT KNITOUT ---
def generatePieceMap(k, imagePath='graphics/knitMap.png', gauge=1):
	'''
	*k is knitout Writer
	*imagePath is the path to the image that contains the piece data
	*gauge is gauge

	- Reads an image (black and white) and generates an array of rows containing pixel sub-arrays that either have the value 0 (black) or 255 (white)
	- Goes through each row and separates each chunk of black pixels into sections (based on whether there is white space separating sections of black pixels)
	- Goes through rows again and assigns a carrier to each section, allowing for shortrowing; information is stored in 'pieceMap', with lists containing tuples for each section -- e.g. pieceMap[0] = [(1, [1, 2, 3]), (2, [10, 11, 12])] means row 0 uses carrier 1 on needles 1,2,3 and carrier 2 on needles 10,11,12
	- Finally, outputs a 'visualization' (just for, ya know, visualization purposes) with 0 being white space, and knitted mass indicated by carrier number

	TODO: keep in mind when converting to knitout: shortrow carrier on right side should have opposite directional pattern and end on right side during waste yarn / initialization (in other words, should go neg pos rather than pos neg for passes in a row)
	'''

	#1. Read image data from input path
	imageData = io.imread(imagePath)
	imageData = np.flipud(imageData) #so going from bottom to top

	width = len(imageData[0])
	carrierCount = 1
	emptyNeedles = [] #push to this if gauge > 1 #TODO: add awareness of this for knitting

	if gauge > 1:
		for n in range(0, width):
			if n % gauge == 0: emptyNeedles.append(f'b{n}')
			elif (n-1) % gauge == 0: emptyNeedles.append(f'f{n}')
			else:
				emptyNeedles.append(f'f{n}')
				emptyNeedles.append(f'b{n}')

	print('\nimageData:') #remove
	print(imageData) #remove

	class SectionInfo: #class for keeping track of section info
		def __init__(self, c):
			self.c = c #carrier used in section (constant)
			self.leftN = None #changing property based on left-most needle in section, used as reference when deciding which carrier to assign to a given section in the next row (same for rightN below)
			self.rightN = None

	#2. Go through ndarray data and separate it into sections represented by lists containing respective needles (i.e. multiple sections if shortrowing)
	rows = [] #list for storing row-wise section data

	castonLeftN = None
	castonRightN = None

	for r in range(0, len(imageData)):
		row = []

		row = []
		section = []

		for n in range(0, len(imageData[r])):
			if imageData[r][n] == 0:
				section.append(n)

				if n == len(imageData[r]) - 1:
					row.append(section)
					if len(row) > carrierCount: carrierCount = len(row)
					rows.append(row)
			else:
				if len(section) == 0: continue
				else:
					row.append(section)
					section = []
					newSection = False
					for x in range(n, len(imageData[r])):
						if imageData[r][x] == 0:
							n = x
							newSection = True
							break
							
					if not newSection:
						if r == 0:
							castonLeftN = row[0][0]
							castonRightN = row[0][len(row[0])-1]
						if len(row) > carrierCount: carrierCount = len(row)
						rows.append(row)
						break #go to next row
		
	#3. Go through rows data and assign carriers to each section
	sections = [] #list for storing SectionInfo

	carrierOrder = [] #list for storing carrier order, helpful when want a certain carrier to be used e.g. always on left (will change if > 2 sections in piece)
	for cs in range(0, carrierCount): #initialize sections (but won't add leftN & rightN until later)
		sections.append(SectionInfo(cs + 1))
		carrierOrder.append(str(cs+1)) #carrierOrder starts out as just [1, 2, 3]

	availableCarriers = []
	for cs in range(6, carrierCount, -1):
		availableCarriers.append(str(cs))
	
	wasteWeightCarriers = []
	
	
	shortrowLeftPrep = [idx for idx, element in enumerate(rows) if len(element) > 1] #check if the piece contains > 2 sections in any given row and then, if so, assigns index of that row #TODO: make this possible for multiple left sections
	# shortrowLeftPrep = [idx for idx, element in enumerate(rows) if len(element) > 2] #check if the piece contains > 2 sections in any given row and then, if so, assigns index of that row #TODO: make this possible for multiple left sections
	srLneedleR = None #used for if there are > 2 sections so can make sure carrier that will eventually do shortrowing on the left knits up to (inclusive) the right-most needle in the first shortrowing row prior to that row

	if len(shortrowLeftPrep) > 0:
		if len(shortrowLeftPrep) > 1 and len(rows[shortrowLeftPrep[0]]) < 3:
			manySections = []
			manyIdx = None
			for sr in shortrowLeftPrep:
				if len(rows[sr]) > 2:
					manyIdx = sr
					manySections = rows[sr]
					break
			if manyIdx is not None:
				firstSectionLeftN = manySections[0][0]
				twoSections = rows[shortrowLeftPrep[0]]
				if twoSections[0][0] - firstSectionLeftN < 0: shortrowLeftPrep = manyIdx #this is really not always true but my brain hurts so it will have to do for now
				else: shortrowLeftPrep = shortrowLeftPrep[0]
		else: shortrowLeftPrep = shortrowLeftPrep[0]

		# shortrowLeftPrep = shortrowLeftPrep[0] #just flattening it
		srLneedleR = rows[shortrowLeftPrep][0][len(rows[shortrowLeftPrep][0])-1] #detect what the right-most needle is in first left-most shortrow section (referenced as 'shortrowLeft' in future comments)
	else: shortrowLeftPrep = False #if the piece doesn't contain > 2 sections in any row

	pieceMap = [] #list for storing overarching carrier/needles data for rows/sections
	#now finally going through rows

	mainCSection = 0 #might be redefined
	rightCarriers = [] #carriers to the right of main carrier

	firstNeedles = {}

	wasteWeights = {}
	
	for r in range (0, len(rows)):
		rowMap = {}
		
		taken = [] #not sure if this is really needed, but it's just an extra step to absolutely ensure two sections in one row don't used same carrier

		#loop through sections in row
		for i in range (0, len(rows[r])): 
			leftN = rows[r][i][0] #detect the left and right-most needle in each section for that row
			rightN = rows[r][i][len(rows[r][i]) - 1]

			match = False #bool that is toggled to True if the prev leftN & rightN for a carrier aligns with section (otherwise, use 'unusedC')
			unusedC = None #if above^ stays False, stores index (in reference to 'sections' list) of carrier that hasn't been used in piece yet

			for s in range(0, carrierCount):
				if s in taken: continue

				if sections[s].leftN is None: #leftN & rightN will still be 'None' (see class SectionInfo) if not used in piece yet
					if unusedC is None: unusedC = s #index of unused carrier, if needed
					continue

				if (leftN < sections[s].leftN and rightN < sections[s].leftN) or (leftN > sections[s].rightN and rightN > sections[s].rightN):
					continue #prev leftN & rightN for this carrier doesn't align with leftN & rightN of current section, so continue searching
				else: #it's a match!
					if i == 0 and r == shortrowLeftPrep: #if it's the row before the 1st actual shortrow for shortrowLeft, update carrierOrder so this for loop checks that carrier first & it remains on the left
						prevSectionStart = sections[s].leftN #new #check #come back!
						if prevSectionStart - leftN > 2:
							if not r in wasteWeights: wasteWeights[r] = dict()
							wasteWeightCarrier = availableCarriers.pop()
							wasteWeightCarriers.append(wasteWeightCarrier)
							wasteWeights[r][wasteWeightCarrier] = {'left': [leftN, prevSectionStart-1]} #TODO: maybe add back to available carriers once start knitting (or move this assignment down so can keep track better)
							# wasteWeights[r][carrierOrder[s]] = {'left': [leftN, prevSectionStart-1]}

						carrierOrder.insert(0, carrierOrder.pop(carrierCount-1)) #move shortrowLeft carrier to front of carrierOrder list
						sections.insert(0, sections.pop(carrierCount-1)) #move section to correct location too so can be referenced by index (s) correctly
						firstNeedles[carrierOrder[0]] = [leftN, rightN]
						for o in range(0, len(carrierOrder)):
							if carrierOrder[o] == '1':
								mainCSection = o
								break
					else:
						if sections[s].leftN - leftN > 2: #TODO: test which number should be for >
							wasteWeightCarrier = availableCarriers.pop()
							wasteWeightCarriers.append(wasteWeightCarrier)
							if not r in wasteWeights: wasteWeights[r] = dict()
							# wasteWeights[r][carrierOrder[s]] = {'left': [leftN, sections[s].leftN-1]}
							wasteWeights[r][wasteWeightCarrier] = {'left': [leftN, sections[s].leftN-1]}
						if rightN - sections[s].rightN > 2:
							if not r in wasteWeights: wasteWeights[r] = dict()
							wasteWeightCarrier = availableCarriers.pop()
							wasteWeightCarriers.append(wasteWeightCarrier)
							rightCarriers.append(wasteWeightCarrier)
							wasteWeights[r][wasteWeightCarrier]= {'right': [rightN, sections[s].rightN+1]}
							# if wasteWeightCarrier is None:
							# 	wasteWeightCarrier = availableCarriers.pop()
							# 	wasteWeights[r][wasteWeightCarrier] = {'right': [rightN, sections[s].rightN+1]}
							# else: wasteWeights[r][wasteWeightCarrier]['right'] = [rightN, sections[s].rightN+1]

					sections[s].leftN = leftN
					sections[s].rightN = rightN
					rowMap[carrierOrder[s]] = rows[r][i]
					taken.append(s)
					match = True
					break
			
			if not match: #need to used unusedC and add new carrier for shortrowing
				if carrierOrder[unusedC] != '1':
					firstNeedles[carrierOrder[unusedC]] = [leftN, rightN]
					if leftN > sections[mainCSection].rightN: rightCarriers.append(carrierOrder[unusedC])

					rowMapKeys = list(rowMap.keys()) #new #check #come back!
					prevSectionEnd = pieceMap[r-1][carrierOrder[carrierOrder.index(rowMapKeys[len(rowMapKeys)-1])]]
					prevSectionEnd = prevSectionEnd[len(prevSectionEnd)-1]
					if rightN - prevSectionEnd > 2:
						if not r in wasteWeights: wasteWeights[r] = dict()
						wasteWeightCarrier = availableCarriers.pop()
						wasteWeightCarriers.append(wasteWeightCarrier)
						rightCarriers.append(wasteWeightCarrier)
						wasteWeights[r][wasteWeightCarrier] = {'right': [rightN, prevSectionEnd+1]}

				taken.append(unusedC)
				sections[unusedC].leftN = leftN
				sections[unusedC].rightN = rightN
				rowMap[carrierOrder[unusedC]] = rows[r][i]

		pieceMap.append(rowMap) #new

	print('\npieceMap:') #remove
	print(pieceMap) #remove

	print('rightCarriers:', rightCarriers) #remove

	print('firstNeedles:', firstNeedles) #remove

	print('wasteWeights:', wasteWeights) #remove

	#5. Add waste section and cast-on
	otherCs = []
	if carrierCount > 2:
		for c in range(3, carrierCount+1):
			otherCs.append(f'{c}')
	otherCs.extend(wasteWeightCarriers) #check

	wasteSection(k=k, leftN=castonLeftN, rightN=castonRightN, otherCs=otherCs, gauge=gauge, endOnRight=rightCarriers, firstNeedles=firstNeedles)

	tubeCaston(k, castonLeftN, castonRightN, '1', gauge)

	#5. Convert generated data to knitout; also generate visualization of pieceMap data so can see what it would actually look like (0 == whitespace, other numbers == stitch knit with respective carrier number) 
	visualization = [] #list for storing visualization

	#TODO: make it so it does ~4 rows per section before switching to new section (more efficient) #TODO: check what max short row count is that the kniterate can handle

	takeOutAtEnd = []
	wasteWeightsDraw = availableCarriers.pop() #TODO: should pause to have this guy on the correc side each time #TODO: throw error if not enough carriers (i.e. don't add wasteWeights sections)
	for r in range(0, len(pieceMap)):
		# if (r==0 and any(k < 10 for k in wasteWeights.keys())) or r+10 in wasteWeights:
		wasteMatches = [k for k in wasteWeights if k-r <= 10 and k-r >= 0] #TODO: ensure 10 rows is enough for rollers to catch
		if len(wasteMatches):
			takenNeedles = []
			for s in pieceMap[r]:
				takenNeedles.extend(pieceMap[r][s])
			
			for wr in wasteMatches:
				addCaston = False
				addDraw = False
				if wr-r == 10 or r == 0: addCaston = True
				elif r == wr: addDraw = True 
				for wc in wasteWeights[wr]:
					waste = wasteWeights[wr][wc]
					if 'left' in waste:
						needles = waste['left'] #TODO: limit by whether needles are taken by other sections
						if addCaston:
							k.rack(0.25)
							for n in range(needles[0], needles[1]+1):
								if n not in takenNeedles:
									k.knit('+', f'f{n}', wc)
									k.knit('+', f'b{n}', wc)
							k.rack(0)

						if not addCaston:
							for n in range(needles[0], needles[1]+1):
								if n not in takenNeedles: k.knit('+', f'f{n}', wc)
						for n in range(needles[1], needles[0]-1, -1):
							if n not in takenNeedles: k.knit('-', f'b{n}', wc)
						
						if addDraw:
							k.outcarrier(wc) #check
							for n in range(needles[0], needles[1]+1): #pos so carriage isn't in the way of placing draw carrier
								k.drop(f'b{n}')
							k.pause(f'C{wasteWeightsDraw} on L?')
							for n in range(needles[0], needles[1]+1):
								k.knit('+', f'f{n}', wasteWeightsDraw) #TODO: ensure not taken ....
							k.pause(f'move C{wasteWeightsDraw} out')
					if 'right' in waste:
						needles = waste['right'] #TODO: limit by whether needles are taken by other sections
						if addCaston:
							k.rack(0.25)
							for n in range(needles[0], needles[1]-1, -1):
								if n not in takenNeedles:
									k.knit('-', f'b{n}', wc)
									k.knit('-', f'f{n}', wc)
							k.rack(0)

						if not addCaston:	
							for n in range(needles[0], needles[1]-1, -1):
								if n not in takenNeedles: k.knit('-', f'b{n}', wc)
						for n in range(needles[1], needles[0]+1):
							if n not in takenNeedles: k.knit('+', f'f{n}', wc)
						
						if addDraw:
							k.miss('+', 'f252', wc)
							takeOutAtEnd.append(wc)
							for n in range(needles[0], needles[1]-1, -1): #neg so carriage isn't in the way of placing draw carrier
								k.drop(f'b{n}')
							k.pause(f'C{wasteWeightsDraw} on R?')
							for n in range(needles[0], needles[1]-1, -1):
								k.knit('-', f'f{n}', wasteWeightsDraw)
							k.pause(f'move C{wasteWeightsDraw} out')

		row = []
		n0 = 0

		for s in pieceMap[r]:
			carrier = s
			needles = pieceMap[r][s]

			# wasteNeedles = []
			# if len(wasteMatches):
			# 	for wr in wasteMatches:
			# 		if carrier in wasteWeights[wr]: wasteNeedles = wasteWeights[wr][carrier]
		
			dir1 = '+'
			if carrier in rightCarriers: dir1 = '-'

			prevLeftN = None
			prevRightN = None
			xferL = 0
			xferR = 0

			twistedStitches = []
			
			n1 = needles[0]
			n2 = needles[len(needles) - 1]

			sectionCount = len(pieceMap[r])
			mapKeys = list(pieceMap[r].keys())
			sectionIdx = mapKeys.index(s)

			placementPass = []

			sectionFinished = False
			if r == len(pieceMap)-1 or (r < len(pieceMap)-1 and s not in pieceMap[r+1]): sectionFinished = True

			if r > 0 and s not in pieceMap[r-1]: #might need to cast some needles on #TODO: maybe remove this, it might never be needed
				prevRowNeedles = []
				for p in pieceMap[r-1]:
					prevRowNeedles.extend(pieceMap[r-1][p])
				newNeedles = []
				needleRange = range(n1, n2+1)
				if dir1 == '-': needleRange = range(n2, n1-1, -1)
				for n in needleRange:
					if n not in prevRowNeedles: newNeedles.append(n)
				if len(newNeedles):
					k.rack(0.25)
					for n in range(0, len(newNeedles)-1):
						k.knit(dir1, f'f{n}', carrier)
					k.rack(0)

					dir2 = '-'
					needleRange = range(n2, n1-1, -1)
					if dir1 == '-':
						dir2 = '+'
						needleRange = range(n1, n2+1)
					for n in needleRange: #back pass to get carrier on correct side
						k.knit(dir2, f'b{n}', carrier)

			if r < len(pieceMap)-1 and len(pieceMap[r+1]) > sectionCount and s in pieceMap[r+1]:
				futureMapKeys = list(pieceMap[r+1].keys())
				# futureNeedles = pieceMap[r+1][s] #remove
				if sectionIdx == 0 and futureMapKeys.index(s) != 0: #new left shortrow section coming
					futureNewSectionNeedles = pieceMap[r+1][futureMapKeys[0]]
					futureNewSectionRightN = futureNewSectionNeedles[len(futureNewSectionNeedles)-1]
					placementPass = [n1, futureNewSectionRightN] #knit up until futureLeftN on back bed #TODO: make sure it misses an extra needle here so not in the way #TODO: maybe plan ahead for future part to make up for extra pass on back bed in left shortrow section?

			if r > 0 and s in pieceMap[r-1]:
				prevNeedles = pieceMap[r-1][s]
				prevLeftN = prevNeedles[0]
				prevRightN = prevNeedles[len(prevNeedles)-1]

				if sectionCount > len(pieceMap[r-1]): #new section here
					prevMapKeys = list(pieceMap[r-1].keys())

					if sectionIdx > 0 and mapKeys[sectionIdx-1] not in prevMapKeys: #new left section
						prevSectionEnd = pieceMap[r][mapKeys[sectionIdx-1]][len(pieceMap[r][mapKeys[sectionIdx-1]])-1]
						if prevLeftN < prevSectionEnd: prevLeftN = prevSectionEnd+1
					if sectionIdx < len(mapKeys)-1 and mapKeys[sectionIdx+1] not in prevMapKeys: #new right section
						nextSectionStart = pieceMap[r][mapKeys[sectionIdx+1]][0]
						if prevRightN > nextSectionStart: prevRightN = nextSectionStart-1

				xferL = prevLeftN - n1 #dec/inc on left side (neg if dec)
				xferR = n2 - prevRightN #dec/inc on right side (neg if dec)
			
			def leftShaping():
				if xferL:
					if xferL > 0: #increase
						dummyLeft, twistedLeft = incDoubleBed(k, xferL, prevLeftN, carrier, 'l', emptyNeedles) #TODO: have option to pass incMethod in main function parameters
						twistedStitches.extend(twistedLeft)
					else: #decrease
						dummyLeft = decDoubleBed(k, abs(xferL), prevLeftN, carrier, 'l', emptyNeedles)
			def rightShaping():
				if xferR:
					if xferR > 0:
						dummyRight, twistedRight = incDoubleBed(k, xferR, prevRightN, carrier, 'r', emptyNeedles) #TODO: have option to pass incMethod in main function parameters
						twistedStitches.extend(twistedRight)
					else:
						dummyRight = decDoubleBed(k, abs(xferR), prevRightN, carrier, 'r', emptyNeedles)
			
			def backBedPass():
				rightShaping()
				for n in range(n2, n1-1, -1):
					k.knit('-', f'b{n}', carrier)
			
			for n in range(n0, n1):
				row.append(0)
			
			if dir1 == '-':
				backBedPass()
				if (xferL <-2): #so no ladder (carrier is in correct spot to dec)
					for n in range(n1-1, prevLeftN-1, -1):
						k.knit('-', f'b{n}', carrier)

			leftShaping()
			for n in range(n1, n2 + 1):
				row.append(int(carrier))
				if xferR <= 0 or n < prevRightN+1: k.knit('+', f'f{n}', carrier) #don't add the knits if increasing, since they will be added anyway thru increasing #TODO: make sure twisted stitches are all actually happening with this alteration (pretty sure it's working for everything except for when dir1 == '-', but actually might be working? since rightShaping is before knitting)
			
			if dir1 == '+' and (xferR < -2): #so no ladder (carrier is in right spot to dec or inc with yarn) #check
				for n in range(n2+1, prevRightN+1):
					k.knit('+', f'f{n}', carrier)

			
			if dir1 == '+': backBedPass()

			if len(placementPass): #if applicable, place middle section carrier by new left-most needle to get it out of the way for new left-most shortrow section in next row
				for n in range(placementPass[0], placementPass[1]+1):
					k.knit('+', f'b{n}', carrier)
				k.miss('+', f'b{placementPass[1]+1}', carrier)

			for bn in twistedStitches:
				k.twist(bn)

			n0 = n2 + 1

			if sectionFinished:
				rollOut = False
				outCarriers = []
				if r == len(pieceMap)-1:
					rollOut = True
					outCarriers = carrierOrder.copy()
					outCarriers.extend(takeOutAtEnd)
				dropFinish(k, [n1, n2], [n1, n2], outCarriers, rollOut)

		#-------------------------
		for n in range(n0, width):
			row.append(0)
		
		visualization.append(row)
		
	print('\nvisualization:') #remove
	for v in visualization: #remove
		print(v)
	

