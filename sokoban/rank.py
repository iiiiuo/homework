import pygame
from mysql_rank import mysql_rank
from button_unchange import Button_unchange
class Rank:
    def __init__(self,sk_game):
        self.ranks = mysql_rank()
        self.screen = sk_game.screen
        self.screen_rect = sk_game.screen.get_rect()

        self.font = pygame.font.Font('CN-Bold.ttf', 44)

        self.image = pygame.image.load('images/rank_back.bmp')
        self.image = pygame.transform.scale(self.image, (800, 800))  # 改变大小
        self.rect = self.image.get_rect()

        self.button_back = Button_unchange(sk_game, 'back.png', 100, 700,100,100)
        #显示排行的字
        self.settings = sk_game.settings
        self.text_color=(255,255,255)

    def update_ranks(self):
        # 在每次进入排行榜页面的时候都更新一下
        self.ranks.search_highest_ranks()
        self.ranks_info=self.ranks.highest_results
        # print(self.ranks_info)



    def drawme(self):
        # 更改屏幕大小
        self.update_ranks()
        self.name_img=[]
        self.name_rect=[]
        self.moves_img=[]
        self.moves_rect=[]
        self.upper_text1="用户名"
        self.upper_text2 = "步数"
        self.upper_text1_img=self.font.render(self.upper_text1,True,self.text_color)
        self.upper_text2_img = self.font.render(self.upper_text2, True, self.text_color)
        self.upper_rect1=self.upper_text1_img.get_rect()
        self.upper_rect2 = self.upper_text2_img.get_rect()
        self.upper_rect1.center=(300,220)
        self.upper_rect2.center=(600,220)
        for i in range(0,5):
            img=self.font.render(self.ranks_info[i][0],True,self.text_color)
            rect=img.get_rect()
            img2=self.font.render(str(self.ranks_info[i][1]),True,self.text_color)
            rect2 = img.get_rect()
            rect.center=(300,300+i*80)
            rect2.center=(650,300+i*80)
            self.name_img.append(img)
            self.name_rect.append(rect)
            self.moves_img.append(img2)
            self.moves_rect.append(rect2)
        self.screen = pygame.display.set_mode((800, 800))
        self.rect.x = 0
        self.rect.y = 0
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.upper_text1_img, self.upper_rect1)
        self.screen.blit(self.upper_text2_img, self.upper_rect2)
        for i in range(0,5):
            self.screen.blit(self.name_img[i],self.name_rect[i])
            self.screen.blit(self.moves_img[i],self.moves_rect[i])
        self.button_back.draw_button()
