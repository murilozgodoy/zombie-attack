import pygame
from random import randint
class Zumbies(pygame.sprite.Sprite):
    def __init__(self, imagem_andar, frames_andar, tela, escala):
        super().__init__()
        self.escala = escala
        self.animacoes = {
            'andar': (imagem_andar, frames_andar),
            'ataque': None,
            'dano': None
        }

        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.estado = 'andando'
        self.animacao_dano = False

        self.carregar_frames(*self.animacoes['andar'])

        largura_frame = escala.escalar(112 * 5)
        altura_frame = escala.escalar(128 * 5)

        # Frame visual
        y_base = randint(180, 350)
        y = escala.escalar(y_base)
        self.image_rect = pygame.Rect(
            tela["largura"],
            tela["altura"] - y,
            largura_frame,
            altura_frame
        )

        # Hitbox de colisão
        hitbox_largura = escala.escalar(150)
        hitbox_altura = escala.escalar(350)
        self.rect = pygame.Rect(
            self.image_rect.centerx - hitbox_largura // 2,
            tela["altura"] - escala.escalar(y_base * 2),
            hitbox_largura,
            hitbox_altura
        )

        self.image_rect.midbottom = self.rect.midbottom

        self.vidas = 3
        self.velocidade = escala.escalar(23)

    def carregar_frames(self, imagem, frames):
        imagem = imagem.convert_alpha()
        altura = imagem.get_height()
        largura_total = imagem.get_width()
        largura_quadro = largura_total // frames
        self.frames = [imagem.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]
        self.image = self.frames[0]

    def trocar_animacao(self, imagem, frames, dano=False, novo_estado=None):
        self.carregar_frames(imagem, frames)
        self.frame_atual = 0
        self.animacao_dano = dano
        if novo_estado:
            self.estado = novo_estado
        self.image_rect = self.image.get_rect()
        self.image_rect.midbottom = self.rect.midbottom

    def definir_animacao_ataque(self, spritesheet, frames):
        self.animacoes['ataque'] = (spritesheet, frames)

    def definir_animacao_dano(self, spritesheet, frames):
        self.animacoes['dano'] = (spritesheet, frames)

    def update(self):
        agora = pygame.time.get_ticks()
        delta_time = (agora - self.tempo_ultimo_update) / 1000

        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual += 1
            if self.frame_atual >= len(self.frames):
                if self.estado == 'dano':
                    self.trocar_animacao(*self.animacoes['andar'])
                    self.estado = 'andando'
                    self.animacao_dano = False
                elif self.estado == 'Ataque':
                    self.trocar_animacao(*self.animacoes['andar'])
                    self.estado = 'andando'
                else:
                    self.frame_atual = 0
            self.image = self.frames[self.frame_atual]

        if self.estado == 'andando':
            self.rect.x -= self.velocidade * delta_time
            if self.rect.x < -self.escala.escalar(200):
                self.kill()

        self.image_rect.midbottom = self.rect.midbottom

    def desenha(self, janela):
        janela.blit(self.image, self.image_rect)


class Zumbies_Corredores(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela, escala):
        super().__init__()
        self.escala = escala
        self.animacoes = {
            "andar": (image, frames),
            "dano": None
        }
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.estado = 'andando'
        self.animacao_dano = False
        largura_frame = escala.escalar(112 * 5)
        altura_frame = escala.escalar(128 * 5)
        y = randint(0,1)
        if y == 0:
            self.image_rect = pygame.Rect(tela["largura"] ,
                tela["altura"] - escala.escalar(20),
                largura_frame,
                altura_frame - escala.escalar(190)
            )
            hitbox_largura = escala.escalar(150)
            hitbox_altura = escala.escalar(300)
            self.rect = pygame.Rect(
                (self.image_rect.centerx - hitbox_largura // 2) ,
                tela["altura"] - escala.escalar(300),
                hitbox_largura,
                hitbox_altura
            )
        else:
            self.image_rect = pygame.Rect(tela["largura"] ,
                tela["altura"] - escala.escalar(20),
                largura_frame,
                altura_frame - escala.escalar(190)
            )
            hitbox_largura = escala.escalar(150)
            hitbox_altura = escala.escalar(300)
            self.rect = pygame.Rect(
                (self.image_rect.centerx - hitbox_largura // 2) ,
                tela["altura"] - escala.escalar(600),
                hitbox_largura,
                hitbox_altura
            )

        self.image = self.frames[0]
        self.vidas = 2
        self.velocidade = escala.escalar(43)

    def carregar_frames(self, image, frames):
        image = image.convert_alpha()
        altura = image.get_height()
        largura_total = image.get_width()
        largura_quadro = largura_total // frames
        self.frames = [image.subsurface((i * largura_quadro, 0, largura_quadro, altura)) for i in range(frames)]

    def trocar_animacao(self, image, frames, dano=False, novo_estado=None):
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.image = self.frames[0]
        self.image_rect.midbottom = self.rect.midbottom
        if dano:
            self.animacao_dano = True
            self.animacoes["dano"] = (image, frames)
        if novo_estado:
            self.estado = novo_estado

    def update(self):
        agora = pygame.time.get_ticks()
        delta_time = (agora - self.tempo_ultimo_update) / 1000

        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual += 1
            if self.frame_atual >= len(self.frames):
                if self.estado == 'dano':
                    self.trocar_animacao(*self.animacoes["andar"], novo_estado='andando')
                    self.animacao_dano = False
                else:
                    self.frame_atual = 0
            self.image = self.frames[self.frame_atual]

        if self.estado == 'andando':
            self.rect.x -= self.velocidade * delta_time
            if self.rect.x < -self.escala.escalar(200):
                self.kill()

        self.image_rect.midbottom = self.rect.midbottom

    def desenha(self, janela):
        janela.blit(self.image, self.image_rect)

