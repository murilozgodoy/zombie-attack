import pygame
from telas import TelaInicial

class Jogo:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        tela = {
            "largura": info.current_w,
            "altura": info.current_h,
        }
        self.janela = pygame.display.set_mode((tela["largura"], tela["altura"]))
        pygame.display.set_caption("Zombie Attack")
        self.tela_atual = TelaInicial(self, tela)

    def trocar_tela(self, nova_tela):
        self.tela_atual = nova_tela

    def roda(self):
        rodando = True
        while rodando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
            self.tela_atual.trata_eventos(eventos)
            self.tela_atual.atualiza()
            self.tela_atual.desenha(self.janela)
        pygame.quit()