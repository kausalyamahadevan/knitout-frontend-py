import knitout

k = knitout.Writer('1 2 3 4 5 6')

k.incarrier('1')

'''
# insert knitout here
'''

# for n in range(0, 10):
# 	k.knit('+', f'f{n}', '1')

# k.twist('f6')

k.outcarrier('1')

k.write('out.k')