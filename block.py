"""
generic class to describe a tetris block
all dimensions are in terms of grid cells
indexing starts at (0,0) at top left corner
orientation goes from 0 to 3 indicating 0 to 270 degrees
"""

class Block:

    # width and height are the dimensions of a bounding box for the block
    # color is a tuple of block color (r,g,b)
    # spots is a matrix (array of arrays) indicating filled spots
    def __init__(self, name, width, height, color, spots):
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        if len(spots) != height :
            raise Exception("spots array should have height = height arg")
        if len(spots[0]) != width :
            raise Exception("spots array should have height = height arg")
        self.spots = spots
        
        self.x = 0
        self.y = 0
        self.orient = 0

    def __str__(self):
        string = self.name + " Object\n"
        string += "  width: {}, height: {}\n".format(self.width, self.height)
        string += "  x: {}, y: {}, orient: {}\n".format(self.x, self.y, self.orient)
        string += "  color: {}\n".format(self.color)
        string += "  spots: {}\n".format(self.spots)
        return string

    # rotates a block once (+ve direction is clockwise, -ve is counter)
    def rotate(self, direction) :
        # transpose spots array
        transp = zip(*self.spots)

        # create new spots array and set values to 0
        self.width, self.height = self.height, self.width
        w = self.width
        h = self.height
        self.spots = [[0 for x in range(w)] for x in range(h)]

        # need to flip transposed array to complete the rotation
        if direction > 0: #clockwise
            self.orient = (self.orient + 1) % 4
            for i in range(h):
                for j in range(w):
                    self.spots[i][j] = transp[i][w - j -1]

        else: #counterclockwise
            self.orient = (self.orient - 1) % 4
            for i in range(h):
                for j in range(w):
                    self.spots[i][j] = transp[h - i -1][j]


    # changes the absolute position of a block
    def move_absolute(self, x, y, orient) :
        if x < 0 or y < 0:
            print "Invalid block position to move_absolute (negative)"
            return
        self.x = x
        self.y = y

        # rotate
        orient = orient % 4
        numrots = abs(orient - self.orient)
        if orient > self.orient :
            direction = 1
        else:
            direction = -1
                
        for i in range(numrots):
            self.rotate(direction)

    # move a block relative to current positon
    def move(self, x, y) :
        #update x,y
        self.x += x
        self.y += y


## Define tetris shapes ##
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
gray = (128, 128, 128)
yellow = (255,255,0)
orange = (255,128,0)
pink = (255, 128, 128)

def Square_Block():
    return Block("Square", 2,2, gray, [[1,1],[1,1]])

def Line_Block():
    return Block("Line", 4,1, green, [[1,1,1,1]])

def T_Block():
    return Block("T", 3,2, blue, [[1,1,1],[0,1,0]])

def L1_Block():
    return Block("L1", 3,2, yellow, [[1,0,0],[1,1,1]])

def L2_Block():
    return Block("L2", 3,2, orange, [[0,0,1],[1,1,1]])

def S1_Block():
    return Block("S1", 3,2, red, [[1,1,0],[0,1,1]])

def S2_Block():
    return Block("S2", 3,2, pink, [[0,1,1],[1,1,0]])


## Testing ##
if __name__ == '__main__':
    square = Square_Block()
    print square
    print "Move square to 25,20:"
    square.move_absolute(25, 20, 0)
    print square

    tblock = T_Block()
    print tblock
    print "rotate T counterclockwise:"
    tblock.rotate(-1)
    print tblock

    lineblock = Line_Block()
    print lineblock
    print "move Line to 50,50 and rotate twice clockwise:"
    lineblock.move_absolute(50, 50, 2)
    print lineblock

    l1block = L1_Block()
    print l1block
    print "move L1 to 50,50 and rotate once counterclockwise:"
    l1block.move_absolute(50, 50, -1)
    print l1block
