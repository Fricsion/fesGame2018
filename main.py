#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCR_RECT = Rect(0, 0, 640, 480)

def load_image(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
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
    
#class Barrage(pygame.sprite.Sprite):
#    def __init__(self, filename, x, y, vx, vy, width, height):
#        # デフォルトグループをセット
#        pygame.sprite.Sprite.__init__(self, self.containers)
#        self.image = load_image(filename, width, height)
#        self.rect = Rect(x, y, width, height)
#        self.vx = vx
#        self.vy = vy
#        self.radius = width/3   # 円の当たり判定で使うゾ
#    
#    def update(self):
#        self.rect.move_ip(self.vx, self.vy)
#        # 壁にぶつかったら跳ね返る
#        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
#            self.vx = -self.vx
#        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
#            self.vy = -self.vy
#        # 画面からはみ出ないようにする
#        self.rect = self.rect.clamp(SCR_RECT)

class Button(pygame.sprite.Sprite):
    def __init__(self, filename, width, height, x, y):
        self.button = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.button, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"Undertale")

    game_status = 0
    #ステータス、０：メインメニュー、１：ゲームメニュー、２、ゲームオーバー画面

    player = Player("images/heart.png", 200, 150, 20, 20)

    bullet_list = []
    
#    # スプライトグループを作成してスプライトクラスに割り当て
#    bars = pygame.sprite.RenderUpdates()
#    Barrage.containers = bars 
#    
#    # スプライトを作成
#    bar1 = Barrage("images/asteroid1.png", 0, 0, 2, 2, 30, 30)
#    bar2 = Barrage("images/asteroid2.png", 10, 10, 5, 5, 30, 30)
#    bar3 = Barrage("images/asteroid3.png", 320, 240, -2, 3, 30, 30)
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)  # 60fps
        screen.fill((0,0,0))



        #プレイヤー移動＆描画
        player.move()
        player.draw(screen)

        # スプライトグループを更新＆描画
#        bars.update()
#        bars.draw(screen)

        #当たり判定
#        bar_collision = pygame.sprite.spritecollide(player, bars, True, pygame.sprite.collide_circle)
#        if bar_collision:
#            player.kill()
            


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
