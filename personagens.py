import pygame
import math

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, destino_x, destino_y, imagem):
        super().__init__()
        self.image = pygame.transform.scale(imagem, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))

        dx = destino_x - x
        dy = destino_y - y
        distancia = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        angulo = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(imagem, angulo)
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidade = 100
        self.velocidade_x = (dx / distancia) * self.velocidade
        self.velocidade_y = (dy / distancia) * self.velocidade

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if (self.rect.right < 0 or self.rect.left > 1920 or
            self.rect.bottom < 0 or self.rect.top > 1080):
            self.kill()

class Impacto(pygame.sprite.Sprite):
    def __init__(self, center, spritesheet, frames):
        super().__init__()
        self.frames = self.carregar_frames(spritesheet, frames)
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=center)
        self.tempo_anterior = pygame.time.get_ticks()
        self.intervalo = 200

    def carregar_frames(self, spritesheet, frames):
        image = spritesheet.convert_alpha()
        altura = image.get_height()
        largura_total = image.get_width()
        largura_quadro = largura_total // frames
        return [image.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_anterior > self.intervalo:
            self.tempo_anterior = agora
            self.frame_atual += 1
            if self.frame_atual < len(self.frames):
                self.image = self.frames[self.frame_atual]
            else:
                self.kill()

class Personagens(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.tela = tela
        largura = self.frames[0].get_width()
        altura = self.frames[0].get_height()
        self.rect = pygame.Rect(tela["largura"] - 1000, tela["altura"] - 700, largura, altura)
        self.vidas = 3

    def carregar_frames(self, image, frames):
        image = image.convert_alpha()
        altura = image.get_height()
        largura_total = image.get_width()
        largura_quadro = largura_total // frames
        self.frames = [image.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]
        self.image = self.frames[0]

    def trocar_animacao(self, image, frames):
        self.carregar_frames(image, frames)
        self.frame_atual = 0

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

    def mover(self, velocidadex, velocidadey):
        agora = pygame.time.get_ticks()
        delta_time = (agora - self.tempo_ultimo_update) / 1000
        self.rect.x -= velocidadex * delta_time
        self.rect.y += velocidadey * delta_time

    def desenha(self, janela):
        janela.blit(self.image, self.rect)

class Zumbies(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.walk = image
        self.intervalo_animacao = 100
        largura = self.frames[0].get_width()
        altura = self.frames[0].get_height()
        self.rect = pygame.Rect(tela["largura"], tela["altura"] - 700, largura, altura)
        self.vidas = 2
        self.velocidade = 10
        self.estado = 'andando'
        self.animacao_dano = False

    def carregar_frames(self, image, frames):
        image = image.convert_alpha()
        altura = image.get_height()
        largura_total = image.get_width()
        largura_quadro = largura_total // frames
        self.frames = [image.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]
        self.image = self.frames[0]

    def trocar_animacao(self, image, frames, dano=False, novo_estado=None):
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.animacao_dano = dano
        if novo_estado:
            self.estado = novo_estado

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual += 1
            if self.frame_atual >= len(self.frames):
                if self.animacao_dano:
                    self.trocar_animacao(self.walk, 10)
                    self.estado = 'andando'
                    self.animacao_dano = False
                else:
                    self.frame_atual = 0
            self.image = self.frames[self.frame_atual]

        if self.estado == 'andando':
            delta_time = (agora - self.tempo_ultimo_update) / 1000
            self.rect.x -= self.velocidade * delta_time
            if self.rect.x < 0:
                self.kill()

    def desenha(self, janela):
        janela.blit(self.image, self.rect)