

# class Nave(pygame.sprite.Sprite):
#     def __init__(self, grupo_tiros):
#         super().__init__()
#         self.tiro_imagem = pygame.image.load("assets/img/laserRed16.png")
#         self.image = pygame.image.load("assets/img/playerShip1_orange.png")
#         self.tiro = pygame.mixer.Sound("assets/snd/pew.wav")
#         self.image = pygame.transform.scale(self.image, (40, 40))
#         self.rect = self.image.get_rect()
#         self.rect.center = (320, 600)
#         self.x = self.rect.centerx
#         self.y = self.rect.centery
#         self.vel_x = 0
#         self.vel_y = 0
#         self.last_updated = pygame.time.get_ticks()
#         self.radius = self.rect.width / 2
#         self.grupo_tiros = grupo_tiros

#     def update(self):
#         t1 = pygame.time.get_ticks()
#         delta = (t1 - self.last_updated) / 1000
#         self.last_updated = t1
#         self.x += self.vel_x * delta
#         self.y += self.vel_y * delta
#         self.x = max(20, min(640 - 20, self.x))
#         self.y = max(20, min(720 - 20, self.y))
#         self.rect.center = (self.x, self.y)

#     def movimentacao(self, evento):
#         if evento.key == pygame.K_LEFT:
#             self.vel_x = -200
#         elif evento.key == pygame.K_RIGHT:
#             self.vel_x = 200
#         elif evento.key == pygame.K_UP:
#             self.vel_y = -200
#         elif evento.key == pygame.K_DOWN:
#             self.vel_y = 200
#         elif evento.key == pygame.K_SPACE:
#             self.tiro.play()
#             tiro = Tiro(self.rect.centerx, self.rect.top)
#             self.grupo_tiros.add(tiro)

#     def parar(self, evento):
#         if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
#             self.vel_x = 0
#         elif evento.key in (pygame.K_UP, pygame.K_DOWN):
#             self.vel_y = 0

# class Explosao(pygame.sprite.Sprite):
#     def __init__(self, center):
#         super().__init__()
#         self.frames = [
#             pygame.image.load(f"assets/img/regularExplosion0{i}.png") for i in range(9)
#         ]
#         self.frame_atual = 0
#         self.image = self.frames[self.frame_atual]
#         self.rect = self.image.get_rect()
#         self.rect.center = center
#         self.tempo_anterior = pygame.time.get_ticks()
#         self.intervalo = 20

#     def update(self):
#         agora = pygame.time.get_ticks()
#         if agora - self.tempo_anterior > self.intervalo:
#             self.tempo_anterior = agora
#             self.frame_atual += 1
#             if self.frame_atual < len(self.frames):
#                 self.image = self.frames[self.frame_atual]
#             else:
#                 self.kill()

import pygame
import random


class Personagens(pygame.sprite.Sprite):
    def __init__(self, image, frames):
        super().__init__()
        self.frame_atual = 0
        self.path = image
        self.carregar_frames(image, frames)
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        largura = self.frames[0].get_width()
        altura = self.frames[0].get_height()
        self.rect = pygame.Rect(320, 200, largura, altura)  # Facilita movimentação e colisão

    def carregar_frames(self, image, frames):
        image = pygame.image.load(image).convert_alpha()
        largura = image.get_width() * 5
        altura = image.get_height() * 5
        self.spritesheet = pygame.transform.scale(image, (largura, altura))
        self.frames = [self.spritesheet.subsurface((i * altura, 0, altura, altura)) for i in range(frames)]
        self.image = self.frames[0]

    def trocar_animacao(self, path, frames):
        self.carregar_frames(path, frames)
        self.frame_atual = 0

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def desenha(self, janela):
        janela.blit(self.image, self.rect)


