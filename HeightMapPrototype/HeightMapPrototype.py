import random
import numpy
import matplotlib.pyplot as plt

########################
#Configuration variables
########################
debug = 0
method = 2 #1: hill, 2: ridge

SIZE_X=100
SIZE_Y=100

if method == 1:
    #hill
    HILL_MIN_HEIGHT = 5
    HILL_MAX_HEIGHT = 30
    NUMBER_HILL = 6000
elif method == 2:
    #ridge
    NUMBER_OF_RIDGE = 30
    RIDGE_HEIGHT_MIN = 10
    RIDGE_HEIGHT_MAX = 10
    RIDGE_SIZE_MIN = 15
    RIDGE_SIZE_MAX = 30
    RIDGE_NOISE_VALUE = 0

#####################
#end of configuration
#####################

mat_map = numpy.ones((SIZE_X, SIZE_Y))
rdgSize = numpy.ones((1,NUMBER_OF_RIDGE))
rdgHeight = numpy.ones((1,NUMBER_OF_RIDGE))
rdgDirection = numpy.ones((NUMBER_OF_RIDGE, 2))
rdgStart = numpy.ones((NUMBER_OF_RIDGE, 2))

if method == 1:
    mat_rand_pos = numpy.ones((2, NUMBER_HILL))
    mat_rand_height = numpy.ones((1,NUMBER_HILL))

rows = mat_map.shape[0]
cols = mat_map.shape[1]

#######
#checks
#######
if method == 1:
    assert HILL_MIN_HEIGHT <= HILL_MAX_HEIGHT



####################
#Function definition
####################

#init the figure plot
def initPlotHeightmap():
    #init the figure but omit the show
    plt.figure()
    plt.title('z as 2d heat map')

def showHeightmap():
    p = plt.imshow(mat_map)
    plt.colorbar(p)
    plt.show()

#Generate a ridge
def genRidge(matrix, rdgSize, rdgNoise, rdgDirection, rdgStart_l):
        for idx, block in enumerate(range(int(rdgSize))):
            temp = rdgStart_l+idx*rdgDirection
            if (temp[0] >= SIZE_X-1) or (temp[1] >= SIZE_Y-1) or (temp[0] == 0) or (temp[1] == 0):
                return
            matrix[int(temp[0]),int(temp[1])]=rdgHeight[0,idx]


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











########################
#Start of execution here
########################


initPlotHeightmap()


#init of random matrices
if method == 1:
    #hill location
    for temp in range(mat_rand_pos.shape[1]):
      mat_rand_pos[:,temp] = [random.randint(0,SIZE_X-1), random.randint(0,SIZE_Y-1)]
    #hill height
    for temp in range(mat_rand_height.shape[1]):
      mat_rand_height[0,temp] = random.randint(HILL_MIN_HEIGHT,HILL_MAX_HEIGHT)
elif method == 2:
    #ridge size
    for temp in range(0,NUMBER_OF_RIDGE):
        rdgSize[0,temp] = random.randint(RIDGE_SIZE_MIN, RIDGE_SIZE_MAX)
    #ridge height
    for temp in range(0,NUMBER_OF_RIDGE):
        rdgHeight[0,temp] = random.randint(RIDGE_HEIGHT_MIN, RIDGE_HEIGHT_MAX)
    #ridge start
    for temp in range(0,NUMBER_OF_RIDGE):
        rdgStart[temp, :] = [random.randint(0,SIZE_X-1), random.randint(0,SIZE_Y-1)]
    #ridge directtion
    for temp in range(0,NUMBER_OF_RIDGE):
        while True: #direction must not be (0,0)
            x=random.randint(-1,1)
            y=random.randint(-1,1)
            if (x!=0) or (y!=0):
                break
        rdgDirection[temp, :] = [x, y]
    #generate the ridge
    for temp in range(NUMBER_OF_RIDGE):
        genRidge(mat_map, rdgSize[0,temp], RIDGE_NOISE_VALUE, rdgDirection[temp,:], rdgStart[temp,:])


#debug
if debug == 1:
    for temp in range(mat_rand_pos.shape[1]):
      mat_rand_pos[0,temp] = round(HILL_MIN_HEIGHT*1.2*(temp+2))

    for temp in range(mat_rand_pos.shape[1]):
      mat_rand_pos[1,temp] = round(SIZE_Y/2)+1

    for temp in range(mat_rand_height.shape[1]):
      mat_rand_height[0,temp] = HILL_MAX_HEIGHT

#set fix values in map
if method == 1:
    for temp in range(mat_rand_height.shape[1]):
        mat_map[int(mat_rand_pos[0,temp]),int(mat_rand_pos[1,temp])]=mat_rand_height[0,temp]




#calculate the height of indices set to -1
while isMatrixReady(mat_map)==-1:
    for x in range(0, rows):
        for y in range(0, cols):
             newHeightTemp = calculateHeight(mat_map, x, y)
             if newHeightTemp >= 0:
                 mat_map[x,y]=newHeightTemp
             else:
                raise ValueError('Error: new heigh value was under 0')


showHeightmap()

