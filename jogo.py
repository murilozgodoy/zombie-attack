

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

def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
    if rect_x <= ponto_x and ponto_x <= rect_x + rect_w and rect_y <= ponto_y and ponto_y <= rect_y + rect_h:
        return True
    return False

class Tiro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagem_tiro = pygame.image.load("assets/img/bala.png") # precisa ser self.image toda sprite, não self.imagem ou algo do tipo
        self.image = pygame.transform.scale(self.imagem_tiro, (65,40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 10
        # self.velocidade_y = algum numero (se quisermos fazer um tiro em diagonal)
    
    def update(self):
        info = pygame.display.Info()
        largura_tela = info.current_w
        altura_tela = info.current_h
        self.rect.x += self.velocidade_x
        if self.rect.right >= largura_tela:
            self.kill()

class Impacto(pygame.sprite.Sprite):
    def __init__(self, center, spritesheet, frames):
        super().__init__()
        self.frames = self.carregar_frames(spritesheet, frames)
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.tempo_anterior = pygame.time.get_ticks()
        self.intervalo = 50 

    def carregar_frames(self, spritesheet, frames):
        image = pygame.image.load(spritesheet).convert_alpha()
        largura = pygame.Surface.get_width(image) * 5
        altura = pygame.Surface.get_height(image) * 5
        spritesheet = pygame.transform.scale(image, (largura, altura))
        # largura = spritesheet.get_width()
        # altura = spritesheet.get_height()
        # largura_quadro = largura // frames
        frames = [spritesheet.subsurface((i * altura, 0, altura, altura)) 
                  for i in range(frames)]
        return frames
    
    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_anterior > self.intervalo:
            self.tempo_anterior = agora
            self.frame_atual += 1
            if self.frame_atual < len(self.frames):
                self.image = self.frames[self.frame_atual]
            else:
                self.kill()


class Cronometro:
    def __init__(self, minutos, fonte):
        self.tempo_restante = minutos * 60 * 1000
        self.tempo_de_inicio = pygame.time.get_ticks()
        self.fonte = fonte
        self.tempo_acabou = False
    
    def atualizar(self):
        agora = pygame.time.get_ticks()
        self.tempo_restante -= agora - self.tempo_de_inicio
        self.tempo_de_inicio = agora
        if self.tempo_restante <= 0:
            self.tempo_restante = 0
            self.tempo_acabou = True

    def desenha(self, janela, x, y):
        minutos = self.tempo_restante // (60 * 1000)
        segundos = (self.tempo_restante // 1000) % 60
        texto = f"{minutos:02}:{segundos:02}"
        renderizado = self.fonte.render(texto, True, (255, 255, 255))
        janela.blit(renderizado, (x, y))
        
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
        info = pygame.display.Info()
        largura_tela = info.current_w
        altura_tela = info.current_h
        self.frame_atual = 0
        self.path = image
        self.carregar_frames(image, frames)
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        largura = self.frames[0].get_width()
        altura = self.frames[0].get_height()
        self.rect = pygame.Rect(largura_tela, 200, largura, altura)

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
        imagem = pygame.image.load("assets/img/Inicial.png")
        self.image = pygame.transform.scale(imagem, (largura, altura))
    def trata_eventos(self, eventos):
        for evento in eventos:
            if colisao_ponto_retangulo(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 535, 374, 475, 135): # Verifica se o mouse está sobre o botão jogar
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.jogo.trocar_tela(TelaJogo(self.jogo))
            if colisao_ponto_retangulo(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],535, 550, 475, 135): # Verifica se o mouse está sobre o botão instruções
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pass # temos que colocar para ir para a pagina de instruções

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
        self.zumbies = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.impactos = pygame.sprite.Group() 
        image = pygame.image.load("assets/img/fundo.png")
        self.fundo = pygame.transform.scale(image, (self.largura, self.altura))
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        self.fps_monitor = FPS()

        self.animacao_tiro = False
        self.animacao_repetir = False

        self.cronometro = Cronometro(1, self.fonte)

        self.ultima_geracao = pygame.time.get_ticks()
        self.intervalo_geracao = 4000 # 3000 porque seriam 3000 milisegundos

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    if not self.animacao_tiro:  # Inicia a animação apenas se não estiver ativa
                        self.personagem.trocar_animacao("assets/img/Shot_1.png", 4)  # Animação de tiro
                        self.animacao_tiro = True  # Marca que a animação está em progresso
                    x = self.personagem.rect.centerx
                    y = self.personagem.rect.centery
                    novo_tiro = Tiro(x+20,y+130)
                    self.tiros.add(novo_tiro)
                    self.animacao_repetir = True  # Indica que a tecla está pressionada
                if evento.key == pygame.K_a:  
                    self.moving_left = True
                    self.moving_right = False
                    self.personagem.trocar_animacao("assets/img/Walk_inverted.png", 7)
                if evento.key == pygame.K_d: 
                    self.moving_right = True
                    self.moving_left = False
                    self.personagem.trocar_animacao("assets/img/Walk.png", 7)
                if evento.key == pygame.K_w: 
                    self.moving_up = True
                if evento.key == pygame.K_s:  
                    self.moving_down = True

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_p:
                    self.animacao_repetir = False  # Para de repetir quando a tecla for solta

                if evento.key == pygame.K_a:
                    self.moving_left = False
                    if not self.moving_right:
                        self.personagem.trocar_animacao("assets/img/Idle.png", 7)
                if evento.key == pygame.K_d:
                    self.moving_right = False
                    if not self.moving_left:
                        self.personagem.trocar_animacao("assets/img/Idle.png", 7)
                if evento.key == pygame.K_w:
                    self.moving_up = False
                if evento.key == pygame.K_s:
                    self.moving_down = False

    def atualiza(self):
        self.cronometro.atualizar()
        if self.cronometro.tempo_acabou:
            self.jogo.trocar_tela(TelaGameOver(self.jogo))

        agora = pygame.time.get_ticks()
        if agora - self.ultima_geracao > self.intervalo_geracao:
            self.ultima_geracao = agora
            novo_zumbi = Zumbies("assets/img/Zombie_1/Walk.png", 10)
            self.zumbies.add(novo_zumbi)

        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, True)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                impacto = Impacto(zumbi.rect.center, "assets/img/Zombie_1/Hurt_invertida.png", 4)
                self.zumbies.add(impacto) 

        # Atualizar as animações do personagem e verificar o término da animação de tiro
        if self.animacao_tiro:
            if self.personagem.frame_atual == len(self.personagem.frames) - 1:  # Último quadro
                if self.animacao_repetir:  # Se a tecla ainda estiver pressionada, reinicia
                    self.personagem.trocar_animacao("assets/img/Shot_1.png", 4)  # Reinicia animação
                    x = self.personagem.rect.centerx
                    y = self.personagem.rect.centery
                    novo_tiro = Tiro(x+30,y+140)
                    self.tiros.add(novo_tiro)
                else:
                    self.animacao_tiro = False  # Conclui a animação de tiro
                    self.personagem.trocar_animacao("assets/img/Idle.png", 7)  # Retorna à animação parado

        self.personagem.update()
        self.zumbies.update()
        self.tiros.update()

        # Verificar movimento horizontal
        if self.moving_left or self.moving_right:
            if self.moving_left:
                self.personagem.mover(-1, 0)
            if self.moving_right:
                self.personagem.mover(1, 0)

        # Verificar movimento vertical
        if self.moving_up or self.moving_down:
            if self.moving_up and self.personagem.rect.y > 35:
                self.personagem.mover(0, -1)
            if self.moving_down and self.personagem.rect.y + self.personagem.rect.height < self.altura:
                self.personagem.mover(0, 1)

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.fundo, (0, 0))
        self.fps_monitor.calcula_fps()
        texto_fps = self.fonte.render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        texto_fps = pygame.transform.scale(texto_fps, (150, 30))
        janela.blit(texto_fps, ((self.largura - 150), (self.altura - 30)))
        
        self.cronometro.desenha(janela, (self.largura // 2) - 50, 10)  # Desenha o cronômetro no canto superior esquerdo
        



        self.personagem.desenha(janela)
        self.zumbies.draw(janela)
        self.tiros.draw(janela)
        self.impactos.draw(janela)
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