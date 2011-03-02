# tetris.py
# Christian Jauvin <cjauvin@gmail.com>
# Sometime in 2010
#

import pygame, sys, time, random, copy

unit = 25 # cell: unit x unit
unit_width = 10 # grid width in cells
unit_height = 18 # grid height in cells
margin = unit
size = width, height = (unit * unit_width) + (2 * margin), (unit * unit_height) + (2 * margin)
grid_left = margin
grid_top = margin
grid_height = unit * unit_height
grid_width = unit * unit_width
drop_speed = 500 # in msecs
move_speed = 200 # lateral

tetrominoes = {
    'I': {'grid': [[0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0], [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0]], 'color': pygame.color.Color('red')},
    'S': {'grid': [[0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0], [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0]], 'color': pygame.color.Color('green')},
    'Z': {'grid': [[0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0], [0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0]], 'color': pygame.color.Color('pink')},
    'T': {'grid': [[0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0], [0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0], 
                    [0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0], [0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0]], 'color': pygame.color.Color('blue')},
    'O': {'grid': [[0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0]], 'color': pygame.color.Color('yellow')},
    'L': {'grid': [[0,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0], [0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0], 
                   [1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0], [0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0]], 'color': pygame.color.Color('turquoise')},
    'J': {'grid': [[0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0], [1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0], 
                   [0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0], [0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0]], 'color': pygame.color.Color('cyan')}
}

class Piece:
    
    def __init__(self):
        self.reset()

    def draw(self):
#        pygame.draw.rect(screen, pygame.color.Color('lightgrey'), (self.left, self.top, 4*unit, 4*unit), 1)
        for i in range(4):
            for j in range(4):
                k = (i * 4) + j
                if tetrominoes[self.tetromino]['grid'][self.index][k]:
                    pygame.draw.rect(screen, tetrominoes[self.tetromino]['color'], \
                                         (self.left + (j * unit), self.top + (i * unit), unit, unit), 3)

    def reset(self):
        global colors, color_idx
        self.left = margin + (grid_width / 2) - (2 * unit)
        self.top = margin - (2 * unit)
        self.tetromino = random.choice(tetrominoes.keys())
        self.index = 0
        
    def canGo(self, dir):
        if dir == 'down': return not self.isColliding(1, 0)
        elif dir == 'left': return not self.isColliding(0, -1)
        elif dir == 'right': return not self.isColliding(0, 1)

    def isColliding(self, gi_disp, gj_disp, index = None):
        gi, gj = self.getGridCoords()
        for i in range(4):
            for j in range(4):
                k = (i * 4) + j
                if tetrominoes[self.tetromino]['grid'][index if index is not None else self.index][k] \
                        and grid[gi + i + gi_disp + 4][gj + j + gj_disp + 4]:
                    return True
        return False

    def drop(self):
        if self.canGo('down'):
            self.top += unit
        else: # stopped
            self.fixToGrid()
            self.reset()

    def rotate(self):
        next_index = self.index + 1
        next_index %= len(tetrominoes[self.tetromino]['grid'])
        if not self.isColliding(0, 0, next_index):
            self.index += 1
            self.index %= len(tetrominoes[self.tetromino]['grid'])

    def move(self, dir):
        if dir == 'left' and self.canGo('left'):
            self.left -= unit
        elif dir == 'right' and self.canGo('right'):
            self.left += unit

    def getGridCoords(self):
        gi = (self.top - margin) / unit
        gj = (self.left - margin) / unit
        return (gi, gj)

    def fixToGrid(self):
        gi, gj = self.getGridCoords()
        for i in range(4):
            for j in range(4):
                k = (i * 4) + j
                if tetrominoes[self.tetromino]['grid'][self.index][k]:
                    grid[gi + i + 4][gj + j + 4] = tetrominoes[self.tetromino]['color']
        lookForRowClearing() 
        # look for game over
        for j in range(4, unit_width + 4):
            if grid[4][j]:
                sys.exit(0)
                
def drawGrid():
    for i in range(unit_height + 8):
        for j in range(unit_width + 8):
            if grid[i][j] and grid[i][j] != -1:
                pygame.draw.rect(screen, grid[i][j], (margin + ((j-4) * unit), \
                                                          margin + ((i-4) * unit), unit, unit), 3)

def lookForRowClearing():
    i = unit_height - 1 + 4
    while i >= 4:
        full_row = True
        for j in range(4, unit_width + 4):
            if not grid[i][j]:
                full_row = False
                break
        if full_row:
            g = copy.deepcopy(grid)
            for ii in range(4, i):
                grid[ii + 1] = g[ii]
        else:
            i -= 1
                
pygame.init()
screen = pygame.display.set_mode(size)
pygame.time.set_timer(pygame.USEREVENT + 1, drop_speed)

p = Piece()
grid = [[0 for i in range(unit_width + 8)] for j in range(unit_height + 8)]
for i in range(unit_height + 8):
    for j in range(unit_width + 8):
        if i >= unit_height + 4:
            grid[i][j] = -1
        elif j < 4 or j >= unit_width + 4:
            grid[i][j] = -1
        
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.USEREVENT + 1: p.drop()
        elif event.type == pygame.USEREVENT + 2: p.move('left')
        elif event.type == pygame.USEREVENT + 3: p.move('right')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: sys.exit(0)
            if event.key == pygame.K_UP: p.rotate()
            elif event.key == pygame.K_DOWN: pygame.time.set_timer(pygame.USEREVENT + 1, drop_speed / 10)
            elif event.key == pygame.K_LEFT:
                p.move('left')
                pygame.time.set_timer(pygame.USEREVENT + 2, move_speed)
            elif event.key == pygame.K_RIGHT:
                p.move('right')
                pygame.time.set_timer(pygame.USEREVENT + 3, move_speed)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: pygame.time.set_timer(pygame.USEREVENT + 1, drop_speed)
            if event.key == pygame.K_LEFT: pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            if event.key == pygame.K_RIGHT: pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                                                    
    screen.fill(pygame.color.Color('black'))

    # draw objects: the pit, the piece and the grid
    pygame.draw.lines(screen, pygame.color.Color('grey'), False, \
                          [(grid_left - 1, grid_top), (grid_left - 1, grid_top + grid_height + 1), \
                               (grid_left + grid_width + 1, grid_top + grid_height + 1), \
                               (grid_left + grid_width + 1, grid_top)], 1)
    p.draw()
    drawGrid()
    
    pygame.display.update()
