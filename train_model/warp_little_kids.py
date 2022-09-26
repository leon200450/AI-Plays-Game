import numpy as np
import sys
import pygame
from pygame.locals import *
import time
import random
from itertools import cycle
import pygame.surfarray as surfarray
from playsound import playsound
from abc import ABC

from little_kids_game.platform.platform_struct import Platform
from little_kids_game.platform.platform_struct import Board
from little_kids_game.platform.platform_struct import Nails
from little_kids_game.platform.platform_struct import ConveyorLeft
from little_kids_game.platform.platform_struct import ConveyorRight
from little_kids_game.wall.wall_struct import Wall
from little_kids_game.wall.wall_struct import WallCeil

from __init__ import *

width, height = 480, 640  # 把螢幕長寬
pygame.init()
pygame.display.set_caption('小朋友下樓梯')  # 設定視窗名稱
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))  # 設定螢幕長寬
FPS = 60  # 設定幀數
FPSCLOCK = pygame.time.Clock()
PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])



RectFlag = 0
# drop_distance = 0
dmg_judge = [True]

keys = [False, False]  # 設定上下左右判定的list
# count_floor = 0  # 設定往下樓層的變數
walk_count = [0]
gravity = [True]

player_data = {'hp': 10, 'x': 240, 'y': 120, 'img': player_img, 'vel': 1.5}

hp_bar = {0: life0_img, 1: life1_img, 2: life2_img, 3: life3_img,
          4: life4_img, 5: life6_img, 6: life6_img, 7: life7_img,
          8: life8_img, 9: life9_img, 10: life10_img}


class Player:
    def __init__(self, player_data):  # 以後playerdata寫在別的py檔裡面import
        self.hp = player_data['hp']
        self.x = player_data['x']
        self.y = player_data['y']
        self.img = player_data['img']
        self.vel = player_data['vel']
        self.width = 31
        self.height = 31

    def move(self):

        key_p = pygame.key.get_pressed()  # 判定我按的按鍵
        if (key_p[pygame.K_LEFT]):
            keys[0] = True
            keys[1] = False
            if keys[0] == True:
                self.x -= self.vel
                self.img = walk_left_img_list[walk_count[0] % 2]
                walk_count[0] += 1

        elif (key_p[pygame.K_RIGHT]):
            keys[1] = True
            keys[0] = False
            if keys[1] == True:
                self.x += self.vel
                self.img = walk_right_img_list[walk_count[0] % 2]
                walk_count[0] += 1

        else:
            keys[0] = False
            keys[1] = False
            self.img = player_data['img']

from abc import ABC
import random
import pygame
from pygame.locals import *


from __init__ import*

class Platform(ABC):
    def __inif__(self, x, y):
        pass

    def stop_player_fall(self):
        pass

    def float(self):
        pass


class Board (Platform):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = board_pf_img
        self.width =  95
        self.height = 1
        self.cure = 1
        self.cure_judge = True

    def stop_player_fall(self, player1):
        player1.y -=1
    def float(self):
        self.y -= 0.5
        if self.y < 100 or self.y > 1240:
            self.x = random.randint(114, 366)
            self.y = random.randint(740, 1240)
    def rect_collision(self, player1): #創造兩物之間的碰撞
        #上下的碰撞

        platform_rect_up = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
        platform_rect_left = pygame.Rect(self.x, self.y+5, 1, 25)
        platform_rect_right = pygame.Rect(self.x+95, self.y+5, 1, 25)

        if (pygame.Rect.colliderect(platform_rect_up, player_rect) == 1):
            self.stop_player_fall(player1)
            #print(self.cure_judge, player1.hp)
            if player1.hp < 10 and self.cure_judge:

                player1.hp += self.cure
                self.cure_judge = False# 補過血馬上關閉 否則站在上面會一直補血

        else:
            self.cure_judge = True

        if (pygame.Rect.colliderect(platform_rect_left, player_rect) == 1):
            player1.x -= player1.vel

        elif (pygame.Rect.colliderect(platform_rect_right, player_rect) == 1):
            player1.x += player1.vel

        #左右的碰撞
