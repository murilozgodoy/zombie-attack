import pygame
import math

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, destino_x, destino_y, imagem):
        super().__init__()
        self.image = pygame.transform.scale(imagem, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))

        dx = destino_x - x
        dy = destino_y - y
        distancia = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        angulo = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(imagem, angulo)
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidade = 100
        self.velocidade_x = (dx / distancia) * self.velocidade
        self.velocidade_y = (dy / distancia) * self.velocidade

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if (self.rect.right < 0 or self.rect.left > 1920 or
            self.rect.bottom < 0 or self.rect.top > 1080):
            self.kill()