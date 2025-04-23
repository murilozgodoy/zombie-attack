import pygame
from .tela import Tela
from .tela_jogo import TelaJogo
from ranking.ranking import load_ranking  

class TelaNome(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.font = pygame.font.Font("assets/font/PressStart2P.ttf", 32)
        self.prompt_surf = self.font.render("Digite seu nome:", True, (222,177,61))
        self.input_text = ""
        self.error_message = ""
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active   = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        w, h = tela["largura"] // 2, 50
        x = (tela["largura"] - w) // 2
        y = (tela["altura"]  - h) // 2
        self.input_rect = pygame.Rect(x, y, w, h)
        self.active = False

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(evento.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive

            if evento.type == pygame.KEYDOWN and self.active:
                if evento.key == pygame.K_RETURN:
                    nome = self.input_text.strip() or "Jogador"
                    nomes_existentes = [entry["name"] for entry in load_ranking()]
                    if nome in nomes_existentes:
                        self.error_message = "Nome já cadastrado!"
                    else:
                        self.jogo.player_name = nome
                        self.jogo.trocar_tela(TelaJogo(self.jogo, self.tela))
                elif evento.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    self.error_message = ""
                elif len(self.input_text) < 20:
                    self.input_text += evento.unicode
                    self.error_message = ""

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        prompt_x = (self.tela["largura"] - self.prompt_surf.get_width()) // 2
        janela.blit(self.prompt_surf, (prompt_x, self.input_rect.y - 60))

        txt_surf = self.font.render(self.input_text, True, (255,255,255))
        width = max(self.input_rect.w, txt_surf.get_width()+10)
        self.input_rect.w = width
        pygame.draw.rect(janela, self.color, self.input_rect, 2, border_radius=5)
        janela.blit(txt_surf, (self.input_rect.x+5, self.input_rect.y+8))

        if self.error_message:
            erro_font = pygame.font.Font("assets/font/PressStart2P.ttf", 20)
            erro_surf = erro_font.render(self.error_message, True, (255, 0, 0))
            erro_x = (self.tela["largura"] - erro_surf.get_width()) // 2
            janela.blit(erro_surf, (erro_x, self.input_rect.y + 70))

        pygame.display.flip()