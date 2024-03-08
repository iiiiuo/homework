import pygame

class Button_unchange:
    def __init__(self,sk_game,file_name,rect_x,rect_y,height,width):
        self.screen=sk_game.screen
        self.img=pygame.image.load(f"button_img/{file_name}")
        self.img=pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect()
        self.rect.center=(rect_x,rect_y)



    def draw_button(self):
        # print(self.img_index)
        # print(self.imgs[0],self.imgs[1])
        self.screen.blit(self.img,self.rect)



