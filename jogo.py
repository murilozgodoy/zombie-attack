
import pygame
import random
import math
## Inicia o Pygame e pega o tamanho da tela 
# pygame.init()
# info = pygame.display.Info()
# largura_tela = info.current_w
# altura_tela = info.current_h
def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
    return rect_x <= ponto_x <= rect_x + rect_w and rect_y <= ponto_y <= rect_y + rect_h

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
    def __init__(self, image, frames,tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 100
        self.tela =  tela
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
    def __init__(self, image, frames,tela):
        super().__init__()
        self.carregar_frames(image, frames)
        self.frame_atual = 0
        self.tempo_ultimo_update = pygame.time.get_ticks()
        self.walk = pygame.transform.scale(pygame.image.load('assets/img/Zombie_1/Walk.png'),(pygame.image.load('assets/img/Zombie_1/Walk.png').get_width()*5,pygame.image.load('assets/img/Zombie_1/Walk.png').get_height()*5))
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
    def __init__(self, jogo,tela):
        self.jogo = jogo
        # info = pygame.display.Info()
        # largura = info.current_w
        # altura = info.current_h
        self.tela = tela
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        imagem = pygame.image.load("assets/img/Inicial.png")
        self.image = pygame.transform.scale(imagem, (self.tela["largura"], self.tela["altura"]))
        self.jogar = pygame.image.load("assets/img/Botao_jogar.png")
    def trata_eventos(self, eventos):
        for evento in eventos:
            if colisao_ponto_retangulo(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 535, 374, 475, 135): # Verifica se o mouse está sobre o botão jogar
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.jogo.trocar_tela(TelaJogo(self.jogo,self.tela))
            if colisao_ponto_retangulo(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],535, 550, 475, 135): # Verifica se o mouse está sobre o botão instruções
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pass # temos que colocar para ir para a pagina de instruções

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        # janela.blit(self.jogar,(300,300))
        pygame.display.flip()


class TelaGameOver(Tela):
    def __init__(self, jogo,tela):
        self.jogo = jogo
        # info = pygame.display.Info()
        # largura = info.current_w
        # altura = info.current_h
        self.image = pygame.transform.scale(pygame.image.load("assets/img/gameover.png"), (tela["largura"], tela['altura']))
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.jogo.trocar_tela(TelaJogo(self.jogo))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image,(0,0))
        # texto = self.fonte.render("GAME OVER", True, (255, 0, 0))
        # texto2 = self.fonte.render("R - Reiniciar", True, (255, 255, 255))
        # janela.blit(texto, (180, 300))
        # janela.blit(texto2, (140, 350))
        pygame.display.flip()


