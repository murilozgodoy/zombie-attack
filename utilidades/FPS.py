import pygame
class FPS:
    def __init__(self):
        self.fps = 0
        self.t0 = 0

    def calcula_fps(self):
        t1 = pygame.time.get_ticks()
        if self.t0 >= 0:
            delta = (t1 - self.t0) / 1000
            if delta > 0:
                self.fps = 1 / delta
        self.t0 = t1