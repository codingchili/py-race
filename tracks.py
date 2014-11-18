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

#The car will emit tracks.
import os, sys, pygame
from pygame.locals import *
from loader import load_image

LIFETIME = 300

#rotate tracks.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#Initialize, load the tracks image.
def initialize():
    global tracks_img
    tracks_img = load_image('tracks.png', False)

#Track sprite class.
class Track(pygame.sprite.Sprite):
    def __init__(self, car_x, car_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = rot_center(tracks_img, tracks_img.get_rect(), angle)
        self.lifetime = LIFETIME
        self.screen = pygame.display.get_surface()
        self.x = car_x  + 3 
        self.y = car_y  + 20
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        self.lifetime = self.lifetime - 1

        if (self.lifetime < 1):
            pygame.sprite.Sprite.kill(self)
        