class Zumbies(pygame.sprite.Sprite):
    def __init__(self, image, frames):
        super().__init__()
        self.frame_atual = 0
        self.path = image
        self.carregar_frames(image, frames)
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        largura = self.frames[0].get_width()
        altura = self.frames[0].get_height()
        self.rect = pygame.Rect(1000, 200, largura, altura)

    def carregar_frames(self, image, frames):
        image = pygame.image.load(image).convert_alpha()
        largura = pygame.Surface.get_width(image) * 5
        altura = pygame.Surface.get_height(image) * 5
        self.spritesheet = pygame.transform.scale(image, (largura, altura))
        self.frames = [self.spritesheet.subsurface((i * altura, 0, altura, altura)) for i in range(frames)]
        self.image = self.frames[0]

    def trocar_animacao(self, path, frames):
        self.carregar_frames(path, frames)
        self.frame_atual = 0

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_update > self.intervalo_animacao:
            self.tempo_ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]
            self.rect.x -= 10

    def desenha(self, janela):
        janela.blit(self.image, self.rect)


class FPS:
    def __init__(self):
        self.fps = 0
        self.t0 = 0

    def calcula_fps(self):
        t1 = pygame.time.get_ticks()
        if self.t0 >= 0:
            delta = (t1 - self.t0) / 1000
            if delta > 0:
                self.fps = 1 / delta
        self.t0 = t1


class Tela:
    def trata_eventos(self, eventos):
        pass

    def atualiza(self):
        pass

    def desenha(self, janela):
        pass


class TelaInicial(Tela):
    def __init__(self, jogo):
        self.jogo = jogo
        info = pygame.display.Info()
        largura = info.current_w
        altura = info.current_h
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        imagem = pygame.image.load("assets/img/tela_incio.png")
        self.image = pygame.transform.scale(imagem, (largura, altura))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.jogo.trocar_tela(TelaJogo(self.jogo))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        pygame.display.flip()


class TelaGameOver(Tela):
    def __init__(self, jogo):
        self.jogo = jogo
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.jogo.trocar_tela(TelaJogo(self.jogo))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        texto = self.fonte.render("GAME OVER", True, (255, 0, 0))
        texto2 = self.fonte.render("R - Reiniciar", True, (255, 255, 255))
        janela.blit(texto, (180, 300))
        janela.blit(texto2, (140, 350))
        pygame.display.flip()


class TelaJogo(Tela):
    def __init__(self, jogo):
        self.jogo = jogo
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        self.personagem = Personagens("assets/img/Idle.png", 7)
        self.zumbies = Zumbies("assets/img/Zombie_1/Walk.png", 10)
        image = pygame.image.load("assets/img/fundo.png")
        self.fundo = pygame.transform.scale(image, (self.largura, self.altura))
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        self.fps_monitor = FPS()

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  
                    self.moving_left = True
                if evento.key == pygame.K_d: 
                    self.moving_right = True
                if evento.key == pygame.K_w: 
                    self.moving_up = True
                if evento.key == pygame.K_s:  
                    self.moving_down = True
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a:
                    self.moving_left = False
                if evento.key == pygame.K_d:
                    self.moving_right = False
                if evento.key == pygame.K_w:
                    self.moving_up = False
                if evento.key == pygame.K_s:
                    self.moving_down = False

    def atualiza(self):
        self.personagem.update()
        self.zumbies.update()

        # Verificar limites do movimento no eixo Y
        if self.moving_up and self.personagem.rect.y > 35:
            self.personagem.mover(0, -2)
        if self.moving_down and self.personagem.rect.y + self.personagem.rect.height < self.altura:  # Não ultrapassa o limite inferior da tela
            self.personagem.mover(0, 2)

        # Movimento no eixo X (sem limites, mas pode ser adicionado se necessário)
        if self.moving_left:
            self.personagem.mover(-2, 0)
        if self.moving_right:
            self.personagem.mover(2, 0)

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.fundo, (0, 0))
        self.fps_monitor.calcula_fps()
        texto_fps = self.fonte.render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        texto_fps = pygame.transform.scale(texto_fps, (150, 30))
        janela.blit(texto_fps, ((self.largura - 150), (self.altura - 30)))
        self.personagem.desenha(janela)
        self.zumbies.desenha(janela)
        pygame.display.flip()


