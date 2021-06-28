import knitout
import gabrielle

k = knitout.Writer('1 2 3 4 5 6')

#customizable variables
filename = 'small-split'
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

k.incarrier('2')
# k.drop(f'f-47')
# k.drop(f'f98')
k.split('+', f'b40', f'f40', '2')
k.pause('ok?')
k.split('-', f'f10', f'b10', '2')

k.outcarrier('2')

print(f'\nwrote {filename}.k')
k.write(f'{filename}.k')