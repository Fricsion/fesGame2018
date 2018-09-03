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
        self.rect = Rect(x, y, width, height)
        self.radius = width/3 # 円の当たり判定で使うゾ

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LSHIFT]:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-2, 0)
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(2, 0)
            if pressed_key[K_UP]:
                self.rect.move_ip(0, -2)
            if pressed_key[K_DOWN]:
                self.rect.move_ip(0, 2)
        else:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(5, 0)
            if pressed_key[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_key[K_DOWN]:
                self.rect.move_ip(0, 5)

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
