import pygame
import sys
import block
import grid as tetrisgrid
import PygameRenderer as pgrender
import random # random number generator
import copy

"""
Tetris game module
Implements controls and mechanics of Tetris game
Uses block, grid, and PygameRendered modules
"""

class Tetris:
    def __init__(self, ncols, nrows, celldim, bgcolor, blocks):
        self.ncols = ncols
        self.nrows = nrows
        self.celldim = celldim
        self.bgcolor = bgcolor
        self.blocks = blocks
        self.reset_game()

    def _get_new_block(self):
        rand_block = self.blocks[random.randrange(0, len(self.blocks))]
        rand_block.move_absolute(ncols/2 - rand_block.width/2, 0, 0)
        return rand_block

    def refresh_screen(self, render):
        render.clear()
        render.drawgrid(self.grid)
        render.drawblock(self.currblock)

    def reset_game(self):
        self.grid = tetrisgrid.Grid(self.ncols, self.nrows, self.bgcolor)
        self.currblock = self._get_new_block()

    def is_valid_move(self, block):
        if self.grid.isinbounds(block) == False:
            return False
        if self.grid.checkcollision(block) == True:
            return False
        return True

    def rotate_cw(self):
        temp = copy.deepcopy(self.currblock)
        temp.rotate(1)
        if self.is_valid_move(temp) == True:
            self.currblock = temp

    def move_left(self):
        temp = copy.deepcopy(self.currblock)
        temp.move(-1, 0)
        if self.is_valid_move(temp) == True:
            self.currblock = temp

    def move_right(self):
        temp = copy.deepcopy(self.currblock)
        temp.move(1, 0)
        if self.is_valid_move(temp) == True:
            self.currblock = temp

    def move_down(self):
        temp = copy.deepcopy(self.currblock)
        temp.move(0, 1)
        if self.is_valid_move(temp) == True:
            self.currblock = temp
        else:
            self.grid.addblock(self.currblock)
            self.currblock = self._get_new_block()
            if self.is_valid_move(self.currblock) == False:
                return False
        return True

# globals
celldim = 30
nrows = 20
ncols = 10
white = (255,255,255)
frametime = 33
timerms = 1000 # time elapsed between auto block moves

blocks = [block.Square_Block(), block.Line_Block(), block.T_Block(),\
          block.S1_Block(), block.S2_Block(),\
          block.L1_Block(), block.L2_Block()]

# Pygame Initializaions
pygame.init()
pygame.display.set_caption('PyPyTetris')
pygame.key.set_repeat(250, frametime) # handles holding down of arrow keys
pygame.time.set_timer(pygame.USEREVENT, timerms) # periodic timer event

# Create game screen and grid
render = pgrender.PgRenderer(ncols,nrows,celldim, white)
tetris = Tetris(ncols, nrows, celldim, white, blocks)
tetris.refresh_screen(render)

def move_down_action(tetris, render):
    ret = tetris.move_down()
    tetris.refresh_screen(render)
    if ret == False:
        tetris.reset_game()
        tetris.refresh_screen(render)

# main program event handling loop
while (True):
    pygame.time.delay(frametime)

    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

        if event.type == pygame.USEREVENT: #timer event (move down)
            move_down_action(tetris, render)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetris.rotate_cw()
                tetris.refresh_screen(render)

            if event.key == pygame.K_DOWN:
                move_down_action(tetris, render)

            if event.key == pygame.K_LEFT:
                tetris.move_left()
                tetris.refresh_screen(render)

            if event.key == pygame.K_RIGHT:
                tetris.move_right()
                tetris.refresh_screen(render)
