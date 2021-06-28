import numpy as np
import math
import warnings

from skimage import io
from skimage.transform import resize
# from skimage import data

#NOTE: for gauge > 1: decided baseBed should consistently be front so as to make things less complicated (because doesn't really matter) --- so translation would be fn -> f(gauge*n) bn -> b((gauge*n)+1)

#---------------------------------------------
#--- CUSTOMIZABLE VARIABLES FOR EXTENSIONS ---
#---------------------------------------------
#for waste section
wasteSpeedNumber = 400

#for main section
speedNumber = 300
# stitchNumber = 5
stitchNumber = 4
rollerAdvance = 300

#for xfers
xferSpeedNumber = 100
xferStitchNumber = math.ceil(stitchNumber//2)
xferRollerAdvance = 0 #100 #?

#for wasteWeights
wasteWeightsRowCount = 20

#----------------------
#--- MISC FUNCTIONS ---
#----------------------
def xferSettings(k, alterations={}):
	xSpeed = xferSpeedNumber
	xStitch = xferStitchNumber
	xRoll = xferRollerAdvance

	if 'speedNumber' in alterations: xSpeed = alterations['speedNumber']
	if 'stitchNumber' in alterations: xStitch = alterations['stitchNumber']
	if 'rollerAdvance' in alterations: xRoll = alterations['rollerAdvance']

	k.speedNumber(xSpeed)
	k.stitchNumber(xStitch)
	k.rollerAdvance(xRoll)

def resetSettings(k):
	k.speedNumber(speedNumber)
	k.stitchNumber(stitchNumber)
	k.rollerAdvance(rollerAdvance)


def availableCarrierCheck(usedCarriers, reusableCarriers=[]):
	if len(usedCarriers) == 6: raise ValueError('Not enough available carriers.')
	elif len(usedCarriers) + len(reusableCarriers) == 6:
		warnings.warn('Reusing carrier.')
		return usedCarriers[0]
	else: return None


def convertGauge(gauge=2, leftN=None, rightN=None): #maybe move outside of this?
	newLeftN = leftN
	newRightN = rightN
	if gauge > 1:
		if leftN is not None: newLeftN *= gauge
		if rightN is not None: newRightN = (rightN*gauge)+1

	if leftN is None: return newRightN
	elif rightN is None: return newLeftN
	else: return newLeftN, newRightN


def tempMissOut(k, width, direction, c=None, buffer=None):
	#if c is None, meant to just move carriage out of way, without carrier
	autobuffer = np.floor((252-width)/2)
	if buffer is not None and buffer > autobuffer:
		buffer = None
		warnings.warn(f'Passes buffer value is too large, using default buffer value {autobuffer} instead.')

	if direction == '-':
		if buffer is None: missN = 0 - np.floor((252-width)/2)
		else: missN = 0 - buffer

		if c is None: k.drop(f'f{missN}') #just move carriage out of way #TODO: add carriage move (no drop) to knitout-backend-kniterate
		else: k.miss('-', f'f{missN}', c) #move carrier out of way
	else:
		if buffer is None: missN = (width-1) + np.floor((252-width)/2)
		else: missN = (width-1) + buffer

		if c is None: k.drop(f'f{missN}') #just move carriage out of way
		else: k.miss('+', f'f{missN}', c) #move carrier out of way


#--------------------------
#--- KNITTING FUNCTIONS ---
#--------------------------

#--- KNITTING PASSES ---
def knitPass(k, startN, endN, c, bed='f', gauge=1, emptyNeedles=[]):
	if endN > startN: #pass is pos
		for n in range(startN, endN+1):
			if n not in emptyNeedles:
				if (bed == 'f' and n % gauge == 0) or (bed == 'b' and (gauge == 1 or n % gauge != 0)): k.knit('+', f'{bed}{n}', c) #check
				elif n == endN: k.miss('+', f'{bed}{n}', c)
				# elif bed == 'b' and (gauge == 1 or n % gauge != 0): k.knit('+', f'b{n}', c) #check
			elif n == endN: k.miss('+', f'{bed}{n}', c)
	else: #pass is neg
		for n in range(startN, endN-1, -1):
			if n not in emptyNeedles:
				if (bed == 'f' and n % gauge == 0) or (bed == 'b' and (gauge == 1 or n % gauge != 0)): k.knit('-', f'{bed}{n}', c) #check
				elif n == endN: k.miss('-', f'{bed}{n}', c)
				# if bed == 'b' and (gauge == 1 or n % gauge != 0): k.knit('-', f'b{n}', c) #check
				# elif bed == 'f' and n % gauge == 0: k.knit('-', f'f{n}', c) #check
			elif n == endN: k.miss('-', f'{bed}{n}', c)

#--- FUNCTION FOR KNITTING ON ALT NEEDLES, PARITY SWITCHING FOR FRONT & BACK ---
def interlockRange(k, startN, endN, length, c, gauge=1):
	'''Knits on every needle interlock starting on side indicated by which needle value is greater.
	In this function length is the number of total passes knit so if you want an interlock segment that is 20 courses long on each side set length to 40. Useful if you want to have odd amounts of interlock.
	*k is knitout Writer
	*startN is the starting needle to knit on
	*endN is the last needle to knit on (***note: no longer needs to be +1)
	*length is total passes knit
	*c is carrier
	*gauge is the... well, gauge
	'''

	length *= 2 #check

	if endN > startN: #first pass is pos
		beg = 0
		leftN = startN
		rightN = endN
	else: #first pass is neg
		beg = 1
		length += 1
		leftN = endN
		rightN = startN

	# for h in range(beg, length*2):
	for h in range(beg, length): #check
		if h % 2 == 0:
			for n in range(leftN, rightN+1):
				if n % gauge == 0 and (((n/gauge) % 2) == 0):
					k.knit('+', f'f{n}', c)
				elif (gauge == 1 or n % gauge != 0) and ((((n-1)/gauge) % 2) == 0):
					k.knit('+', f'b{n}', c)
				elif n == rightN: k.miss('+', f'f{n}', c)
		else:
			for n in range(rightN, leftN-1, -1):
				if n % gauge == 0 and (((n/gauge) % 2) != 0):
					k.knit('-', f'f{n}', c)
				elif (gauge == 1 or n % gauge != 0) and ((((n-1)/gauge) % 2) != 0):
					k.knit('-', f'b{n}', c)
				elif n == leftN: k.miss('-', f'f{n}', c)

#--- FUNCTION FOR DOING THE MAIN KNITTING OF CIRCULAR, OPEN TUBES ---
def circular(k, startN, endN, length, c, gauge=1):
	'''
	Knits on every needle circular tube starting on side indicated by which needle value is greater.
	In this function length is the number of total passes knit so if you want a tube that
	is 20 courses long on each side set length to 40.

	*k is knitout Writer
	*startN is the starting needle to knit on
	*endN is the last needle to knit on
	*length is total passes knit
	*c is carrier
	*gauge is... gauge
	'''

	if endN > startN: #first pass is pos
		beg = 0
		leftN = startN
		rightN = endN
	else: #first pass is neg
		beg = 1
		length += 1
		leftN = endN
		rightN = startN

	for h in range(beg, length):
		if h % 2 == 0:
			for n in range(leftN, rightN+1):
				if n % gauge == 0: k.knit('+', f'f{n}', c) #check
				# if gauge == 1 or n % gauge != 0: k.knit('+', f'b{n}', c) #remove #?
		else:
			for n in range(rightN, leftN-1, -1):
				if gauge == 1 or n % gauge != 0: k.knit('-', f'b{n}', c) #check
				# if n % gauge == 0: k.knit('-', f'f{n}', c) #remove #?


#--------------------------
#--- PREPARING KNITTING ---
#--------------------------

#--- FUNCTION FOR BRINGING IN CARRIERS ---
def catchYarns(k, leftN, rightN, carriers, gauge=1, endOnRight=[], missNeedles={}, catchMaxNeedles=False):
	if wasteSpeedNumber > 200: k.speedNumber(wasteSpeedNumber-100)
	else: k.speedNumber(100)

	for i,c in enumerate(carriers):
		k.incarrier(c)

		if c in endOnRight: passes = range(0, 5)
		else: passes = range(0, 4)

		frontCount = 1
		backCount = 1

		for h in passes:
			if frontCount % 2 != 0: frontCount = 0
			else: frontCount = 1
			if backCount % 2 != 0: backCount = 0
			else: backCount = 1

			if h % 2 == 0:
				for n in range(leftN, rightN+1):
					if n % gauge == 0 and ((catchMaxNeedles and ((n/gauge) % 2) == 0) or (((n/gauge) % len(carriers)) == i)):
						if frontCount % 2 == 0: k.knit('+', f'f{n}', c)
						elif n == rightN: k.miss('+', f'f{n}', c) #TODO: make boolean #?
						frontCount += 1
					elif (gauge == 1 or n % gauge != 0) and ((catchMaxNeedles and (((n-1)/gauge) % 2) == 0) or ((((n-1)/gauge) % len(carriers)) == i)):
						if backCount % 2 == 0: k.knit('+', f'b{n}', c)
						elif n == rightN: k.miss('+', f'f{n}', c)
						backCount += 1
					elif n == rightN: k.miss('+', f'f{n}', c)
			else:
				for n in range(rightN, leftN-1, -1):
					if n % gauge == 0 and ((catchMaxNeedles and ((n/gauge) % 2) != 0) or (((n/gauge) % len(carriers)) == i)):
						if frontCount % 2 != 0: k.knit('-', f'f{n}', c)
						elif n == leftN: k.miss('-', f'f{n}', c)
						frontCount += 1
					elif (gauge == 1 or n % gauge != 0) and ((catchMaxNeedles and (((n-1)/gauge) % 2) != 0) or ((((n-1)/gauge) % len(carriers)) == i)):
						if backCount % 2 != 0: k.knit('-', f'b{n}', c)
						elif n == leftN: k.miss('-', f'f{n}', c)
						backCount += 1
					elif n == leftN: k.miss('-', f'f{n}', c)

		if c in missNeedles:
			if c in endOnRight: k.miss('+', f'f{missNeedles[c]}', c)
			else: k.miss('-', f'f{missNeedles[c]}', c)


#--- FUNCTION FOR DOING ALL THINGS BEFORE CAST-ON (catch/initialize yarns, waste yarn, draw thread) ---
def wasteSection(k, leftN, rightN, closedCaston=True, wasteC='1', drawC='2', otherCs = [], gauge=1, endOnRight=[], firstNeedles={}, catchMaxNeedles=False, initial=True):
	'''
	Does everything to prepare for knitting prior to (and not including) the cast-on.
		- bring in carriers
		- catch the yarns to make them secure
		- knit waste section for the rollers to catch
		- add draw thread
	Can also be used to produce a waste section to go in-between samples.

	*k is knitout Writer
	*leftN is the left-most needle to knit on
	*rightN is the right-most needle to knit on
	*closedCaston is a boolean that determines what happens with the draw thread (if True, drops back-bed needles and knits draw on front-bed; if False, doesn't drop and knits draw on both beds)
	*wasteC is an integer in string form indicating the carrier number to be used for the waste yarn
	*drawC is same as above, but for the draw thread carrier
	*otherCs is an *optional* list of other carriers that should be brought in/positioned with catchYarns (NOTE: leave empty if not initial wasteSection)
	*gauge is... gauge
	*endOnRight is an *optional* list of carriers that should be parked on the right side after the wasteSection (**see NOTE below for details about what to do if not initial**) — e.g.: endOnRight=['2', '3']
	*firstNeedles is an *optional* dictionary with carrier as key and a list of [leftN, rightN] as the value. It indicates the edge-most needles in the first row that the carrier is used in for the main piece. — e.g.: firstNeedles={'1': [0, 10]}
	*catchMaxNeedles is a boolean that determines whether or not the maximum number of needles (possible for the given gauge) will be knitted on for *every* carrier (yes if True; if False, knits on interval determined by number of carriers)
	*initial is a boolean that, if True, indicates that this wasteSection is the very first thing being knitted for the piece; otherwise, if False, it's probably a wasteSection to separate samples (and will skip over catchYarns)

	NOTE:
	if initial wasteSection, side (prior to this wasteSection) is assumed to be left for all carriers
	if not initial wasteSection, follow these guidelines for positioning:
		-> wasteC: if currently on right side (prior to this wasteSection), put it in 'endOnRight' list; otherwise, don't
		-> drawC: if currently on left side, put it in 'endOnRight' list; otherwise, don't
	'''
	k.stitchNumber(stitchNumber)
	k.rollerAdvance(rollerAdvance)
	
	if initial:
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

		if len(endOnRight) and closedCaston:
			if drawC in endOnRight: catchEndOnRight.remove(drawC)
			else: catchEndOnRight.append(drawC)

		catchYarns(k, leftN, rightN, carriers, gauge, catchEndOnRight, missOtherCs, catchMaxNeedles)

	k.comment('waste section')
	k.speedNumber(wasteSpeedNumber)

	if wasteC in endOnRight: #TODO: add extra pass if wasteC == drawC and closedCaston == True
		interlockRange(k, rightN, leftN, 36, wasteC, gauge)
		circular(k, rightN, leftN, 8, wasteC, gauge)
		if missWaste is not None: k.miss('+', f'f{missWaste}', wasteC)
	else:
		interlockRange(k, leftN, rightN, 36, wasteC, gauge)
		circular(k, leftN, rightN, 8, wasteC, gauge)
		if missWaste is not None: k.miss('-', f'f{missWaste}', wasteC)

	if closedCaston:
		for n in range(leftN, rightN+1):
			if (n + 1) % gauge == 0: k.drop(f'b{n}')

	k.comment('draw thread')

	def posDraw(bed='f', addMiss=True):
		for n in range(leftN, rightN+1):
			if n % gauge == 0: k.knit('+', f'{bed}{n}', drawC)
		if addMiss and missDraw is not None: k.miss('+', f'f{missDraw}', drawC)

	def negDraw(bed='f', addMiss=True):
		for n in range(rightN, leftN-1, -1):
			if n % gauge == 0: k.knit('-', f'{bed}{n}', drawC)
		if addMiss and missDraw is not None: k.miss('-', f'f{missDraw}', drawC)

	if len(endOnRight) == 0 or drawC in endOnRight:
		if not closedCaston: negDraw('b', False)
		posDraw()
	else:
		if not closedCaston: posDraw('b', False)
		negDraw()


#--------------------------------------
#--- CASTONS / BINDOFFS / PLACEMENT ---
#--------------------------------------

#--- FUNCTION FOR CASTING ON CLOSED TUBES (zig-zag) ---
def closedTubeCaston(k, startN, endN, c, gauge=1):
	k.comment('closed tube cast-on')
	k.speedNumber(speedNumber)

	if endN > startN: #pass is pos
		dir = '+'
		needleRange = range(startN, endN+1)
	else: #pass is neg
		dir = '-'
		needleRange = range(startN, endN-1, -1)

	k.rack(0.25)

	for n in needleRange:
		if n % gauge == 0: k.knit(dir, f'f{n}', c)
		if (n+1) % gauge == 0: k.knit(dir, f'b{n}', c)

	k.rack(0)
	k.comment('begin main piece')


#--- FUNCTION FOR CASTING ON OPEN TUBES ---
def openTubeCaston(k, startN, endN, c, gauge=1):
	k.comment('open tube cast-on')
	k.speedNumber(speedNumber)

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

	for n in needleRange1:
		if n % gauge == 0 and (((n/gauge) % 2) == 0):
			k.knit(dir1, f'f{n}', c)
		elif n == endN: k.miss(dir1, f'f{n}', c)
	for n in needleRange2:
		if (gauge == 1 or n % gauge != 0) and ((((n-1)/gauge) % 2) == 0):
			k.knit(dir2, f'b{n}', c)
		elif n == startN: k.miss(dir2, f'b{n}', c)

	for n in needleRange1:
		if n % gauge == 0 and (((n/gauge) % 2) != 0):
			k.knit(dir1, f'f{n}', c)
		elif n == endN: k.miss(dir1, f'f{n}', c)
	for n in needleRange2:
		if (gauge == 1 or n % gauge != 0) and ((((n-1)/gauge) % 2) != 0):
			k.knit(dir2, f'b{n}', c)
		elif n == startN: k.miss(dir2, f'b{n}', c)

	#two final passes now that loops are secure
	for n in needleRange1:
		if n % gauge == 0: k.knit(dir1, f'f{n}', c)
		elif n == endN: k.miss(dir1, f'f{n}', c)
	for n in needleRange2:
		if (n+1) % gauge == 0: k.knit(dir2, f'b{n}', c)
		elif n == startN: k.miss(dir2, f'b{n}', c)

	k.comment('begin main piece')


#--- FUNCTION FOR TAIL AT END OF BINDOFF ---
def bindoffTail(k, lastNeedle, dir, c, bed='b', shortrowing=False):
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

	k.miss(dir, f'{bed}{miss1}', c)

	for i in range(0, 6):
		k.knit(otherDir, f'{bed}{lastNeedle}', c)
		k.miss(otherDir, f'{bed}{miss2}', c)
		k.knit(dir, f'{bed}{lastNeedle}', c)
		k.miss(dir, f'{bed}{miss1}', c)

	k.outcarrier(c)
	k.pause(f'cut C{c}')

	k.addRollerAdvance(200)
	k.drop(f'{bed}{lastNeedle}')

#--- SECURE BINDOFF FUNCTION (can also be used for decreasing large number of stitches) ---
def bindoff(k, count, xferNeedle, c, side='l', doubleBed=True, asDecMethod=False, emptyNeedles=[]):
	if not asDecMethod: k.comment('bindoff')

	def posLoop(op=None, bed=None):
		for x in range(xferNeedle, xferNeedle+count):
			if op == 'knit' and f'{bed}{x}' not in emptyNeedles: k.knit('+', f'{bed}{x}', c)
			elif op == 'xfer':
				receive = 'b'
				if bed == 'b': receive = 'f'
				if f'{bed}{x}' not in emptyNeedles: k.xfer(f'{bed}{x}', f'{receive}{x}')
			else:
				if x == xferNeedle + count - 1 and not asDecMethod: break

				k.xfer(f'b{x}', f'f{x}') #don't have to worry about empty needles here because binding these off
				k.rack(-1)
				k.xfer(f'f{x}', f'b{x+1}')
				k.rack(0)
				if x != xferNeedle:
					if x > xferNeedle+3: k.addRollerAdvance(-50)
					k.drop(f'b{x-1}')
				k.knit('+', f'b{x+1}', c)

				if asDecMethod and len(emptyNeedles) and x == xferNeedle+count-1 and f'b{x+1}' in emptyNeedles: #transfer this to a non-empty needle if at end and applicable
					if f'f{x+1}' not in emptyNeedles: k.xfer(f'b{x+1}', f'f{x+1}')
					else:
						for z in range(x+2, x+7): #TODO: check what gauge should be
							if f'f{z}' not in emptyNeedles:
								k.rack(z-(x+1))
								k.xfer(f'b{x+1}', f'f{z}')
								k.rack(0)
								break
							elif f'b{z}' not in emptyNeedles:
								k.xfer(f'b{x+1}', f'f{x+1}')
								k.rack((x+1)-z)
								k.xfer(f'f{x+1}', f'b{z}')
								k.rack(0)
								break

				if x < xferNeedle+count-2: k.tuck('-', f'b{x}', c)
				if not asDecMethod and (x == xferNeedle+3 or (x == xferNeedle+count-2 and xferNeedle+3 > xferNeedle+count-2)): k.drop(f'b{xferNeedle-1}')

	def negLoop(op=None, bed=None):
		for x in range(xferNeedle+count-1, xferNeedle-1, -1):
			if op == 'knit' and f'{bed}{x}' not in emptyNeedles: k.knit('-', f'{bed}{x}', c)
			elif op == 'xfer':
				receive = 'b'
				if bed == 'b': receive = 'f'
				if f'{bed}{x}' not in emptyNeedles: k.xfer(f'{bed}{x}', f'{receive}{x}')
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

				if asDecMethod and len(emptyNeedles) and x == xferNeedle-2 and f'b{x-1}' in emptyNeedles: #transfer this to a non-empty needle if at end and applicable
					if f'f{x-1}' not in emptyNeedles: k.xfer(f'b{x-1}', f'f{x-1}')
					else:
						for z in range(x-2, x-7, -1): #TODO: check what gauge should be
							if f'f{z}' not in emptyNeedles:
								k.rack(z-(x+1))
								k.xfer(f'b{x-1}', f'f{z}')
								k.rack(0)
								break
							elif f'b{z}' not in emptyNeedles:
								k.xfer(f'b{x-1}', f'f{x-1}')
								k.rack((x+1)-z)
								k.xfer(f'f{x-1}', f'b{z}')
								k.rack(0)
								break

				if x > xferNeedle+1: k.tuck('+', f'b{x}', c)
				if not asDecMethod and (x == xferNeedle+count-4 or (x == xferNeedle+1 and xferNeedle+count-4 < xferNeedle+1)): k.drop(f'b{xferNeedle+count}')

	#-------------
	if side == 'l':
		if not asDecMethod:
			posLoop('knit', 'f')
			if doubleBed: negLoop('knit', 'b')

		xferSettings(k)
		posLoop('xfer', 'f')
		k.rollerAdvance(50)
		k.addRollerAdvance(-50)
		if not asDecMethod: k.tuck('-', f'b{xferNeedle-1}', c)
		k.knit('+', f'b{xferNeedle}', c)
		posLoop()

		if not asDecMethod: bindoffTail(k, xferNeedle+count-1, '+', c)
	else:
		xferNeedle = xferNeedle-count + 1

		if not asDecMethod:
			negLoop('knit', 'f')
			if doubleBed: posLoop('knit', 'b')

		xferSettings(k)
		negLoop('xfer', 'f')
		k.rollerAdvance(50)
		k.addRollerAdvance(-50)
		if not asDecMethod: k.tuck('+', f'b{xferNeedle+count}', c)
		k.knit('-', f'b{xferNeedle+count-1}', c)
		negLoop()

		if not asDecMethod: bindoffTail(k, xferNeedle, '-', c)


def halfGaugeOpenBindoff(k, count, xferNeedle, c, side='l'):
	k.comment('open-tube bindoff')

	if xferNeedle % 2 == 0:
		bed1 = 'f'
		bed2 = 'b'
	else:
		bed1 = 'b'
		bed2 = 'f'

	if side == 'l':
		adjust = 2
		if bed1 == 'f': rack = 2
		else: rack = -2
		dir1 = '+'
		dir2 = '-'
		otherEdgeN = xferNeedle+count-1
		bindRange1 = range(xferNeedle, xferNeedle+count, 2)
		if (bed2 == 'b' and otherEdgeN % 2 != 0) or (bed2 == 'f' and otherEdgeN % 2 == 0):
			smallRack = 1
			bindRange2 = range(otherEdgeN, xferNeedle, -2)
		else:
			smallRack -1
			bindRange2 = range(otherEdgeN-1, xferNeedle, -2)
	else:
		adjust = -2
		if bed1 == 'f': rack = -2
		else: rack = 2
		dir1 = '-'
		dir2 = '+'
		otherEdgeN = xferNeedle-count+1
		bindRange1 = range(xferNeedle, xferNeedle-count, -2)
		if (bed2 == 'b' and otherEdgeN % 2 != 0) or (bed2 == 'f' and otherEdgeN % 2 == 0):
			bindRange2 = range(otherEdgeN, xferNeedle, 2)
		else:
			bindRange2 = range(otherEdgeN+1, xferNeedle, 2)

	for n in bindRange1:
		k.xfer(f'{bed1}{n}', f'{bed2}{n}')
		if abs(n-otherEdgeN) != 1: #skip if 1 in from otherEdgeN (note: only applicable if count % 2 == 0, since xferNeedle & otherEdgeN would have different parity)
			k.rack(rack)
			k.xfer(f'{bed2}{n}', f'{bed1}{n+adjust}')
			k.rack(0)
			k.knit(dir1, f'{bed1}{n+adjust}', c)

	k.rack(rack//2)
	if count % 2 != 0: #note: if count % 2 != 0, xferNeedle & otherEdgeN have same parity
		k.xfer(f'{bed1}{otherEdgeN}', f'{bed2}{otherEdgeN-(adjust//2)}')
		k.rack(0)
		k.knit(dir2, f'{bed2}{otherEdgeN-(adjust//2)}', c)
	else:
		k.xfer(f'{bed2}{otherEdgeN-(adjust//2)}', f'{bed1}{otherEdgeN}')
		k.rack(0)
		k.xfer(f'{bed1}{otherEdgeN}', f'{bed2}{otherEdgeN}')
		k.knit(dir2, f'{bed2}{otherEdgeN}', c)

	for n in bindRange2:
		k.xfer(f'{bed2}{n}', f'{bed1}{n}')
		k.rack(rack)
		k.xfer(f'{bed1}{n}', f'{bed2}{n-adjust}') #+rack
		k.rack(0)
		k.knit(dir2, f'{bed2}{n-adjust}', c)

	bindoffTail(k, xferNeedle-(adjust//2), dir2, c, bed2)


#--- FINISH BY DROP FUNCTION ---
def dropFinish(k, frontNeedleRanges=[], backNeedleRanges=[], carriers=[], rollOut=True, emptyNeedles=[]):
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
				if n not in emptyNeedles: k.drop(f'{bed}{n}')
		else: #multiple ranges (multiple sections, likely shortrowing)
			for nr in needleRanges:
				if rollOut and needleRanges.index(nr) == len(needleRanges)-1 and (needleRanges is backNeedleRanges or not len(backNeedleRanges)): k.addRollerAdvance(2000) #TODO: determine what max roller advance is
				for n in range(nr[0], nr[1]+1):
					if n not in emptyNeedles: k.drop(f'f{n}')

	k.comment('drop finish')

	if len(frontNeedleRanges): dropOnBed(frontNeedleRanges, 'f')
	if len(backNeedleRanges): dropOnBed(backNeedleRanges, 'b')

	if len(carriers):
		for c in carriers: k.outcarrier(c)


#----------------------------------
#--- SHAPING (INC/DEC) & BINDOFF---
#----------------------------------
def notEnoughNeedlesDecCheck(k, decNeedle, otherEdgeNeedle, c, gauge=1, rearrange=True): #TODO: note that this is not applicable in this way for gauge == 1 and dec == 2 (only need to worry if width == 1 [not 2]) #check if enough needles to dec (for when dec == 2) #NOTE: should only do this after *all* dec #NOTE: should knit through stacked loops if dec by > 2 on both side and width isn't big enough
	'''
	*decNeedle and otherEdgeNeedle reference front bed for gauge > 1
	'''
	if gauge > 1:
		if decNeedle % 2 != 0: decNeedle -= 1
		if otherEdgeNeedle % 2 != 0: otherEdgeNeedle -= 1

	width = abs(decNeedle-otherEdgeNeedle)

	if (gauge == 2 and width < 6) or (gauge == 1 and width < 2): #not enough needles #TODO: determine if should be width <= 6
		bAdjust = 0
		if gauge > 1: bAdjust = 1

		if decNeedle-otherEdgeNeedle > 0: #right side
			originalFN = decNeedle-(3*gauge)
			originalBN = decNeedle-(3*gauge)+bAdjust
			newFNLoc = decNeedle-(3*gauge)+gauge
			newBNLoc = decNeedle-(3*gauge)+gauge+bAdjust

			k.comment(f'not enough needles, shifting loop on f{originalFN} to f{newFNLoc} and b{originalBN} to b{newBNLoc}')

			for n in range(newBNLoc, originalFN-1, -1):
				if n % gauge == 0: k.knit('-', f'f{n}', c)
			for n in range(originalFN, newBNLoc+1):
				if (n+1) % gauge == 0: k.knit('+', f'b{n}', c)
			
			k.rack(-gauge) #check
			k.xfer(f'f{originalFN}', f'b{newFNLoc}')
			k.rack(gauge)
			k.xfer(f'b{originalBN}', f'f{newBNLoc}')
			k.rack(0)
			k.xfer(f'f{newBNLoc}', f'b{newBNLoc}')
			k.xfer(f'b{newFNLoc}', f'f{newFNLoc}')
			#TODO: maybe knit through them, since they're stacked? probably don't need to, though

		else: #left side
			originalFN = decNeedle+(3*gauge)
			originalBN = decNeedle+(3*gauge)+bAdjust
			newFNLoc = decNeedle+(3*gauge)-gauge
			newBNLoc = decNeedle+(3*gauge)-gauge+bAdjust

			k.comment(f'not enough needles, shifting loop on f{originalFN} to f{newFNLoc} and b{originalBN} to b{newBNLoc}')

			for n in range(newFNLoc, originalBN+1):
				if (n+1) % gauge == 0: k.knit('+', f'b{n}', c)
			for n in range(originalBN, newFNLoc-1, -1):
				if n % gauge == 0: k.knit('-', f'f{n}', c)

			k.rack(gauge)
			k.xfer(f'f{originalFN}', f'b{newFNLoc}')
			k.rack(-gauge)
			k.xfer(f'b{originalBN}', f'f{newBNLoc}')
			k.rack(0)
			k.xfer(f'f{newBNLoc}', f'b{newBNLoc}')
			k.xfer(f'b{newFNLoc}', f'f{newFNLoc}')
			#TODO: maybe knit through them, since they're stacked? probably don't need to, though


def shapeXferDoubleBedHalfGauge(k, type, count, edgeNeedle, side='l'):
# def shapeXferDoubleBedHalfGauge(k, type, count, edgeNeedleF, side='l'):
	'''
	*k in knitout Writer
	*count is number of needles to dec (**note: based on gauge 1, so enter count assuming will convert according to gauge in this function**)
	*edgeNeedle is the edge-most needle being xferred
	*side is side to xfer on

	NOTE: only for dec/xfer inc method, <= 2
	'''
	if edgeNeedle % 2 == 0:
		if side == 'l':
			edgeNeedleF = edgeNeedle
			edgeNeedleB = edgeNeedle+1
		else:
			edgeNeedleF = edgeNeedle
			edgeNeedleB = edgeNeedle-1
		
		#variable naming convention based on count == 1
		rack1st = 1
		rack2nd = -1
		bed1 = 'f'
		bed2 = 'b'
		needle1 = edgeNeedleF
		needle2 = edgeNeedleB
	else:
		if side == 'l':
			edgeNeedleB = edgeNeedle
			edgeNeedleF = edgeNeedle+1
		else:
			edgeNeedleB = edgeNeedle
			edgeNeedleF = edgeNeedle-1
		
		#variable naming convention based on count == 1
		rack1st = -1
		rack2nd = 1
		bed1 = 'b'
		bed2 = 'f'
		needle1 = edgeNeedleB
		needle2 = edgeNeedleF

	if count == 1:
		if (type == 'inc' and side == 'l') or (type == 'dec' and side == 'r'): #left side inc or right side dec
			k.rack(rack1st)
			k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2-2}')
			k.rack(rack2nd)
			k.xfer(f'{bed2}{needle2-2}', f'{bed1}{needle1-2}')
			k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1}')
			k.rack(rack1st)
			k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2-2}')
			k.rack(0)
			# if type == 'dec': return [] #? #TODO: figure out which loops are stacked here
		else: #right side inc or left side dec
			k.rack(rack1st)
			k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1+2}')
			k.rack(rack2nd)
			k.xfer(f'{bed1}{needle1+2}', f'{bed2}{needle2+2}')
			k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2}')
			k.rack(rack1st)
			k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1+2}')
			k.rack(0)
			# if type == 'dec': return [] #? #TODO: figure out which loops are stacked here
	else: #count == 2
		if type == 'inc': #inc
			if side == 'l': #left side inc
				k.rack(rack1st*2)
				k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2-3}')
				k.rack(rack2nd*2)
				k.xfer(f'{bed2}{needle2-3}', f'{bed1}{needle1-4}')
				k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1-1}')
				k.rack(rack1st*2)
				k.xfer(f'{bed1}{needle1-1}', f'{bed2}{needle2-4}')
				k.rack(0)
			else: #right side inc
				k.rack(rack2nd*2)
				k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2+1}')
				k.rack(rack1st*2)
				k.xfer(f'{bed2}{needle2+1}', f'{bed1}{needle1+4}')
				k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1+3}')
				k.rack(rack2nd*2)
				k.xfer(f'{bed1}{needle1+3}', f'{bed2}{needle2+4}')
				k.rack(0)
		else: #dec
			if side == 'l': #left side dec
				k.rack(rack1st*2)
				k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1+3}')
				k.xfer(f'{bed2}{needle2+2}', f'{bed1}{needle1+5}')
				k.xfer(f'{bed1}{needle1+6}', f'{bed2}{needle2+3}')
				k.rack(rack2nd*2)
				k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2+1}')
				k.xfer(f'{bed1}{needle1+2}', f'{bed2}{needle2+3}')
				k.xfer(f'{bed1}{needle1+3}', f'{bed2}{needle2+4}')
				k.xfer(f'{bed1}{needle1+5}', f'{bed2}{needle2+6}')
				k.rack(rack1st*2)
				k.xfer(f'{bed2}{needle2+1}', f'{bed1}{needle1+4}')
				k.xfer(f'{bed2}{needle2+3}', f'{bed1}{needle1+6}')
				k.rack(0)
				return [f'{bed1}{needle1+4}', f'{bed2}{needle2+4}', f'{bed1}{needle1+6}', f'{bed2}{needle2+6}'] #stacked-loop needles
			else: #right side dec
				k.rack(rack2nd*2)
				k.xfer(f'{bed2}{needle2}', f'{bed1}{needle1-1}')
				k.xfer(f'{bed2}{needle2-2}', f'{bed1}{needle1-3}')
				k.rack(rack1st*2)
				k.xfer(f'{bed1}{needle1}', f'{bed2}{needle2-3}')
				k.xfer(f'{bed1}{needle1-1}', f'{bed2}{needle2-4}')
				k.xfer(f'{bed1}{needle1-2}', f'{bed2}{needle2-5}')
				k.xfer(f'{bed1}{needle1-3}', f'{bed2}{needle2-6}')
				k.rack(rack2nd*2)
				k.xfer(f'{bed2}{needle2-3}', f'{bed1}{needle1-4}')
				k.xfer(f'{bed2}{needle2-5}', f'{bed1}{needle1-6}')
				k.rack(0)
				return [f'{bed2}{needle2-4}', f'{bed1}{needle1-4}', f'{bed2}{needle2-6}', f'{bed1}{needle1-6}'] #stacked-loop needles


