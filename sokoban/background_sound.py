import pygame

class Background_Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sound/background.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.start_music=1

    def pause_music(self):
        self.start_music=0
        pygame.mixer.music.pause()
        print("背景音乐停止")

    def unpause_music(self):
        self.start_music=1
        pygame.mixer.music.unpause()
        print("背景音乐播放")


