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

#Show the player where to find the flag.

import pygame, math
from pygame.locals import *
from loader import load_image

PI = 3.14

#rotate the arrow.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#Guide the player with a giant arrow.
class Tracker(pygame.sprite.Sprite):

    def __init__(self, screen_x, screen_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = load_image('direction.png', False)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect_orig = self.rect
        self.x = screen_x - 150
        self.y = screen_y - 150
        self.rect.topleft = self.x, self.y
        self.dir = 0

#Update the rotation of the arrow.
    def update(self, point_x, point_y, target_x, target_y):
        self.dir = (math.atan2(point_y - target_y, target_x - point_x) * 180 / PI)
        self.image, self.rect = rot_center(self.image_orig, self.rect_orig, self.dir)
        
    
