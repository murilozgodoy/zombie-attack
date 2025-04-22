import pygame
import math
class Impacto(pygame.sprite.Sprite):
    def __init__(self, center, spritesheet, frames,entidade):
        super().__init__()
        self.frames = self.carregar_frames(spritesheet, frames)
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=center)
        self.tempo_anterior = pygame.time.get_ticks()
        self.intervalo = 200
        self.entidade = entidade
        

    def carregar_frames(self, spritesheet, frames):
        image = spritesheet.convert_alpha()
        altura = image.get_height()
        largura_total = image.get_width()
        largura_quadro = largura_total // frames
        return [image.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_anterior > self.intervalo:
            self.tempo_anterior = agora
            self.frame_atual += 1
            if self.frame_atual < len(self.frames):
                self.image = self.frames[self.frame_atual]
            else:
                if self.entidade != "Personagem":
                    self.kill()