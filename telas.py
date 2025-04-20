import pygame
from personagens import Personagens, Zumbies, Tiro, Impacto
from utilidades import Cronometro, FPS

class Tela:
    def trata_eventos(self, eventos):
        pass
    def atualiza(self):
        pass
    def desenha(self, janela):
        pass

class TelaInicial(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        imagem = pygame.image.load("assets/img/Inicial.png")
        self.image = pygame.transform.scale(imagem, (tela["largura"], tela["altura"]))
        self.jogar = pygame.image.load("assets/img/Botao_jogar.png")
        self.botao_jogar_rect = pygame.Rect((tela["largura"] - 475) // 2, (tela["altura"] - 135) // 2, 475, 135)

    def trata_eventos(self, eventos):
        for evento in eventos:
            if self.botao_jogar_rect.collidepoint(pygame.mouse.get_pos()):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    from telas import TelaJogo
                    self.jogo.trocar_tela(TelaJogo(self.jogo, self.tela))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        pygame.display.flip()

class TelaGameOver(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.image = pygame.transform.scale(pygame.image.load("assets/img/gameover.png"), (self.tela["largura"], self.tela['altura']))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.jogo.tela_atual.tela.copy()))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        pygame.display.flip()


class TelaVitoria(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.image = pygame.transform.scale(pygame.image.load("assets/img/vitoria.png"), (self.tela["largura"], self.tela['altura']))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.jogo.tela_atual.tela.copy()))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
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
            "personagem_morre":pygame.image.load("assets/img/Soldier_1/Dead.png"),
            "zumbi_morto":pygame.image.load("assets/img/Zombie_1/Dead.png"),
            "zumbi_ferido":pygame.image.load("assets/img/Zombie_1/Hurt_invertida.png"),
            "zumbi_andar":pygame.image.load("assets/img/Zombie_1/Walk.png"),
            "zumbi_ataque":pygame.image.load("assets/img/Zombie_1/Attack.png")
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
            "zombie_walk": pygame.transform.scale(self.sprites["zumbi_andar"], (self.sprites["zumbi_andar"].get_width()*5, self.sprites["zumbi_andar"].get_height()*5)),
            "zombie_attack": pygame.transform.scale(self.sprites["zumbi_ataque"],(self.sprites["zumbi_ataque"].get_width()*5,self.sprites["zumbi_ataque"].get_height()*5)),
            "personagem_dead": pygame.transform.scale(self.sprites["personagem_morre"],(self.sprites["personagem_morre"].get_width()*5,self.sprites["personagem_morre"].get_height()*5))
        }
        self.personagem = Personagens(self.assets['parado'], 7,self.tela)
        self.grupo_pesonagem = pygame.sprite.GroupSingle(self.personagem)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.fps_monitor = FPS()
        self.cooldown = 250
        self.ultimo_update = pygame.time.get_ticks()
        self.personagem_vida = 100
        self.x = 0
        pygame.mouse.set_visible(False)
        self.mira = pygame.transform.scale(self.assets["mira"], (27, 27))

        self.animacao_tiro = False
        self.animacao_repetir = False

        self.cronometro = Cronometro(1, self.assets["fonte"])

        self.ultima_geracao = pygame.time.get_ticks()
        self.intervalo_geracao = 4000 # 4000 porque seriam 3000 milisegundos
        self.cooldown_gameover = 5000
        self.estado = "vivo"
        self.tempo_morte = None  # Marca quando morreu

    def trata_eventos(self, eventos):
        agora = pygame.time.get_ticks()
        if self.estado == "morto":
            return
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                destino_x, destino_y = pygame.mouse.get_pos()
                if (destino_x > self.personagem.rect.centerx) and destino_y >= 400:
                    if agora - self.ultimo_update > self.cooldown:
                        # if not self.animacao_tiro:
                        self.personagem.trocar_animacao(self.assets['tiro'], 4)
                        self.animacao_tiro = True

                        x = self.personagem.rect.centerx
                        y = self.personagem.rect.centery

                        destino_x, destino_y = pygame.mouse.get_pos()
                        novo_tiro = Tiro(x +30 , y , destino_x, destino_y, self.assets['bala'])
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
            if self.estado == "vivo":
                self.jogo.trocar_tela(TelaVitoria(self.jogo,self.tela))
            else:
                self.jogo.trocar_tela(TelaGameOver(self.jogo,self.tela))

        agora = pygame.time.get_ticks()
        if agora - self.ultima_geracao > self.intervalo_geracao:
            self.ultima_geracao = agora
            novo_zumbi = Zumbies(self.assets["zombie_walk"], 10, self.tela)
            self.zumbies.add(novo_zumbi)
        colisao_zumbi_personagem = pygame.sprite.groupcollide(self.grupo_pesonagem,self.zumbies,False,False)
        if colisao_zumbi_personagem:
            for personagem, zumbie in colisao_zumbi_personagem.items():
                for zumbi in zumbie:
                    if zumbi.estado != 'Ataque':  
                        zumbi.trocar_animacao(self.assets["zombie_attack"], 5, dano=False, novo_estado='Ataque')
                        self.personagem.vidas -= 10
                        if self.personagem.vidas <= 0 and self.estado != "morto":
                            self.personagem.vidas = 0
                            morte = Impacto(self.personagem.image_rect.center, self.assets["personagem_dead"], 4, "Personagem")
                            self.impactos.add(morte)
                            self.grupo_pesonagem.remove(self.personagem)
                            self.estado = "morto"
                            self.tempo_morte = pygame.time.get_ticks()  # Marca o momento da morte
    
                            
            
        else:
            pass
        
        
        if self.estado == "morto" and self.tempo_morte is not None:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_morte > self.cooldown_gameover:
                self.jogo.trocar_tela(TelaGameOver(self.jogo, self.tela))
                
                
        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, False)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                zumbi.vidas -= 1
                if zumbi.vidas <= 0:
                    impacto = Impacto(zumbi.image_rect.center,self.assets["zumbi_morto"],5,"zumbi")
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
                        x = self.personagem.rect.x
                        y = self.personagem.rect.y
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
            if self.moving_left and self.personagem.rect.x - self.personagem.rect.width >= 0:
                self.personagem.mover(30, 0)
            if self.moving_right and self.personagem.rect.x + self.personagem.rect.width < self.tela["largura"]:
                self.personagem.mover(-30, 0)

        # Verificar movimento vertical
        if self.moving_up or self.moving_down:
            if self.moving_up and  self.personagem.rect.y - self.personagem.rect.height >= 0:
                self.personagem.mover(0, -30)
            if self.moving_down and  self.personagem.rect.y + self.personagem.rect.height < self.tela["altura"]:
                self.personagem.mover(0, 30)

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.assets["img_fundo"], (0, 0))
        self.fps_monitor.calcula_fps()
        texto_fps = self.assets["fonte"].render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        texto_fps = pygame.transform.scale(texto_fps, (150, 30))
        janela.blit(texto_fps, ((self.tela["largura"]- 150), (self.tela["altura"] - 30)))
        
        
        vida = self.assets["fonte"].render(f'  {self.personagem.vidas}', True, (255, 0,0))
        vida = pygame.transform.scale(vida, (150, 30))
        janela.blit(vida, ((self.tela["largura"]- 150), 30))
        self.cronometro.desenha(janela, (self.tela["largura"] // 2) - 50, 10)  # Desenha o cronômetro no canto superior esquerdo
        


        mouse_x, mouse_y = pygame.mouse.get_pos()
        mira_rect = self.mira.get_rect(center=(mouse_x, mouse_y))
        janela.blit(self.mira, mira_rect)
        for zumbi in self.zumbies:
            # pygame.draw.rect(janela,(0,255,0),zumbi.rect)
            zumbi.desenha(janela)
            
        if self.personagem in self.grupo_pesonagem:
            self.personagem.desenha(janela)
        # self.zumbies.draw(janela)
        self.tiros.draw(janela)
        self.impactos.draw(janela)
        pygame.display.update()