class TelaJogo(Tela):
    def __init__(self, jogo,tela):
        self.jogo = jogo
        # info = pygame.display.Info()
        # self.largura = info.current_w
        # self.altura = info.current_h
        self.tela = tela
        self.zumbies = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.impactos = pygame.sprite.Group() 
        self.sprites = {
            "personagem_atirando":pygame.image.load("assets/img/Shot_1.png"),
            "personagem_parado":pygame.image.load("assets/img/Idle.png"),
            "personagem_andar_para_tras":pygame.image.load("assets/img/Walk_inverted.png"),
            "personagem_andar":pygame.image.load("assets/img/Walk.png"),
            "zumbi_morto":pygame.image.load("assets/img/Zombie_1/Dead.png"),
            "zumbi_ferido":pygame.image.load("assets/img/Zombie_1/Hurt_invertida.png"),
            "zumbi_andar":pygame.image.load("assets/img/Zombie_1/Walk.png"),
        }
        self.assets = {
            "img_fundo": pygame.transform.scale(pygame.image.load("assets/img/Fundo.png"), (self.tela["largura"], self.tela["altura"])),
            "fonte": pygame.font.Font("assets/font/PressStart2P.ttf", 30),
            "mira": pygame.transform.scale(pygame.image.load("assets/img/mira.png"), (27, 27)),
            "bala": pygame.transform.scale(pygame.image.load("assets/img/bala.png"), (20, 20)),
            "tiro": pygame.transform.scale(self.sprites["personagem_atirando"],(self.sprites["personagem_atirando"].get_width()*5,self.sprites["personagem_atirando"].get_height()*5)),
            "parado": pygame.transform.scale(self.sprites["personagem_parado"], (self.sprites["personagem_parado"].get_width()*5, self.sprites["personagem_parado"].get_height()*5)),
            "walk_inverted": pygame.transform.scale(self.sprites["personagem_andar_para_tras"], (self.sprites["personagem_andar_para_tras"].get_width()*5, self.sprites["personagem_andar_para_tras"].get_height()*5)),
            "walk": pygame.transform.scale(self.sprites["personagem_andar"], (self.sprites["personagem_andar"].get_width() * 5, self.sprites["personagem_andar"].get_height() * 5)),
            "zumbi_morto": pygame.transform.scale(self.sprites["zumbi_morto"], (self.sprites["zumbi_morto"].get_width()*5, self.sprites["zumbi_morto"].get_height()*5)),
            "zumbi_ferido": pygame.transform.scale(self.sprites["zumbi_ferido"], (self.sprites["zumbi_ferido"].get_width()*5, self.sprites["zumbi_ferido"].get_height()*5)),
            "zombie_walk": pygame.transform.scale(self.sprites["zumbi_andar"], (self.sprites["zumbi_andar"].get_width()*5, self.sprites["zumbi_andar"].get_height()*5))
        }
        self.personagem = Personagens(self.assets['parado'], 7,self.tela)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.fps_monitor = FPS()
        self.cooldown = 250
        self.ultimo_update = pygame.time.get_ticks()

        pygame.mouse.set_visible(False)
        self.mira = pygame.transform.scale(self.assets["mira"], (27, 27))

        self.animacao_tiro = False
        self.animacao_repetir = False

        self.cronometro = Cronometro(1, self.assets["fonte"])

        self.ultima_geracao = pygame.time.get_ticks()
        self.intervalo_geracao = 4000 # 4000 porque seriam 3000 milisegundos

    def trata_eventos(self, eventos):
        agora = pygame.time.get_ticks()
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                destino_x, destino_y = pygame.mouse.get_pos()
                if (destino_x >= self.personagem.rect.centerx) and destino_y >= 400:
                    if agora - self.ultimo_update > self.cooldown:
                        # if not self.animacao_tiro:
                        self.personagem.trocar_animacao(self.assets['tiro'], 4)
                        self.animacao_tiro = True

                        x = self.personagem.rect.centerx
                        y = self.personagem.rect.centery

                        destino_x, destino_y = pygame.mouse.get_pos()
                        novo_tiro = Tiro(x + 20, y + 130, destino_x, destino_y, self.assets['bala'])
                        self.tiros.add(novo_tiro)

                        self.animacao_repetir = False
                        self.ultimo_update = agora
                    else:
                        self.personagem.trocar_animacao(self.assets["parado"], 7)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  
                    self.moving_left = True
                    self.moving_right = False
                    self.personagem.trocar_animacao(self.assets['walk_inverted'], 7)
                if evento.key == pygame.K_d: 
                    self.moving_right = True
                    self.moving_left = False
                    self.personagem.trocar_animacao(self.assets["walk"], 7)
                if evento.key == pygame.K_w: 
                    self.moving_up = True
                if evento.key == pygame.K_s:  
                    self.moving_down = True
            # if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            #         self.animacao_repetir = False  # Para de repetir quando a tecla for solta
            #         # self.ultima_update = agora
            if evento.type == pygame.KEYUP:
                # if agora - self.ultimo_update > self.cooldown:
                        
                if evento.key == pygame.K_a:
                    self.moving_left = False
                    if not self.moving_right:
                        self.personagem.trocar_animacao(self.assets["parado"], 7)
                if evento.key == pygame.K_d:
                    self.moving_right = False
                    if not self.moving_left:
                        self.personagem.trocar_animacao(self.assets["parado"], 7)
                if evento.key == pygame.K_w:
                    self.moving_up = False
                if evento.key == pygame.K_s:
                    self.moving_down = False

    def atualiza(self):
        self.cronometro.atualizar()
        if self.cronometro.tempo_acabou:
            self.jogo.trocar_tela(TelaGameOver(self.jogo,self.tela))

        agora = pygame.time.get_ticks()
        if agora - self.ultima_geracao > self.intervalo_geracao:
            self.ultima_geracao = agora
            novo_zumbi = Zumbies(self.assets["zombie_walk"], 10, self.tela)
            self.zumbies.add(novo_zumbi)
    
        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, False,pygame.sprite.collide_mask)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                zumbi.vidas -= 1
                if zumbi.vidas <= 0:
                    impacto = Impacto(zumbi.rect.center,self.assets["zumbi_morto"],5)
                    self.impactos.add(impacto) 
                    self.zumbies.remove(zumbi)
                    self.tiros.remove(tiro)
                else:
                    if zumbi.estado != 'ferido': #'assets/img/Zombie_1/Hurt_invertida.png'
                        zumbi.trocar_animacao(self.assets["zumbi_ferido"], 4, dano=True, novo_estado='ferido')

        # Atualizar as animações do personagem e verificar o término da animação de tiro
        if self.animacao_tiro:
                if self.personagem.frame_atual == len(self.personagem.frames) - 1:  # Último quadro
                    if self.animacao_repetir:  # Se a tecla ainda estiver pressionada, reinicia
                        self.personagem.trocar_animacao(self.assets['tiro'], 4)  # Reinicia animação
                        x = self.personagem.rect.centerx
                        y = self.personagem.rect.centery
                        destino_x, destino_y = pygame.mouse.get_pos()
                        novo_tiro = Tiro(x+100,y+140, destino_x, destino_y, self.assets['bala'])
                        self.tiros.add(novo_tiro)
                    else:
                        self.animacao_tiro = False  # Conclui a animação de tiro
                        self.personagem.trocar_animacao(self.assets['parado'], 7)  # Retorna à animação parado

        self.personagem.update()
        self.zumbies.update()
        self.tiros.update()
        self.impactos.update()

        # Verificar movimento horizontal
        if self.moving_left or self.moving_right:
            if self.moving_left:
                self.personagem.mover(30, 0)
            if self.moving_right:
                self.personagem.mover(-30, 0)

        # Verificar movimento vertical
        if self.moving_up or self.moving_down:
            if self.moving_up and self.personagem.rect.y > 35:
                self.personagem.mover(0, -30)
            if self.moving_down and self.personagem.rect.y + self.personagem.rect.height < self.tela["altura"]:
                self.personagem.mover(0, 30)

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.assets["img_fundo"], (0, 0))
        self.fps_monitor.calcula_fps()
        texto_fps = self.assets["fonte"].render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        texto_fps = pygame.transform.scale(texto_fps, (150, 30))
        janela.blit(texto_fps, ((self.tela["largura"]- 150), (self.tela["altura"] - 30)))
        
        self.cronometro.desenha(janela, (self.tela["largura"] // 2) - 50, 10)  # Desenha o cronômetro no canto superior esquerdo
        


        mouse_x, mouse_y = pygame.mouse.get_pos()
        mira_rect = self.mira.get_rect(center=(mouse_x, mouse_y))
        janela.blit(self.mira, mira_rect)

        self.personagem.desenha(janela)
        self.zumbies.draw(janela)
        self.tiros.draw(janela)
        self.impactos.draw(janela)
        pygame.display.update()


class Jogo:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.tela = {
            "largura": info.current_w,
            "altura": info.current_h,
        }
        self.janela = pygame.display.set_mode((self.tela["largura"], self.tela["altura"]), pygame.FULLSCREEN)
        pygame.display.set_caption("Zombie Attack")
        self.tela_atual = TelaInicial(self,self.tela)

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
    
