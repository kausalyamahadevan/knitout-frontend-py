import sys
sys.path.append('../knitout-frontend-py')
from library.castonbindoff import *

ribpattern = np.array([0,0,1,1,1,1])
ribsize = len(ribpattern)
totrepeats
width  = ribsize*totrepeats
kwriter = knitout.Writer('1 2 3 4 5 6')

kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'

kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)
kwriter.stitchNumber(4)

caston(kwriter,width,[draw,waste,main])
