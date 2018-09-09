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
sysfont = pygame.font.SysFont(None, 40)

pygame.display.set_caption(u"Undertale")
TITLE, PLAY, CLEAR, GAMEOVER = (0, 1, 2, 3)
START, FIGHT, FLAG = (0, 1, 2)
VIS, UNVIS = (1, 0)
TOUCHABLE, UNTOUCHABLE = (1, 0)
stages = ['None', 'Stage1', 'Stage2']

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
        self.status = TOUCHABLE
        self.speed = 3
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
        self.radius = self.rect.width/2
        print(self.radius)

    def draw(self, screen):
        screen.blit(self.combat, self.rect)
    
class Enemy(pygame.sprite.Sprite):
    shot_prob = 10 # 球発車の乱数ジェネレート。当たり前だが小さいほど頻度が上がる
    def __init__(self, filename, width, height, x, y, max_health, type):
        pygame.sprite.Sprite.__init__(self)
        self.enemy = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.health = max_health 
        self.x = x
        self.y = y
        self.type = type 

    def update(self):
       
        if self.rect.y <= 30:
            self.rect.move_ip(0, 1)

        elif self.rect.y >= 30:
            if self.type == 1:
                shot_prob = 100
                if not random.randrange(shot_prob):
                    new = Barrage("images/asteroid1.png", self.rect.x, self.rect.y, 30, 30, 15, 15, 1, [5])
    
            if self.type == 2:
                shot_prob = 10
                if not random.randrange(shot_prob):
                    new = Barrage("images/asteroid1.png", self.rect.x, self.rect.y, 30, 30, 15, 15, 1, [5])
                    return None


    def draw(self, screen):
        screen.blit(self.enemy, self.rect)
        
        pygame.draw.line(screen, (90, 140, 40), (self.rect.x, self.rect.y-10), (self.rect.x + self.health * 10, self.rect.y-10), 5)

class Barrage(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy, width, height, type, option = None):
        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image(filename, width, height)
        self.rect = Rect(x, y, width, height)
        self.x = x; self.y = y;
        self.vx = random.randrange(-3, 3) 
        self.vy = random.randrange(-3, 3)
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
            if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
                self.vy = -self.vy
                self.bounce_counter += 1

            if self.bounce_counter >= self.option[0]:
                self.kill()
                
          # 画面からはみ出ないようにする
            self.rect = self.rect.clamp(SCR_RECT)

        elif self.type == 2:    # type_2: 頂点を出発点、ランダムな傾きを加えた二次関数、式は上に凸だが実際は下に凸として描画される。また左右もランダム
            for x in range(100):
                y = (x - self.x)^2 + self.y
                self.rect.move_ip(x-self.rect.x, y-self.rect.y)
            
class Button(pygame.sprite.Sprite):
    def __init__(self, filename, width, height, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.button = load_image(filename, width, height)
        self.width = width; self.height = height;
        self.rect = Rect(x, y, width, height)

    def update(self):

        self.x = random.randrange(1, 400)
        self.y = random.randrange(30, 200)
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.button, self.rect)

#class Explosion(pygame.sprite.Sprite):
#    animcycle = 5
#    frame = 0
#    def __init__(self, pos):
#        self.image = self.images[0]
#        self.rect = self.rect = self.image.get_rect()
#        self.rect.center = pos
#        self.max_frame = len(self.images) * self.animcycle
#    def update(self):
#        self.image = self.images[self.frame/self.animcycle]
#        self.frame += 1
#        if self.frame == self.max_frame:
#            self.kill()

class Underheart:
    def __init__(self):
        Explosion.images = [load_image("images/healthy_heart.png", 10, 10), load_image("images/broken_heart.png", 10, 10)]
        self.game_status = TITLE 
        self.game_init()
        self.load_bullets()
        self.stage_flag = 0
        self.fullscreen_flag = False

        self.hit_sound = pygame.mixer.Sound("sounds/bad.wav")
        self.break_sound = pygame.mixer.Sound("sounds/break.wav")
        self.select_sound = pygame.mixer.Sound("sounds/select.wav")
        self.enter_sound = pygame.mixer.Sound("sounds/enter.wav")
        self.attack_sound = pygame.mixer.Sound("sounds/attack.wav")

