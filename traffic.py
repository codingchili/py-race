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

#Traffic module.

import pygame, os, sys, math, maps
from pygame.locals import *
from random import randint
from loader import load_image

BOUND_MIN = 380
BOUND_MAX = 620
TURN_LOCK = 375 
DISPLACEMENT = 65 
CENTER_W = -1
CENTER_H = -1
HALF_TILE = 500

cars = []
car_files = ['traffic1.png', 'traffic2.png', 'traffic3.png',
             'traffic4.png', 'traffic5.png']

#Rotate cars.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#Initialize cars.
def initialize(center_w, center_h):
    CENTER_W = center_w
    CENTER_H = center_h

    for index in range(0, len(car_files)):
        cars.append(load_image(car_files[index], True))

#Traffic sprite and AI controller.
class Traffic(pygame.sprite.Sprite):

    def road_tile(self):
        x = randint(0,9)
        y = randint(0,9)
        while (maps.map_1[x][y] != 0):
            x = randint(0,9)
            y = randint(0,9)
        return x * 1000 + HALF_TILE, y * 1000 + HALF_TILE

#Turn the vehicle!
    def turning(self):
        self.turning_cooldown = TURN_LOCK
        try:
            tile_type = maps.map_1[int((self.y + CENTER_H) / 1000)][int((self.x + CENTER_W) / 1000)]
            tile_rot  = maps.map_1_rot[int((self.y + CENTER_H) / 1000)][int((self.x + CENTER_W) / 1000)]

#turn controller
            if tile_type == maps.turn:
                if (tile_rot + 2 == self.dir / 90) or (-(tile_rot + 2) == self.dir / 90):
                    self.dir += 90
                else:
                    self.dir -= 90

#split controller
            if tile_type == maps.split:
                self.dir = -180 - tile_rot * 90
                self.dir += randint(-1, 1) * 90

#crossing controller
            if tile_type == maps.crossing:
                self.dir += randint(1,3) * 90

#dead end controller
            if tile_type == maps.deadend:
                self.dir -= 180 

        except:
            return

#Rotate the image.
    def rotate(self):
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

#Initialize the object.           
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cars[randint(0, len(cars))-1] 
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.id = randint(0,99)
        self.area = self.screen.get_rect()
        self.x, self.y = self.road_tile()
        self.rect.topleft = self.x, self.y
        self.dir = 0
        self.turning()
        self.rotate()
        self.speed = randint(60, 145) / 100
        self.turning_cooldown = 0

#Update the position.
    def update(self, cam_x, cam_y):
        """update direction of traffic based on current tile"""
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
        
#trigger turn when vehicle is at center of tile.
        if (self.turning_cooldown > 0):
                self.turning_cooldown = self.turning_cooldown - 1
        elif (randint(0, DISPLACEMENT) == 2):
            if (self.x % 1000 > BOUND_MIN and self.x % 1000 < BOUND_MAX):
                if (self.y % 1000 > BOUND_MIN and self.y % 1000 < BOUND_MAX):
                        self.turning()
                        self.rotate()   

        self.rect.topleft = self.x - cam_x, self.y - cam_y



              
