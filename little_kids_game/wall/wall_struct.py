import pygame
from pygame.locals import *

from __init__ import*





class Wall ():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = wall_img
        self.width =  15
        self.height = 560
    def rect_collision(self, player1):  # 創造兩物之間的碰撞

        platform_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
        if (pygame.Rect.colliderect(platform_rect, player_rect) == 1):
            return 1 #若碰撞到回傳1

class WallCeil (Wall):
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.dmg = 2
        self.img = ceil_img
        self.width =  480
        self.height = 32
