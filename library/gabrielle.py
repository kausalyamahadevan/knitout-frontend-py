import numpy as np

from skimage import io
# from skimage import data

#-----------------------------------------
#--- FUNCTION FOR BRINGING IN CARRIERS ---
#-----------------------------------------
def catchyarns(k, leftN, rightN, carriers, gauge=1):
	for i,c in enumerate(carriers):
		k.incarrier(c)

		toggleF = True
		toggleB = True
		for h in range(0,4):
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
		if h %2 == 0:
			for s in range(leftN, rightN+1):
				if gauge == 1 or s % gauge != 0: k.knit('+',('b',s),c)
		else:
			for s in range(rightN, leftN-1, -1):
				if s % gauge == 0: k.knit('-',('f',s),c)


#NOTE: decided baseBed should consistently be front so as to make things less complicated (because doesn't really matter)
def wasteSection(k, leftN, rightN, wasteC='1', drawC='2', castonC='1', gauge=1):

	# width = rightN - leftN + 1

	catchyarns(k, leftN, rightN, list(set([wasteC, drawC, castonC])), gauge)

	k.comment('waste section')
	#interlock / waste yarn
	k.speedNumber(400)
	interlockRange(k, leftN, rightN, 36, wasteC, gauge)
	#circular / waste Yarn
	circular(k, leftN, rightN, 8, wasteC, gauge)

	for s in range(leftN, rightN+1):
		if (s + 1) % gauge == 0: k.drop(('b',s))

	k.comment('draw thread')
	for s in range(leftN, rightN+1):
		if s % gauge == 0: k.knit('+',('f',s),drawC)
	
	# tubeCaston(k, leftN, rightN, castonC, gauge)



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
		if s % gauge != 0 and ((((s-1)/gauge) % 2) == 0):
			k.knit(dir2,('b',s),c)
		elif s == startN: k.miss(dir2,('b',s),c)

	for s in needleRange1:
		if s % gauge == 0 and (((s/gauge) % 2) != 0):
			k.knit(dir1,('f',s),c)
		elif s == endN: k.miss(dir1,('f',s),c)
	for s in needleRange2:
		if s % gauge != 0 and ((((s-1)/gauge) % 2) != 0):
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

#----------------------------------
#--- SHAPING (INC/DEC) & BINDOFF---
#----------------------------------

#--- bindoff function; can also be used for decreasing large number of stitches ---
def bindoff(k, count, xferNeedle, c, side='l', doubleBed=True, asDecMethod=False):
# def bindoff(k, start,width,c,side='l',onfront=1):
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
					k.drop(f'b{x+1}')
				k.knit('+', f'b{x+1}', c)

				if x < xferNeedle+count-2: k.tuck('-', f'b{x}', c)
				if not asDecMethod and x == xferNeedle+3: k.drop(f'b{xferNeedle-1}')

	def negLoop(op=None, bed=None):
		for x in range(xferNeedle+count-1, xferNeedle+1, -1):
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
	if side == 'l': newEdgeNeedle += count
	else: newEdgeNeedle -= count

	if count == 1:
		if len(emptyNeedles): k.stoppingDistance(3.5) #TODO: check if this needs to be '>0'
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
		if len(emptyNeedles): k.stoppingDistance(3.5) #TODO: check if this needs to be '>0'
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
	newEdgeNeedle = edgeNeedle
	if side == 'l': newEdgeNeedle -= count
	else: newEdgeNeedle += count

	if len(emptyNeedles) > 0: incMethod='twist' #TODO: make sure increasing doesn't occur on empty needles for incMethod='xfer' ... for now, makes it so incMethod='twist' so don't have to worry about issue (but should have it be possible to use xfer method for e.g. half-gauge)

	twistedStitches = []
	# if side == 'both': incMethod = 'twist' #note: currently doesn't support side='both' for incMethod='xfer'
	if incMethod == 'xfer':
		if count == 1:
			if f'b{edgeNeedle}' not in emptyNeedles: twistedStitches.append(f'b{edgeNeedle}')
			if f'f{edgeNeedle}' not in emptyNeedles: twistedStitches.append(f'f{edgeNeedle}')
			if side == 'l': #left side
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
				k.rack(0)
				k.addRollerAdvance(-100)
				k.miss('+', f'f{edgeNeedle}', c)
				k.xfer(f'f{edgeNeedle}', f'b{edgeNeedle}')
				k.xfer(f'f{edgeNeedle-1}', f'b{edgeNeedle-1}')
				k.rack(-1)
				k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
				k.rack(0)
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
				k.rack(0)
	else:
		# if side != 'r': #left or both
		if side == 'l': #left side
			for n in range(count, 0, -1):
				if f'f{n}' not in emptyNeedles: twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles: twistedStitches.append(f'b{n}')
		# if side != 'l': #right or both
		else: #right side
			for n in range(1, count+1):
				if f'f{n}' not in emptyNeedles: twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles: twistedStitches.append(f'b{n}')
	
	return newEdgeNeedle, twistedStitches
	# for p in range(0, len(pass)):
	# 	if 'knit' in pass[p] and f'f{'


