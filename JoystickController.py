import pygame
from threading import Thread
class joyCont:
    def __init__(self, joyName):
        self.joyName = joyName
        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            pygame.quit()