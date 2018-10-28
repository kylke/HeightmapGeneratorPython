import random
import numpy
import matplotlib.pyplot as plt

SIZE_X=30
SIZE_Y=30

HILL_MIN_HEIGHT = 3
HILL_MAX_HEIGHT = 10

NUMBER_HILL = 20


mat_map = numpy.full((SIZE_X, SIZE_Y),-2)
mat_rand_pos = numpy.ones((2, NUMBER_HILL))
mat_rand_height = numpy.ones((1,NUMBER_HILL))

rows = mat_map.shape[0]
cols = mat_map.shape[1]


#calculate the height value of the block (x,y)
def calculateHeight(matrix, x, y):
    if (x == 0) and (y == 0):
        newHeight = max(matrix[x+1, y],matrix[x, y+1])-1
    elif (x == 0) and (y == SIZE_Y - 1):
        newHeight = max(matrix[x+1, y],matrix[x, y-1])-1
    elif (x == SIZE_X - 1) and (y == 0):
        newHeight = max(matrix[x-1, y],matrix[x, y+1])-1
    elif (x == SIZE_X - 1) and (y == SIZE_Y - 1):
        newHeight = max(matrix[x-1, y],matrix[x, y-1])-1
    elif x == 0:
        newHeight = max(matrix[x+1, y],matrix[x, y-1],matrix[x, y+1])-1
    elif  y == 0:
        newHeight = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y+1])-1
    elif x == SIZE_X - 1:
        newHeight = max(matrix[x-1, y],matrix[x, y-1],matrix[x, y+1])-1
    elif y == SIZE_Y - 1:
        newHeight = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y-1])-1
    else:
        newHeight = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y-1],matrix[x, y+1])-1

    if newHeight==-1:
        newHeight=0

    return newHeight

#the matrix is ready when there is no -2 inside
def isMatrixReady(matrix):
    for x in range(0, rows):
        for y in range(0, cols):
            if matrix[x,y] < 0:
                return -1

    return 1




#init of random matrix
for temp in range(mat_rand_pos.shape[1]):
  mat_rand_pos[0,temp] = random.randint(0,SIZE_X-1)

for temp in range(mat_rand_pos.shape[1]):
  mat_rand_pos[1,temp] = random.randint(0,SIZE_Y-1)

for temp in range(mat_rand_height.shape[1]):
  mat_rand_height[0,temp] = random.randint(3,10)

#set fix values in map
for temp in range(mat_rand_height.shape[1]):
  mat_map[int(mat_rand_pos[0,temp]),int(mat_rand_pos[1,temp])]=mat_rand_height[0,temp]

#calculate the height of indices set to -1
while isMatrixReady(mat_map)==-1:
    for x in range(0, rows):
        for y in range(0, cols):
            if mat_map[x,y] < -1:
                mat_map[x,y] = calculateHeight(mat_map, x, y)

 
print (mat_map)
#print(mat_rand_pos)
#print(mat_rand_height)



# show hight map in 2d
plt.figure()
plt.title('z as 2d heat map')
p = plt.imshow(mat_map)
plt.colorbar(p)
plt.show()