import pygame

class Button_img:
    def __init__(self,sk_game,rect_x,rect_y):
        self.screen=sk_game.screen
        self.imgs=[]

        img1 = pygame.image.load(f"button_img/button_unpause.png")
        img1 = pygame.transform.scale(img1, (100, 100))
        self.imgs.append(img1)

        img2 = pygame.image.load(f"button_img/button_pause.png")
        img2 = pygame.transform.scale(img2, (100, 100))
        self.imgs.append(img2)

        self.rect = pygame.Rect(rect_x, rect_y, 100, 100)
        self.img_index=0

    def draw_button(self):
        # print(self.img_index)
        # print(self.imgs[0],self.imgs[1])
        self.screen.blit(self.imgs[self.img_index],self.rect)



