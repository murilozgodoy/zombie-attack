import pygame
import random

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
class Animacoes(pygame.sprite.Sprite):
    def __init__(self,image,frames):
        super().__init__()
        self.frame_atual = 0
        self.path = image
        self.carregar_frames(image,frames)
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100  
        self.rect = (320, 200)



    def carregar_frames(self, image, frames):
        image = pygame.image.load(image).convert_alpha()
        largura = pygame.Surface.get_width(image) * 5
        altura = pygame.Surface.get_height(image) * 5
        self.spritesheet = pygame.transform.scale(image,(largura,altura))
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



class Zumbies(pygame.sprite.Sprite):
    def __init__(self,image,frames):
        super().__init__()
        self.frame_atual = 0
        self.path = image
        self.carregar_frames(image,frames)
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100  
        self.rect = [1000, 200]



    def carregar_frames(self, image, frames):
        image = pygame.image.load(image).convert_alpha()
        largura = pygame.Surface.get_width(image) * 5
        altura = pygame.Surface.get_height(image) * 5
        self.spritesheet = pygame.transform.scale(image,(largura,altura))
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
            self.rect[0] -= 10
# class Parado(Animacoes):
#     def __init__(self):
#         super().__init__("assets/img/Idle.png", 7)
# class Atirando(Animacoes):
#     def __init__(self):
#         super().__init__("assets/img/Idle.png", 4)
# class Tiro(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.image.load("assets/img/laserRed16.png")
#         self.rect = self.image.get_rect()
#         self.rect.centerx = x
#         self.rect.bottom = y
#         self.speed = -400
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
        self.image = pygame.transform.scale(imagem,(largura,altura))

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
        self.personagem = Animacoes("assets/img/Idle.png", 7)
        self.zumbies = Zumbies("assets/img/Zombie_1/Walk.png",10)
        image = pygame.image.load("assets/img/fundo.png")
        self.fundo = pygame.transform.scale(image,(1920,1080))
        self.municao = 30
        # self.grupo_tiros = pygame.sprite.Group()
        # self.nave = Nave(self.grupo_tiros)
        # self.grupo_nave = pygame.sprite.GroupSingle(self.nave)
        # self.grupo_meteoros = pygame.sprite.Group()
        # self.grupo_explosoes = pygame.sprite.Group()
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        # self.coracao = self.fonte.render(chr(9829),True,(255,0,0))
        self.fps_monitor = FPS()
        # for i in range(8):
        #     self.grupo_meteoros.add(Meteoro())
        # self.vidas = 3
        # self.music.play()

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN and self.municao > 0:
                    self.personagem = Animacoes("assets/img/Shot_1.png", 4)
            elif evento.type == pygame.KEYUP:
                self.personagem = Animacoes("assets/img/Idle.png", 7)

    
    def atualiza(self):
        # self.grupo_nave.update()
        # self.grupo_meteoros.update()
        # self.grupo_tiros.update()
        # self.grupo_explosoes.update()
        self.zumbies.update()
        self.personagem.update()

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
        

    def desenha(self, janela):
        janela.fill((0,0,0))
        # pygame.draw.rect(janela,(0,0,0),(0,900,1920,360))
        # pygame.draw.rect(janela,(200,200,200),(0,0,1920,900))
        janela.blit(self.fundo,(0,0))
        # self.fps_monitor.calcula_fps()
        # texto_fps = self.fonte.render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        # texto_fps = pygame.transform.scale(texto_fps, (100, 20))
        # janela.blit(texto_fps, (540, 680))
        # self.grupo_nave.draw(janela)
        janela.blit(self.personagem.image, self.personagem.rect)
        janela.blit(self.zumbies.image,(self.zumbies.rect[0],self.zumbies.rect[1]))
        # self.grupo_meteoros.draw(janela)
        # self.grupo_tiros.draw(janela)
        # self.grupo_explosoes.draw(janela)
        # for i in range(self.vidas):
        #     janela.blit(self.coracao, (10 + i * 30, 10, 20, 20))
        pygame.display.flip()

class Jogo:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        largura = info.current_w
        altura = info.current_h
        self.janela = pygame.display.set_mode((largura, altura),pygame.FULLSCREEN)
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
