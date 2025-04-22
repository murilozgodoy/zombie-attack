import pygame
from .tela import Tela
# from .tela_inicial import TelaInicial
# from .tela_jogo import TelaJogo

class TelaInstrucoes(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.image = pygame.transform.scale(
            pygame.image.load("assets/img/fundo.png"),
            (tela["largura"], tela["altura"])        
        )
    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
                from telas import TelaInicial
                self.jogo.trocar_tela(TelaInicial(self.jogo, self.tela))
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_s: #coloquei qualquer tecla, depois mudamos para a tecla que quisermos#
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.tela))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))

   
        fonte_titulo = pygame.font.SysFont('arialblack', 36)
        fonte_texto = pygame.font.SysFont('lucidaconsole', 22)
        fonte_acao = pygame.font.SysFont('lucidaconsole', 22) 

        cor_caixa = (30, 30, 30)
        cor_texto = (220, 220, 220)
        cor_titulo = (222, 177, 61)

        instrucoes = [
            "Mire com o mouse nos zumbis e atire pressionando o botão esquerdo.",
            "Ande para os lados pressionando as teclas 'A' (esquerda) e 'D' (direita).",
            "Não deixe os zumbis invadirem sua base de proteção, caso contrário o jogo acaba.",
            "Evite que os carniçais de combate se aproximem de você, já que conseguem te atacar.",
            "Desvie das bombas aéreas que caem a todo instante.",
            "Recarregue a arma pressionando 'R'.",
            "Dica: Capriche na mira para estar no ranking final de sobreviventes.",
            "Sobreviva até o tempo acabar para vencer!"
        ]

        largura_caixa = 1120
        altura_caixa = 570
        x_caixa = (self.tela["largura"] - largura_caixa) // 2
        y_caixa = (self.tela["altura"] - altura_caixa) // 2
        pygame.draw.rect(janela, cor_caixa, (x_caixa, y_caixa, largura_caixa, altura_caixa), border_radius=10)


        titulo = fonte_titulo.render("COMO JOGAR", True, cor_titulo)
        janela.blit(titulo, (x_caixa + (largura_caixa - titulo.get_width()) // 2, y_caixa + 25))

        y_texto = y_caixa + 115
        for linha in instrucoes:
            texto = fonte_texto.render(linha, True, cor_texto)
            janela.blit(texto, (x_caixa + (largura_caixa - texto.get_width()) // 2, y_texto))
            y_texto += 40

        y_texto += 45
        texto_acao = fonte_acao.render("PRESSIONE 'S' PARA TENTAR SOBREVIVER AO APOCALIPSE OU 'I' PARA VOLTAR AO INÍCIO!", True, cor_titulo)
        janela.blit(texto_acao, (x_caixa + (largura_caixa - texto_acao.get_width()) // 2, y_texto))

        pygame.display.flip()