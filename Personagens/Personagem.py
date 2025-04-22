import pygame

class Personagens(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.tela = tela
        self.municoes_totais = 120
        self.municoes = 30
        self.zumbies_mortos = 0
        largura_frame = 112 * 5
        altura_frame = 128 * 5

        # Frame da sprite (imagem visual do personagem)
        self.image_rect = pygame.Rect(
            (tela["largura"] // 2) - largura_frame // 2,
            tela["altura"] - altura_frame - 50,
            largura_frame,
            altura_frame
        )

        # Hitbox mais precisa (centralizada na parte do corpo)
        hitbox_largura = 100
        hitbox_altura = 350

        # Alinha o centro da hitbox com a parte inferior do personagem (os pés)
        self.rect = pygame.Rect(
            (self.image_rect.centerx - hitbox_largura // 2)+30,
            self.image_rect.bottom - hitbox_altura,
            hitbox_largura,
            hitbox_altura
        )

    
        self.vidas = 100


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
            # if self.frame_atual >= len(self.frames):
                # if 
                # self.trocar_animacao(self.walk,5)

    def mover(self, velocidadex, velocidadey):
        agora = pygame.time.get_ticks()
        delta_time = (agora - self.tempo_ultimo_update) / 1000
        self.rect.x -= velocidadex * delta_time
        self.rect.y += velocidadey * delta_time

        self.image_rect.x -= velocidadex * delta_time
        self.image_rect.y += velocidadey * delta_time
    def desenha(self, janela):
        janela.blit(self.image, self.image_rect)