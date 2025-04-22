import pygame
import random

class AmeacaAerea(pygame.sprite.Sprite):
    def __init__(self, largura_tela):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/img/boma_aerea.png").convert_alpha(), (80, 75))

     
        margem_inicial = 100
        limite_direito = int(largura_tela * 0.5)
        x = random.randint(margem_inicial, limite_direito)

        self.rect = self.image.get_rect(center=(x, -20))
        self.velocidade = 6
        self.subindo = False  # Quando atinge o jogador

    def update(self):
        if self.subindo:
            self.rect.y -= self.velocidade * 2 
            if self.rect.bottom < 0:
                self.kill()
        else:
            self.rect.y += self.velocidade
            if self.rect.top > 1080:
                self.kill()