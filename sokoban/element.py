import pygame

class Element:
    def __init__(self,sk_game,img_file_name):
        self.screen = sk_game.screen
        self.image = pygame.image.load('images/%s.bmp'%img_file_name)
        self.image = pygame.transform.scale(self.image, (70, 70))  # 改变大小
        self.rect = self.image.get_rect()

    def blitme(self,i,j):
        self.rect.x=70*j
        self.rect.y=70*i
        self.screen.blit(self.image, self.rect)
