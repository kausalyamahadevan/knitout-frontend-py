import numpy as np
misses=5
stitches=7

repeat=misses+stitches

ref=np.concatenate([np.ones(stitches,int),np.zeros(misses,int)])



allback=np.ones(len(ref),int)

print(allback)

x = np.array([[1, 2, 3], [4, 5, 6],[7,8,9]], int)
print(x[2,1])

newx=np.array([[1,1,1,2,2,2,3,3,3,1,1,2,2,3,3], [1,1,2,2,2,3,3,3,1,1,2,2,3,3,1],
    [1,2,2,2,3,3,3,1,1,2,2,3,3,1,1],[2,2,2,3,3,3,1,1,2,2,3,3,1,1,1],[2,2,3,3,3,1,1,2,2,3,3,1,1,1,2],
    [2,3,3,3,1,1,2,2,3,3,1,1,1,2,2],[3,3,3,1,1,2,2,3,3,1,1,1,2,2,2],[3,3,1,1,2,2,3,3,1,1,1,2,2,2,3],
    [3,1,1,2,2,3,3,1,1,1,2,2,2,3,3],[1,1,2,2,3,3,1,1,1,2,2,2,3,3,3],[1,2,2,3,3,1,1,1,2,2,2,3,3,3,1]], int)

newx=newx-1;
np.shape(newx)
print(newx)
print(np.shape(newx))
print(np.shape(newx)[1])

print(1%3)
print(33%15)

tuckarray=np.array([])
print(len(tuckarray))
print(tuckarray)

c1='1'
c2='2'
c3='3'
carriers=[c1,c2,c3]
len(carriers)

beg=5
end=10


tuckarray=np.zeros(end+1,int)
tuckarray[beg-1]=1
tuckarray[end]=1

print(tuckarray)

w=5
print(w%2)
