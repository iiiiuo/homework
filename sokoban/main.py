'地图有七个因素，人物P，箱子B，目标点G，墙壁W，空地N，推到目标点的箱子A，和目标点重合的人物'
'人物的位置和地图分开'
'上下左右键控制人物'
'z控制撤销，r控制重开'
import pygame
import sys
import tkinter
from pygame.locals import *
from settings import Settings
from stats import Stats
from hands import *
from login import *
from start import Start
from rank import Rank
from over import Over
from push_sound import Push_Sound
from background_sound import Background_Sound
from scoreboard import ScoreBoard
from over_scoreboard import Over_ScoreBoard
from element import Element
class Sokoban:
    def __init__(self):
        #必要的初始化
        self.settings = Settings()
        self.stats = Stats()
        # print(id(self.stats.game_stats))
        self.settings = Settings()
        #密码部分


        self.push_sound = Push_Sound()

        # 计算步数steps记录前一个地图的总步数
        self.steps = 0
        self.steps_all=0
        # 常量
        self.Dir = ((-1, 0), (1, 0), (0, -1), (0, 1))  # left,right,up,down
        # 真的要进去就开始吗记得改
        # self._read_map()
        self.open_camera = 0
        #tkinter窗口
        self.login=Login(self.stats)



    def init_pygame(self):
        '初始化'
        # print(self.login.id)
        pygame.init()
        # self.screen=pygame.display.set_mode((1200,800))
        pygame.display.set_caption('Sokoban')
        # pygame.key.set_repeat(10, 15)没用
        # self.bg_color = (230,230,230)
        # self.settings = Settings()
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.stats=Stats()
        self.background_sound = Background_Sound()
        '五个画图要素+1'
        self.chara=Element(self,"rabbit")
        self.box=Element(self,"box_ori")
        self.bush=Element(self,"bush")
        self.grass=Element(self,"grass")
        self.goal=Element(self,"flag")
        self.goal_suc=Element(self,"box_suc")
        self.portal=Element(self,"portal")
        self.hands = Hands()
        #页面login在前面
        self.start=Start(self)
        self.rank=Rank(self)
        self.over=Over(self)
        # 显示得分
        self.sb = ScoreBoard(self)
        # 数据库
        # self.users=mysql_users()
        # self.ranks=mysql_rank()
        # self.password_sent=''
        # self.username_sent=''
        # #音效
        # self.push_sound=Push_Sound()
        # self.background_sound=Background_Sound()
        # #计算步数
        # self.steps=0
        # #常量
        # self.Dir=((-1,0),(1,0),(0,-1),(0,1))#left,right,up,down
        # # 真的要进去就开始吗记得改
        # #self._read_map()
        # self.open_camera=0
        # self.login.drawme()
        self.start.drawme()


    def default(self):
        # self.steps += len(self.stats.game_path)
        # print(self.step
        self.stats.game_path = []
        self.game_map = []
        self.game_map_source = []
        self.stats.box_right = 0

    def _read_map(self):
        '读取地图'
        self.default()
        file_name="map/"+str(self.stats.game_level)+'.dat'
        file = open(file_name, 'r')
        self.stats.map_height, self.stats.map_width, self.stats.box_number=map(int,file.readline().split())
        #dat 第一行存的几行几列
        for i in range(self.stats.map_height):
            self.game_map_source.append(file.readline()[:self.stats.map_width])
        self.game_map=self.game_map_source[:]
        file.close()
        # print(self.game_map[:])#复制列表的副本
        # print(self.stats.map_height)
        # print(self.stats.map_width)
        self.sb.update_scoreboard(self.steps_all)
        self.refresh()

        ##改变游戏状态时读地图

    def refresh(self):
        '更新地图'
        # self._read_map()
        self.sb.prep_score()
        box_right=0
        self.screen = pygame.display.set_mode((self.stats.map_width*70, self.stats.map_height*70))
        for i in range(self.stats.map_height):
            for j in range(self.stats.map_width):
                pos=[j*70,i*70]
                # print(self.stats.game_path)
                # print(i,j)
                # print(self.game_map)
                if self.game_map[i][j] == 'P':
                    self.chara.blitme(i,j)
                    self.stats.player_pos_x=j
                    self.stats.player_pos_y=i
                    # print(self.stats.player_pos_x,self.stats.player_pos_y)
                elif self.game_map[i][j] == 'W':
                    self.bush.blitme(i,j)
                elif self.game_map[i][j] == 'N':
                    self.grass.blitme(i,j)
                elif self.game_map[i][j] == 'B':
                    self.box.blitme(i,j)
                elif self.game_map[i][j] == 'G':
                    self.goal.blitme(i,j)
                elif self.game_map[i][j] == 'A':
                    self.goal_suc.blitme(i,j)
                    box_right+=1
                elif self.game_map[i][j] == 'O':
                    self.portal.blitme(i, j)
                else:
                    print("地图出错")
        self.stats.box_right=box_right
        # print(self.stats.box_right)
        pygame.display.set_caption("Mission " + str(self.stats.game_level))
        # self._update_screen()

    def undo(self):
        '撤销'
        print('undo')
        if self.stats.game_path:
            # print(len(self.stats.game_path))
            self.game_map=self.stats.game_path.pop()
            # print(len(self.stats.game_path))
            # print(self.game_map)
            self.steps_all -= 1
            self.sb.update_scoreboard(self.steps_all)
            # print(self.steps_all)
            # print(self.steps)
            self.refresh()
        else:
            print('you can not undo')

    def redo(self):
        '重新开始'
        # self.game_map=self.game_map_source
        print('redo')
        # print(self.game_map)
        self._read_map()
        self.refresh()
        if self.stats.game_level == 1:
            self.steps_all=0
            self.sb.update_scoreboard(self.steps_all)
            self.steps = 0
        else:
            # print(self.steps,self.steps_all)
            self.steps_all = self.steps
            self.sb.update_scoreboard(self.steps_all)
        # print(self.steps)
        # print(self.steps_all)

    def run_game(self):
        '运行游戏'
        while True:
            self._check_events()  # 代码重构
            self._update_screen()
            self.hands.run_camera()
            self._check_over_time()

    def _check_over_time(self):
        if self.stats.game_stats ==4 :
            self.current_time=pygame.time.get_ticks()
            self.elapsed_time=self.current_time-self.start_time
            self.over_sb.show_score()
            # self.draw_fireworks()
            if self.elapsed_time > 3000:
                # print('time passed')
                self.stats.game_stats = 1
                self.start.drawme()
                # print(self.over.ranks.db)
                self.over.ranks.db.close()
                self.over.ranks.cur.close()
                # print('数据库over')
                # self.firework.kill()
                # print('fireworks killed')

    def _update_screen(self):
        '更新屏幕'
        if self.stats.game_stats == 3:
            # print('sb_show')
            self.sb.show_score()
        pygame.display.update()


    def _check_events(self):#辅助方法
        '检查事件'
        # print('check_events')
        if self.hands.direction_sent == 5 and self.stats.game_stats == 3:
            self.back_to_start()
        elif self.hands.direction_sent and self.stats.game_stats == 3:
            self.move(1)  # 参数随便传的
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print('quit')
                self.background_sound.pause_music()
                self.hands.stop_camera()
                # self.login.root.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # print('keydownevents')
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print('mousedown')
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        if self.stats.game_stats == 0:#登陆页面
            pass
        elif self.stats.game_stats == 1:#开始页面
            button_start_clicked = self.start.button_start.rect.collidepoint(mouse_pos)
            button_rank_clicked = self.start.button_rank.rect.collidepoint(mouse_pos)
            button_music_clicked=self.start.button_music.rect.collidepoint(mouse_pos)
            if button_start_clicked :
                self.stats.game_stats = 3
                self._read_map()
                self.hands.start_camera()
                print('打开摄像头')
            elif button_rank_clicked :
                self.rank=Rank(self)
                self.stats.game_stats = 2
                self.rank.drawme()
            elif button_music_clicked:
                if self.background_sound.start_music:
                    self.start.button_music.img_index = 1
                    self.start.drawme()
                    self.background_sound.pause_music()
                else:
                    self.start.button_music.img_index = 0
                    self.start.drawme()#这里不能单个只拿button_music
                    self.background_sound.unpause_music()
        elif self.stats.game_stats ==2 :#排行榜页面
            button_back_clicked=self.rank.button_back.rect.collidepoint(mouse_pos)
            if button_back_clicked :
                self.stats.game_stats = 1
                self.start.drawme()
                self.rank.ranks.db.close()
                self.rank.ranks.cur.close()

    def _check_keydown_events(self,event):
        # print("enter keydown")
        if self.stats.game_stats==3:
            if event.key == pygame.K_LEFT:
                self.move(0)
            elif event.key == pygame.K_RIGHT:
                self.move(1)
            elif event.key == pygame.K_UP:
                self.move(2)
            elif event.key == pygame.K_DOWN:
                self.move(3)
            elif event.key == K_z:
                self.undo()
            elif event.key == K_r:
                self.redo()
            elif event.key == K_b:
                self.back_to_start()





    # def _check_keyup_events(self,event):
    #     if event.key == pygame.K_RIGHT:
    #         self.move('right',False)
    #     elif event.key == pygame.K_LEFT:
    #         self.move('left',False)
    #     elif event.key == pygame.K_UP:
    #         self.move('up',False)
    #     elif event.key == pygame.K_DOWN:
    #         self.move('down',False)

    def back_to_start(self):
        self.hands.direction_sent = None
        self.hands.direction_sent_info = None
        self.hands.stop_camera()
        self.stats.game_stats=1
        self.start.drawme()
        self.stats.game_stats = 1
        self.stats.game_level = 1
        self.steps_all = 0
        self.steps = 0
        self.stats.game_path = []
        self.sb.update_scoreboard(self.steps_all)

    def move(self,direction):
        '控制移动''每次移动改变三个位置'
        # print(self.stats.player_pos_x)
        # print(self.stats.player_pos_y)
        if not self.hands.direction_sent:
            temp_x = self.stats.player_pos_x + self.Dir[direction][0]
            temp_y = self.stats.player_pos_y + self.Dir[direction][1]
            # print(temp_x)
            # print(temp_y)
            next_x = temp_x + self.Dir[direction][0]
            next_y = temp_y + self.Dir[direction][1]
        else:
            temp_x = self.stats.player_pos_x + self.Dir[self.hands.direction_sent-1][0]
            temp_y = self.stats.player_pos_y + self.Dir[self.hands.direction_sent-1][1]
            # print(temp_x)
            # print(temp_y)
            next_x = temp_x + self.Dir[self.hands.direction_sent-1][0]
            next_y = temp_y + self.Dir[self.hands.direction_sent-1][1]
        # print(next_x)
        # print(next_y)
       #print(direction)

        if self.game_map[temp_y][temp_x] in ('B','A') :
            # print('there is a box')
            # print(self.game_map[temp_y][temp_x])
            # print(self.game_map)
            # print(self.game_map[next_y][next_x])
            if self.game_map[next_y][next_x] in ('N','G'):
                # print('you can move the box')
                self.stats.game_path.append(self.game_map[:])
                if self.game_map[next_y][next_x] == 'G':
                    'str object does not support item assignment'
                    self.change_map(next_x,next_y,'A')
                else:
                    self.change_map(next_x,next_y,'B')
                self.change_map(temp_x,temp_y,'P')
                if self.game_map_source[self.stats.player_pos_y][self.stats.player_pos_x] == 'G':
                    # print(self.game_map_source)
                    self.change_map(self.stats.player_pos_x,self.stats.player_pos_y,'G')
                elif self.game_map_source[self.stats.player_pos_y][self.stats.player_pos_x] == 'O':
                    self.change_map(self.stats.player_pos_x, self.stats.player_pos_y, 'O')
                else:
                    self.change_map(self.stats.player_pos_x, self.stats.player_pos_y, 'N')
                self.stats.player_pos_x = temp_x
                self.stats.player_pos_y = temp_y
                self.push_sound.sound.play()
                self.steps_all+=1
                self.sb.update_scoreboard(self.steps_all)
                # print(self.steps_all)
            else:
                print('你不能移动')
        elif self.game_map[temp_y][temp_x] in ('N','G','O') :
            # print('no box ,but you can move')
            self.stats.game_path.append(self.game_map[:])

            # print(self.game_map_source)
            if self.game_map[temp_y][temp_x] == 'O':
                flag=0
                for x in range(self.stats.map_width):
                    for y in range(self.stats.map_height):
                        # print(x,y)
                        # print(temp_x,temp_y)
                        if x!=temp_x and y!= temp_y and self.game_map_source[y][x]=='O':
                            temp_x=x
                            temp_y=y
                            flag=1
                            break
                    if flag==1:
                        flag=0
                        break
            self.change_map(temp_x, temp_y, 'P')
            if self.game_map_source[self.stats.player_pos_y][self.stats.player_pos_x] == 'G':
                self.change_map(self.stats.player_pos_x, self.stats.player_pos_y, 'G')
            elif self.game_map_source[self.stats.player_pos_y][self.stats.player_pos_x] == 'O':
                self.change_map(self.stats.player_pos_x, self.stats.player_pos_y, 'O')
            else:
                self.change_map(self.stats.player_pos_x, self.stats.player_pos_y, 'N')
            self.stats.player_pos_x = temp_x
            self.stats.player_pos_y = temp_y
            self.steps_all+=1
            self.sb.update_scoreboard(self.steps_all)
            # print(self.steps_all)
        else:
            print('你不能移动')
        self.refresh()
        '判断游戏状态'
        self._check_state()

    def _check_state(self):
        '判断游戏状态'
        if (self.stats.box_number == self.stats.box_right):
            print('你通过了这个等级')
            # print(self.steps)
            self.stats.game_level += 1
            if(self.stats.game_level<=4):#为了方便debug改成了2
                #是不是也可以写=steps_all
                self.steps = self.steps_all

                self._read_map()


                # print(self.game_map)

            else:
                self.hands.stop_camera()
                pygame.display.set_caption("You have passed all levels")
                # 烟花代码
                # self.firework = Firework(self.screen)

                self.start_time = pygame.time.get_ticks()
                self.stats.game_stats = 4
                self.over_sb=Over_ScoreBoard(self)
                self.over.drawme()
                #我以为可以改这个
                self.over.update_ranks(self.login.id,self.steps_all)
                self.stats.game_level=1
                self.steps_all=0
                self.steps=0
                self.stats.game_path=[]
                self.sb.update_scoreboard(self.steps_all)

                # time.sleep(5)

                print('你通过了所有等级')

    # def draw_fireworks(self):
    #     #记得kill
    #     self.firework.update()
    #     self.screen.blit(self.firework.image,self.firework.rect)

    def change_map(self,x,y,object):
        'x是哪一列，y是哪一行'
        self.game_map[y]=self.game_map[y][:x]+object+self.game_map[y][x+1:]




if __name__ == '__main__':
    box1=Sokoban()
    box1.login.root.mainloop()
    # print('im here')
    if box1.login.login_success:
        box1.init_pygame()
        box1.run_game()



