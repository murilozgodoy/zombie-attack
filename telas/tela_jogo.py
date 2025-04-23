import pygame, random
from .tela import Tela
from utilidades.tiro import Tiro
from utilidades.impacto import Impacto
from Personagens.Zumbies import Zumbies, Zumbies_Corredores
from Personagens.Personagem import Personagens
from Bombas.Aerea import AmeacaAerea
from Bombas.explosao import ExplosaoAerea
from ranking.ranking import add_score, load_ranking
from utilidades.cronometro import Cronometro
from utilidades.FPS import FPS
import math
# from utilidades.kit_medico import KitMedico



class TelaJogo(Tela):
    def __init__(self, jogo,tela):
        pygame.mixer.init()
        self.jogo = jogo
        # self.zumbies_mortos = 0
        self.tela = tela
        # self.kit_medico = KitMedico(self.tela)
        self.zumbies = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.impactos = pygame.sprite.Group()
        self.ameacas = pygame.sprite.Group()
        self.ultimo_spawn_ameaca = pygame.time.get_ticks()
        self.intervalo_ameaca = random.randint(1000, 3000)
        self.corredores = pygame.sprite.Group()
        self.recarregar_sound = pygame.mixer.Sound("assets/snd/recarregar.wav")
        self.zumbi_grunindo = pygame.mixer.Sound("assets/snd/zumbiegrunindo.wav")
        self.sirene = pygame.mixer.Sound("assets/snd/sirene.wav")
        self.duracao = self.sirene.get_length()
        print(self.duracao)
        self.zumbi_grunindo.set_volume(0.5)
        # self.arma_vazia = pygame.mixer.Sound("assets/snd/sem_municao.wav")
        # self.arma_vazia.set_volume(1.0)
        self.tiro_sound = pygame.mixer.Sound("assets/snd/som_tiro.wav")
        self.tiro_sound.set_volume(0.1)
        self.sprites = {
            "personagem_atirando":pygame.image.load("assets/img/Soldier_1/Shot_2.png"),
            "personagem_parado":pygame.image.load("assets/img/Idle.png"),
            "personagem_andar_para_tras":pygame.image.load("assets/img/Walk_inverted.png"),
            "personagem_recarregar":pygame.image.load("assets/img/Soldier_1/Recharge.png"),
            "personagem_andar":pygame.image.load("assets/img/Walk.png"),
            "personagem_morre":pygame.image.load("assets/img/Soldier_1/Dead.png"),
            "zumbi_morto":pygame.image.load("assets/img/Zombie_1/Dead.png"),
            "zumbi_ferido":pygame.image.load("assets/img/Zombie_1/Hurt_invertida.png"),
            "zumbi_andar":pygame.image.load("assets/img/Zombie_1/Walk.png"),
            "zumbi_ataque":pygame.image.load("assets/img/Zombie_1/Attack.png"),
            "zumbi_andar_corredor":pygame.image.load("assets/img/ZombieMan/Walk.png"),
            "zumbi_morte_corredor":pygame.image.load("assets/img/ZombieMan/Dead.png"),
            "kit_medico":pygame.image.load("assets/img/kitmedico.png"),
            "corredor_ferido":pygame.image.load("assets/img/ZombieMan/Hurt.png"),
        }
        self.assets = {
            "img_fundo": pygame.transform.scale(pygame.image.load("assets/img/Fundo.png"), (self.tela["largura"], self.tela["altura"])),
            "kit_medico": pygame.transform.scale(pygame.image.load("assets/img/kitmedico.png"), (100, 100)),
            "fonte": pygame.font.Font("assets/font/PressStart2P.ttf", 30),
            "mira": pygame.transform.scale(pygame.image.load("assets/img/mira2.png"), (27, 27)),
            "bala": pygame.transform.scale(pygame.image.load("assets/img/bala.png"), (20, 20)),
            "tiro": pygame.transform.scale(self.sprites["personagem_atirando"],(self.sprites["personagem_atirando"].get_width()*5,self.sprites["personagem_atirando"].get_height()*5)),
            "parado": pygame.transform.scale(self.sprites["personagem_parado"], (self.sprites["personagem_parado"].get_width()*5, self.sprites["personagem_parado"].get_height()*5)),
            "walk_inverted": pygame.transform.scale(self.sprites["personagem_andar_para_tras"], (self.sprites["personagem_andar_para_tras"].get_width()*5, self.sprites["personagem_andar_para_tras"].get_height()*5)),
            "walk": pygame.transform.scale(self.sprites["personagem_andar"], (self.sprites["personagem_andar"].get_width() * 5, self.sprites["personagem_andar"].get_height() * 5)),
            "zumbi_morto": pygame.transform.scale(self.sprites["zumbi_morto"], (self.sprites["zumbi_morto"].get_width()*5, self.sprites["zumbi_morto"].get_height()*5)),
            "zumbi_ferido": pygame.transform.scale(self.sprites["zumbi_ferido"], (self.sprites["zumbi_ferido"].get_width()*5, self.sprites["zumbi_ferido"].get_height()*5)),
            "zombie_walk": pygame.transform.scale(self.sprites["zumbi_andar"], (self.sprites["zumbi_andar"].get_width()*5, self.sprites["zumbi_andar"].get_height()*5)),
            "zombie_attack": pygame.transform.scale(self.sprites["zumbi_ataque"],(self.sprites["zumbi_ataque"].get_width()*5,self.sprites["zumbi_ataque"].get_height()*5)),
            "personagem_dead": pygame.transform.scale(self.sprites["personagem_morre"],(self.sprites["personagem_morre"].get_width()*5,self.sprites["personagem_morre"].get_height()*5)),
            "pesonagem_recarregar": pygame.transform.scale(self.sprites["personagem_recarregar"],(self.sprites["personagem_recarregar"].get_width()*5,self.sprites["personagem_recarregar"].get_height()*5)),
            "explosao_aerea": pygame.image.load("assets/img/explodindo.png"),
            "bomba_aerea": pygame.transform.scale(pygame.image.load("assets/img/boma_aerea.png").convert_alpha(), (80, 75)),
            "zombie_walk_corredor": pygame.transform.scale(self.sprites["zumbi_andar_corredor"], (self.sprites["zumbi_andar_corredor"].get_width()*4.5, self.sprites["zumbi_andar_corredor"].get_height()*4.5)),
            "zumbi_morte_corredor": pygame.transform.scale(self.sprites["zumbi_morte_corredor"], (self.sprites["zumbi_morte_corredor"].get_width()*4.5, self.sprites["zumbi_morte_corredor"].get_height()*4.5)),
            "corredor_ferido": pygame.transform.scale(self.sprites["corredor_ferido"], (self.sprites["corredor_ferido"].get_width()*4.5, self.sprites["corredor_ferido"].get_height()*4.5)),
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
        self.ultima_geracao_corredores = pygame.time.get_ticks()
        # self.cooldown_kitmedico = random.randint(10000, 30000)
        # self.ultima_geracao_kitmedico = pygame.time.get_ticks()
        self.intervalo_geracao = 2800 # 4000 porque seriam 3000 milisegundos
        self.cooldown_gameover = 5000
        self.estado = "vivo"
        self.tempo_morte = None  # Marca quando morreu
        self.personagem_recarregando = False
        self.zumbies_atingidos = 0
        self.estado_geral = "normal"

        self.usuario = {
            "vida": self.personagem.vidas,
            "municoes": self.personagem.municoes,
            "municoes_totais": self.personagem.municoes_totais,
            "zumbies_mortos": self.personagem.zumbies_mortos,
            "acertos": 0,

        }
    def trata_eventos(self, eventos):
        agora = pygame.time.get_ticks()
        if self.estado == "morto":
            return
        if self.personagem_recarregando:
            self.moving_left = False
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            return
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.personagem.municoes > 0:
                    destino_x, destino_y = pygame.mouse.get_pos()
                    if (destino_x > self.personagem.rect.centerx) and destino_y >= 400:
                        if agora - self.ultimo_update > self.cooldown:
                            # if not self.animacao_tiro:
                            self.personagem.trocar_animacao(self.assets['tiro'], 4)
                            self.animacao_tiro = True

                            x = self.personagem.rect.centerx
                            y = self.personagem.rect.centery

                            destino_x, destino_y = pygame.mouse.get_pos()
                            novo_tiro = Tiro(x +50 , y - 40 , destino_x, destino_y, self.assets['bala'])
                            self.tiros.add(novo_tiro)

                            self.animacao_repetir = False
                            self.ultimo_update = agora
                            self.tiro_sound.play()
                            self.personagem.municoes -= 1
                        else:
                            # if self.personagem.municoes <= 0:
                            #     self.arma_vazia.play()
                            self.personagem.trocar_animacao(self.assets["parado"], 7)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    if self.personagem.municoes <= 0 and self.personagem.municoes_totais >= 30:
                        self.personagem.municoes = 30
                        self.personagem.municoes_totais -= 30
                        self.personagem.trocar_animacao(self.assets["pesonagem_recarregar"], 13)
                        self.recarregar_sound.play()
                        self.personagem_recarregando = True
                    if 0 < self.personagem.municoes < 30:
                        diferenca = 30 - self.personagem.municoes
                        self.personagem.municoes = 30
                        self.personagem.municoes_totais -= diferenca
                        self.personagem.trocar_animacao(self.assets["pesonagem_recarregar"], 13)
                        self.recarregar_sound.play()
                        self.personagem_recarregando = True
                    if self.personagem.municoes_totais < 30:
                        self.personagem.municoes = self.personagem.municoes_totais
                        self.personagem.municoes_totais = 0
                        self.personagem.trocar_animacao(self.assets["pesonagem_recarregar"], 13)
                        self.recarregar_sound.play()
                        self.personagem_recarregando = True
                # Teste para tela de vitoria 
                if evento.key == pygame.K_t:
                    self.usuario["vida"] = self.personagem.vidas
                    self.usuario["municoes"] = self.personagem.municoes
                    self.usuario["municoes_totais"] = self.personagem.municoes_totais
                    self.usuario["zumbies_mortos"] = self.personagem.zumbies_mortos
                    tiros_disparados = 150 - (self.personagem.municoes_totais + self.personagem.municoes)
                    if self.zumbies_atingidos == 0:
                        self.usuario["acertos"] = 0
                    else:
                        self.usuario["acertos"] = (self.zumbies_atingidos/tiros_disparados) *100 if tiros_disparados > 0 else 0
                    from telas import TelaVitoria
                    self.jogo.trocar_tela(TelaVitoria(self.jogo,self.tela,self.usuario))
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
                self.usuario["vida"] = self.personagem.vidas
                self.usuario["municoes"] = self.personagem.municoes
                self.usuario["municoes_totais"] = self.personagem.municoes_totais
                self.usuario["zumbies_mortos"] = self.personagem.zumbies_mortos
                tiros_disparados = 150 - (self.personagem.municoes_totais + self.personagem.municoes)
                if self.zumbies_atingidos == 0:
                    self.usuario["acertos"] = 0
                else:
                    self.usuario["acertos"] = (self.zumbies_atingidos/tiros_disparados) *100 if tiros_disparados > 0 else 0
                    from telas import TelaVitoria
                self.jogo.trocar_tela(TelaVitoria(self.jogo,self.tela,self.usuario))
            else:
                from telas import TelaGameOver
                self.jogo.trocar_tela(TelaGameOver(self.jogo,self.tela))

        agora = pygame.time.get_ticks()
        if agora - self.ultima_geracao > self.intervalo_geracao:
            self.ultima_geracao = agora
            novo_zumbi = Zumbies(self.assets["zombie_walk"], 10, self.tela)
            self.zumbies.add(novo_zumbi)
        if agora - self.ultima_geracao_corredores > self.intervalo_geracao:
            self.ultima_geracao_corredores = agora
            corredor = Zumbies_Corredores(self.assets["zombie_walk_corredor"], 8, self.tela)
            self.corredores.add(corredor)
        


        agora = pygame.time.get_ticks()
        if agora - self.ultimo_spawn_ameaca > self.intervalo_ameaca:
            self.ultimo_spawn_ameaca = agora
            self.intervalo_ameaca = random.randint(1000, 3000)

            nova_ameaca = AmeacaAerea(self.assets["bomba_aerea"], self.tela["largura"])
            self.ameacas.add(nova_ameaca)


        colisao_zumbi_personagem = pygame.sprite.groupcollide(self.grupo_pesonagem, self.zumbies, False, False)
        for personagem, zumbie in colisao_zumbi_personagem.items():
            for zumbi in zumbie:
                if zumbi.estado == 'andando':  # só inicia ataque se ainda estiver andando
                    dx = self.personagem.rect.centerx - zumbi.rect.centerx
                    dy = self.personagem.rect.centery - zumbi.rect.centery
                    distancia = math.hypot(dx, dy)
                    if distancia < 70:  # Ajuste esse valor para calibrar proximidade ideal
                            zumbi.trocar_animacao(self.assets["zombie_attack"], 5, novo_estado='Ataque')
                            self.personagem.vidas -= 10
                            self.zumbi_grunindo.play()
                            if self.personagem.vidas <= 0 and self.estado != "morto":
                                self.personagem.vidas = 0
                                morte = Impacto(self.personagem.image_rect.center, self.assets["personagem_dead"], 4, "Personagem")
                                self.impactos.add(morte)
                                self.grupo_pesonagem.remove(self.personagem)
                                self.estado = "morto"
                                self.tempo_morte = pygame.time.get_ticks()

        colisoes_ameaca = pygame.sprite.spritecollide(self.personagem, self.ameacas, False)
        for ameaca in colisoes_ameaca:
            if ameaca.rect.bottom <= self.personagem.rect.centery:
                self.personagem.vidas -= 15

    
                offset_x = 0
                offset_y = 37 
                explosao_pos = (ameaca.rect.centerx + offset_x, ameaca.rect.centery + offset_y)

                explosao = ExplosaoAerea(explosao_pos, self.assets["explosao_aerea"], colunas=5, linhas=1, tamanho=(80, 80))
                self.impactos.add(explosao)

                ameaca.kill()

                if self.personagem.vidas <= 0 and self.estado != "morto":
                    self.personagem.vidas = 0
                    morte = Impacto(self.personagem.image_rect.center, self.assets["personagem_dead"], 4, "Personagem")
                    self.impactos.add(morte)
                    self.grupo_pesonagem.remove(self.personagem)
                    self.estado = "morto"
                    self.tempo_morte = pygame.time.get_ticks()
    
        if self.estado == "morto" and self.tempo_morte is not None:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_morte > self.cooldown_gameover:
                from telas import TelaGameOver
                self.jogo.trocar_tela(TelaGameOver(self.jogo, self.tela))
 
        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, False)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                zumbi.vidas -= 1
                self.zumbies_atingidos += 1
                self.zumbi_grunindo.play()
                if zumbi.vidas <= 0:
                    impacto = Impacto(zumbi.image_rect.center, self.assets["zumbi_morto"], 5, "zumbi")
                    self.impactos.add(impacto)
                    self.zumbies.remove(zumbi)
                    self.tiros.remove(tiro)
                    self.personagem.zumbies_mortos += 1
                else:
                    if zumbi.estado != 'dano':
                        zumbi.trocar_animacao(self.assets["zumbi_ferido"], 4, dano=True, novo_estado='dano')


        colisao_tiro_corredor = pygame.sprite.groupcollide(self.tiros, self.corredores, True, False)
        for tiro, corredores_atingidos in colisao_tiro_corredor.items():    
            for corredor in corredores_atingidos:
                corredor.vidas -= 1
                self.zumbies_atingidos += 1
                self.zumbi_grunindo.play()
                if corredor.vidas <= 0:
                    impacto = Impacto(corredor.image_rect.center,self.assets["zumbi_morte_corredor"],5,"zumbi")
                    self.impactos.add(impacto) 
                    self.corredores.remove(corredor)
                    self.tiros.remove(tiro)
                    self.personagem.zumbies_mortos += 1
                else:
                    if corredor.estado != 'dano':
                        corredor.trocar_animacao(self.assets["corredor_ferido"], 3, novo_estado='dano')
        # Atualizar as animações do personagem e verificar o término da animação de tiro
        if self.animacao_tiro:
                if self.personagem.frame_atual == len(self.personagem.frames) - 1:  # Último quadro
                    if self.animacao_repetir:  # Se a tecla ainda estiver pressionada, reinicia
                        self.personagem.trocar_animacao(self.assets['tiro'], 4)  # Reinicia animação
                        x = self.personagem.rect.x
                        y = self.personagem.rect.y
                        destino_x, destino_y = pygame.mouse.get_pos()
                        novo_tiro = Tiro(x +50 , y - 40 , destino_x, destino_y, self.assets['bala'])
                        self.tiros.add(novo_tiro)
                    else:
                        self.animacao_tiro = False  # Conclui a animação de tiro
                        self.personagem.trocar_animacao(self.assets['parado'], 7)  # Retorna à animação parado

        self.personagem.update()
        if self.personagem_recarregando:
            if self.personagem.frame_atual == len(self.personagem.frames) - 1:
                self.personagem_recarregando = False
                self.personagem.trocar_animacao(self.assets["parado"], 7)
        self.zumbies.update()
        for zumbie in self.zumbies:
            if zumbie.rect.x < -150:
                if self.estado_geral == "normal":
                    self.sirene.play()
                    self.sirene.set_volume(0.5)
                    self.acionamento = pygame.time.get_ticks()
                    self.estado_geral = "invasao"
        self.corredores.update()
        for corredores in self.corredores:
            if corredores.rect.x < -150:
                if self.estado_geral == "normal":
                    self.sirene.play()
                    self.sirene.set_volume(0.5)
                    self.acionamento = pygame.time.get_ticks()
                    self.estado_geral = "invasao"
        if self.estado_geral == "invasao" and self.acionamento is not None:
            agora = pygame.time.get_ticks()
            if agora - self.acionamento >= self.duracao*1000:
                from telas import TelaGameOver02
                self.jogo.trocar_tela(TelaGameOver02(self.jogo, self.tela))
        self.tiros.update()
        self.impactos.update()
        self.ameacas.update()
        

        # Verificar movimento horizontal
        if self.moving_left or self.moving_right:
            if self.moving_left and self.personagem.rect.x - self.personagem.rect.width >= 0:
                self.personagem.mover(40, 0)
            if self.moving_right and self.personagem.rect.x + self.personagem.rect.width < self.tela["largura"]:
                self.personagem.mover(-40, 0)

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
        # ## Kit medico
        # janela.blit(self.kit_medico.image, self.kit_medico.rect)
        # pygame.draw.rect(janela, (255, 0, 0), self.kit_medico.rect, 2)  # Desenha a hitbox para depuração
        
        vida = self.assets["fonte"].render(f'   {self.personagem.vidas}', True, (255, 0,0))
        vida = pygame.transform.scale(vida, (150, 30))
        janela.blit(vida, ((self.tela["largura"]- 150), 30))
        self.cronometro.desenha(janela, (self.tela["largura"] // 2) - 50, 10)  # Desenha o cronômetro no canto superior esquerdo
        
        municao = self.assets["fonte"].render(f'  {self.personagem.municoes}/{self.personagem.municoes_totais}', True, (255,255,255))
        municao = pygame.transform.scale(municao, (150, 30))
        janela.blit(municao, ((self.tela["largura"]- 150), 80))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mira_rect = self.mira.get_rect(center=(mouse_x, mouse_y))
        janela.blit(self.mira, mira_rect)
        for zumbi in self.zumbies:
            zumbi.desenha(janela)
        for corredores in self.corredores:
            # pygame.draw.rect(janela,(0,255,0),corredores.rect)
            corredores.desenha(janela)
            
        if self.personagem in self.grupo_pesonagem:
            self.personagem.desenha(janela)
        # self.zumbies.draw(janela)
        self.tiros.draw(janela)
        self.ameacas.draw(janela)
        self.impactos.draw(janela)
        pygame.display.update()