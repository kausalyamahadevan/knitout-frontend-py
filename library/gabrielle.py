import numpy as np

from skimage import io
# from skimage import data

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


#--- image processing ---

rows = []
# class Section: #remove
# 	def __init__(self, c, needles=[]):
# 		self.c = c
# 		self.needles = needles

sections = []

class SectionInfo:
	def __init__(self, c):
		self.c = c
		self.leftN = None
		self.rightN = None

def generatePieceMap(k, imagePath='graphics/knitMap.png'):
	'''
	- k is knitout Writer
	- imagePath is the path to the image that contains the piece data

	Reads an image (black and white) and generates an array of rows containing pixel sub-arrays that either have the value 0 (black) or 255 (white)

	Goes through each row and separates each chunk of black pixels into sections (based on whether there is white space separating sections of black pixels)

	Goes through rows again and assigns a carrier to each section, allowing for shortrowing; information is stored in 'pieceMap', with lists containing tuples for each section -- e.g. pieceMap[0] = [(1, [1, 2, 3]), (2, [10, 11, 12])] means row 0 uses carrier 1 on needles 1,2,3 and carrier 2 on needles 10,11,12

	Finally, outputs a 'visualization' (just for, ya know, visualization purposes) with 0 being white space, and knitted mass indicated by carrier number

	TODO: keep in mind when converting to knitout: shortrow carrier on right side should have opposite directional pattern and end on right side during waste yarn / initialization (in other words, should go neg pos rather than pos neg for passes in a row)
	'''

	imageData = io.imread(imagePath)
	imageData = np.flipud(imageData) #so going from bottom to top

	width = len(imageData[0])
	carrierCount = 1

	print(imageData) #remove

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
	
	carrierOrder = []
	for cs in range(0, carrierCount):
		sections.append(SectionInfo(cs + 1))
		carrierOrder.append(cs+1)

	pieceMap = []

	# shortrowing = False

	# matches = [x for x in rows if len(x) > 2]
	# shortrowLeft = [idx for idx, element in enumerate(rows) if len(element) > 2][0]
	srLneedleR = None
	shortrowLeft = [idx for idx, element in enumerate(rows) if len(element) > 2]

	if len(shortrowLeft) > 0:
		shortrowLeft = shortrowLeft[0]
		srLneedleR = rows[shortrowLeft][0][len(rows[shortrowLeft][0])-1]
	else: shortrowLeft = False

	for r in range (0, len(rows)):
		rowMap = {}

		# shortrowLeft = (r < len(rows) - 1 and len(rows[r+1]) > 2 and len(rows[r+1]) > len(rows[r]))
		
		# if not shortrowing and len(rows[r]) == 1:
		# 	sections[0].leftN = rows[r][0][0]
		# 	sections[0].rightN = rows[r][0][len(rows[r][0]) - 1]
		# 	pieceMap.append([tuple([1, rows[r][0]])])
		# else:
		# 	shortrowing = True
		taken = []
		for i in range (0, len(rows[r])):
			leftN = rows[r][i][0]
			rightN = rows[r][i][len(rows[r][i]) - 1]

			match = False
			unusedC = None
			for s in range(0, carrierCount):
				if s in taken: continue
				if sections[s].leftN is None:
					if unusedC is None: unusedC = s
					continue

				if (leftN < sections[s].leftN and rightN < sections[s].leftN) or (leftN > sections[s].rightN and rightN > sections[s].rightN):
					continue #shortrow, different section
				else:
					if i == 0 and shortrowLeft and leftN <= srLneedleR:
						section1 = []
						section2 = []
						for n in range(leftN, rightN+1):
							if n <= srLneedleR: section1.append(n)
							else: section2.append(n)

						unusedC = carrierOrder[carrierCount-1]

						rowMap[unusedC] = section1
						sections[carrierCount-1].leftN = leftN
						sections[carrierCount-1].rightN = srLneedleR
						taken.append(unusedC)

						rowMap[carrierOrder[s]] = section2
						sections[s].leftN = srLneedleR+1
						sections[s].rightN = rightN

						if r == shortrowLeft-1:
							carrierOrder.insert(0, carrierOrder.pop(carrierCount-1)) #move left carrier to front
							sections.insert(0, sections.pop(carrierCount-1)) #move section to correct location too
							shortrowLeft = False


					else:
						sections[s].leftN = leftN
						sections[s].rightN = rightN
						rowMap[carrierOrder[s]] = rows[r][i] #new
					taken.append(s)
					match = True
					break
			
			if not match:
				taken.append(unusedC)
				sections[unusedC].leftN = leftN
				sections[unusedC].rightN = rightN
				rowMap[carrierOrder[unusedC]] = rows[r][i]

			
		pieceMap.append(sorted(rowMap.items(), key=lambda x: x[1])) #new

	print(pieceMap) #remove


	visualization = []

	for r in range(0, len(pieceMap)):
		row = []
		n0 = 0
		for s in pieceMap[r]:
			carrier = s[0]
			needles = s[1]
			
			n1 = needles[0]
			n3 = needles[len(needles) - 1]
			for n in range(n0, n1):
				row.append(0)
			for n in range(n1, n3 + 1):
				row.append(carrier)
			n0 = n3 + 1

		for n in range(n0, width):
			row.append(0)
		
		visualization.append(row)
	
	for v in visualization: #remove
		print(v)
