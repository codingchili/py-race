#The MIT License (MIT)

#Copyright (c) 2012 Robin Duda, (chilimannen)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#Camera module will keep track of sprite offset.

#Map file.

import os, sys, pygame, math
from pygame.locals import *
from loader import load_image
from random import randrange

#Map filenames.

map_files = []
map_tile = ['X.png', 'I.png', 'L.png', 'T.png', 'O.png', 'null.png']

#Map to tile.
crossing = 0
straight = 1
turn     = 2
split    = 3
deadend  = 4
null     = 5

#tilemap.
map_1 = [
          [2,1,3,1,1,3,1,1,1,4],
          [1,5,1,5,4,0,1,2,5,4],
          [1,4,3,1,3,3,1,3,2,1],
          [3,1,3,1,3,5,4,5,1,1],
          [3,2,1,5,1,5,3,1,0,3],
          [1,2,0,1,0,3,0,4,1,1],
          [1,5,1,4,2,1,1,2,3,1],
          [1,2,0,1,3,3,0,0,2,1],
          [1,1,4,2,2,5,1,2,1,3],
          [2,3,1,3,1,1,3,1,1,2]
        ]

#tilemap rotation, x90ccw
map_1_rot = [
          [1,1,0,1,1,0,1,1,1,3],
          [0,0,0,0,1,0,1,0,0,0],
          [0,1,2,1,0,2,1,2,0,0],
          [1,1,0,1,3,0,0,0,0,0],
          [1,0,0,0,0,0,1,1,0,3],
          [0,2,0,1,0,0,0,3,0,0],
          [0,0,0,1,3,0,0,1,3,0],
          [0,1,0,1,0,2,0,0,3,0],
          [0,0,2,1,3,0,0,2,1,3],
          [2,2,1,2,1,1,2,1,1,3]
            ]


class Map(pygame.sprite.Sprite):
    def __init__(self, tile_map, y, x, rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = map_files[tile_map]
        self.rect = self.image.get_rect()

        if rot != 0:
            self.image = pygame.transform.rotate(self.image, rot * 90)

        self.x = x
        self.y = y

#Realign the map
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        
     
