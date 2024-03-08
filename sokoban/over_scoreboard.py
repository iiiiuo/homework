import pygame

class Over_ScoreBoard:
    def __init__(self,sk_game):
        self.screen=sk_game.screen
        self.screen_rect=sk_game.screen.get_rect()
        self.steps=sk_game.steps_all
        # print(id(self.steps))
        # print(id(sk_game.steps_all))
        self.stats=sk_game.stats

        self.text_color=(0,0,0)
        self.bg_color=(255,255,255)
        self.font=pygame.font.Font('CN-Bold.ttf',40)
        self.text = "你的总成绩为:"
        self.prep_score()
        # self.prep_text()



    def prep_score(self):
        # print('prep_score')
        self.steps_str=str(self.steps)
        self.all=self.text+self.steps_str
        self.all_image=self.font.render(self.all,True, self.text_color,self.bg_color)
        # print(self.steps)
        self.all_rect=self.all_image.get_rect()
        self.all_rect.center=(400,400)
        # print(self.steps_rect)


    def show_score(self):
        #显示得分
        # print(self.steps)
        self.screen.blit(self.all_image,self.all_rect)
        # self.screen.blit(self.text_image,self.text_rect)


