import random
import numpy
import matplotlib.pyplot as plt

debug = 0

SIZE_X=100
SIZE_Y=100

HILL_MIN_HEIGHT = 5
HILL_MAX_HEIGHT = 10


NUMBER_HILL = 400


mat_map = numpy.full((SIZE_X, SIZE_Y),0)
mat_rand_pos = numpy.ones((2, NUMBER_HILL))
mat_rand_height = numpy.ones((1,NUMBER_HILL))

rows = mat_map.shape[0]
cols = mat_map.shape[1]

#checks
assert HILL_MIN_HEIGHT <= HILL_MAX_HEIGHT

#gets the max values of the adjacent block in the matrix (no diagonal)
def getMaxValueOfAdjacentBlock(matrix, x ,y):
    if (x == 0) and (y == 0):
        adjValue = max(matrix[x+1, y],matrix[x, y+1])
    elif (x == 0) and (y == SIZE_Y - 1):
        adjValue = max(matrix[x+1, y],matrix[x, y-1])
    elif (x == SIZE_X - 1) and (y == 0):
        adjValue = max(matrix[x-1, y],matrix[x, y+1])
    elif (x == SIZE_X - 1) and (y == SIZE_Y - 1):
        adjValue = max(matrix[x-1, y],matrix[x, y-1])
    elif x == 0:
        adjValue = max(matrix[x+1, y],matrix[x, y-1],matrix[x, y+1])
    elif  y == 0:
        adjValue = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y+1])
    elif x == SIZE_X - 1:
        adjValue = max(matrix[x-1, y],matrix[x, y-1],matrix[x, y+1])
    elif y == SIZE_Y - 1:
        adjValue = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y-1])
    else:
        adjValue = max(matrix[x-1, y],matrix[x+1, y],matrix[x, y-1],matrix[x, y+1])
    return adjValue


#calculate the height value of the block (x,y)
def calculateHeight(matrix, x, y):
    newHeight = getMaxValueOfAdjacentBlock(matrix, x ,y) -1

    #height of the block can't decrease
    if newHeight < matrix[x,y]:
        newHeight = matrix[x,y]

    #valid blocks can't be under 0
    assert newHeight>=0

    return newHeight

#the matrix is ready when there is no -2 inside
def isMatrixReady(matrix):
    for x in range(0, rows):
        for y in range(0, cols):
            if matrix[x,y] < (getMaxValueOfAdjacentBlock(matrix, x ,y)-1):
                if debug:
                    print(matrix[x-2:x+2,y-2:y+2])
                return -1

    return 1




#init of random matrix
for temp in range(mat_rand_pos.shape[1]):
  mat_rand_pos[0,temp] = random.randint(0,SIZE_X-1)

for temp in range(mat_rand_pos.shape[1]):
  mat_rand_pos[1,temp] = random.randint(0,SIZE_Y-1)

for temp in range(mat_rand_height.shape[1]):
  mat_rand_height[0,temp] = random.randint(HILL_MIN_HEIGHT,HILL_MAX_HEIGHT)

#debug
if debug == 1:
    for temp in range(mat_rand_pos.shape[1]):
      mat_rand_pos[0,temp] = round(HILL_MIN_HEIGHT*1.2*(temp+2))

    for temp in range(mat_rand_pos.shape[1]):
      mat_rand_pos[1,temp] = round(SIZE_Y/2)+1

    for temp in range(mat_rand_height.shape[1]):
      mat_rand_height[0,temp] = HILL_MAX_HEIGHT

#set fix values in map
for temp in range(mat_rand_height.shape[1]):
    mat_map[int(mat_rand_pos[0,temp]),int(mat_rand_pos[1,temp])]=mat_rand_height[0,temp]




#calculate the height of indices set to -1
while isMatrixReady(mat_map)==-1:
    for x in range(0, rows):
        for y in range(0, cols):
            mat_map[x,y] = calculateHeight(mat_map, x, y)
                #plt.show()


# show height map in 2d
plt.figure()
plt.title('z as 2d heat map')
p = plt.imshow(mat_map)
plt.colorbar(p)
plt.show()

