import pygame
from button_img import Button_img
from button_unchange import Button_unchange
class Start:
    def __init__(self,sk_game):
        self.screen = sk_game.screen
        self.screen_rect = sk_game.screen.get_rect()
        self.settings = sk_game.settings

        self.image = pygame.image.load('images/start.bmp')
        self.image = pygame.transform.scale(self.image, (800, 800))  # 改变大小
        self.rect = self.image.get_rect()

        self.button_start = Button_unchange(sk_game,"start.png",380,520,300,500)
        self.button_rank=Button_unchange(sk_game,"rank.png",100,750,200,200)
        self.button_music=Button_img(sk_game,700,100)

    def drawme(self):
        # 更改屏幕大小
        self.screen = pygame.display.set_mode((800, 800))
        self.rect.x = 0
        self.rect.y = 0
        self.screen.blit(self.image, self.rect)
        self.button_start.draw_button()
        self.button_rank.draw_button()
        self.button_music.draw_button()
