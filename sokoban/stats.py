

class Stats:
    def __init__(self):
        '地图设定'
        self.map_width=10
        self.map_height=10
        '游戏设定'
        '游戏状态0-login 1-开始页面 2-排行榜 3-游戏 4-游戏结束'
        self.game_stats=0
        self.game_level = 1
        self.game_path=[]
        '人物'
        self.player_pos_x=1
        self.player_pos_y=1
        '箱子'
        self.box_number = 4
        self.box_right = 0

