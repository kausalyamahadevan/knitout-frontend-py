from castonbindoff import *
kwriter = knitout.Writer('1 2 3 4 5 6')

kwriter.addHeader('Machine','kniterate')

draw = '1'
waste = '2'
main = '3'
kwriter.ingripper(waste)
kwriter.ingripper(draw)
kwriter.ingripper(main)

caston(kwriter,8,[draw,waste,main])
kwriter.write('caston.k')
