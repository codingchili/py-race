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

import os, sys, pygame, random, array, gamemode
import direction,  bounds, timeout, menu
from pygame.locals import *

#Import game modules.
from loader import load_image
import player, maps, traffic, camera, tracks


TRAFFIC_COUNT = 45
CENTER_W = -1
CENTER_H = -1


#Main function.
def main():
#initialize objects.
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = player.Player()
    cam = camera.Camera()
    target = gamemode.Finish()
    bound_alert = bounds.Alert()
    time_alert = timeout.Alert()
    info = menu.Alert()
    pointer = direction.Tracker(int(CENTER_W * 2), int(CENTER_H * 2))
#create sprite groups.
    map_s     = pygame.sprite.Group()
    player_s  = pygame.sprite.Group()
    traffic_s = pygame.sprite.Group()
    tracks_s  = pygame.sprite.Group()
    target_s  = pygame.sprite.Group()
    pointer_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    menu_alert_s = pygame.sprite.Group()

#generate tiles
    for tile_num in range (0, len(maps.map_tile)):
        maps.map_files.append(load_image(maps.map_tile[tile_num], False))
    for x in range (0, 10):
        for y in range (0, 10):
            map_s.add(maps.Map(maps.map_1[x][y], x * 1000, y * 1000, maps.map_1_rot[x][y]))

#load tracks
    tracks.initialize()
#load finish
    target_s.add(target)
#load direction
    pointer_s.add(pointer)
#load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    menu_alert_s.add(info)
#load traffic
    traffic.initialize(CENTER_W, CENTER_H)
    for count in range(0, TRAFFIC_COUNT):
        traffic_s.add(traffic.Traffic())

    player_s.add(car)

    cam.set_pos(car.x, car.y)

    while running:
#Render loop.

#Check for menu/reset, (keyup event - trigger ONCE)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if keys[K_m]:
                    if (info.visibility == True):
                        info.visibility = False
                    else:
                        info.visibility = True
                if (keys[K_p]):
                    car.reset()
                    target.reset()
                if (keys[K_q]):
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

#Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if (target.timeleft > 0):
            if keys[K_LEFT]:
                car.steerleft()
            if keys[K_RIGHT]:
                car.steerright()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()

        cam.set_pos(car.x, car.y)

#Show text data.
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (224, 16, 16))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)

        text_score = font.render('Score: ' + str(target.score), 1, (224, 16, 16))
        textpos_score = text_fps.get_rect(centery=45, centerx=60)

        text_timer = font.render('Timer: ' + str(int((target.timeleft / 60)/60)) + ":" + str(int((target.timeleft / 60) % 60)), 1, (224, 16, 16))
        textpos_timer = text_fps.get_rect(centery=65, centerx=60)

#Render Scene.
        screen.blit(background, (0,0))

        #cam.set_pos(car.x, car.y)

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)
        
#Conditional renders/effects
        car.grass(screen.get_at(((int(CENTER_W-5), int(CENTER_H-5)))).g)
        if (car.tracks):
            tracks_s.add(tracks.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

#Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)
        
        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        traffic_s.update(cam.x, cam.y)
        traffic_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        pointer_s.update(car.x + CENTER_W, car.y + CENTER_H, target.x, target.y)
        pointer_s.draw(screen)

#Conditional renders.
        if (bounds.breaking(car.x+CENTER_W, car.y+CENTER_H) == True):
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if (target.timeleft == 0):
            timer_alert_s.draw(screen)
            car.speed = 0
            text_score = font.render('Final Score: ' + str(target.score), 1, (224, 16, 16))
            textpos_score = text_fps.get_rect(centery=CENTER_H+56, centerx=CENTER_W-20)
        if (info.visibility == True):
            menu_alert_s.draw(screen)
            
#Blit Blit..       
        screen.blit(text_fps, textpos_fps)
        screen.blit(text_score, textpos_score)
        screen.blit(text_timer, textpos_timer)
        pygame.display.flip()

#Check collision!!!
        if pygame.sprite.spritecollide(car, traffic_s, False):
            car.impact()
            target.car_crash()

        if pygame.sprite.spritecollide(car, target_s, True):
            target.claim_flag()
            target.generate_finish()
            target_s.add(target)
            
        clock.tick(64)
        

#initialization
pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)


pygame.display.set_caption('Race of Math.')
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 24)

CENTER_W =  int(pygame.display.Info().current_w /2)
CENTER_H =  int(pygame.display.Info().current_h /2)

#new background surface
background = pygame.Surface(screen.get_size())
background = background.convert_alpha()
background.fill((26, 26, 26))

#Enter the mainloop.
main()

pygame.quit()
sys.exit(0)













        

