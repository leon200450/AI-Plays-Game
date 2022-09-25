import pygame
from pygame.locals import *
import time
import random
from playsound import playsound
from __init__ import*


width, height = 480, 640  # 把螢幕長寬
pygame.init()
pygame.display.set_caption('小朋友下樓梯')  # 設定視窗名稱
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))  # 設定螢幕長寬
FPS = 100  # 設定幀數
running = [True]
head_font = pygame.font.SysFont(None, 60)  # 設定大小60的標題框框

    # 5 - clear the screen before drawing it again
    # screen.fill((0, 0, 0))
    # 6 - draw the screen elements

RectFlag = 0

HPJudge = [True]
keys = [False, False, False, False]  # 設定上下左右判定的list
CountF = 0  # 設定往下樓層的變數
walk_count = [0]
gravity = [True]
Xlist = []  # 紀錄每個X值
Ylist = []  # 紀錄每個y值
count = 0  # 刷新板子亂數
count2 = 0




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

    def move(self):
        #global walk_count #因為我要讓這個值一直存活 而且不要重製 要永遠記錄這個值

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
            self.img = self.img


player1 = Player(player_data)  # 宣告P1玩家是player class


class Game():
    def __init__(self):
        self.floor = 0


    def run_game(self):

        print('結束遊戲請按 Q')
        while (running[0]):#running[0]是True [1]是False


            for event in pygame.event.get():
                if event.type == KEYDOWN:  # 如果有按到離開視窗則停止執行while 就會執行到關閉
                    if str(event.key) =='113':
                        print('結束遊戲')
                        running[0] =False
            player1.move()
            self.set_game_env()


        pygame.quit()

    def set_game_env(self):

        def build_wall():
            for x in range(80, 700, 100):  # 設定牆壁 以及生命值
                screen.blit(wall_img, (0, x))
                screen.blit(wall_img, (460, x))

        def build_ceil():
            screen.blit(ceil_img, (20, 80))
            screen.blit(ceil_img, (55, 80))

        def build_player():
            screen.blit(player1.img, (player1.x, player1.y))

        def build_floor_label():
            head_font = pygame.font.SysFont(None, 60)  # 設定大小60的標題框框
            text_surface = head_font.render('B%04dF'%CountF, True, (121, 255, 121))  # 設定標題的字跟顏色
            screen.blit(text_surface, (300, 25))  # 讓標題印在畫布300,25的地方
        def build_hp_bar():
            screen.blit(hp_bar[player1.hp], (10, 0))

        def build_gravity(player1):#建造地心引力
            player1.y += 0.5

        screen.fill((0, 0, 0))  # 把畫布塗黑
        build_player()#創造角色
        build_wall()#建造牆壁
        build_ceil()#建造陷阱
        build_floor_label()#建造樓層標題
        build_hp_bar()#建造血條
        if gravity[0]:#地心引力判定 若碰到板子就取消
            build_gravity(player1)#建造地心引力

        pygame.display.update()#刷新畫面



def main():
    Game().run_game()


main()



# 宣告 font 文字物件

