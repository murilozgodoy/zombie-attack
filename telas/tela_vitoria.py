import pygame
from .tela import Tela
from .tela_jogo import TelaJogo
from ranking.ranking import add_score

class TelaVitoria(Tela):
    def __init__(self, jogo, tela, usuario):
        pygame.mixer.quit()
        self.jogo   = jogo
        self.tela   = tela
        self.usuario = usuario
        self.escala = jogo.escalonamento
        self.fonte  = pygame.font.Font("assets/font/PressStart2P.ttf", self.escala.escalar(30))
        self.image  = pygame.transform.scale(
            pygame.image.load("assets/img/vitoria_3.png"),
            (tela["largura"], tela['altura'])
        )

        # --- registra no ranking e obtém lista atualizada ---
        # use self.jogo.player_name como nome do jogador
        # Corrigido: cálculo de pontos (acertos é porcentagem, não precisa dividir por 100)
        pontos = (usuario["zumbies_mortos"] * 2) + usuario["vida"] + (usuario["acertos"] * 2)
        self.ranking = add_score(self.jogo.player_name, pontos)

        # pré-render de estatísticas (removida duplicação)
        self.zumbies_mortos = self.fonte.render(f'Zumbis mortos: {self.usuario["zumbies_mortos"]}', True, (255, 255, 255))
        self.zumbies_mortos = pygame.transform.scale(self.zumbies_mortos, (self.escala.escalar(500), self.escala.escalar(100)))
        
        self.vidas = self.fonte.render(f'Vida: {self.usuario["vida"]}', True, (255, 255, 255))
        self.vidas = pygame.transform.scale(self.vidas, (self.escala.escalar(500), self.escala.escalar(100)))


        self.municoes = self.fonte.render(f'Munições: {self.usuario["municoes_totais"] + self.usuario["municoes"]}', True, (255, 255, 255))
        self.municoes = pygame.transform.scale(self.municoes, (self.escala.escalar(500), self.escala.escalar(100)))

        self.acertos = self.fonte.render(f'% de Acertos: {self.usuario["acertos"]:.2f}', True, (255, 255, 255))
        self.acertos = pygame.transform.scale(self.acertos, (self.escala.escalar(500), self.escala.escalar(100)))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.jogo.tela_atual.tela.copy()))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        janela.blit(self.vidas, (self.tela["largura"] - self.escala.escalar(750), self.tela["altura"] - self.escala.escalar(900)))
        janela.blit(self.zumbies_mortos, (self.tela["largura"] - self.escala.escalar(750), self.tela["altura"] - self.escala.escalar(700)))
        janela.blit(self.municoes, (self.tela["largura"] - self.escala.escalar(750), self.tela["altura"] - self.escala.escalar(500)))
        janela.blit(self.acertos, (self.tela["largura"] - self.escala.escalar(750), self.tela["altura"] - self.escala.escalar(300)))
        # Exibe o ranking (top 5)
        # emoji_font = pygame.freetype.Font("C:/Windows/Fonts/seguiemj.ttf", 32)
        x_rank, y_rank = self.escala.escalar(100), self.escala.escalar(300)
        # emoji_font.render_to(janela, (100, 296), "🏆", fgcolor=(222,177,61))
        titulo = self.fonte.render(" Top 5 Jogadores", True, (222,177,61))
        janela.blit(titulo, (x_rank, y_rank))
        y_rank += self.escala.escalar(40)

        for pos, entry in enumerate(self.ranking[:5], start=1):
            txt = self.fonte.render(
                f'{pos}. {entry["name"]}: {entry["score"]:.0f}',
                True, (255,255,255)
            )
            janela.blit(txt, (x_rank, y_rank))
            y_rank += self.escala.escalar(30)

        pygame.display.flip()
        