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

# gabrielle.generatePieceMap(k, 'graphics/cactus.png')
# k.write('cactus-test.k')

gabrielle.generatePieceMap(k, 'graphics/cactus.png', 2)
k.write('cactus-test-gauge2.k')

# gabrielle.generatePieceMap(k, 'graphics/cactus-waste-test.png')
# k.write('cactus-waste-test.k')

# gabrielle.generatePieceMap(k, 'graphics/cactus-4sections.png')
# k.write('cactus-4sections.k')

# gabrielle.generatePieceMap(k, 'graphics/cactus-5sections.png')
# k.write('cactus-5sections.k')