import numpy as np
misses=5
stitches=7

repeat=misses+stitches

ref=np.concatenate([np.ones(stitches,int),np.zeros(misses,int)])



allback=np.ones(len(ref))

print(allback)
