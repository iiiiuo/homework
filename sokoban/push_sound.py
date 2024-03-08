import pygame

class Push_Sound:
    def __init__(self):
        pygame.mixer.init()

        self.sound = pygame.mixer.Sound('sound/move_box.wav')
        self.sound.set_volume(0.3)