def decDoubleBed(k, count, decNeedle, c=None, side='l', gauge=1, emptyNeedles=[]):
	'''
	*k in knitout Writer
	*count is number of needles to dec
	*decNeedle is edge-most needle being decreased (so reference point for increasing)
	*c is carrier (optional, but necessary if dec > 2, so worth including anyway)
	*side is side to dec on
	*emptyNeedles is an optional list of needles that are not currently holding loops (e.g. if using stitch pattern), so don't waste time xferring them

	returns new edge-needle on given side based on decrease count, so should be called as so (e.g.):
	leftneedle = decDoubleBed(...)
	'''
	stackedLoopNeedles = []

	decMethod = 'xfer'
	if count > 2: decMethod = 'bindoff'

	if gauge == 1:
		edgeNeedleF = decNeedle
		edgeNeedleB = decNeedle
	else:
		if side == 'l':
			if decNeedle % 2 == 0:
				edgeNeedleF = decNeedle
				edgeNeedleB = decNeedle+1
			else:
				edgeNeedleB = decNeedle
				edgeNeedleF = decNeedle+1
		else:
			if decNeedle % 2 != 0:
				edgeNeedleB = decNeedle
				edgeNeedleF = decNeedle-1
			else:
				edgeNeedleF = decNeedle
				edgeNeedleB = decNeedle-1

	newEdgeNeedle = decNeedle
	if side == 'l':
		count *= gauge
		newEdgeNeedle += count
		k.comment(f'dec {count} on left ({decNeedle} -> {newEdgeNeedle})')
	else:
		count *= gauge
		newEdgeNeedle -= count
		k.comment(f'dec {count} on right ({decNeedle} -> {newEdgeNeedle})')

	if decMethod == 'xfer':
		xferSettings(k)

		if gauge == 1:
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
		else:
			if gauge == 2:
				stackedLoopNeedles = shapeXferDoubleBedHalfGauge(k, 'dec', (count/gauge), decNeedle, side)
			else: print('#TODO') #add for other gauges
	else: #dec by more than 2, bindoff method
		bindNeedle = decNeedle

		bindoff(k, count, bindNeedle, c, side, True, True, emptyNeedles)

	resetSettings(k)
	return newEdgeNeedle, stackedLoopNeedles


