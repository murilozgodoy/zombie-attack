import pygame
from .tela import Tela
from .tela_nome import TelaNome
from .tela_instrucoes import TelaInstrucoes

class TelaInicial(Tela):
    def __init__(self, jogo, tela):
        pygame.mixer.init()
        pygame.mouse.set_visible(True)
        self.jogo = jogo
        self.tela = tela
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        self.som_ambiente = pygame.mixer.Sound("assets/snd/som_ambiente.wav")
        self.som_ambiente.set_volume(0.1)
        self.som_ambiente.play(-1)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/img/Inicial.png"),
            (tela["largura"], tela["altura"])            
        )
        self.botao_jogar_rect = pygame.Rect(
            (tela["largura"] - 643) // 2,
            (tela["altura"] - 184) // 2,
            575, 170
        )
        self.botao_instrucoes_rect = pygame.Rect(
            (tela["largura"] - 643) // 2,
            (tela["altura"] + 229) // 2,
            575, 170
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
        mouse_pos = pygame.mouse.get_pos()
        if self.botao_jogar_rect.collidepoint(mouse_pos): 
            pygame.draw.rect(janela, (255, 200, 60) , self.botao_jogar_rect, 10, border_radius=10)

        if self.botao_instrucoes_rect.collidepoint(mouse_pos):
            pygame.draw.rect(janela, (255, 200, 60) , self.botao_instrucoes_rect,10, border_radius=10)

        pygame.display.flip()