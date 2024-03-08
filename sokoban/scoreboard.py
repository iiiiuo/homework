import pygame

class ScoreBoard:
    def __init__(self,sk_game):
        self.screen=sk_game.screen
        self.screen_rect=sk_game.screen.get_rect()
        self.steps=sk_game.steps_all
        # print(id(self.steps))
        # print(id(sk_game.steps_all))
        self.stats=sk_game.stats

        self.text_color=(0,0,0)
        self.bg_color=(255,255,255)
        self.font=pygame.font.Font('CN-Bold.ttf',20)
        self.text = "你的总步数为:"
        self.prep_score()
        # self.prep_text()

    # def prep_text(self):
    #     # 提示显示
    #     self.text = "你的总步数为"
    #     self.text_image = self.font.render(self.text, True, self.text_color, self.bg_color)
    #     self.text_rect = self.steps_image.get_rect()
    #     self.text_rect.right = self.steps_rect.right- 125
    #     self.text_rect.top = 0


    def prep_score(self):
        # print('prep_score')
        self.steps_str=str(self.steps)
        self.all=self.text+self.steps_str
        self.all_image=self.font.render(self.all,True, self.text_color,self.bg_color)
        # print(self.steps)
        self.all_rect=self.all_image.get_rect()
        self.all_rect.right=self.stats.map_width*50-50
        self.all_rect.top=0
        # print(self.steps_rect)


    def show_score(self):
        #显示得分
        # print(self.steps)
        self.screen.blit(self.all_image,self.all_rect)
        # self.screen.blit(self.text_image,self.text_rect)


    def update_scoreboard(self,steps):
        self.steps=steps
        # print('updating steps')
        # print(self.steps)
        self.prep_score()