# Pygame template - skeleton for a new pygame project
from ast import While
from itertools import count
import re
import time
from tkinter import Y
from numpy import record
import pygame
import random
import os
import json
from math import *
from pygame.display import flip, gl_get_attribute, update

#Hero data
hero_damage = 10
hero_life = 10
bullet_frequence = 7

#enemy1 data
enemy1_heart = 10
enemy1_frequence = 30

#enemy2 data
enemy2_heart = 30
enemy2_frequence = 100

#game constants
WIDTH = 360 #screen WIDTH
HEIGHT = 540 #screen HEIGHT
FPS = 30 # Game FPS
count1 = 0  #count for bullet refresh rate
count2 = 0  #enemy 1
count3 = 0  #enemy 2
score = 0 # score for every game
running1 = True # whether shown the window
running2 = False # whether start a game
running3 = False # whether break the record
deathX_array = [] # Store the dead x-coordinate of enemy
deathY_array = [] # Store the dead y-coordinate of enemy

# define colors (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (195, 176, 145)

with open("record.json",'r',encoding='utf-8') as load_f: #read json document
    record = json.load(load_f) # json.load() can convert document into python object(dictionary)


# initialize pygame and create window
pygame.init()
pygame.mixer.init() # initialize mixer 
pygame.mixer.music.set_volume(0.3)# set the sound size (a float value from 0-1)
pygame.mixer.music.load(os.path.join('sound', 'bgm.ogg')) # read background music ducument
explosion_sound = pygame.mixer.Sound(os.path.join('sound', 'explosion.wav')) #read the explosion sound as an object

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #create screen object with Width and height
pygame.display.set_caption("The plane war") #Set window title
clock = pygame.time.Clock() #create time object

#define font with type and size
myfont = pygame.font.SysFont('algerian',40)
myfont2 = pygame.font.SysFont('curlz',55)

#creat spites list object
bulletSprites = pygame.sprite.Group() 
meSprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
ExplosionSprites = pygame.sprite.Group()

#hero class
class Player(pygame.sprite.Sprite): #inherite pygame. sprite.Sprite object
    def __init__(self): #rewrite a constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("img", 'me.png')).convert() #read heros picture
        self.image.set_colorkey(WHITE) # set White color to transparent
        self.rect = self.image.get_rect() # rect of object equal to rect of picture
        self.rect.center = (WIDTH / 2, HEIGHT / 2) # initial xy coordinate of rect
        self.life = hero_life # initial hero's life
    
    def update(self): #rewrite undate 
        self.rect.center = (meX,meY) # update rect coordinate with same value of mouse position
        if self.life <= 0: #if hero don't have life, kill this object
            self.kill()
player = Player() # referenced object
meSprites.add(player) # add object to list

#子弹
class MyBullet(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("img", 'shoot.png')).convert()
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect() 
        self.rect.topleft  = (meX,meY)

    def update(self):
        self.rect.y -= 5 # move upward for each update
        if self.rect.y < 0: # kill themselves if they are out of screen
            self.kill()

#爆炸
class explosion(pygame.sprite.Sprite):  # 继承pygame.sprite.Sprite精灵对象
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("img", 'explosion.png')).convert()
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect() 
        self.rect.center = (deathX,deathY) # create exposion at where the enemy dead
        self.count = 0 #count for showing time

    def update(self):
        self.count += 1
        if self.count == 3: #shown 3 times then kill them self
            self.kill()
            


class Enemy1(pygame.sprite.Sprite):  # 继承pygame.sprite.Sprite精灵对象
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(os.path.join("img", 'enemy1.png')).convert()
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect() 
        self.rect.center  = (random.randint(10,WIDTH-10),0)
        self.life = enemy1_heart # life variable

    def update(self):
        self.rect.y += 5 # move downward for each update 
        if self.rect.y > HEIGHT: #kill themselves when they reach the planet, and minus 1 life of heros
            self.kill()
            player.life -= 1
        if pygame.sprite.groupcollide(bulletSprites, enemySprites, True, False): # if bullet in bulletSprites collide enemySprites, kill bullet
            self.life -= hero_damage    # enemy life minus damage caused by bullet
        if pygame.sprite.groupcollide(meSprites, enemySprites, False, True): #if hero collide with enemy, kill enemy
            deathX_array.append(self.getposX()) #add value of xy-coordinate in list
            deathY_array.append(self.getposY())
            player.life -= 1 #hero life minus 1, because of collison
        if self.life <= 0: # don't have life because of shoot
            global score
            score += 1 # these two line is add point to global score, instead of create a new score
            self.kill()
            deathX_array.append(self.getposX()) # add death position to list
            deathY_array.append(self.getposY())

    def getposX(self): #return current x
        return self.rect.x

    def getposY(self): #return current y
        return self.rect.y
   
