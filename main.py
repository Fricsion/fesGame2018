#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random

SCR_RECT = Rect(0, 0, 640, 360) 
pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size)
#screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|HWSURFACE|FULLSCREEN)
sysfont = pygame.font.SysFont(None, 80)

pygame.display.set_caption(u"Undertale")
TITLE, PLAY, CLEAR, GAMEOVER = (0, 1, 2, 3)
START, FIGHT, FLAG = (0, 1, 2)
VIS, UNVIS = (1, 0)

def load_image(filename, width, height):
   image = pygame.image.load(filename).convert_alpha()
   image = pygame.transform.scale(image, (width, height))
   return image

def simplize(number):
    answer = round(number, -3)
    return answer
 
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
    shot_prob = 200 # 球発車の乱数ジェネレート。当たり前だが小さいほど頻度が上がる
    def __init__(self, filename, width, height, x, y, max_health, type):
        self.enemy = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.health = max_health 
        self.x = x
        self.y = y
        self.type = type
        

    def update(self):
        if self.rect.y <= 30:
            self.rect.move_ip(0, 1)

#        shot_orNot = random.randrange(300)
#        if shot_orNot == 1:
#            new = Barrage("images/asteroid1.png", self.x, self.y, 30, 30, 5, 5, 1)
        if self.type == 1:
            if not random.randrange(self.shot_prob):
                new = Barrage("images/asteroid1.png", self.x, self.y, 30, 30, 15, 15, 1, [5])

        if self.type == 2:
            if not random.randrange(self.shot_prob):
                return None


    def draw(self, screen):
        screen.blit(self.enemy, self.rect)

class Barrage(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy, width, height, type, option = None):
        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.vx = random.randint(1, 10)
        self.vy = random.randint(1, 10)
        self.type = type
        self.option = option
        self.bounce_counter = 0
        self.radius = width/3   # 円の当たり判定で使うゾ
    
    def update(self):

        if self.type == 0:  # type_0: 直線移動して画面外に出たら消える
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
                self.kill()
            if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
                self.kill()

        elif self.type == 1:    # type_1: 直線移動して画面外に出ず淵で跳ね返る。Option０に跳ね返り回数を指定可
            self.rect.move_ip(self.vx, self.vy)
            # 壁にぶつかったら跳ね返る
            if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
                self.vx = -self.vx
                self.bounce_counter += 1
                print(self.bounce_counter)

            if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
                self.vy = -self.vy
                self.bounce_counter += 1
                print(self.bounce_counter)

            if self.bounce_counter >= self.option[0]:
                self.kill()
                
          # 画面からはみ出ないようにする
            self.rect = self.rect.clamp(SCR_RECT)
class Button(pygame.sprite.Sprite):
    def __init__(self, filename, width, height, x, y):
        self.button = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.button, self.rect)



class Underheart:
    def __init__(self):
        self.game_status = TITLE 
        self.game_init()
        self.load_bullets()
        self.stage_flag = 0

        self.title_phrase = load_image("images/title_phrase.png", 400, 40)
        
        self.fight_button = Button("images/button_fight.png", 100, 50, 200, 200)
        self.start_button = Button("images/button_mercy.png", 100, 50, 320, 100)
        self.stage1_button = Button("images/button_stage1.png", 100, 50, 70, 180)
        self.clock = pygame.time.Clock()

        while True:
            self.clock.tick(60)

            
            self.update()
            self.draw(screen)

            pygame.display.update()

            self.key_handler()

    def game_init(self):

        self.frame = 0 # ゲームスタート時にカウントを始めゲーム内時間を計算（ゲーム起動時ではない）
        self.player_health = 2
        self.player_scale = [10, 15, 20] # プレイヤーの体力に応じた大きさの設定
        self.player = Player("images/heart.png", self.player_scale[self.player_health], self.player_scale[self.player_health], 320, 180)

#        self.enemy = Enemy("images/spaceship.png", 50, 50, 320, -100, 14)

    def load_bullets(self):

#        self.bullet_list = [[0, 5000, UNVIS], [0, 7000, UNVIS], [1, 9000, UNVIS], [1, 11000, UNVIS],  [1, 13000, UNVIS]]
#        self.bullets = [3000, 9000, 15000, 20000]

        self.bars = pygame.sprite.RenderUpdates()
        Barrage.containers = self.bars


    def update(self):
        if self.game_status == TITLE:
            self.player.move()
            return None

        elif self.game_status == PLAY:
            self.frame += self.clock.get_time()
            self.player.move()
            self.enemy.update()
            self.bars.update()
            self.collisionOfBullet()
            # 敵の体力がなくなったらクリア画面へ
            if self.enemy.health < 0:
                pygame.time.delay(10)
                self.game_status = CLEAR

            return None

        elif self.game_status == CLEAR:
            return None

        elif self.game_status == GAMEOVER:
            return None


    def draw(self, screen):
        if self.game_status == TITLE:
            screen.fill((0, 0, 0))
            screen.blit(self.title_phrase, (110, 30))
            self.stage1_button.draw(screen)
            self.start_button.draw(screen)
            self.player.draw(screen)
            return None

        elif self.game_status == PLAY:
            screen.fill((0, 0, 0))
#            screen.blit(sysfont.render("Now frame is equal"+str(self.frame), False, (255, 255, 255)), (0, 0))
            self.fight_button.draw(screen)
            self.enemy.draw(screen)
            self.bars.draw(screen)
            self.player.draw(screen)
            return None

        elif self.game_status == CLEAR:
            screen.fill((200, 200, 200))
            return None

        elif self.game_status == GAMEOVER:
            screen.fill((100, 100, 100))
            return None

    def over_anime(self):
        
       # mes = "Except Your Dead.\nIf you refuse to die, press Z"
        
        return None
        
    def collisionOfBullet(self):
        bullet_col = pygame.sprite.spritecollide(self.player, self.bars, True, pygame.sprite.collide_circle)
        if bullet_col:
            self.player_health -= 1 
            # ダメージを受けるとダンダン自機が小さくなっていく
            self.player.combat = pygame.transform.scale(self.player.combat, (self.player_scale[self.player_health], self.player_scale[self.player_health]))
            # プレイヤーの体力がなくなったらゲームオーバー
            if self.player_health < 0:
                self.game_status = GAMEOVER

    def collisionOfButton(self, button, act, flag = None):
        button_col = pygame.sprite.collide_rect(self.player, button)
        if button_col:
            if act == FLAG:
                if flag == 1:
                    self.stage_flag = 1
                self.enemy = Enemy("images/spaceship.png", 50, 50, 320, -100, 14, self.stage_flag)

            if act == START:
                self.game_status = PLAY
            if act == FIGHT:
                self.enemy.health -= 1
            

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
                        self.collisionOfButton(self.stage1_button, FLAG, 1) 
                        if self.stage_flag != 0:
                            self.collisionOfButton(self.start_button, START)
                        

                elif self.game_status == PLAY:
                    if event.key == K_z:
                        self.collisionOfButton(self.fight_button, FIGHT)
                elif self.game_status == GAMEOVER or self.game_status == CLEAR:
                    if event.key == K_z:
                        self.bars.empty()
                        self.game_status = TITLE 
                        self.game_init()

if __name__ == "__main__":
    myGame = Underheart()