class Jogo:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        largura = info.current_w
        altura = info.current_h
        self.janela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
        pygame.display.set_caption("Zombie Attack")
        self.tela_atual = TelaInicial(self)

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


if __name__ == "__main__":
    jogo = Jogo()
    jogo.roda()
    
## Save 8/04

# class Parado(Personagens):
#     def __init__(self):
#         super().__init__("assets/img/Idle.png", 7)
# class Atirando(Personagens):
#     def __init__(self):
#         super().__init__("assets/img/Idle.png", 4)

# class Tiro(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.image.load("assets/img/laserRed16.png")
#         self.rect = self.image.get_rect()
#         self.rect.centerx = x
#         self.rect.bottom = y
#         self.speed = +400
#         self.last_updated = pygame.time.get_ticks()

#     def update(self):
#         t1 = pygame.time.get_ticks()
#         delta = (t1 - self.last_updated) / 1000
#         self.last_updated = t1
#         self.rect.y += self.speed * delta
#         if self.rect.bottom < 0:
#             self.kill()

# class Estrelas:
#     def __init__(self):
#         self.lista = []
#         for i in range(50):
#             x = random.randint(20, 600)
#             y = random.randint(20, 600)
#             r = random.randint(1, 5)
#             self.lista.append([x, y, r])


# class Botoes:
#     def __init__(self):
#         self.start = pygame.image.load()
#     def jogar(self):

# class Meteoro(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("assets/img/meteorBrown_med1.png")
#         self.rect = self.image.get_rect()
#         self.radius = self.image.get_height() / 5
#         self.rect.x = random.randrange(0, 640 - self.rect.width)
#         self.rect.y = random.randrange(-100, -40)
#         self.speed = random.randint(2, 5)

#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.top > 720:
#             self.rect.y = random.randrange(-100, -40)
#             self.rect.x = random.randrange(0, 640 - self.rect.width)
#             self.speed = random.randint(2, 5)

# self.grupo_tiros = pygame.sprite.Group()
# self.nave = Nave(self.grupo_tiros)
# self.grupo_nave = pygame.sprite.GroupSingle(self.nave)
# self.grupo_meteoros = pygame.sprite.Group()
# self.grupo_explosoes = pygame.sprite.Group()
# self.coracao = self.fonte.render(chr(9829),True,(255,0,0))
# for i in range(8):
#     self.grupo_meteoros.add(Meteoro())
# self.vidas = 3
# self.music.play()


# self.grupo_nave.update()
# self.grupo_meteoros.update()
# self.grupo_tiros.update()
# self.grupo_explosoes.update()

# colisoes = pygame.sprite.groupcollide(self.grupo_nave, self.grupo_meteoros, False, True, pygame.sprite.collide_circle)
# if colisoes:
#     self.vidas -= 1
#     for i in range(len(colisoes[list(colisoes.keys())[0]])):
#         self.grupo_meteoros.add(Meteoro())
#     if self.vidas <= 0:
#         self.jogo.trocar_tela(TelaGameOver(self.jogo))
#         self.music.stop()

# colisoes_tiro_meteoro = pygame.sprite.groupcollide(self.grupo_tiros, self.grupo_meteoros, True, True, pygame.sprite.collide_circle)
# for tiro, meteoros_atingidos in colisoes_tiro_meteoro.items():
#     for meteoro in meteoros_atingidos:
#         x = meteoro.rect.centerx
#         y = meteoro.rect.centery
#         explosao = Explosao((x, y))
#         self.grupo_explosoes.add(explosao)
#         self.grupo_meteoros.add(Meteoro())


        # pygame.draw.rect(janela,(0,0,0),(0,900,1920,360))
        # pygame.draw.rect(janela,(200,200,200),(0,0,1920,900))
        # self.grupo_nave.draw(janela)
        # self.grupo_meteoros.draw(janela)
        # self.grupo_tiros.draw(janela)
        # self.grupo_explosoes.draw(janela)
        # for i in range(self.vidas):
        #     janela.blit(self.coracao, (10 + i * 30, 10, 20, 20))