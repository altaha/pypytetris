import block as bl

"""
Module to describe a tetris grid.
A grid is an array of an array of Cells
Dimensions are in terms of grid cells
Indexing starts at (0,0) at top left corner
"""

class Cell:
    def __init__(self, color, val):
        self.color = color
        if abs(val) > 0:
            self.val = 1
        else:
            self.val = 0
    def __str__(self):
        return str(self.val)

    # support sum() method on Cell object
    def __radd__(self, other):
        return self.val + other

class Grid:
    # width and height are the # of horizontal and veritcal cells in grid
    # color is default (empty) cell color
    def __init__(self, width, height, color):
        self.defaultcolor = color
        self.width = width
        self.height = height
        self.grid = [[Cell(color, 0) for x in range(width)] for x in range(height)]

    def __str__(self):
        string = "Grid of width {} and height {}\n".format(self.width, self.height)
        string += "First cell: color {}, value {}".format(self.grid[0][0].color,\
                                                          self.grid[0][0].val)
        return string

    # check if block is within the bounds of the grid's dimensions
    def isinbound(self,block):
        if block.x > self.width or block.y > self.height:
            return False
        if (block.x + block.width) > self.width or \
           (block.y + block.height) > self.height:
            return False
        return True

    def _assertbounds(self, block):
        if self.isinbound(block) == False:
            raise Exception("Block is out of grid bounds")
            
    # check if block touches any filled cell(s)
    def checkcollision(self, block):
        self._assertbounds(block)
        # check all spots in block against grid
        for i in range(block.y, block.y + block.height):
            for j in range(block.x, block.x + block.width):
                if block.spots[i-block.height][i-block.width] > 0 and \
                   self.grid[i][j].val > 0:
                    return True
        return False

    # add block to the grid
    def addblock(self, block):
        self._assertbounds(block)
        # add block to grid
        for i in range(block.y, block.y + block.height):
            for j in range(block.x, block.x + block.width):
                self.grid[i][j].color = block.color
                self.grid[i][j].val = \
                    block.spots[i-block.height][i-block.width]

        # check for completed lines and update grid
        for i in range(self.height):
            if sum(self.grid[i]) == self.width :
                self._fillgap(i)

    def _fillgap(self, emptynum):
        # go up starting from empty line to line 0
        for i in range(emptynum, 0, -1):
            self.grid[i] = self.grid[i-1]
        self.grid[0] = [Cell(self.defaultcolor, 0) for x in range(self.width)]


## Testing ##
if __name__ == '__main__':

    grid = Grid(6,12, (255,255,255))
    print grid

    square = bl.Square_Block()
    print grid.checkcollision(square)
    grid.addblock(square)
    print grid.checkcollision(square)

    square.move_absolute(0,2,0)
    grid.addblock(square)

    square.move_absolute(2,2,0)
    grid.addblock(square)

    print sum(grid.grid[0])
    print sum(grid.grid[1])
    print sum(grid.grid[2])
    print sum(grid.grid[3])

    square.move_absolute(4,2,0)
    grid.addblock(square)

    print sum(grid.grid[0])
    print sum(grid.grid[1])
    print sum(grid.grid[2])
    print sum(grid.grid[3])