def incDoubleBed(k, count, edgeNeedle, c, side='l', gauge=1, emptyNeedles=[], incMethod='xfer'):
	'''
	*k in knitout Writer
	*count is number of needles to inc
	*edgeNeedle is *current* edge-most needle before inc occurs (so reference point for increasing)
	*c is carrier
	*side is side to inc on
	*gauge is gauge
	*emptyNeedles is an optional list of needles that are not currently holding loops (e.g. if using stitch pattern), so don't place loops on those
	*incMethod is the chosen method for increasing, options are: 'xfer', 'zig-zag', and 'twist'

	returns 1) new edge-needle on given side based on inc count and 2) list of now-empty needles to perform twisted stitches on, so should be called as so (e.g.):
	leftneedle, twistedStitches = incDoubleBed(...)
	'''
	if count > 2: incMethod='zig-zag' #default since no code for inc > 2 by xfer

	if gauge == 1:
		edgeNeedleF = edgeNeedle
		edgeNeedleB = edgeNeedle
	else:
		if side == 'l':
			if edgeNeedle % 2 == 0:
				edgeNeedleF = edgeNeedle
				edgeNeedleB = edgeNeedle+1
			else:
				edgeNeedleB = edgeNeedle
				edgeNeedleF = edgeNeedle+1
		else:
			if edgeNeedle % 2 != 0:
				edgeNeedleB = edgeNeedle
				edgeNeedleF = edgeNeedle-1
			else:
				edgeNeedleF = edgeNeedle
				edgeNeedleB = edgeNeedle-1

	newEdgeNeedle = edgeNeedle
	if side == 'l': #left side
		count *= gauge
		newEdgeNeedle -= count
		k.comment(f'inc {count} on left ({edgeNeedle} -> {newEdgeNeedle}) by {incMethod}')
	else: #right side
		count *= gauge
		newEdgeNeedle += count
		k.comment(f'inc {count} on right ({edgeNeedle} -> {newEdgeNeedle}) by {incMethod}')

	twistedStitches = []
	if incMethod == 'xfer':
		xferSettings(k)

		if side == 'r': shift = -1
		else: shift = 1

		if count > 2: #applicable for when count is adjusted based on gauge #TODO: adjust this once have xfer methods for inc with gauge > 2
			if f'b{edgeNeedleB}' not in emptyNeedles: twistedStitches.append(f'b{edgeNeedleB}')
			if f'f{edgeNeedleF}' not in emptyNeedles: twistedStitches.append(f'f{edgeNeedleF}')

		if f'b{(edgeNeedleB)-(shift*count)+(shift*gauge)}' not in emptyNeedles: twistedStitches.append(f'b{(edgeNeedleB)-(shift*count)+(shift*gauge)}')
		if f'f{edgeNeedleF-(shift*count)+(shift*gauge)}' not in emptyNeedles: twistedStitches.append(f'f{edgeNeedleF-(shift*count)+(shift*gauge)}')

		if gauge == 1:
			if count == 1:
				if side == 'l':
					k.rack(-1)
					if f'b{edgeNeedle}' not in emptyNeedles: k.xfer(f'b{edgeNeedle}', f'f{edgeNeedle-1}')
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
		else:
			if gauge == 2: shapeXferDoubleBedHalfGauge(k, 'inc', (count/gauge), edgeNeedle, side)
			#TODO: add for other gauges
		resetSettings(k)
	elif incMethod == 'zig-zag':
		k.rack(0.25) #half-rack for knitout (note: could do true half rack for kniterate - 0.5 - but then wouldn't look right in visualizer)
		if side == 'l':
			for x in range(edgeNeedle-1, edgeNeedle-count-1, -1):
				if f'b{x}' not in emptyNeedles: k.knit('-', f'b{x}', c)
				if f'f{x}' not in emptyNeedles: k.knit('-', f'f{x}', c)
		else:
			for x in range(edgeNeedle+1, edgeNeedle+count+1):
				if f'f{x}' not in emptyNeedles: k.knit('+', f'f{x}', c)
				if f'b{x}' not in emptyNeedles: k.knit('+', f'b{x}', c)
		k.rack(0)
	elif incMethod == 'split': #TODO: add stuff for empty needle check
		k.speedNumber(xferSpeedNumber)
		if gauge == 1:
			if side == 'l':
				k.rack(1)
				k.split('+', f'f{edgeNeedle}', f'b{edgeNeedle-1}', c)
				k.rack(-1)
				k.split('+', f'b{edgeNeedle}', f'f{edgeNeedle-1}', c)
				k.rack(0)
			else:
				k.rack(-1)
				k.split('-', f'f{edgeNeedle}', f'b{edgeNeedle+1}', c)
				k.rack(1)
				k.split('+', f'b{edgeNeedle}', f'f{edgeNeedle+1}', c)
				k.rack(0)
		else: # gauge > 1
			if (count//gauge) == 1:
				if side == 'l':
					k.deleteLastOp(kwd = f'knit - f{edgeNeedleF}', breakCondition = lambda op: 'knit + ' in op)
					k.deleteLastOp(kwd = f'knit - b{edgeNeedleB}', breakCondition = lambda op: 'knit + ' in op)
					if edgeNeedleF > edgeNeedleB: k.split('-', f'f{edgeNeedleF}', f'b{edgeNeedleF}', c)
					k.split('-', f'b{edgeNeedleB}', f'f{edgeNeedleB}', c)
					if edgeNeedleF < edgeNeedleB: k.split('-', f'f{edgeNeedleF}', f'b{edgeNeedleF}', c)

					k.rack(-gauge)
					if edgeNeedleF > edgeNeedleB: #?
						k.tuck('-', f'f{edgeNeedleF-1}', c)
						k.tuck('-', f'b{edgeNeedleF-2-gauge}', c)

					k.xfer(f'b{edgeNeedleF}', f'f{edgeNeedleF-gauge}')
					if edgeNeedleF > edgeNeedleB: #?
						k.drop(f'b{edgeNeedleF-2-gauge}')
						k.drop(f'f{edgeNeedleF-1}')

					k.rack(gauge)
					if edgeNeedleF < edgeNeedleB: #?
						k.tuck('-', f'b{edgeNeedleB-1}', c)
						k.tuck('-', f'f{edgeNeedleB-2-gauge}', c)

					k.xfer(f'f{edgeNeedleB}', f'b{edgeNeedleB-gauge}')

					if edgeNeedleF < edgeNeedleB: #?
						k.drop(f'f{edgeNeedleB-2-gauge}')
						k.drop(f'b{edgeNeedleB-1}')

					k.rack(0)
				else:
					k.deleteLastOp(kwd = f'knit + f{edgeNeedleF}', breakCondition = lambda op: 'knit - ' in op)
					k.deleteLastOp(kwd = f'knit + b{edgeNeedleB}', breakCondition = lambda op: 'knit - ' in op)
					if edgeNeedleF < edgeNeedleB: k.split('+', f'f{edgeNeedleF}', f'b{edgeNeedleF}', c)
					k.split('+', f'b{edgeNeedleB}', f'f{edgeNeedleB}', c)
					if edgeNeedleF > edgeNeedleB: k.split('+', f'f{edgeNeedleF}', f'b{edgeNeedleF}', c)

					k.rack(-gauge)
					if edgeNeedleF < edgeNeedleB: #?
						k.tuck('+', f'f{edgeNeedleB+1}', c)
						k.tuck('+', f'b{edgeNeedleB+2+gauge}', c)
					
					k.xfer(f'f{edgeNeedleB}', f'b{edgeNeedleB+gauge}')

					if edgeNeedleF < edgeNeedleB:
						k.drop(f'b{edgeNeedleB+2+gauge}')
						k.drop(f'f{edgeNeedleB+1}')
					
					k.rack(gauge)
					if edgeNeedleF > edgeNeedleB:
						k.tuck('+', f'b{edgeNeedleF+1}', c) #?
						k.tuck('+', f'f{edgeNeedleF+2+gauge}', c) #?

					k.xfer(f'b{edgeNeedleF}', f'f{edgeNeedleF+gauge}')

					if edgeNeedleF > edgeNeedleB:
						k.drop(f'f{edgeNeedleF+2+gauge}') #?
						k.drop(f'b{edgeNeedleF+1}') #?

					k.rack(0)
					#TODO: make sure it knits on 1 in from new edgeNeedle in next pass	
			elif (count//gauge == 2):
				print('#TODO')

		k.speedNumber(speedNumber)
	else: #just twisted stitches
		if side == 'l': #left side
			for n in range(edgeNeedle-1, edgeNeedle-count-1, -1):
				if f'f{n}' not in emptyNeedles and (gauge == 1 or n % gauge == 0): twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles and (gauge == 1 or (n+1) % gauge == 0): twistedStitches.append(f'b{n}')
		else: #right side
			for n in range(edgeNeedle+1, edgeNeedle+count+1):
				if f'f{n}' not in emptyNeedles and (gauge == 1 or n % gauge == 0): twistedStitches.append(f'f{n}')
				if f'b{n}' not in emptyNeedles and (gauge == 1 or (n+1) % gauge == 0): twistedStitches.append(f'b{n}')

	return newEdgeNeedle, twistedStitches


#------------------------------------------------------------------------
#--- IMAGE PROCESSING / KNITTING WITH KNITOUT FOR CACTUS-ESQUE THINGS ---
#------------------------------------------------------------------------

#--- FUNCTION TO PROCESS/ANALYZE IMAGE AND OUTPUT KNITOUT ---
def shapeImgToKnitout(k, imagePath='graphics/knitMap.png', gauge=1, scale=1, maxShortrowCount=1, addBindoff=True, excludeCarriers=[]):
	'''
	*k is knitout Writer
	*imagePath is the path to the image that contains the piece data
	*gauge is gauge

	- Reads an image (black and white) and generates an array of rows containing pixel sub-arrays that either have the value 0 (black) or 255 (white)
	- Goes through each row and separates each chunk of black pixels into sections (based on whether there is white space separating sections of black pixels)
	- Goes through rows again and assigns a carrier to each section, allowing for shortrowing; information is stored in 'pieceMap', with lists containing tuples for each section -- e.g. pieceMap[0] = [(1, [1, 2, 3]), (2, [10, 11, 12])] means row 0 uses carrier 1 on needles 1,2,3 and carrier 2 on needles 10,11,12
	- Finally, outputs a 'visualization' (just for, ya know, visualization purposes) with 0 being white space, and knitted mass indicated by carrier number
	'''

	#1. Read image data from input path; resize based on gauge
	imageData = io.imread(imagePath)
	if scale != 1: imageData = resize(imageData, (imageData.shape[0]*scale, imageData.shape[1]*scale), anti_aliasing=True) #scale image according to passed 'scale' value

	if gauge > 1: imageData = resize(imageData, (imageData.shape[0]*gauge, imageData.shape[1]), anti_aliasing=True) #scale gauge vertically to elongate image, if gauge > 1
	imageData = np.flipud(imageData) #so going from bottom to top

	width = len(imageData[0])
	carrierCount = 1
	emptyNeedles = []

	if gauge > 1:
		width = (width*gauge)+1
		for n in range(0, width):
			if n % gauge == 0: emptyNeedles.append(f'b{n}')
			elif (n-1) % gauge == 0: emptyNeedles.append(f'f{n}')
			else:
				emptyNeedles.append(f'f{n}')
				emptyNeedles.append(f'b{n}')

	# print('\nimageData:') #remove
	# print(imageData) #remove

	class SectionInfo: #class for keeping track of section info
		def __init__(self, c):
			self.c = c #carrier used in section (constant)
			self.leftN = None #changing property based on left-most needle in section, used as reference when deciding which carrier to assign to a given section in the next row (same for rightN below)
			self.rightN = None

	#2. Go through ndarray data and separate it into sections represented by lists containing respective needles (i.e. multiple sections if shortrowing)
	rows = [] #list for storing row-wise section data
	rowsEdgeNeedles = []

	castonLeftN = None
	castonRightN = None

	for r in range(0, len(imageData)):
		leftmostN = None

		row = []
		section = []

		for n in range(0, len(imageData[r])):
			if imageData[r][n] == 0:
				if leftmostN is None: leftmostN = n

				section.append(n)

				if n == len(imageData[r]) - 1:
					row.append(section)
					if len(row) > carrierCount: carrierCount = len(row)

					if r > 0 and r < (len(imageData)-1) and len(rows[len(rows)-1]) < len(rows[len(rows)-2]) and carrierCount >= len(rows[len(rows)-2]): #if necessary, split prev row [-1] into multiple sections (based on number of sections in prev row to that [-2]) if current carrierCount >= # of sections in [-2]
						minus1Needles = rows[len(rows)-1]
						minus2Needles = rows[len(rows)-2]
						startPt = 1
						for n2 in range(startPt, len(minus2Needles)):
							for n1 in range(0, len(minus1Needles)):
								for i in range(1, len(minus1Needles[n1])):
									if minus2Needles[n2][0] == minus1Needles[n1][i]:
										minus1Needles[n1:n1+1] = minus1Needles[n1][:i], minus1Needles[n1][i:]
										startPt += 1
										break

					rowsEdgeNeedles.append([leftmostN, n])

					rows.append(row)
			else:
				if len(section) == 0: continue
				else:
					rowsEdgeNeedles.append([leftmostN, section[len(section)-1]]) #TODO: determine if still need this

					row.append(section)
					section = []
					newSection = False
					for x in range(n, len(imageData[r])):
						if imageData[r][x] == 0:
							n = x
							newSection = True
							break

					if not newSection: #very last section
						if r == 0: castonLeftN, castonRightN = convertGauge(gauge, row[0][0], row[0][len(row[0])-1])

						if len(row) > carrierCount: carrierCount = len(row)

						if r > 0 and r < (len(imageData)-1) and len(rows[len(rows)-1]) < len(rows[len(rows)-2]) and carrierCount >= len(rows[len(rows)-2]): #if necessary, split prev row [-1] into multiple sections (based on number of sections in prev row to that [-2]) if current carrierCount >= # of sections in [-2]
							startPt = 1
							minus1Needles = rows[len(rows)-1]
							minus2Needles = rows[len(rows)-2]
							for n2 in range(startPt, len(minus2Needles)):
								for n1 in range(0, len(minus1Needles)):
									for i in range(1, len(minus1Needles[n1])):
										if minus2Needles[n2][0] == minus1Needles[n1][i]:
											minus1Needles[n1:n1+1] = minus1Needles[n1][:i], minus1Needles[n1][i:]
											startPt += 1
											break

						rows.append(row)
						break #go to next row


	#3. Go through rows data and assign carriers to each section
	sections = [] #list for storing SectionInfo

	carrierOrder = [] #list for storing carrier order, helpful when want a certain carrier to be used e.g. always on left (will change if > 2 sections in piece)
	for cs in range(0, carrierCount): #initialize sections (but won't add leftN & rightN until later)
		if str(cs) in excludeCarriers: #new #check
			ec = cs + 1
			while ec < 6:
				if str(ec) in excludeCarriers:
					ec += 1
				else:
					cs = ec
					break
		
		sections.append(SectionInfo(cs + 1))
		carrierOrder.append(str(cs+1)) #carrierOrder starts out as just [1, 2, 3]

	availableCarriers = []
	for cs in range(6, carrierCount, -1):
		if str(cs) not in excludeCarriers: availableCarriers.append(str(cs))

	wasteWeightCarriers = []

	print('OG availableCarriers:', availableCarriers) #remove

	shortrowLeftPrep = [idx for idx, element in enumerate(rows) if len(element) > 1] #here we check if the piece contains > 2 sections in any given row and then, if so, assigns index of that row #TODO: make sure this is possible/effective for multiple left sections

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

	else: shortrowLeftPrep = False #if the piece doesn't contain > 2 sections in any row

	print('shortrowLeftPrep:', shortrowLeftPrep) #remove

	pieceMap = [] #list for storing overarching carrier/needles data for rows/sections

	#now finally going through rows

	mainCSection = 0 #might be redefined
	rightCarriers = [] #carriers to the right of main carrier

	firstNeedles = {}

	wasteWeights = {}
	wasteBoundaryExpansions = {}

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

				if r != shortrowLeftPrep and (leftN < sections[s].leftN and rightN < sections[s].leftN) or (leftN > sections[s].rightN and rightN > sections[s].rightN):
					continue #prev leftN & rightN for this carrier doesn't align with leftN & rightN of current section, so continue searching
				else: #it's a match! (or time for shortrowLeftPrep)
					if i == 0 and r == shortrowLeftPrep: #if it's the row before the 1st actual shortrow for shortrowLeft, update carrierOrder so this for loop checks that carrier first & it remains on the left
						prevSectionStart = sections[s].leftN
						if prevSectionStart - leftN > 2:
							if not r in wasteWeights: wasteWeights[r] = dict()
							wasteWeightCarrier = None
							wasteWeightLeftCs = [idx for idx, wasteCarrier in enumerate(wasteWeightCarriers) if wasteCarrier not in rightCarriers]
							if len(wasteWeightLeftCs): wasteWeightCarrier = wasteWeightCarriers[wasteWeightLeftCs[0]]
							else:
								wasteWeightCarrier = availableCarrierCheck(carrierOrder, wasteWeightCarriers)
								if wasteWeightCarrier is None:
									wasteWeightCarrier = availableCarriers.pop()
									wasteWeightCarriers.append(wasteWeightCarrier)

							if r - wasteWeightsRowCount > 0: pStart = r - wasteWeightsRowCount
							else: pStart = 0

							wasteRightBoundary = None
							expandBoundaryRow = None
							for p in range(pStart, r): #to make sure wasteWeights aren't knitted on taken needles
								if carrierOrder[s] in pieceMap[p]:
									relevantSection = pieceMap[p][carrierOrder[s]]
									sectionLeftN = relevantSection[0]
									if wasteRightBoundary is None or sectionLeftN <= wasteRightBoundary:
										expandBoundaryRow = None
										wasteRightBoundary = sectionLeftN-1
									elif sectionLeftN-1 > wasteRightBoundary and expandBoundaryRow is None: expandBoundaryRow = p
							if expandBoundaryRow is not None:
								if expandBoundaryRow in wasteBoundaryExpansions: wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, rightN=prevSectionStart-1)
								else:
									wasteBoundaryExpansions[expandBoundaryRow] = {}
									wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, rightN=prevSectionStart-1)

							wasteWeights[r][wasteWeightCarrier] = {'left': list(convertGauge(gauge, leftN, wasteRightBoundary))}
							if wasteWeightCarrier not in firstNeedles: firstNeedles[wasteWeightCarrier] = list(convertGauge(gauge, wasteRightBoundary+1, rightN))

						carrierOrder.insert(0, carrierOrder.pop(carrierCount-1)) #move shortrowLeft carrier to front of carrierOrder list
						sections.insert(0, sections.pop(carrierCount-1)) #move section to correct location too so can be referenced by index (s) correctly
						firstNeedles[carrierOrder[0]] = list(convertGauge(gauge, rowsEdgeNeedles[r][0], rowsEdgeNeedles[r][1]))
						for o in range(0, len(carrierOrder)):
							if carrierOrder[o] == '1':
								mainCSection = o
								break
					else:
						if sections[s].leftN - leftN > 2: #TODO: test which number should be for >
							if not r in wasteWeights: wasteWeights[r] = dict()
							wasteWeightCarrier = None
							wasteWeightLeftCs = [idx for idx, wasteCarrier in enumerate(wasteWeightCarriers) if wasteCarrier not in rightCarriers]
							if len(wasteWeightLeftCs): wasteWeightCarrier = wasteWeightCarriers[wasteWeightLeftCs[0]]
							else:
								wasteWeightCarrier = availableCarrierCheck(carrierOrder, wasteWeightCarriers)
								if wasteWeightCarrier is None:
									wasteWeightCarrier = availableCarriers.pop()
									wasteWeightCarriers.append(wasteWeightCarrier)
							
							if r - wasteWeightsRowCount > 0: pStart = r - wasteWeightsRowCount
							else: pStart = 0

							wasteRightBoundary = None
							expandBoundaryRow = None
							for p in range(pStart, r): #to make sure wasteWeights aren't knitted on taken needles
								if carrierOrder[s] in pieceMap[p]:
									relevantSection = pieceMap[p][carrierOrder[s]]
									sectionLeftN = relevantSection[0]
									if wasteRightBoundary is None or sectionLeftN <= wasteRightBoundary:
										expandBoundaryRow = None
										wasteRightBoundary = sectionLeftN-1
									elif sectionLeftN-1 > wasteRightBoundary and expandBoundaryRow is None: expandBoundaryRow = p
							if expandBoundaryRow is not None:
								if expandBoundaryRow in wasteBoundaryExpansions: wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, rightN=prevSectionStart-1)
								else:
									wasteBoundaryExpansions[expandBoundaryRow] = {}
									wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, rightN=sections[s].leftN-1)

							wasteWeights[r][wasteWeightCarrier] = {'left': list(convertGauge(gauge, leftN, wasteRightBoundary))}
							if wasteWeightCarrier not in firstNeedles: firstNeedles[wasteWeightCarrier] = list(convertGauge(gauge, wasteRightBoundary+1, rightN))

						if rightN - sections[s].rightN > 2:
							if not r in wasteWeights: wasteWeights[r] = dict()
							wasteWeightCarrier = None
							wasteWeightRightCs = [idx for idx, wasteCarrier in enumerate(wasteWeightCarriers) if wasteCarrier in rightCarriers]
							if len(wasteWeightRightCs):
								wasteWeightCarrier = wasteWeightCarriers[wasteWeightRightCs[0]]
							else:
								wasteWeightCarrier = availableCarrierCheck(carrierOrder, wasteWeightCarriers)
								if wasteWeightCarrier is None:
									wasteWeightCarrier = availableCarriers.pop()
									wasteWeightCarriers.append(wasteWeightCarrier)
									rightCarriers.append(wasteWeightCarrier)
							
							if r - wasteWeightsRowCount > 0: pStart = r - wasteWeightsRowCount
							else: pStart = 0
							wasteLeftBoundary = None
							expandBoundaryRow = None
							for p in range(pStart, r): #to make sure wasteWeights aren't knitted on taken needles
								if carrierOrder[s] in pieceMap[p]:
									relevantSection = pieceMap[p][carrierOrder[s]]
									sectionRightN = relevantSection[len(relevantSection)-1]
									if wasteLeftBoundary is None or sectionRightN >= wasteLeftBoundary: # >= #?
										expandBoundaryRow = None
										wasteLeftBoundary = sectionRightN+1
									elif sectionRightN+1 < wasteLeftBoundary and expandBoundaryRow is None: expandBoundaryRow = p
							if expandBoundaryRow is not None:
								if expandBoundaryRow in wasteBoundaryExpansions: wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, leftN=sections[s].rightN+1)
								else:
									wasteBoundaryExpansions[expandBoundaryRow] = {}
									wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, leftN=sections[s].rightN+1)

							wasteWeights[r][wasteWeightCarrier] = {'right': list(convertGauge(gauge, wasteLeftBoundary, rightN))}
							if wasteWeightCarrier not in firstNeedles: firstNeedles[wasteWeightCarrier] = list(convertGauge(gauge, leftN, wasteLeftBoundary-1))

					sections[s].leftN = leftN
					sections[s].rightN = rightN
					rowMap[carrierOrder[s]] = rows[r][i]
					taken.append(s)
					match = True
					break

			if not match: #need to use unusedC and add new carrier for shortrowing
				if carrierOrder[unusedC] != '1':
					firstNeedles[carrierOrder[unusedC]] = list(convertGauge(gauge, rowsEdgeNeedles[r][0], rowsEdgeNeedles[r][1]))
					if leftN > sections[mainCSection].rightN: rightCarriers.append(carrierOrder[unusedC])

					lastRowMapKeys = list(pieceMap[r-1].keys())
					prevSectionEnd = pieceMap[r-1][lastRowMapKeys[len(lastRowMapKeys)-1]] #last needle of last section
					prevSectionEnd = prevSectionEnd[len(prevSectionEnd)-1]

					if rightN - prevSectionEnd > 2:
						if not r in wasteWeights: wasteWeights[r] = dict()
						wasteWeightCarrier = None
						wasteWeightRightCs = [idx for idx, wasteCarrier in enumerate(wasteWeightCarriers) if wasteCarrier in rightCarriers]
						if len(wasteWeightRightCs):
							wasteWeightCarrier = wasteWeightCarriers[wasteWeightRightCs[0]]
						else:
							wasteWeightCarrier = availableCarrierCheck(carrierOrder, wasteWeightCarriers)
							if wasteWeightCarrier is None:
								wasteWeightCarrier = availableCarriers.pop()
								wasteWeightCarriers.append(wasteWeightCarrier)
								rightCarriers.append(wasteWeightCarrier)
						
						if r - wasteWeightsRowCount > 0: pStart = r - wasteWeightsRowCount
						else: pStart = 0
						wasteLeftBoundary = None
						expandBoundaryRow = None
						for p in range(pStart, r): #to make sure wasteWeights aren't knitted on taken needles
							if carrierOrder[s] in pieceMap[p]:
								relevantSection = pieceMap[p][carrierOrder[s]]
								sectionRightN = relevantSection[len(relevantSection)-1]
							if wasteLeftBoundary is None or sectionRightN >= wasteLeftBoundary:
								wasteLeftBoundary = sectionRightN+1
							elif sectionRightN+1 < wasteLeftBoundary and expandBoundaryRow is None: expandBoundaryRow = p
						if expandBoundaryRow is not None:
							if expandBoundaryRow in wasteBoundaryExpansions: wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, leftN=sections[s].rightN+1)
							else:
								wasteBoundaryExpansions[expandBoundaryRow] = {}
								wasteBoundaryExpansions[expandBoundaryRow][wasteWeightCarrier] = convertGauge(gauge, leftN=sections[s].rightN+1)

						wasteWeights[r][wasteWeightCarrier] = {'right': list(convertGauge(gauge, wasteLeftBoundary, rightN))}
						if wasteWeightCarrier not in firstNeedles: firstNeedles[wasteWeightCarrier] = list(convertGauge(gauge, leftN, wasteLeftBoundary-1))

				taken.append(unusedC)
				sections[unusedC].leftN = leftN
				sections[unusedC].rightN = rightN
				rowMap[carrierOrder[unusedC]] = rows[r][i]

		pieceMap.append(rowMap)

	# print('\npieceMap:') #remove
	# print(pieceMap) #remove

	wasteWeightsKeys = list(wasteWeights.keys())

	print('wasteBoundaryExpansions:', wasteBoundaryExpansions) #remove

	print('rightCarriers:', rightCarriers) #remove

	print('firstNeedles:', firstNeedles) #remove

	print('wasteWeights:', wasteWeights) #remove

	print('availableCarriers leftover:', availableCarriers) #remove

	#5. Add waste section and cast-on
	wasteWeightsLeft = [wc for wc in wasteWeights.values() if any('left' in ws for ws in wc.values())]
	wasteWeightsRight = [wc for wc in wasteWeights.values() if any('right' in ws for ws in wc.values())]

	print('wasteWeightsLeft:', wasteWeightsLeft, len(wasteWeightsLeft)) #remove
	print('wasteWeightsRight:', wasteWeightsRight, len(wasteWeightsRight)) #remove

	def assignWasteDraw(right=False):
		if len(availableCarriers):
			assignedC = availableCarriers.pop()
			wasteWeightCarriers.append(assignedC)
			if right: rightCarriers.append(assignedC)
			# if right: #remove #? v
			# 	rightCarriers.append(assignedC)
			# 	firstNeedles[assignedC] = wasteWeightsRight[0][list(wasteWeightsRight[0].keys())[0]]['right']
			# else: wasteWeightsLeft[0][list(wasteWeightsLeft[0].keys())[0]]['left']

			firstNeedles[assignedC] = [0, width] #remove #? ^

			return assignedC
		else: return None

	if len(wasteWeightsRight) > len(wasteWeightsLeft):
		wasteWeightsDrawRight = assignWasteDraw(True)
		if len(wasteWeightsLeft): wasteWeightsDrawLeft = assignWasteDraw()
	else:
		wasteWeightsDrawLeft = assignWasteDraw()
		if len(wasteWeightsRight): wasteWeightsDrawRight = assignWasteDraw(True)

	otherCs = []
	if carrierCount > 2:
		for c in range(3, carrierCount+1):
			otherCs.append(f'{c}')
	otherCs.extend(wasteWeightCarriers)

	if ((castonRightN/gauge)-(castonLeftN/gauge) < 16): catchMaxNeedles = True #TODO: have it be is it is < 4 when divided by carriers length (but >= 16 otherwise), have it treat it as len(carriers)/2
	else: catchMaxNeedles = False

	# if (((castonRightN/gauge)-(castonLeftN/gauge))//(6-len(availableCarriers)) < 4): catchMaxNeedles = True #check len(otherCs)+2 #? < 4 #?
	# else: catchMaxNeedles = False

	wasteRightCarriers = rightCarriers.copy()

	if gauge == 1: closedCaston = False
	else:
		wasteRightCarriers.append('1') #have wasteSection func put main carrier (aka caston carrier) on right, side doing closedTubeCaston, so it will actually end on left (since closedTubeCaston is only one pass)
		closedCaston = True

	wasteSection(k=k, leftN=castonLeftN, rightN=castonRightN, closedCaston=closedCaston, otherCs=otherCs, gauge=gauge, endOnRight=wasteRightCarriers, firstNeedles=firstNeedles, catchMaxNeedles=catchMaxNeedles)

	if closedCaston: closedTubeCaston(k, castonRightN, castonLeftN, '1', gauge)
	else: openTubeCaston(k, castonLeftN, castonRightN, '1', gauge)

	#5. Convert generated data to knitout; also generate visualization of pieceMap data so can see what it would actually look like (0 == whitespace, other numbers == stitch knit with respective carrier number)
	visualization = [] #list for storing visualization

	#TODO: check what max short row count is that the kniterate can handle

	extraCarriersIn = []
	# takeOutAtEnd = [] #remove

	sectionIdx = 0
	shortrowCount = 0
	endPoints = []

	r = 0

	while r < len(pieceMap):
		sectionCount = len(pieceMap[r]) #number of sections in this row
		mapKeys = list(pieceMap[r].keys()) #carriers used in this row #check #new location #* ^

		if (r+1) < len(pieceMap)-1 and (sectionCount < len(pieceMap[r+1]) or sectionCount > len(pieceMap[r+1])): sectionCountChangeNext = True
		else: sectionCountChangeNext = False #check #new location #* ^

		if sectionIdx == 0 and shortrowCount == 0: #check #new #*
		# if sectionIdx == 0: #go back! #? or #remove #? #*
			
			# wasteIdx = 0 #*#*
			# wasteRowCount = 0 #*#*
			# rs = r #*#*
			# while rs < r+maxShortrowCount: #*#* 
			for rs in range(r, r+maxShortrowCount): #indent below == #new # +1 #? #remove#*#*
				if (rs+1) < len(pieceMap)-1 and (sectionCount < len(pieceMap[rs+1]) or sectionCount > len(pieceMap[rs+1])): break #check

				wasteMatches = [w for w in wasteWeights if w-rs <= wasteWeightsRowCount and w-rs >= 0] #TODO: ensure 20 rows is enough for rollers to catch
				# wasteSectionCount = len(wasteMatches) #new #check #*#*

				if len(wasteMatches):
					boundaryExpansions = []
					if len(wasteBoundaryExpansions) and rs-1 in wasteBoundaryExpansions: boundaryExpansions = wasteBoundaryExpansions[rs-1]

					takenNeedles = []
					for s in pieceMap[rs]:
						for n in pieceMap[rs][s]:
							takenNeedles.append(n*gauge)

					skip = []
					for wr in wasteMatches: #go through row keys to knit on needles that have currently active wasteWeights sections
						# print('!!!', wasteMatches[wasteIdx], wasteWeights[wasteMatches[wasteIdx]]) #remove #*#*
						wasteMatchIdx = wasteMatches.index(wr)

						addCaston = False #only for wr, not addons (this too v)
						addDraw = False
						if wr-rs == wasteWeightsRowCount or rs == 0: addCaston = True
						elif rs == wr: addDraw = True

						for wc in wasteWeights[wr]:
							waste = wasteWeights[wr][wc]

							takeWcOut = True
							for wk in range(wasteWeightsKeys.index(wr)+1, len(wasteWeightsKeys)):
								if wc in wasteWeights[wasteWeightsKeys[wk]]: takeWcOut = False

							if 'left' in waste:
								needles = waste['left'].copy()

								lastSection = waste['left']

								inBetweenNeedles = []

								castonNeedles = []
								drawNeedles = []
								drawMiss = None

								if addCaston:
									for n in range(needles[0], needles[1]+1):
										if n not in takenNeedles: castonNeedles.append(n)
								elif addDraw:
									drawMiss = needles[1]+1
									for n in range(needles[0], needles[1]+1): drawNeedles.append(n)
								
								if needles not in skip: #aka if not added to previous wasteWeights section 								
									if wasteMatchIdx < len(wasteMatches)-1:
										addonMatches = [w for w in wasteMatches if wasteMatches.index(w) > wasteMatchIdx and wc in wasteWeights[w] and 'left' in wasteWeights[w][wc]]

										if len(addonMatches):
											lastSection = wasteWeights[addonMatches[len(addonMatches)-1]][wc]['left'] #keep track of right-most section if adding on sections
											for a in addonMatches:
												addonLeftN = wasteWeights[a][wc]['left'][0]
												addonRightN = wasteWeights[a][wc]['left'][1]

												if addonLeftN - needles[1] > 1: #identify needles in-between sections so don't knit on them
													for n in range(needles[1]+1, addonLeftN):
														inBetweenNeedles.append(n)
												
												if a-rs == wasteWeightsRowCount or rs == 0: #add to caston needles
													for n in range(addonLeftN, addonRightN+1):
														if n not in takenNeedles: castonNeedles.append(n)
												elif rs == a: #add to draw thread needles
													drawMiss = addonRightN+1
													for n in range(addonLeftN, addonRightN+1): drawNeedles.append(n)

												needles[1] = addonRightN #change right-most needle to right-most needle in add-on sections (keep doing until last)
												skip.append(wasteWeights[a][wc]['left']) #skip this one when looping again since already taking care of it here
						
									if len(castonNeedles):
										if addCaston: #meaning first wasteWeights section has a caston
											k.miss('+', f'f{needles[1]+1}', wc)
											tempMissOut(k, width, '-') #move carriage out of the way
											k.pause(f'C{wc} R of N{needles[1]+1}?') #remove #?
										k.rack(0.25)
										for n in reversed(castonNeedles):
											k.knit('-', f'b{n}', wc)
											k.knit('-', f'f{n}', wc)
										k.rack(0)

									if len(drawNeedles) and wasteWeightsDrawLeft is not None: #do this before knitting so it's secure
										k.miss('-', f'f{needles[0]-1}', wasteWeightsDrawLeft) 
										k.pause(f'fix slack on draw C{wasteWeightsDrawLeft}')

									for n in range(needles[0], needles[1]+1):
										if n not in takenNeedles and n not in inBetweenNeedles: #interlock
											if n % 2 == 0: k.knit('+', f'f{n}', wc)
											else: k.knit('+', f'b{n}', wc)

									if wc in boundaryExpansions:
										lastSection[1] = boundaryExpansions[wc]
										k.rack(0.25)
										for n in range(needles[1]+1, lastSection[1]+1):
											if n not in takenNeedles:
												k.knit('+', f'f{n}', wc)
												k.knit('+', f'b{n}', wc)
										k.rack(0)
										needles[1] = lastSection[1]

									for n in range(needles[1], needles[0]-1, -1):
										if n not in takenNeedles and n not in inBetweenNeedles: #interlock
											if n % 2 != 0: k.knit('-', f'f{n}', wc)
											else: k.knit('-', f'b{n}', wc)

									if len(drawNeedles):
										k.rack(0.25) #so can drop on front & back bed at same time #check if necessary
										for n in drawNeedles: #pos so carriage isn't in the way of placing draw carrier
											k.drop(f'b{n}')
											if f'f{n}' in emptyNeedles: k.drop(f'f{n}')
										k.rack(0) #check^

										if takeWcOut: tempMissOut(k, width, '-', wc, 6)

										if wasteWeightsDrawLeft is None:
											tempMissOut(k, width, '-') #move *carriage* out of way
											k.pause(f'manual draw thread over C{wc}') #find which ones by dropped #TODO: determine if manual draw thread is even necessary (is caston enough?)
										else:
											for n in drawNeedles:
												if f'f{n}' not in emptyNeedles: k.knit('+', f'f{n}', wasteWeightsDrawLeft)

											tempMissOut(k, width, '-', wasteWeightsDrawLeft, 4)


							if 'right' in waste: #right side
								needles = waste['right'].copy()

								inBetweenNeedles = []

								castonNeedles = []
								drawNeedles = []
								drawMiss = None

								if addCaston:
									for n in range(needles[0], needles[1]+1):
										if n not in takenNeedles: castonNeedles.append(n)
								elif addDraw:
									drawMiss = needles[1]+1
									for n in range(needles[0], needles[1]+1): drawNeedles.append(n)
								
								if needles not in skip: #aka if not added to previous wasteWeights section 								
									if wasteMatchIdx < len(wasteMatches)-1:
										addonMatches = [w for w in wasteMatches if wasteMatches.index(w) > wasteMatchIdx and wc in wasteWeights[w] and 'right' in wasteWeights[w][wc]]

										if len(addonMatches):
											for a in addonMatches:
												addonLeftN = wasteWeights[a][wc]['right'][0]
												addonRightN = wasteWeights[a][wc]['right'][1]

												if addonLeftN - needles[1] > 1: #identify needles in-between sections so don't knit on them
													for n in range(needles[1]+1, addonLeftN):
														inBetweenNeedles.append(n)
												
												if a-rs == wasteWeightsRowCount or rs == 0: #add to caston needles
													for n in range(addonLeftN, addonRightN+1):
														if n not in takenNeedles: castonNeedles.append(n)
												elif rs == a: #add to draw thread needles
													drawMiss = addonRightN+1
													for n in range(addonLeftN, addonRightN+1): drawNeedles.append(n)

												needles[1] = addonRightN #change right-most needle to right-most needle in add-on sections (keep doing until last)
												skip.append(wasteWeights[a][wc]['right']) #skip this one when looping again since already taking care of it here

									if len(castonNeedles):
										if addCaston: #meaning first wasteWeights section has a caston
											k.miss('-', f'f{needles[0]-1}', wc)
											tempMissOut(k, width, '+') #move carriage out of the way
											k.pause(f'C{wc} L of N{needles[0]-1}?') #remove #?
										k.rack(0.25)
										for n in castonNeedles:
											k.knit('+', f'f{n}', wc)
											k.knit('+', f'b{n}', wc)
										k.rack(0)

									if len(drawNeedles) and wasteWeightsDrawRight is not None: #do this before knitting so it's secure #TODO: determine if changing the drawDir makes it more secure
										k.miss('+', f'f{drawMiss}', wasteWeightsDrawRight)
										k.pause(f'fix slack on draw C{wasteWeightsDrawRight}')

									for n in range(needles[1], needles[0]-1, -1):
										if n not in takenNeedles and n not in inBetweenNeedles: #interlock
											if n % 2 == 0: k.knit('-', f'b{n}', wc)
											else: k.knit('-', f'f{n}', wc)

									if wc in boundaryExpansions:
										waste['right'][0] = boundaryExpansions[wc]
										k.rack(0.25)
										for n in range(needles[0]-1, waste['right'][0]-1, -1):
											if n not in takenNeedles and n not in inBetweenNeedles:
												k.knit('-', f'b{n}', wc)
												k.knit('-', f'f{n}', wc)
										k.rack(0)
										needles[0] = waste['right'][0]

									for n in range(needles[0], needles[1]+1):
										if n not in takenNeedles and n not in inBetweenNeedles: #interlock
											if n % 2 != 0: k.knit('+', f'b{n}', wc)
											else: k.knit('+', f'f{n}', wc)

									if len(drawNeedles):
										k.rack(0.25) #so can drop on front & back bed at same time #check #v
										for n in reversed(drawNeedles): #neg (reversed) so carriage isn't in the way of placing draw carrier
											k.drop(f'b{n}')
											if f'f{n}' in emptyNeedles: k.drop(f'f{n}')
										k.rack(0) #^

										if takeWcOut: tempMissOut(k, width, '+', wc, 6)

										if wasteWeightsDrawRight is None:
											tempMissOut(k, width, '+') #move *carriage* out of way
											k.pause(f'manual draw thread over C{wc}') #find which ones by dropped #TODO: determine if manual draw thread is even necessary (is caston enough?)
										else:
											for n in reversed(drawNeedles):
												if f'f{n}' not in emptyNeedles: k.knit('-', f'f{n}', wasteWeightsDrawRight)
											
											tempMissOut(k, width, '+', wasteWeightsDrawRight, 4)

				# rs += 1 #*#* v
				# wasteRowCount += 1

				# nextWasteSectionCount = len([w for w in wasteWeights if w-(rs+1) <= wasteWeightsRowCount and w-(rs+1) >= 0])
				# if (rs+1) < len(pieceMap)-1 and (wasteSectionCount < nextWasteSectionCount or sectionCount > nextWasteSectionCount): wasteSectionCountChangeNext = True
				# else: wasteSectionCountChangeNext = False #check #new #*

				# if wasteIdx < wasteSectionCount-1: #check
				# 	if wasteSectionCountChangeNext:
				# 		wasteIdx += 1
				# 		rs -= wasteRowCount
				# 		wasteRowCount = 0
				# 	elif wasteRowCount == maxShortrowCount:
				# 		wasteRowCount = 0
				# 		wasteIdx += 1
				# 		rs -= maxShortrowCount
				# else:
				# 	if wasteSectionCountChangeNext or wasteRowCount == maxShortrowCount:
				# 		wasteRowCount = 0
				# 		wasteIdx = 0 #*#* ^
			

		if sectionIdx == 0:
			visualization.append([])
			n0 = 0 #for whitespace (just for visualization, not knitout)
		else: n0 = endPoints.pop(0)
		# sectionCount = len(pieceMap[r]) #number of sections in this row
		# mapKeys = list(pieceMap[r].keys()) #carriers used in this row #go back! #? or #remove #? #* ^

		carrier = mapKeys[sectionIdx]
		needles = pieceMap[r][mapKeys[sectionIdx]]

		k.comment(f'row: {r+1} (section {sectionIdx+1}/{sectionCount})')

		dir1 = '+' #left side
		if carrier in rightCarriers: dir1 = '-' #right side

		prevLeftN = None
		prevRightN = None
		xferL = 0
		xferR = 0

		twistedStitches = [] #might use later on if increasing

		n1, n2 = convertGauge(gauge, needles[0], needles[len(needles) - 1])

		placementPass = []

		sectionFinished = False
		if r == len(pieceMap)-1 or (r < len(pieceMap)-1 and carrier not in pieceMap[r+1]): sectionFinished = True

		if r > 0 and carrier not in pieceMap[r-1]: #means this is a new section #might need to cast some needles on
			if sectionIdx != 0 and sectionIdx != len(mapKeys)-1: #means that it is a new shortrow section that is not on the edge, so need to place carrier in correct spot
				if dir1 == '+': k.miss('+', f'f{n1-1}', carrier)
				else: k.miss('-', f'f{n2+1}', carrier)
				k.pause(f'cut C{carrier}')


			#TODO: maybe remove this, it might never be needed (doesn't look like there is need for caston) #actually, go for if need to increase
			prevRowMapKeys = list(pieceMap[r-1].keys())
			prevRowNeedles = range(pieceMap[r-1][prevRowMapKeys[0]][0]*gauge, (pieceMap[r-1][prevRowMapKeys[len(prevRowMapKeys)-1]][len(pieceMap[r-1][prevRowMapKeys[len(prevRowMapKeys)-1]])-1]*gauge)+1)

			newNeedles = []
			needleRange = range(n1, n2+1)
			if dir1 == '-': needleRange = range(n2, n1-1, -1)
			for n in needleRange:
				if n not in prevRowNeedles: newNeedles.append(n)
			if len(newNeedles):
				k.rack(0.25)
				for n in range(0, len(newNeedles)):
					if f'f{newNeedles[n]}' not in emptyNeedles: k.knit(dir1, f'f{n}', carrier)
					if f'b{newNeedles[n]}' not in emptyNeedles: k.knit(dir1, f'b{n}', carrier)
				k.rack(0)

				dir2 = '-'
				needleRange = range(n2, n1-1, -1)
				if dir1 == '-':
					dir2 = '+'
					needleRange = range(n1, n2+1)

				k.comment('back pass to get carrier on correct side')
				for n in range(len(newNeedles)-1, -1, -1): #back pass to get carrier on correct side #check
					if f'b{newNeedles[n]}' not in emptyNeedles: k.knit(dir2, f'b{n}', carrier)

		if r < len(pieceMap)-1 and len(pieceMap[r+1]) > sectionCount and carrier in pieceMap[r+1]:
			futureMapKeys = list(pieceMap[r+1].keys())
			if sectionIdx == 0 and futureMapKeys.index(carrier) != 0: #means new left shortrow section coming
				futureNewSectionNeedles = pieceMap[r+1][futureMapKeys[0]]
				futureNewSectionRightN = convertGauge(gauge, rightN=futureNewSectionNeedles[len(futureNewSectionNeedles)-1])
				placementPass = [n1, futureNewSectionRightN] #knit up until futureLeftN on back bed #TODO: make sure it misses an extra needle here so not in the way #TODO: maybe plan ahead for future part to make up for extra pass on back bed in left shortrow section? #?

		if r > 0 and carrier in pieceMap[r-1]:
			prevNeedles = pieceMap[r-1][carrier]
			prevLeftN, prevRightN = convertGauge(gauge, prevNeedles[0], prevNeedles[len(prevNeedles)-1])

			if sectionCount > len(pieceMap[r-1]): #means new section here
				prevMapKeys = list(pieceMap[r-1].keys())

				if sectionIdx > 0 and mapKeys[sectionIdx-1] not in prevMapKeys: #means new left section was added before this section
					prevSectionEnd = convertGauge(gauge, rightN=pieceMap[r][mapKeys[sectionIdx-1]][len(pieceMap[r][mapKeys[sectionIdx-1]])-1])
					if prevLeftN < prevSectionEnd: prevLeftN = prevSectionEnd+1
				if sectionIdx < len(mapKeys)-1 and mapKeys[sectionIdx+1] not in prevMapKeys: #means new right section will be added after this section
					nextSectionStart = convertGauge(gauge, leftN=pieceMap[r][mapKeys[sectionIdx+1]][0])
					if prevRightN > nextSectionStart: prevRightN = nextSectionStart-1

			xferL = int((prevLeftN - n1)/gauge) #dec/inc on left side (neg if dec)
			xferR = int((n2 - prevRightN)/gauge) #dec/inc on right side (neg if dec)

		def leftShaping():
			if xferL:
				if xferL > 0: #increase
					dummyLeft, twistedLeft = incDoubleBed(k, xferL, prevLeftN, carrier, 'l', gauge, emptyNeedles) #TODO: have option to pass incMethod in main function parameters
					twistedStitches.extend(twistedLeft)
				else: #decrease
					dummyLeft, stackedLoopNeedles = decDoubleBed(k, abs(xferL), prevLeftN, carrier, 'l', gauge, emptyNeedles)
					if dir1 == '-': #rightShaping happened first
						if xferL == -2: notEnoughNeedlesDecCheck(k, prevLeftN, n2-1, carrier, gauge)
					else:
						if xferL == -2 and abs(prevLeftN-(n2-1)) < 8 and xferR < 0: #TODO: #check if it applies for dec by 1 on either side, dec by > 3 on R, and inc (by xfer, ofc)
							knitStacked = []
							for n in stackedLoopNeedles:
								needleNumber = int(n[1:])
								if needleNumber < n1: k.knit('+', n, carrier)
								elif n[0] == 'b' or needleNumber > n2: knitStacked.append(n)
							return knitStacked
			return [] #just return empty list if no knitStacked

		def rightShaping():
			if xferR:
				if xferR > 0:
					dummyRight, twistedRight = incDoubleBed(k, xferR, prevRightN, carrier, 'r', gauge, emptyNeedles)
					twistedStitches.extend(twistedRight)
				else:
					dummyRight, stackedLoopNeedles = decDoubleBed(k, abs(xferR), prevRightN, carrier, 'r', gauge, emptyNeedles)
					if dir1 == '+': #leftShaping happened first
						if xferR == -2: notEnoughNeedlesDecCheck(k, prevRightN-1, n1, carrier, gauge)
					else:
						if xferR == -2 and abs((prevRightN-1)-n1) < 8 and xferL < 0: #TODO: #check if it applies for dec by 1 on either side, dec by > 3 on L, and inc (by xfer, ofc)
							knitStacked = []
							for n in stackedLoopNeedles:
								needleNumber = int(n[1:])
								if needleNumber > n2: k.knit('-', n, carrier)
								elif n[0] == 'f' or needleNumber < n1: knitStacked.append(n)
							return knitStacked
			return [] #just return empty list if no knitStacked

		def backBedPass():
			knitStacked = rightShaping()
			if dir1 == '+' and xferR > 0 and xferR < 3: #so can 1. get twisted stitches in *after* xfers, not before and 2. not have ladder
				for n in range(prevRightN+1, n2+1):
					if f'f{n}' not in emptyNeedles: k.knit('+', f'f{n}', carrier)

			for n in range(n2, n1-1, -1):
				if f'b{n}' not in emptyNeedles and (dir1 == '+' or xferL <= 0 or n >= prevLeftN):
					if n == n2 and f'b{n-gauge}' in twistedStitches: #if edge needle and just increased to it, do twisted stitch first so don't drop edge loop; note that the twisted stitch will be knitted again in next iteration
						k.knit('-', f'b{n-gauge}', carrier) #to be twisted
						k.twist(f'b{n-gauge}', -rollerAdvance) #do twisted stitch now so can add another knit on that needle without additional knit being interpreted as twisted stitch
						twistedStitches.remove(f'b{n-gauge}') #get rid of it since we already twisted it

					k.knit('-', f'b{n}', carrier)

			if len(knitStacked):
				for n in knitStacked:
					k.knit('-', n, carrier)

		for n in range(n0, n1):
			visualization[r].append(0)

		if dir1 == '-':
			backBedPass()
			if (xferL <-2): #so no ladder (carrier is in correct spot to dec)
				for n in range(n1-1, prevLeftN-1, -1):
					if f'b{n}' not in emptyNeedles: k.knit('-', f'b{n}', carrier)

		knitStacked = leftShaping()
		for n in range(n1, n2 + 1):
			visualization[r].append(int(carrier))
			if (dir1 == '-' or xferR <= 0 or n <= prevRightN) and f'f{n}' not in emptyNeedles: #don't add the knits if increasing, since they will be added anyway thru increasing
				if n == n1 and f'f{n+gauge}' in twistedStitches: #if edge needle and just increased to it, do twisted stitch first so don't drop edge loop; note that the twisted stitch will be knitted again in next iteration
					k.knit('+', f'f{n+gauge}', carrier) #to be twisted
					k.twist(f'f{n+gauge}', -rollerAdvance) #do twisted stitch now so can add another knit on that needle without additional knit being interpreted as twisted stitch
					twistedStitches.remove(f'f{n+gauge}') #get rid of it since we already twisted it

				k.knit('+', f'f{n}', carrier)

		if len(knitStacked):
			for n in knitStacked:
				k.knit('+', n, carrier)

		if dir1 == '+' and (xferR < -2): #so no ladder (carrier is in correct spot to dec or inc with yarn)
			for n in range(n2+1, prevRightN+1):
				if f'f{n}' not in emptyNeedles: k.knit('+', f'f{n}', carrier)

		if dir1 == '+': backBedPass()

		if len(placementPass): #if applicable, place middle section carrier by new left-most needle to get it out of the way for new left-most shortrow section in next row
			for n in range(placementPass[0], placementPass[1]+1):
				if f'b{n}' not in emptyNeedles: k.knit('+', f'b{n}', carrier)
			k.miss('+', f'b{placementPass[1]+1}', carrier)

		for bn in twistedStitches:
			k.twist(bn, -rollerAdvance)

		if sectionFinished:
			if addBindoff:
				if dir1 == '+':
					bindSide = 'l'
					bindXferN = n1
				else:
					bindSide = 'r'
					bindXferN = n2
				if closedCaston: halfGaugeOpenBindoff(k, (n2-n1+1), bindXferN, carrier, bindSide)
				else: bindoff(k, (n2-n1+1), bindXferN, carrier, bindSide, emptyNeedles=emptyNeedles)
			else: #drop finish
				outCarriers = []
				if r == len(pieceMap)-1:
					rollOut = True
					outCarriers = carrierOrder.copy()
					outCarriers.extend(wasteWeightCarriers)
					# outCarriers.extend(takeOutAtEnd) #remove
				else: rollOut = False
				dropFinish(k, [n1, n2], [n1, n2], outCarriers, rollOut, emptyNeedles)

		#-------------------------
		n0 = n2 + 1

		if sectionIdx == sectionCount-1:
			for n in range(n0, width):
				row.append(0)
				visualization[r].append(0)
		else: endPoints.append(n0)

		shortrowCount += 1

		r += 1

		# if r < len(pieceMap)-1 and (sectionCount < len(pieceMap[r]) or sectionCount > len(pieceMap[r])): sectionCountChangeNext = True
		# else: sectionCountChangeNext = False #go back! #? or #remove #? #* ^


		if sectionIdx < sectionCount-1:
			if sectionCountChangeNext:
				sectionIdx += 1
				r -= shortrowCount
				shortrowCount = 0
			elif shortrowCount == maxShortrowCount:
				shortrowCount = 0
				sectionIdx += 1
				r -= maxShortrowCount
		else:
			if sectionCountChangeNext or shortrowCount == maxShortrowCount:
				shortrowCount = 0
				sectionIdx = 0
		
		#do it until: maxShortrowCount or sectionCountChangeNext #come back! #*

	if addBindoff: #take out extra carriers if not already done thru dropFinish
		for carrier in wasteWeightCarriers: k.outcarrier(carrier)

	vFile = open('visualization.txt', 'w')
	 
	# print('\nvisualization:') #remove
	for v in visualization:
		for c in v: vFile.write(''.join(str(c)))
		vFile.write('\n')
		# print(v) #remove

	vFile.close()