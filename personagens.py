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
    def __init__(self, center, spritesheet, frames,entidade):
        super().__init__()
        self.frames = self.carregar_frames(spritesheet, frames)
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=center)
        self.tempo_anterior = pygame.time.get_ticks()
        self.intervalo = 200
        self.entidade = entidade
        

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
                if self.entidade != "Personagem":
                    self.kill()

class Personagens(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.tela = tela
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

class Zumbies(pygame.sprite.Sprite):
    def __init__(self, image, frames, tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.walk = image
        self.intervalo_animacao = 100
        largura_frame = 112 * 5
        altura_frame = 128 * 5

        # Frame da sprite (imagem visual do personagem)
        self.image_rect = pygame.Rect(tela["largura"] ,
            tela["altura"] - 400,
            largura_frame,
            altura_frame
        )

        # Hitbox mais precisa (centralizada na parte do corpo)
        hitbox_largura = 150
        hitbox_altura = 350

        # Alinha o centro da hitbox com a parte inferior do personagem (os pés)
        self.rect = pygame.Rect(
            (self.image_rect.centerx - hitbox_largura // 2),
            tela["altura"] - 400,
            hitbox_largura,
            hitbox_altura
        )

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
        delta_time = (agora - self.tempo_ultimo_update) / 1000
        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual += 1
            if self.frame_atual >= len(self.frames):
                if self.animacao_dano:
                    self.trocar_animacao(self.walk, 10)
                    self.estado = 'andando'
                    self.animacao_dano = False
                elif self.estado == "Ataque":
                    self.trocar_animacao(self.walk,5)
                    self.rect.x -= 20 * delta_time
                    self.image_rect.midbottom = self.rect.midbottom
                    self.estado = "andando"
                else:
                    self.frame_atual = 0
            self.image = self.frames[self.frame_atual]
            
        if self.estado == 'andando':
            self.rect.x -= self.velocidade * delta_time
            self.image_rect.midbottom = self.rect.midbottom  # mantém sprite sempre alinhado com a hitbox
            if self.rect.x < -200:
                self.kill()
            

    def desenha(self, janela):
        janela.blit(self.image, self.image_rect)
        # pygame.draw.rect(janela, (0, 255, 0), self.rect)