class Nails (Board):
    def __init__(self,x ,y):
        self.x = x
        self.y = y
        self.img = nails_pf_img
        self.width = 95
        self.height = 1
        self.cure = -2
        self.cure_judge = True

    def rect_collision(self, player1): #創造兩物之間的碰撞
        #上下的碰撞

        platform_rect_up = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
        platform_rect_left = pygame.Rect(self.x, self.y+5, 1, 25)
        platform_rect_right = pygame.Rect(self.x+95, self.y+5, 1, 25)

        if (pygame.Rect.colliderect(platform_rect_up, player_rect) == 1):
            self.stop_player_fall(player1)
            #print(self.self.dmg_judge, player1.hp)
            if self.cure_judge:

                player1.hp += self.cure
                self.cure_judge = False# 補過血馬上關閉 否則站在上面會一直補血

        else:
            self.cure_judge = True

        if (pygame.Rect.colliderect(platform_rect_left, player_rect) == 1):
            player1.x -= player1.vel

        elif (pygame.Rect.colliderect(platform_rect_right, player_rect) == 1):
            player1.x += player1.vel

class ConveyorLeft (Board):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = conveyor_left_img
        self.width =  95
        self.height = 1
        self.cure = 1
        self.cure_judge = True
        self.direction = -0.25
    def rect_collision(self, player1): #創造兩物之間的碰撞
        #上下的碰撞

        platform_rect_up = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
        platform_rect_left = pygame.Rect(self.x, self.y+5, 1, 25)
        platform_rect_right = pygame.Rect(self.x+95, self.y+5, 1, 25)

        if (pygame.Rect.colliderect(platform_rect_up, player_rect) == 1):
            self.stop_player_fall(player1)
            player1.x += self.direction
            if player1.hp < 10 and self.cure_judge:

                player1.hp += self.cure
                self.cure_judge = False# 補過血馬上關閉 否則站在上面會一直補血

        else:
            self.cure_judge = True

        if (pygame.Rect.colliderect(platform_rect_left, player_rect) == 1):
            player1.x -= player1.vel

        elif (pygame.Rect.colliderect(platform_rect_right, player_rect) == 1):
            player1.x += player1.vel

class ConveyorRight (ConveyorLeft):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = conveyor_right_img
        self.width =  95
        self.height = 1
        self.cure = 1
        self.cure_judge = True
        self.direction = 0.25

