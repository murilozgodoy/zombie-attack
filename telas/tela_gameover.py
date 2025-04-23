import pygame
from .tela import Tela

class TelaGameOver(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        pygame.mixer.quit()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/img/gameover1.png"),
            (tela["largura"], tela["altura"])        
        )
    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.jogo.tela_atual.tela.copy()))
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
                from telas import TelaInicial
                self.jogo.trocar_tela(TelaInicial(self.jogo, self.jogo.tela_atual.tela.copy()))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        pygame.display.flip()