# 渲染方法會回傳 surface 物件
'''
# blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗
global tmpHP, jump, PY, run
PY = 0  # platform Y值
jump = 0  # 彈跳開關


class player:
    def __init__(self, X, Y, HP, img, vel):
        self.X = X
        self.Y = Y
        self.HP = HP
        self.img = img
        self.vel = vel

    def player_move(walkCount, player):

        key_p = pygame.key.get_pressed()
        if (key_p[pygame.K_LEFT]):
            keys[2] = True
            keys[3] = False
            player.X -= player.vel

        elif (key_p[pygame.K_RIGHT]):
            keys[3] = True
            keys[2] = False
            player.X += player.vel

        else:
            keys[2] = False
            keys[3] = False
            walkCount = 0

        if keys[2]:
            player.img = walkLeft[walkCount % 2]
            walkCount += 1

        elif keys[3]:
            player.img = walkRight[walkCount % 2]
            walkCount += 1
        else:
            player.img = player

        return walkCount

    def player_fall(player):
        player.Y += 0.5

    def player_stop_fall(player, CountF):
        if CountF < 50:
            player.Y -= 1.5
        else:
            player.Y -= 1.8

    def player_stop_float(player):
        player.Y += 11
        HPJudge[0] = True
        if HPJudge[0]:
            player.HP -= 2

    def player_jump(player, CountF):
        global jump, PY
        if player.Y < (PY - 130):
            jump = 0

        elif player.Y < 115:
            player.player_stop_float()
            jump = 0


        else:
            if CountF < 50:
                player.Y -= 0.7
            else:
                player.Y -= 1.1


class Platform:
    def __init__(self, X, Y, dmg, img):
        self.X = X
        self.Y = Y
        self.dmg = dmg
        self.img = img

    def Platform_float(Board, CountF):
        if CountF < 50:
            Board.Y -= 0.5
        else:
            Board.Y -= 0.7

        if Board.Y < 100 or Board.Y > 1240:
            Board.X = random.randint(114, 366)
            Board.Y = random.randint(740, 1240)

            BoardYlist = [Board1.Y, Board2.Y, Board3.Y, Nails1.Y, Nails2.Y, Nails3.Y, Nails4.Y, Trampoline.Y,
                          conveyor_left.Y, conveyor_right.Y]
            for i in BoardYlist[1:]:
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:1] + BoardYlist[2:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:2] + BoardYlist[3:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:3] + BoardYlist[4:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:4] + BoardYlist[5:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:5] + BoardYlist[6:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:6] + BoardYlist[7:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:7] + BoardYlist[8:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:8] + BoardYlist[9:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

            for i in (BoardYlist[:9] + BoardYlist[10:]):
                if (Board.Y - i) ** 2 < 1400:
                    Board.Y += 50

    def Platform_right(self, player):
        player.X += player.vel / 2

    def Platform_left(self, player):
        player.X -= player.vel / 2

    def Platform_Rect(Platform, Player, PlatWidth, PlatHigth, PlayerWidth, PlayerHight, CountF):
        PlatformRect = pygame.Rect(Platform.X, Platform.Y, PlatWidth, PlatHigth)
        PlayerRect = pygame.Rect(Player.X, Player.Y, PlayerWidth, PlayerHight)
        if (pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1 and Platform.img == ceil):
            player.player_stop_float(Player)
            RectFlag = 1
            return RectFlag

        elif (pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Platform.img == TrampolineUP):
            global jump, PY, run
            jump = 1
            PY = Platform.Y

            if HPJudge[0]:
                Player.HP -= Platform.dmg
                if Player.HP > 10:
                    Player.HP = 10

                HPJudge[0] = False


        elif (pygame.Rect.colliderect(PlayerRect, PlatformRect) == 1) and (Player.Y + 27 < Platform.Y):
            if ((Player.X + PlayerWidth / 2) >= (Platform.X + PlatWidth / 2)) and (
                    (Player.X + 0.2 * PlayerWidth) < (Platform.X + PlatWidth)):
                Player.Y = Platform.Y - 29
                if HPJudge[0]:
                    Player.HP -= Platform.dmg
                    if Player.HP > 10:
                        Player.HP = 10

                    HPJudge[0] = False

            elif ((Player.X + PlayerWidth / 2) < (Platform.X + PlatWidth / 2)) and (
                    (Player.X + 0.8 * PlayerWidth) > Platform.X):
                Player.Y = Platform.Y - 29
                if HPJudge[0]:
                    Player.HP -= Platform.dmg
                    if Player.HP > 10:
                        Player.HP = 10

                    HPJudge[0] = False

            if (Platform.img == conveyor_right):
                if ((Player.X + PlayerWidth / 2) >= (Platform.X + PlatWidth / 2)) and (
                        (Player.X + 0.2 * PlayerWidth) < (Platform.X + PlatWidth)):
                    Platform.Platform_right(Player)
                elif ((Player.X + PlayerWidth / 2) < (Platform.X + PlatWidth / 2)) and (
                        (Player.X + 0.8 * PlayerWidth) > Platform.X):
                    Platform.Platform_right(Player)

            if (Platform.img == conveyor_left):
                if ((Player.X + PlayerWidth / 2) >= (Platform.X + PlatWidth / 2)) and (
                        (Player.X + 0.2 * PlayerWidth) < (Platform.X + PlatWidth)):
                    Platform.Platform_left(Player)
                elif ((Player.X + PlayerWidth / 2) < (Platform.X + PlatWidth / 2)) and (
                        (Player.X + 0.8 * PlayerWidth) > Platform.X):
                    Platform.Platform_left(Player)

    def SetPlatform(times, platformtime, platform, CountF):  # 幾秒要生成 BOARDTIME 板子生成時間
        if (platformtime > times):
            screen.blit(platform.img, (platform.X, platform.Y))
            Platform.Platform_float(platform, CountF)


for i in range(0, 100, 1):
    X = random.randint(30, 365)
    Xlist.append(X)

player1 = player(240, 120, 10, player_img, 0.5)
RandX = random.randint(0, 99)

Board1 = Platform(240, 600, -1, Board)
Nails1 = Platform(Xlist[4], 1241, 3, Nails)
Nails2 = Platform(Xlist[2], 1241, 3, Nails)
Nails3 = Platform(Xlist[7], 1241, 3, Nails)
Nails4 = Platform(Xlist[5], 1241, 3, Nails)
Board2 = Platform(Xlist[3], 1241, -1, Board)
Board3 = Platform(Xlist[3], 1241, -1, Board)
Trampoline = Platform(Xlist[6], 1241, -1, TrampolineUP)
ceil = Platform(20, 80, 0, ceil)
conveyor_left = Platform(Xlist[5], 1241, -1, conveyor_left)
conveyor_right = Platform(Xlist[6], 1241, -1, conveyor_right)

timeflag = 0
tcount = 0
HPflag = 1
timebios = []
run = True

while run:

    ##環境設定

    screen.fill((0, 0, 0))  # 把畫布塗黑

    platformtime = pygame.time.get_ticks()  # 設定一個計時器 單位為毫秒
    times = platformtime % 2500  # 計時器每2.5秒歸0

    if times < 3 and player1.Y <= 640:
        CountF += 1


    elif player1.Y >= 640:
        playsound('./assets/sounds/Fall 2.mp3', block=True)
        run = False

    head_font = pygame.font.SysFont(None, 60)  # 設定大小60的標題框框
    text_surface = head_font.render('B%04dF' % CountF, True, (121, 255, 121))  # 設定標題的字跟顏色
    screen.blit(text_surface, (300, 25))  # 讓標題印在畫布300,25的地方
    # 5 - clear the screen before drawing it again
    # screen.fill((0, 0, 0))
    # 6 - draw the screen elements
  
    
    for x in range(80, 700, 100):  # 設定牆壁 以及生命值
        screen.blit(wall, (0, x))
        screen.blit(wall, (460, x))

    screen.blit(player1.img, (player1.X, player1.Y))  # 設定玩家
    screen.blit(ceil, (20, 80))
    screen.blit(ceil, (55, 80))

    if player1.HP == 10:
        screen.blit(life, (10, 0))
    elif player1.HP == 9:
        screen.blit(life1, (10, 0))
    elif player1.HP == 8:
        screen.blit(life2, (10, 0))
    elif player1.HP == 7:
        screen.blit(life3, (10, 0))
    elif player1.HP == 6:
        screen.blit(life4, (10, 0))
    elif player1.HP == 5:
        screen.blit(life5, (10, 0))
    elif player1.HP == 4:
        screen.blit(life6, (10, 0))
    elif player1.HP == 3:
        screen.blit(life7, (10, 0))
    elif player1.HP == 2:
        screen.blit(life8, (10, 0))
    elif player1.HP == 1:
        screen.blit(life9, (10, 0))
    elif player1.HP <= 0:
        screen.blit(life10, (10, 0))
        playsound('./assets/sounds/Stabbed Scream.mp3', block=True)
        run = False

    if jump == 1:
        player.player_jump(player1, CountF)

    else:
        player.player_fall(player1)

    playerRect = pygame.Rect(player1.X, player1.Y, 31, 31)  # 畫出PLAYER1的碰撞範圍
    Platform.Platform_Rect(ceil, player1, 480, 32, 31, 31, CountF)

    WallRect = pygame.Rect(0, 80, 18, 560)
    WallRect2 = pygame.Rect(450, 80, 18, 560)

    if (pygame.Rect.colliderect(playerRect, WallRect) == 1):
        player1.X = 18
    elif (pygame.Rect.colliderect(playerRect, WallRect2) == 1):
        player1.X = 419

    if timeflag == 0:

        timerand = random.randint(500, 3000)
        for x in range(0, 10, 1):
            timebiosrand = random.randint(500, 1500)
            timebios.append(timebiosrand)
        timeflag = 1

    Platform.SetPlatform(0, platformtime, Board1, CountF)
    Platform.Platform_Rect(Board1, player1, 94, 1, 31, 31, CountF)

    Platform.SetPlatform(1900, platformtime, Trampoline, CountF)  # 設定彈簧
    Platform.Platform_Rect(Trampoline, player1, 95, 1, 31, 31, CountF)
    Platform.SetPlatform(500, platformtime, conveyor_left, CountF)
    Platform.Platform_Rect(conveyor_left, player1, 95, 1, 31, 31, CountF)
    Platform.SetPlatform(1200, platformtime, Board2, CountF)
    Platform.Platform_Rect(Board2, player1, 94, 1, 31, 31, CountF)

    Platform.SetPlatform(2400, platformtime, Board3, CountF)
    Platform.Platform_Rect(Board3, player1, 94, 1, 31, 31, CountF)

    Platform.SetPlatform(1500, platformtime, Nails1, CountF)
    Platform.Platform_Rect(Nails1, player1, 95, 1, 31, 31, CountF)

    Platform.SetPlatform(timerand + timebios[4], platformtime, conveyor_right, CountF)
    Platform.Platform_Rect(conveyor_right, player1, 95, 1, 31, 31, CountF)
    if (CountF > 20):
        Platform.SetPlatform(timerand + timebios[5], platformtime, Nails2, CountF)
        Platform.Platform_Rect(Nails2, player1, 95, 1, 31, 31, CountF)
    if (CountF > 30):
        Platform.SetPlatform(timerand + timebios[6], platformtime, Nails3, CountF)
        Platform.Platform_Rect(Nails3, player1, 95, 1, 31, 31, CountF)
    if (CountF > 50):
        Platform.SetPlatform(timerand + timebios[7], platformtime, Nails4, CountF)
        Platform.Platform_Rect(Nails4, player1, 95, 1, 31, 31, CountF)

    PlayerRect = pygame.Rect(player1.X, player1.Y, 31, 31)
    Board1Rect = pygame.Rect(Board1.X, Board1.Y, 94, 1)
    Board2Rect = pygame.Rect(Board2.X, Board2.Y, 94, 1)
    Board3Rect = pygame.Rect(Board3.X, Board3.Y, 94, 1)
    TrampolineRect = pygame.Rect(Trampoline.X, Trampoline.Y, 95, 1)
    conveyor_leftRect = pygame.Rect(conveyor_left.X, conveyor_left.Y, 94, 1)
    conveyor_rightRect = pygame.Rect(conveyor_right.X, conveyor_right.Y, 94, 1)
    Nails1Rect = pygame.Rect(Nails1.X, Nails1.Y, 94, 1)
    Nails2Rect = pygame.Rect(Nails2.X, Nails2.Y, 94, 1)
    Nails3Rect = pygame.Rect(Nails3.X, Nails3.Y, 94, 1)
    Nails4Rect = pygame.Rect(Nails4.X, Nails4.Y, 94, 1)
    CeilRect = pygame.Rect(ceil.X, ceil.Y, 480, 32)
    a = pygame.Rect.colliderect(PlayerRect, Board1Rect)
    b = pygame.Rect.colliderect(PlayerRect, Board2Rect)
    c = pygame.Rect.colliderect(PlayerRect, Board3Rect)
    d = pygame.Rect.colliderect(PlayerRect, TrampolineRect)
    e = pygame.Rect.colliderect(PlayerRect, conveyor_leftRect)
    f = pygame.Rect.colliderect(PlayerRect, conveyor_rightRect)
    g = pygame.Rect.colliderect(PlayerRect, Nails1Rect)
    h = pygame.Rect.colliderect(PlayerRect, Nails2Rect)
    i = pygame.Rect.colliderect(PlayerRect, Nails3Rect)
    j = pygame.Rect.colliderect(PlayerRect, Nails4Rect)
    k = pygame.Rect.colliderect(PlayerRect, CeilRect)
    # print(f'板子1:{a} 板子2:{b} 板子3:{c} 彈簧:{d} 輸送帶左:{e} 輸送帶右:{f} 尖刺1:{g} 尖刺2:{h} 尖刺3:{i} 尖刺4:{j} 上面尖刺{k} ' )
    if not (a or b or c or d or e or f or g or h or i or j):
        HPJudge[0] = True

    pygame.display.flip()  # 環境更新尖刺2{h} 尖刺3{i}

    # 操控角色
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # 如果有按到離開視窗則停止執行while 就會執行到關閉
            run = False
    walkCount = player.player_move(walkCount, player1)

pygame.quit()
'''



