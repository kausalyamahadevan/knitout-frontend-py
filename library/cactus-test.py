import knitout
import gabrielle

k = knitout.Writer('1 2 3 4 5 6')

# for n in range(0, 121):
# 	k.drop(f'f{n}')

# for n in range(120, -1, -1):
# 	k.drop(f'b{n}')


# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png')
# k.write('cactus-test.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', 2)
# k.write('cactus-test-gauge2.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-waste-test.png')
# k.write('cactus-waste-test.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-4sections.png')
# k.write('cactus-4sections.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-5sections.png')
# k.write('cactus-5sections.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', 2, 1, 4)
# k.write('cactus-test-gauge2-sr4.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=2, scale=1, maxShortrowCount=1)
# k.write('cactus-test-gauge2-sr1.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=2, scale=2, maxShortrowCount=4)
# k.write('cactus-test-gauge2-scale2-sr4-2.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=1, scale=2, maxShortrowCount=4)
# k.write('cactus-test-scale2-sr4.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=1, scale=2, maxShortrowCount=4)
# k.write('cactus-test-scale2-sr4-2.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=1, scale=1, maxShortrowCount=4)
# k.write('cactus-test-sr4.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=2, scale=3.5, maxShortrowCount=4)
# k.write('cactus-test-gauge2-scale3-sr4.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus.png', gauge=1, scale=6, maxShortrowCount=4)
# k.write('cactus-test-scale6-sr4.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-boundary.png', gauge=2, scale=2, maxShortrowCount=4)
# k.write('cactus-test-gauge2-scale2-sr4-stackedCheck.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-medium.png', scale=2, maxShortrowCount=4)
# k.write('cactus-test-medium-scale2-sr6.k')

# gabrielle.shapeImgToKnitout(k, 'graphics/cactus-medium.png', gauge=2, maxShortrowCount=4, addBindoff=False, excludeCarriers=['4'])
# k.write('cactus-test-medium-gauge2-sr4-take3.k')

gabrielle.shapeImgToKnitout(k, 'graphics/cactus-medium.png', gauge=2, maxShortrowCount=4, addBindoff=False, excludeCarriers=['4'])
k.write('cactus-test-medium-gauge2-sr4-changes.k')