#        foo = load_image("healthy_heart.png", 10, 10)
#        bar = load_image("broken_heart.png", 10, 10)
#        Explosion.images = [foo, bar]

        self.title_phrase = load_image("images/title_phrase.png", 400, 40)
        self.buttons = pygame.sprite.RenderUpdates()
        Button.containers = self.buttons
        
        self.fight_button = Button("images/button_fight.png", 100, 50, 200, 200)
        self.start_button = Button("images/button_mercy.png", 100, 50, 320, 100)
        self.stage1_button = Button("images/button_stage1.png", 100, 50, 70, 180)
        self.stage2_button = Button("images/button_stage2.png", 100, 50, 200, 180)
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

        self.enemy = Enemy("images/spaceship.png", 50, 50, 320, -100, 10, 0)

        self.stage_flag = 0

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
            self.stage2_button.draw(screen)
            screen.blit(sysfont.render("Selected Stage is "+str(stages[self.stage_flag]), False, (255, 255, 255)), (0, 0))
            self.start_button.draw(screen)
            self.player.draw(screen)
            return None

        elif self.game_status == PLAY:
            screen.fill((0, 0, 0))
            self.fight_button.draw(screen)
            self.enemy.draw(screen)
            pygame.draw.line(screen, (255, 255, 255), (self.enemy.x, self.enemy.y+10), (self.enemy.x + self.enemy.health * 5, self.enemy.y+10), 5)
            self.bars.draw(screen)
            self.player.draw(screen)
            return None

        elif self.game_status == CLEAR:
            screen.fill((200, 200, 200))
            score = self.frame * self.player_health
            screen.blit(sysfont.render("YOUR SCORE : "+str(score), False, (255, 255, 255)), (0, 0))
            return None

        elif self.game_status == GAMEOVER:
            screen.fill((100, 100, 100))
            #self.over_anime()
            return None

    def over_anime(self):   #未実装
        message = "Except Your Dead.\nIf you refuse to die, press Z"
        charactors = message.split(' ')
        for i in range(len(charactors)):
            screen.blit(sysfont.render(charactors[0, i], False, (255, 255, 255)), (0, 0))
         
    def collisionOfBullet(self):
        bullet_col = pygame.sprite.spritecollide(self.player, self.bars, True, pygame.sprite.collide_circle)
        if bullet_col:
            self.player_health -= 1 
            self.hit_sound.play()
            # ダメージを受けるとダンダン自機が小さくなっていく
            self.player.combat = pygame.transform.scale(self.player.combat, (self.player_scale[self.player_health], self.player_scale[self.player_health]))
            self.player.rect = (0, 0, self.player_scale[self.player_health], self.player_scale[self.player_health])
            # プレイヤーの体力がなくなったらゲームオーバー
            if self.player_health < 0:
                self.break_sound.play()
                #Explosion(self.player.rect.center)
                pygame.time.wait(1000)
                self.game_status = GAMEOVER

    def collisionOfButton(self, button, act, flag = None):
        button_col = pygame.sprite.collide_rect(self.player, button)
        if button_col:
            if act == FLAG:
                self.select_sound.play()
                if flag == 1:
                    self.stage_flag = 1

                if flag == 2:
                    self.stage_flag = 2

                self.enemy = Enemy("images/spaceship.png", 50, 50, 320, -100, 30, self.stage_flag)

            if act == START:
                self.enter_sound.play()
                self.game_status = PLAY
            if act == FIGHT:
                self.attack_sound.play()
                self.enemy.health -= 1
                self.fight_button.update()
                        
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_F2:
                    self.fullscreen_flag = not self.fullscreen_flag
                    if self.fullscreen_flag:
                        screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode(SCR_RECT.size, 0, 32)
                
                if self.game_status == TITLE:
                    if event.key == K_z:
                        self.collisionOfButton(self.stage1_button, FLAG, 1) 
                        self.collisionOfButton(self.stage2_button, FLAG, 2) 
                        if self.stage_flag != 0:
                            self.collisionOfButton(self.start_button, START)
                        

                elif self.game_status == PLAY:
                    if event.key == K_z:
                        self.collisionOfButton(self.fight_button, FIGHT)
                elif self.game_status == GAMEOVER or self.game_status == CLEAR:
                    if event.key == K_z:
                        self.bars.empty()
                        self.enemy.kill()
                        self.game_status = TITLE 
                        self.game_init()

if __name__ == "__main__":
    myGame = Underheart()
