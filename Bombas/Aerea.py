import pygame
import random

class AmeacaAerea(pygame.sprite.Sprite):
    def __init__(self, imagem, largura_tela):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=self.gerar_posicao(largura_tela))
        self.velocidade = 6

    def gerar_posicao(self, largura_tela):
        margem_inicial = 100
        limite_direito = int(largura_tela * 0.8)
        x = random.randint(margem_inicial, limite_direito)
        return (x, -20)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 1080:
            self.kill()