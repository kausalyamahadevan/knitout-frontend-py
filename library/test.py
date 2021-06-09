import knitout

# import halfGauge

k = knitout.Writer('1 2 3 4 5 6')

'''
k.incarrier('1')

'''
# insert knitout here
'''

halfGauge.jersey(k=k, beg=0, end=19, length=10, c='3', gauge=2)

k.outcarrier('1')

k.write('out.k')
'''

import gabrielle

gabrielle.generatePieceMap(k, 'graphics/cactus.png')

