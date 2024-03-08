import pygame
from mysql_rank import mysql_rank


class Over:
    def __init__(self,sk_game):
        self.ranks=mysql_rank()
        self.screen = sk_game.screen
        self.screen_rect = sk_game.screen.get_rect()
        self.settings = sk_game.settings

        self.image = pygame.image.load('images/over.bmp')
        self.image = pygame.transform.scale(self.image, (800, 800))  # 改变大小
        self.rect = self.image.get_rect()




    def drawme(self):
        # 更改屏幕大小
        self.screen = pygame.display.set_mode((800, 800))
        self.rect.x = 0
        self.rect.y = 0
        self.screen.blit(self.image, self.rect)



    def update_ranks(self,user_id,moves):
        self.ranks.users_search()
        self.ranks_info=self.ranks.results
        # print(self.ranks_info)
        self.number=len(self.ranks_info)
        self.ranks.insert_ranks(self.number,user_id,moves)



