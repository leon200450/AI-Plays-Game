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
        player1.y -=2
    def float(self):
        self.y -= 1.5
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