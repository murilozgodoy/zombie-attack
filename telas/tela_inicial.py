import pygame
from .tela import Tela
from .tela_nome import TelaNome
from .tela_instrucoes import TelaInstrucoes

class TelaInicial(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/img/Inicial.png"),
            (tela["largura"], tela["altura"])            
        )
        self.botao_jogar_rect = pygame.Rect(
            (tela["largura"] - 640) // 2,
            (tela["altura"] - 175) // 2,
            570, 160
        )
        self.botao_instrucoes_rect = pygame.Rect(
            (tela["largura"] - 640) // 2,
            (tela["altura"] + 235) // 2,
            570, 160
        )

    def trata_eventos(self, eventos):
        for evento in eventos:
            if self.botao_jogar_rect.collidepoint(pygame.mouse.get_pos()):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.jogo.trocar_tela(TelaNome(self.jogo, self.tela))
            if self.botao_instrucoes_rect.collidepoint(pygame.mouse.get_pos()):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.jogo.trocar_tela(TelaInstrucoes(self.jogo, self.tela))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))   
        pygame.draw.rect(janela, (255, 255, 255), self.botao_jogar_rect)
        pygame.draw.rect(janela, (255, 0, 255), self.botao_instrucoes_rect)
        pygame.display.flip()