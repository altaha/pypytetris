import pygame
import block
import grid

"""
Module for rendering to a screen
Uses pygame for drawing methods
Draws shapes defined by grid and block objects
"""

class PgRenderer:

    # nhorz and nvert are the number of grid cols.rows
    # celldim is the cell dimensions in pixels
    # color is default (empty) cell color
    def __init__(self, ncols, nrows, celldim, bgcolor):
        self.nrows = nrows
        self.ncols = ncols
        self.celldim = celldim
        self.pwidth = ncols*celldim  # width in pixels
        self.pheight = nrows*celldim # height in pixels
        self.bgcolor = bgcolor

        self.screen = pygame.display.set_mode((self.pwidth, self.pheight))

        self.clear()

    def clear(self):
        self.screen.fill(self.bgcolor)

        self._drawgridlines()
        pygame.display.update()

    def _drawgridlines(self):
        # draw vertical lines
        linecolor = (255,230,230) # gridlines in a soft color
        for i in range(1, self.ncols):
            pointlist = [(i*self.celldim, 0),(i*self.celldim, self.pheight)]
            pygame.draw.lines(self.screen, linecolor, False, pointlist, 1)
        # draw horizontal lines
        for i in range(1, self.nrows):
            pointlist = [(0, i*self.celldim),(self.pwidth, i*self.celldim)]
            pygame.draw.lines(self.screen, linecolor, False, pointlist, 1)

    def drawgrid(self, grid):
        # Draw all grid cells with val == 1
        for i in range(grid.height):
            for j in range(grid.width):
                if grid.grid[i][j].val == 1:
                    color = grid.grid[i][j].color
                    rect = (j*self.celldim, i*self.celldim, \
                            self.celldim, self.celldim)
                    pygame.draw.rect(self.screen, color, rect, 0)
                    pygame.draw.rect(self.screen, (0,0,0), rect, 1)
        pygame.display.update()

    def drawblock(self, block):
        # Draw all grid cells with val == 1
        for i in range(block.height):
            for j in range(block.width):
                if block.spots[i][j] > 0:
                    rect = ((j+block.x)*self.celldim, \
                            (i+block.y)*self.celldim, self.celldim, self.celldim)
                    pygame.draw.rect(self.screen, block.color, rect, 0)
                    pygame.draw.rect(self.screen, (0,0,0), rect, 1)
        pygame.display.update()
        


## Testing ##
if __name__ == '__main__':

    import sys
    pygame.init()

    render = PgRenderer(10,20,30,(255,255,255))

    grid = grid.Grid(10,20, (255,255,255))

    square = block.Square_Block()
    grid.addblock(square)

    line = block.Line_Block()
    line.move_absolute(5,5,0)

    render.clear()
    render.drawgrid(grid)
    render.drawblock(line)

    while (True):
        pygame.time.delay(33)

        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
        
