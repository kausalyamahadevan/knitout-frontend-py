import knitout
import gabrielle

k = knitout.Writer('1 2 3 4 5 6')

#customizable variables
filename = 'split-inc-test-2'
leftN = 10
rightN = 40
mainC = '1'
drawC = '2'
gauge = 2
posBed = 'f'
negBed = 'b'
rowsBtwInc = 6
rowCount = 100
incMethod = 'split'

rollerAdvance = 300 #for twisted stitches

gabrielle.wasteSection(k, leftN=leftN, rightN=rightN, wasteC=mainC, drawC=drawC, endOnRight=[mainC], gauge=gauge)

k.outcarrier(drawC)

gabrielle.closedTubeCaston(k, startN=rightN, endN=leftN, c=mainC, gauge=gauge)

#knit 6 rows
gabrielle.circular(k, startN=leftN, endN=rightN, length=6, c=mainC, gauge=gauge)

leftoverTwistedStitches = []

prevRowsBtwInc = rowsBtwInc
k.pause(f'{rowsBtwInc} rows btw splits')

for r in range(0, rowCount+1):
	twistedStitches = []

	if r % rowsBtwInc == 0:
		if prevRowsBtwInc != rowsBtwInc: k.pause(f'{rowsBtwInc} rows btw splits')
		leftN, leftTwistedStitches = gabrielle.incDoubleBed(k, count=1, edgeNeedle=leftN, c=mainC, side='l', gauge=gauge, incMethod=incMethod) #inc 1 on left

		if leftTwistedStitches is not None: twistedStitches.extend(leftTwistedStitches)

	gabrielle.knitPass(k, startN=leftN, endN=rightN, c=mainC, bed=posBed, gauge=gauge) #pos pass

	# if r % rowsBtwInc == 0 and len(twistedStitches):
	# 	for i in range(0, len(twistedStitches)):
	# 		k.twist(twistedStitches[i], -rollerAdvance)

	if r % rowsBtwInc == 0:
		rightN, rightTwistedStitches = gabrielle.incDoubleBed(k, count=1, edgeNeedle=rightN, c=mainC, side='r', gauge=gauge, incMethod=incMethod) #inc 1 on right
		prevRowsBtwInc = rowsBtwInc

		if rightTwistedStitches is not None: twistedStitches.extend(rightTwistedStitches)

	gabrielle.knitPass(k, startN=rightN, endN=leftN, c=mainC, bed=negBed, gauge=gauge) #neg pass

	if len(leftoverTwistedStitches): k.twist(leftoverTwistedStitches, -rollerAdvance)

	if r % rowsBtwInc == 0 and len(twistedStitches):
		leftoverTwistedStitches = k.twist(twistedStitches, -rollerAdvance)
		# for i in range(0, len(twistedStitches)):
		# 	k.twist(twistedStitches[i], -rollerAdvance)

	if r == 48: rowsBtwInc = 4 #switch to check it out
	elif r == 76: rowsBtwInc = 2 #switch to check it out

#knit 6 rows
gabrielle.circular(k, startN=leftN, endN=rightN, length=6, c=mainC, gauge=gauge)

gabrielle.dropFinish(k, frontNeedleRanges=[leftN, rightN], backNeedleRanges=[leftN, rightN], carriers=[mainC])

print(f'\nwrote {filename}.k')
k.write(f'{filename}.k')