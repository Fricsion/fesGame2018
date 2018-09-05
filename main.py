#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random

SCR_RECT = Rect(0, 0, 640, 480)
pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size)
pygame.display.set_caption(u"Undertale")
TITLE, PLAY, GAMEOVER = (0, 1, 2)

def load_image(filename, width, height):
   image = pygame.image.load(filename).convert_alpha()
   image = pygame.transform.scale(image, (width, height))
   return image
 
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.combat = load_image(filename, width, height)
        width = self.combat.get_width()
        height = self.combat.get_height()
        self.speed = 5
        self.rect = Rect(x, y, width, height)
        self.radius = width/3 # 円の当たり判定で使うゾ

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LSHIFT]:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-self.speed/2, 0)
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.speed/2, 0)
            if pressed_key[K_UP]:
                self.rect.move_ip(0, -self.speed/2)
            if pressed_key[K_DOWN]:
                self.rect.move_ip(0, self.speed/2)
        else:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.speed, 0)
            if pressed_key[K_UP]:
                self.rect.move_ip(0, -self.speed)
            if pressed_key[K_DOWN]:
                self.rect.move_ip(0, self.speed)
        self.rect = self.rect.clamp(SCR_RECT)

    def draw(self, screen):
        screen.blit(self.combat, self.rect)
    
class Enemy:
    def __init__(self, filename, width, height, x, y):
        self.enemy = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.enemy, self.rect)

class Barrage(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy, width, height, type):
        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.vx = random.randint(1, 10)
        self.vy = random.randint(1, 10)
        self.type = type
        self.radius = width/3   # 円の当たり判定で使うゾ
    
    def update(self):

        if self.type == 0:  # type_0: 直線移動して画面外に出たら消える
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
                self.kill()
            if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
                self.kill()

        elif self.type == 1:    # type_1: 直線移動して画面外に出ず淵で跳ね返る
            self.rect.move_ip(self.vx, self.vy)
            # 壁にぶつかったら跳ね返る
            if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
                self.vx = -self.vx
            if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
                self.vy = -self.vy
            # 画面からはみ出ないようにする
            self.rect = self.rect.clamp(SCR_RECT)

class Button(pygame.sprite.Sprite):
    def __init__(self, filename, width, height, x, y, command):
        self.button = load_image(filename, width, height)
        sdelf.rect = Rect(x, y, width, height)
        self.command = command

    def draw(self, screen):
        screen.blit(self.button, self.rect)

def main():

<<<<<<< HEAD
class Undertale:
    def __init__(self):
        self.game_status = TITLE 
        self.game_init()
        
        self.player = Player("images/heart.png", self.player_health*10, self.player_health*10, 320, 200)

        self.start_button = Button("images/button_mercy.png", 100, 40, 10, 10, 0)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            
            self.update()
            self.draw(screen)

            pygame.display.update()

            self.key_handler()

    def game_init(self):

        self.player_health = 3

        self.enemy = Enemy("images/spaceship.png", 50, 50, 320, 100)

        bullet_list = [0, 0, 1, 1]

        self.bars = pygame.sprite.RenderUpdates()
        Barrage.containers = self.bars
        for type in bullet_list:
            new = Barrage("images/asteroid1.png", self.enemy.x, self.enemy.y, 5, 5, 30, 30, type)

    def update(self):
        if self.game_status == TITLE:
            self.player.move()
            return None

        elif self.game_status == PLAY:
            self.player.move()
            self.bars.update()
            self.collisionOfBullet()
            return None

        elif self.game_status == GAMEOVER:
            return None


    def draw(self, screen):
        if self.game_status == TITLE:
            screen.fill((0, 0, 0))
            self.start_button.draw(screen)
            self.player.draw(screen)
            return None

        if self.game_status == PLAY:
            screen.fill((0, 0, 0))
            self.enemy.draw(screen)
            self.bars.draw(screen)
            self.player.draw(screen)
            return None

        if self.game_status == GAMEOVER:
            return None

    def collisionOfBullet(self):
        bullet_col = pygame.sprite.spritecollide(self.player, self.bars, True, pygame.sprite.collide_circle)
        if bullet_col:
            self.player_health = self.player_health - 1
            self.player.combat = pygame.transform.scale(self.player.combat, (self.player_health*10, self.player_health*10))
            if self.player_health < 0:
                self.game_status == GAMEOVER

    def collisionOfButton(self, button):
        button_col = pygame.sprite.collide_rect(self.player, button)
        if button_col:
            self.game_status = PLAY


    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if self.game_status == TITLE:
                    if event.key == K_z:
                        self.collisionOfButton(self.start_button)
                elif self.game_status == GAMEOVER:
                    if event.key == K_z:
                        self.game_status = TITLE

if __name__ == "__main__":
    Undertale()
=======

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
>>>>>>> 2b22126005da4bd916483a703bf5befa43e270e3