#------------------------------------------------
#--- IMAGE PROCESSING FOR CACTUS-ESQUE THINGS ---
#------------------------------------------------

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
	emptyNeedles = [] #push to this if gauge > 1

	if gauge > 1:
		for n in range(0, width):
			if n % gauge == 0: emptyNeedles.append(f'b{n}')
			elif (n-1) % gauge == 0: emptyNeedles.append(f'f{n}')
			else:
				emptyNeedles.append(f'f{n}')
				emptyNeedles.append(f'b{n}')

	print(imageData) #remove

	class SectionInfo: #class for keeping track of section info
		def __init__(self, c):
			self.c = c #carrier used in section (constant)
			self.leftN = None #changing property based on left-most needle in section, used as reference when deciding which carrier to assign to a given section in the next row (same for rightN below)
			self.rightN = None

	#2. Go through ndarray data and separate it into sections represented by lists containing respective needles (i.e. multiple sections if shortrowing)
	rows = [] #list for storing row-wise section data

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
						if len(row) > carrierCount: carrierCount = len(row)
						rows.append(row)
						break #go to next row
	
	#3. Go through rows data and assign carriers to each section
	sections = [] #list for storing SectionInfo

	carrierOrder = [] #list for storing carrier order, helpful when want a certain carrier to be used e.g. always on left (will change if > 2 sections in piece)
	for cs in range(0, carrierCount): #initialize sections (but won't add leftN & rightN until later)
		sections.append(SectionInfo(cs + 1))
		carrierOrder.append(cs+1) #carrierOrder starts out as just [1, 2, 3]

	# matches = [x for x in rows if len(x) > 2] #remove
	# shortrowLeftPrep = [idx for idx, element in enumerate(rows) if len(element) > 2][0] #remove
	
	shortrowLeftPrep = [idx for idx, element in enumerate(rows) if len(element) > 2] #check if the piece contains > 2 sections in any given row and then assigns index of 
	srLneedleR = None #used for if there are > 2 sections so can make sure carrier that will eventually do shortrowing on the left knits up to (inclusive) the right-most needle in the first shortrowing row prior to that row

	if len(shortrowLeftPrep) > 0:
		shortrowLeftPrep = shortrowLeftPrep[0] #just flattening it (should only be one value anyway)
		srLneedleR = rows[shortrowLeftPrep][0][len(rows[shortrowLeftPrep][0])-1] #detect what the right-most needle is in first left-most shortrow section (referenced as 'shortrowLeft' in future comments)
	else: shortrowLeftPrep = False #if the piece doesn't contain > 2 sections in any row

	pieceMap = [] #list for storing overarching carrier/needles data for rows/sections
	#now finally going through rows
	for r in range (0, len(rows)):
		rowMap = {}

		# shortrowLeftPrep = (r < len(rows) - 1 and len(rows[r+1]) > 2 and len(rows[r+1]) > len(rows[r])) #remove
		
		taken = [] #not sure if this is really needed, but it's just an extra step to absolutely ensure two sections in one row don't used same carrier

		#loop through sections in row
		for i in range (0, len(rows[r])): 
			print(rows[r]) #remove
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
					if i == 0 and shortrowLeftPrep and leftN <= srLneedleR: #for doing that thing mentioned above where knit relevant needles with carrier future left-most shortrowing section in preparation for its first row
						section1 = [] #needles for future shortrowLeft
						section2 = [] #needles for actual carrier being dealt with here
						for n in range(leftN, rightN+1):
							if n <= srLneedleR: section1.append(n)
							else: section2.append(n)

						unusedC = carrierOrder[carrierCount-1] #carrier for shortrowLeft

						rowMap[unusedC] = section1 #send the data to the rowMap
						sections[carrierCount-1].leftN = leftN #updata left & right-most needles
						sections[carrierCount-1].rightN = srLneedleR
						taken.append(unusedC)

						rowMap[carrierOrder[s]] = section2 #send what is left for actual carrier to rowMap
						sections[s].leftN = srLneedleR+1
						sections[s].rightN = rightN

						if r == shortrowLeftPrep-1: #if it's the row before the 1st actual shortrow for shortrowLeft, update carrierOrder so this for loop checks that carrier first & it remains on the left
							carrierOrder.insert(0, carrierOrder.pop(carrierCount-1)) #move shortrowLeft carrier to front of carrierOrder list
							sections.insert(0, sections.pop(carrierCount-1)) #move section to correct location too so can be referenced by index (s) correctly
							shortrowLeftPrep = False #won't do all this stuff since won't need to prepare for shortrowLeft anymore (since it will actually be happening)
					else: #if not prepping for shortrowLeft
						sections[s].leftN = leftN
						sections[s].rightN = rightN
						rowMap[carrierOrder[s]] = rows[r][i]
					taken.append(s)
					match = True
					break
			
			if not match: #need to used unusedC and add new carrier for shortrowing
				taken.append(unusedC)
				sections[unusedC].leftN = leftN
				sections[unusedC].rightN = rightN
				rowMap[carrierOrder[unusedC]] = rows[r][i]

		print(rowMap) #remove
		pieceMap.append(rowMap) #new
		# pieceMap.append(sorted(rowMap.items(), key=lambda x: x[1])) #send data to overarching pieceMap, but sort the rowMap data by left-most needle in sections (low to high) -- note that it becomes tuples rather than objects because of stupid behavior of sorted() >:( #go back! //?

	print(pieceMap) #remove

	#5. Convert generated data to knitout; also generate visualization of pieceMap data so can see what it would actually look like (0 == whitespace, other numbers == stitch knit with respective carrier number) 
	visualization = [] #list for storing visualization

	for r in range(0, len(pieceMap)):
		row = []
		n0 = 0

		sectionCount = 0
		rightSection = None
		if len(pieceMap[r]) > 2: rightSection = len(pieceMap[r])

		for s in pieceMap[r]:
			sectionCount += 1

			dir1 = '+'
			if rightSection:
				if sectionCount == rightSection: dir1 = '-'

			carrier = s
			needles = pieceMap[r][s]
			# carrier = s[0] #remove
			# needles = s[1] #remove

			prevLeftN = None
			prevRightN = None
			xferL = 0
			xferR = 0

			twistedStitches = []
			
			n1 = needles[0]
			n2 = needles[len(needles) - 1]

			if s in pieceMap[r-1]:
				prevNeedles = pieceMap[r-1][s]
				prevLeftN = prevNeedles[0]
				prevRightN = prevNeedles[len(prevNeedles)-1]
				xferL = prevLeftN - n1 #dec/inc on left side (neg if dec)
				xferR = n2 - prevRightN #dec/inc on right side (neg if dec)
				# print('!', prevLeftN - n1) #remove #dec/inc left (neg if dec)
				# print('!', n2 - prevRightN) #remove #dec/inc right (neg if dec)
			
			if xferL:
				if xferL > 0: #increase
					dummyLeft, twistedLeft = incDoubleBed(k, xferL, n1, carrier, 'l', emptyNeedles) #TODO: have option to pass incMethod in main function parameters
					twistedStitches.extend(twistedLeft)
				else: #decrease
					dummyLeft = decDoubleBed(k, abs(xferL), n1, carrier, 'l', emptyNeedles)
			if xferR:
				if xferL > 0:
					dummyRight, twistedRight = incDoubleBed(k, xferR, n2, carrier, 'r', emptyNeedles) #TODO: have option to pass incMethod in main function parameters
					twistedStitches.extend(twistedRight)
				else:
					dummyRight = decDoubleBed(k, abs(xferR), n2, carrier, 'r', emptyNeedles)
			
			def backBedPass():
				for n in range(n2, n1-1, -1):
					k.knit('-', f'b{n}', carrier)
			
			for n in range(n0, n1):
				row.append(0)
			
			if dir1 == '-': backBedPass()

			for n in range(n1, n2 + 1):
				row.append(carrier)
				k.knit('+', f'f{n}', carrier) #TODO: have direction 
			
			if dir1 == '+': backBedPass()

			for bn in twistedStitches:
				k.twist(bn)

			n0 = n2 + 1

		for n in range(n0, width):
			row.append(0)
		
		visualization.append(row)
	
	for v in visualization: #remove
		print(v)
	
	# #5. Convert generated data to knitout
	# for r in range(0, len(pieceMap)): #loop thru rows
	# 	for s in pieceMap[r]: #loop thru sections
	# 		carrier = s[0]
	# 		needles = s[1]
	# 		leftN = needles[0]
	# 		rightN = needles[len(needles) - 1]



