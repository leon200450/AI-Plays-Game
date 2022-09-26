import pygame
from pygame.locals import *
import time
import random
from playsound import playsound
from abc import ABC


from little_kids_game.platform.platform_struct import Platform
from little_kids_game.platform.platform_struct import Board
from little_kids_game.platform.platform_struct import Nails
from little_kids_game.platform.platform_struct  import ConveyorLeft
from little_kids_game.platform.platform_struct  import ConveyorRight
from little_kids_game.wall.wall_struct  import Wall
from little_kids_game.wall.wall_struct  import WallCeil

from __init__ import*



width, height = 480, 640  # 把螢幕長寬
pygame.init()
pygame.display.set_caption('小朋友下樓梯')  # 設定視窗名稱
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))  # 設定螢幕長寬
FPS = 60  # 設定幀數

running = [True]

RectFlag = 0
#drop_distance = 0
dmg_judge = [True]

keys = [False, False, False, False]  # 設定上下左右判定的list
#count_floor = 0  # 設定往下樓層的變數
walk_count = [0]
gravity = [True]




player_data={'hp':10,'x' :240,'y' :120,'img': player_img, 'vel':0.5}


hp_bar = {0: life0_img, 1: life1_img, 2: life2_img, 3: life3_img,
          4: life4_img, 5: life6_img, 6: life6_img, 7: life7_img,
          8: life8_img, 9: life9_img, 10:life10_img}



class Player:
    def __init__(self, player_data):#以後playerdata寫在別的py檔裡面import
        self.hp = player_data['hp']
        self.x  = player_data['x']
        self.y  = player_data['y']
        self.img= player_data['img']
        self.vel =player_data['vel']
        self.width = 31
        self.height = 31

    def move(self):

        key_p = pygame.key.get_pressed()#判定我按的按鍵
        if (key_p[pygame.K_LEFT]):
            keys[2] = True
            keys[3] = False
            if keys[2]== True:
                self.x -= self.vel
                self.img = walk_left_img_list[walk_count[0] % 2]
                walk_count[0] += 1

        elif (key_p[pygame.K_RIGHT]):
            keys[3] = True
            keys[2] = False
            self.x += self.vel
            self.img = walk_right_img_list[walk_count[0] % 2]
            walk_count[0] += 1

        else:
            keys[2] = False
            keys[3] = False
            self.img = player_data['img']




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
                print('扣血了')
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

        print('結束遊戲請按 Q')
        while (running[0]):#running 是True

            for event in pygame.event.get():
                if event.type == KEYDOWN:  # 如果有按到離開視窗則停止執行while 就會執行到關閉
                    if str(event.key) =='113':#如果按到Q 就結束
                        print('結束遊戲')
                        running[0] =False

            player1.move()
            env1.bulid_env(player1, board1)
            self.game_over()

        pygame.quit()

    def game_over(self):
        if player1.hp <=0:
            playsound('../assets/sounds/Stabbed Scream.mp3', block=True)
            running[0] = False
        elif player1.y > 640:
            playsound('../assets/sounds/Fall 2.mp3', block=True)
            running[0] = False

def main():
    Game().run_game()


main()