class Enemy2(pygame.sprite.Sprite):  # same with Enemy1, but different pictures and life
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(os.path.join("img", 'enemy2.png')).convert()
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect() 
        self.rect.center  = (random.randint(10,WIDTH-10),0)
        self.life = enemy2_heart
    def update(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.kill()
            player.life -= 1
        if pygame.sprite.groupcollide(bulletSprites, enemySprites, True, False):
            self.life -= hero_damage
        if pygame.sprite.groupcollide(meSprites, enemySprites, False, True):
            deathX_array.append(self.getposX())
            deathY_array.append(self.getposY())
            player.life -= 1
        if self.life <= 0:
            global score
            score += 5
            deathX_array.append(self.getposX())
            deathY_array.append(self.getposY())
            self.kill()

    def getposX(self): 
        return self.rect.x

    def getposY(self): 
        return self.rect.y

#游戏开始提示
start_image1 = myfont.render("press space", True, WHITE) #create image object by myfont(text you want to show, whether antialias, color)
start_image2 = myfont.render("to start", True, WHITE)
background = pygame.image.load(os.path.join("img", 'background.png')).convert() # read background images
background2 = pygame.image.load(os.path.join("img", 'background2.png')).convert()
screen.blit(background,(0,0)) # drawing image object on screen
screen.blit(start_image1,(50,HEIGHT/2-50))
screen.blit(start_image2,(80,HEIGHT/2))
pygame.display.flip() #show the screen

while running1: 

    pygame.mixer.music.play()# start background music

    if player.life <= 0: # reset and generate player
        player = Player()
        meSprites.add(player)
        player.life = hero_life

    #空格键开始&检测关闭
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # start the game only when keyboard down and this key is space
            running2 = True
        if event.type == pygame.QUIT: #cature the whether the player close the window
            running2 = False
            running1 = False
    
    while running2: # game start
        for event in pygame.event.get():
            # 检测关闭
            if event.type == pygame.QUIT: 
                running2 = False
                running1 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # pause
                running2 = False

        #Control the frequence at which the bullet appears
        count1 += 1 
        if count1 >= bullet_frequence:
            count1 = 0
        if count1 == 0:
            mybullet = MyBullet() # creat referenced object
            bulletSprites.add(mybullet) # add into list

        #control enemy1 like bullet
        if count2 >= enemy1_frequence:
            count2 = 0
            enemy1 = Enemy1()
            enemySprites.add(enemy1)
        count2 += 1
        
        #control enemy2
        if count3 >= enemy2_frequence:
            count3 = 0
            enemy2 = Enemy2()
            enemySprites.add(enemy2) 
        count3 += 1

        #add explosion to every death position in the two lists
        if (len(deathX_array)!=0):
            for i in range(len(deathX_array)):
                deathX = deathX_array[i]
                deathY = deathY_array[i]
                print(deathX,deathY)
                Explosion = explosion()
                ExplosionSprites.add(Explosion)
            deathX_array.clear() # clear all the object in the list
            deathY_array.clear()
            explosion_sound.play() # play explosion sounds

        # keep loop running at the right speed
        clock.tick(FPS)

        # Update new image of life and score
        life_text = myfont.render('Life: ' + str(player.life), True, WHITE)
        scoreImage = myfont.render(str(score), True, WHITE)
        
        #get position of mouse
        meX, meY = pygame.mouse.get_pos()

        #update each sprites
        meSprites.update()
        bulletSprites.update()
        enemySprites.update()
        ExplosionSprites.update()

        # Drawing all sprites in the list
        screen.blit(background,(0,0))
        meSprites.draw(screen)
        bulletSprites.draw(screen)
        enemySprites.draw(screen)
        ExplosionSprites.draw(screen)
        screen.blit(life_text,(200,10))
        screen.blit(scoreImage, (10, 10))


        # *after* drawing everything, flip the display
        pygame.display.flip()

        #gradually increase the interval between enemy appearances
        enemy1_frequence = enemy1_frequence*0.9995
        enemy2_frequence = enemy2_frequence*0.9995

        #check whether player has life
        if player.life == 0:
            screen.blit(background2,(0,0)) #if dead, shown the background2
            y = 250 #y coordinate of record image
            temp_score = score
            for key,value in record.items(): #if player have new record, add it into dictionary and show
                if(score > value):
                    temp = value
                    record[key]= temp_score
                    temp_score = temp
                    running3 = True # the player have new record
                recordLine = str(key) + "  " + str(record[key])
                recordImage = myfont.render(recordLine,True,WHITE)
                screen.blit(recordImage,(50,y))
                y += 50
            
            if(running3): # show new best word with green color and myfont2
                current_score = myfont2.render("new best " + str(score), True, GREEN)
                with open("record.json",'w',encoding='utf-8') as f: # write new record into json document
                    json.dump(record, f,ensure_ascii=False)
            else: # or show regular image
                current_score = myfont.render("this time " + str(score), True, WHITE)

            overImage = myfont2.render("GAME OVER", True, RED) # create image
            Bestscore = myfont.render("best score", True, WHITE)

            screen.blit(overImage,(50,100)) #draw on the screen
            screen.blit(Bestscore,(50,200))
            screen.blit(current_score,(50,400))

            running2 = False # game over
            pygame.display.flip() # show the screen
            score = 0 # set score to 0
            for item in enemySprites: #kill all the enemy left and reset frequency
                item.kill()
                enemy1_frequence = 30
                enemy2_frequence = 100     
            for item in bulletSprites: #kill all the bullet
                item.kill()
            for item in ExplosionSprites: #kill all the explosion
                item.kill()

pygame.quit() # quit the pygame