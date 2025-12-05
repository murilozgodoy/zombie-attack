import pygame
import random

class AmeacaAerea(pygame.sprite.Sprite):
    def __init__(self, imagem, largura_tela, escala):
        super().__init__()
        self.escala = escala
        self.image = imagem
        self.rect = self.image.get_rect(center=self.gerar_posicao(largura_tela))
        self.velocidade = escala.escalar(6)

    def gerar_posicao(self, largura_tela):
        margem_inicial = self.escala.escalar(100)
        limite_direito = int(largura_tela * 0.8)
        x = random.randint(margem_inicial, limite_direito)
        return (x, -self.escala.escalar(20))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > self.escala.altura_atual:
            self.kill()