class set_game_env():
    def __init__(self):
        self.count_floor= 0
        self.drop_distance=0
        self.time = 0
    def build_wall(self):
        for x in range(80, 700, 100):  # 設定牆壁
            screen.blit(wall1.img, (0, x))
            screen.blit(wall2.img, (460, x))
        w1_rect =wall1.rect_collision(player1)#左牆
        w2_rect =wall2.rect_collision(player1)#右牆
        if w1_rect:
            player1.x += player1.vel
        if w2_rect:
            player1.x -= player1.vel

    def build_ceil(self):
        screen.blit(wall_ceil1.img, (20, 80))
        screen.blit(wall_ceil2.img, (55, 80))
        wc1_rect =wall_ceil1.rect_collision(player1)
        wc2_rect =wall_ceil2.rect_collision(player1)
        if wc1_rect or wc2_rect:
            player1.y += 35
            if dmg_judge[0]:#傷害判定
                player1.hp -= wall_ceil1.dmg

                dmg_judge[0] =False#為了不重複扣血 扣血後先把傷害鎖起來
        else:#離開尖刺後把傷害判定重新打開
            dmg_judge[0]= True
    def build_player(self):
        screen.blit(player1.img, (player1.x, player1.y))

    def build_floor_label(self):
        head_font = pygame.font.SysFont(None, 60)  # 設定大小60的標題框框
        text_surface = head_font.render('B%04dF'% self.count_floor, True, (121, 255, 121))  # 設定標題的字跟顏色
        screen.blit(text_surface, (300, 25))  # 讓標題印在畫布300,25的地方
    def build_hp_bar(self, player1):
        if player1.hp > 0:
            screen.blit(hp_bar[player1.hp], (10, 0))
        elif player1.hp <= 0:
            screen.blit(hp_bar[0], (10, 0))
    def build_gravity(self, player1):#建造地心引力
        player1.y += 0.5
        self.drop_distance += 0.5

    def build_platform(self):
        board_list =[board1, conveyor_right1, board2, nails1,conveyor_left1]
        board_tmp_y =0#紀錄上一片板子的y

        def build(platform):
            screen.blit(platform.img, (platform.x, platform.y))
            platform.float()
            platform.rect_collision(player1)

        for board in board_list:#檢查兩塊板子中間有沒有靠太近
            if board_tmp_y == 0 :
                board_tmp_y = board.y
            else:
                if(board_tmp_y > board.y and board_tmp_y - board.y < 20):#如果間隔太近
                    board.y -= 100
                    board_tmp_y = board.y
                elif(board_tmp_y <= board.y and board.y - board_tmp_y < 20):
                    board.y += 100
                    board_tmp_y = board.y
            build(board)

    def count_f(self):
        if self.drop_distance > 500:
            self.count_floor += 1
            self.drop_distance = 0

    def set_time(self):
        self.time = pygame.time.get_ticks()

    def bulid_env(self,player1, board1):
        screen.fill((0, 0, 0))  # 把畫布塗黑
        self.build_player()#創造角色
        self.build_wall()#建造牆壁
        self.build_ceil()#建造陷阱
        self.build_floor_label()#建造樓層標題
        self.build_hp_bar(player1)#建造血條
        self.build_gravity(player1)#建造地心引力 順便紀錄下降距離
        #print(f'下降距離:{self.drop_distance}')
        self.count_f()
        self.build_platform()#建造平台
        self.set_time()
        #print(f'角色座標(x:{player1.x} y:{player1.y}')
        pygame.display.update()#刷新畫面





def random_x():
    x = random.randint(114, 366)
    return x
def random_board_y():
    y = random.randint(740, 3540)
    return y
def random_conveyor_y():
    y = random.randint(5500, 17040)#不同板子有不同的生成時間
    return y


player1 = Player(player_data)  # 宣告P1玩家是player class
board1   = Board(240, 600)

board3   = Board(random_x(), random_board_y())
nails1    = Nails (random_x(), random_board_y())
wall1    = Wall(0, 80)
wall2    = Wall(450, 80)
wall_ceil1 = WallCeil(20, 80)
wall_ceil2 = WallCeil(55, 80)
conveyor_left1 = ConveyorLeft(random_x(),random_conveyor_y())
board2   = Board(random_x(), random_board_y())
conveyor_right1 = ConveyorRight(random_x(),random_conveyor_y())
env1    = set_game_env()


class Game():
    def __init__(self):
        self.floor = 0

    def run_game(self):

        env1.bulid_env(player1, board1)
        self.game_over()

    def game_over(self):

        if player1.hp <= 0:
            playsound('../assets/sounds/Stabbed Scream.mp3', block=True)


        elif player1.y > 640:
            playsound('../assets/sounds/Fall 2.mp3', block=True)




    def frame_step(self, input_actions):
        pygame.event.pump()
        timebios = []
        reward = 0.1
        terminal = False

        if sum(input_actions != 1):#避免同時感應到兩個按鍵
            pass
        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: left
        # input_actions[2] == 1: right
        if input_actions[1] == 1:
            player1.x -= player1.vel
            player1.img = walk_left_img_list[walk_count[0] % 2]
            walk_count[0] += 1

        elif input_actions[2] == 1:
            player1.x += player1.vel
            player1.img = walk_right_img_list[walk_count[0] % 2]
            walk_count[0] += 1

        else:
            player1.img = player_data['img']

        self.run_game()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return image_data, reward, terminal


