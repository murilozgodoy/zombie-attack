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



class TelaJogo(Tela):
    def __init__(self, jogo,tela):
        pygame.mixer.init()
        self.jogo = jogo
        # self.zumbies_mortos = 0
        self.tela = tela
        self.escala = jogo.escalonamento
        # self.kit_medico = KitMedico(self.tela)
        self.zumbies = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.impactos = pygame.sprite.Group()
        self.ameacas = pygame.sprite.Group()
        self.ultimo_spawn_ameaca = pygame.time.get_ticks()
        self.intervalo_ameaca = random.randint(1000, 3000)
        self.corredores = pygame.sprite.Group()
        if not pygame.mixer.get_busy():
                self.som_ambiente = pygame.mixer.Sound("assets/snd/som_ambiente.wav")
                self.som_ambiente.set_volume(0.1)
                self.som_ambiente.play(-1)
        self.recarregar_sound = pygame.mixer.Sound("assets/snd/recarregar.wav")
        self.zumbi_grunindo = pygame.mixer.Sound("assets/snd/zumbiegrunindo.wav")
        self.sirene = pygame.mixer.Sound("assets/snd/sirene.wav")
        self.duracao = self.sirene.get_length()
        self.explosao = pygame.mixer.Sound("assets/snd/explosao.wav")
        self.zumbi_grunindo.set_volume(0.5)
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
            "corredor_ferido":pygame.image.load("assets/img/ZombieMan/Hurt.png"),
            "municoes":pygame.image.load("assets/img/municoes.png"),
            "vida" :pygame.image.load("assets/img/vida.png"),
        }
        # Calcula tamanho base dos sprites (5x o tamanho original)
        fator_sprite = 5
        tamanho_sprite_w = lambda img: self.escala.escalar(img.get_width() * fator_sprite)
        tamanho_sprite_h = lambda img: self.escala.escalar(img.get_height() * fator_sprite)
        
        self.assets = {
            "img_fundo": pygame.transform.scale(pygame.image.load("assets/img/Fundo.png"), (self.tela["largura"], self.tela["altura"])),
            "placa": pygame.transform.scale(pygame.image.load("assets/img/placa.png"), (self.escala.escalar(150), self.escala.escalar(150))),
            "fonte": pygame.font.Font("assets/font/PressStart2P.ttf", self.escala.escalar(24)),
            "mira": pygame.transform.scale(pygame.image.load("assets/img/mira2.png"), (self.escala.escalar(27), self.escala.escalar(27))),
            "bala": pygame.transform.scale(pygame.image.load("assets/img/bala.png"), (self.escala.escalar(20), self.escala.escalar(20))),
            "tiro": pygame.transform.scale(self.sprites["personagem_atirando"],(tamanho_sprite_w(self.sprites["personagem_atirando"]), tamanho_sprite_h(self.sprites["personagem_atirando"]))),
            "parado": pygame.transform.scale(self.sprites["personagem_parado"], (tamanho_sprite_w(self.sprites["personagem_parado"]), tamanho_sprite_h(self.sprites["personagem_parado"]))),
            "walk_inverted": pygame.transform.scale(self.sprites["personagem_andar_para_tras"], (tamanho_sprite_w(self.sprites["personagem_andar_para_tras"]), tamanho_sprite_h(self.sprites["personagem_andar_para_tras"]))),
            "walk": pygame.transform.scale(self.sprites["personagem_andar"], (tamanho_sprite_w(self.sprites["personagem_andar"]), tamanho_sprite_h(self.sprites["personagem_andar"]))),
            "zumbi_morto": pygame.transform.scale(self.sprites["zumbi_morto"], (tamanho_sprite_w(self.sprites["zumbi_morto"]), tamanho_sprite_h(self.sprites["zumbi_morto"]))),
            "zumbi_ferido": pygame.transform.scale(self.sprites["zumbi_ferido"], (tamanho_sprite_w(self.sprites["zumbi_ferido"]), tamanho_sprite_h(self.sprites["zumbi_ferido"]))),
            "zombie_walk": pygame.transform.scale(self.sprites["zumbi_andar"], (tamanho_sprite_w(self.sprites["zumbi_andar"]), tamanho_sprite_h(self.sprites["zumbi_andar"]))),
            "zombie_attack": pygame.transform.scale(self.sprites["zumbi_ataque"],(tamanho_sprite_w(self.sprites["zumbi_ataque"]), tamanho_sprite_h(self.sprites["zumbi_ataque"]))),
            "personagem_dead": pygame.transform.scale(self.sprites["personagem_morre"],(tamanho_sprite_w(self.sprites["personagem_morre"]), tamanho_sprite_h(self.sprites["personagem_morre"]))),
            "pesonagem_recarregar": pygame.transform.scale(self.sprites["personagem_recarregar"],(tamanho_sprite_w(self.sprites["personagem_recarregar"]), tamanho_sprite_h(self.sprites["personagem_recarregar"]))),
            "explosao_aerea": pygame.image.load("assets/img/explodindo.png"),
            "bomba_aerea": pygame.transform.scale(pygame.image.load("assets/img/boma_aerea.png").convert_alpha(), (self.escala.escalar(80), self.escala.escalar(75))),
            "zombie_walk_corredor": pygame.transform.scale(self.sprites["zumbi_andar_corredor"], (tamanho_sprite_w(self.sprites["zumbi_andar_corredor"]), tamanho_sprite_h(self.sprites["zumbi_andar_corredor"]))),
            "zumbi_morte_corredor": pygame.transform.scale(self.sprites["zumbi_morte_corredor"], (tamanho_sprite_w(self.sprites["zumbi_morte_corredor"]), tamanho_sprite_h(self.sprites["zumbi_morte_corredor"]))),
            "corredor_ferido": pygame.transform.scale(self.sprites["corredor_ferido"], (tamanho_sprite_w(self.sprites["corredor_ferido"]), tamanho_sprite_h(self.sprites["corredor_ferido"]))),
            "municoes": pygame.transform.scale(self.sprites["municoes"], (self.escala.escalar(50), self.escala.escalar(50))),
            "vida": pygame.transform.scale(self.sprites["vida"], (self.escala.escalar(40), self.escala.escalar(40))),
        }
        self.personagem = Personagens(self.assets['parado'], 7, self.tela, self.escala)
        self.grupo_pesonagem = pygame.sprite.GroupSingle(self.personagem)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.fps_monitor = FPS()
        self.cooldown = 250
        self.ultimo_update = pygame.time.get_ticks()
        pygame.mouse.set_visible(False)
        # Cooldown para ataque de zumbi (evita dano múltiplo)
        self.ultimo_dano_zumbi = pygame.time.get_ticks()
        self.cooldown_dano_zumbi = 1000  # 1 segundo entre ataques
        self.mira = self.assets["mira"]

        self.animacao_tiro = False
        self.animacao_repetir = False

        self.cronometro = Cronometro(2, self.assets["fonte"])

        self.ultima_geracao = pygame.time.get_ticks()
        self.ultima_geracao_corredores = pygame.time.get_ticks()
        # self.cooldown_kitmedico = random.randint(10000, 30000)
        # self.ultima_geracao_kitmedico = pygame.time.get_ticks()
        self.intervalo_geracao = 2800 # 4000 porque seriam 3000 milisegundos
        self.cooldown_gameover = 3000
        self.estado = "vivo"
        self.tempo_morte = None  # Marca quando morreu
        self.personagem_recarregando = False
        self.zumbies_atingidos = 0
        self.headshots = 0  # Contador de headshots
        self.ultimo_headshot_tempo = 0  # Para feedback visual temporário
        self.estado_geral = "normal"
        self.acionamento = None  # Inicializa variável para invasão

        self.usuario = {
            "vida": self.personagem.vidas,
            "municoes": self.personagem.municoes,
            "municoes_totais": self.personagem.municoes_totais,
            "zumbies_mortos": self.personagem.zumbies_mortos,
            "acertos": 0,
            "headshots": 0,

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
                destino_x, destino_y = pygame.mouse.get_pos()
                if self.personagem.municoes > 0:
                    if (destino_x > self.personagem.rect.centerx) and destino_y >= self.escala.escalar(400):
                        if agora - self.ultimo_update > self.cooldown:
                            self.personagem.trocar_animacao(self.assets['tiro'], 4)
                            self.animacao_tiro = True

                            x = self.personagem.rect.centerx
                            y = self.personagem.rect.centery

                            novo_tiro = Tiro(x + self.escala.escalar(50), y - self.escala.escalar(40), destino_x, destino_y, self.assets['bala'], self.escala)
                            self.tiros.add(novo_tiro)

                            self.animacao_repetir = False
                            self.ultimo_update = agora
                            self.tiro_sound.play()
                            self.personagem.municoes -= 1
                        else:
                            self.personagem.trocar_animacao(self.assets["parado"], 7)
                else:
                    # Feedback visual quando sem munições (pode adicionar som depois)
                    pass
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    # Corrigido: usar elif para evitar múltiplas execuções
                    if self.personagem.municoes_totais <= 0:
                        # Sem munições para recarregar
                        pass
                    elif self.personagem.municoes < 30:
                        # Recarrega até 30 ou até acabar as munições totais
                        diferenca = 30 - self.personagem.municoes
                        if self.personagem.municoes_totais >= diferenca:
                            self.personagem.municoes = 30
                            self.personagem.municoes_totais -= diferenca
                        else:
                            self.personagem.municoes += self.personagem.municoes_totais
                            self.personagem.municoes_totais = 0
                        self.personagem.trocar_animacao(self.assets["pesonagem_recarregar"], 13)
                        self.recarregar_sound.play()
                        self.personagem_recarregando = True
                # Teste para tela de vitoria 
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
            if evento.type == pygame.KEYUP:

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
                self.usuario["headshots"] = self.headshots
                tiros_disparados = 240 - (self.personagem.municoes_totais + self.personagem.municoes)
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
            novo_zumbi = Zumbies(self.assets["zombie_walk"], 10, self.tela, self.escala)
            self.zumbies.add(novo_zumbi)
        if agora - self.ultima_geracao_corredores > self.intervalo_geracao:
            self.ultima_geracao_corredores = agora
            corredor = Zumbies_Corredores(self.assets["zombie_walk_corredor"], 8, self.tela, self.escala)
            self.corredores.add(corredor)
        


        agora = pygame.time.get_ticks()
        if agora - self.ultimo_spawn_ameaca > self.intervalo_ameaca:
            self.ultimo_spawn_ameaca = agora
            self.intervalo_ameaca = random.randint(1000, 1600)

            nova_ameaca = AmeacaAerea(self.assets["bomba_aerea"], self.tela["largura"], self.escala)
            self.ameacas.add(nova_ameaca)


        # Colisão zumbi-personagem usando rect.colliderect para melhor precisão
        agora = pygame.time.get_ticks()
        colisao_zumbi_personagem = pygame.sprite.groupcollide(self.grupo_pesonagem, self.zumbies, False, False)
        for personagem, zumbie in colisao_zumbi_personagem.items():
            for zumbi in zumbie:
                # Verifica colisão real usando rect
                if self.personagem.rect.colliderect(zumbi.rect):
                    if zumbi.estado == 'andando':  # só inicia ataque se ainda estiver andando
                        # Verifica proximidade para iniciar ataque
                        dx = self.personagem.rect.centerx - zumbi.rect.centerx
                        dy = self.personagem.rect.centery - zumbi.rect.centery
                        distancia = math.hypot(dx, dy)
                        if distancia < self.escala.escalar(70):
                            zumbi.trocar_animacao(self.assets["zombie_attack"], 5, novo_estado='Ataque')
                            # Cooldown para evitar dano múltiplo
                            if agora - self.ultimo_dano_zumbi >= self.cooldown_dano_zumbi:
                                self.personagem.vidas -= 10
                                self.ultimo_dano_zumbi = agora
                                self.zumbi_grunindo.play()
                                if self.personagem.vidas <= 0 and self.estado != "morto":
                                    self.personagem.vidas = 0
                                    morte = Impacto(self.personagem.image_rect.center, self.assets["personagem_dead"], 4, "Personagem")
                                    self.impactos.add(morte)
                                    self.grupo_pesonagem.remove(self.personagem)
                                    self.estado = "morto"
                                    self.tempo_morte = pygame.time.get_ticks()

        # Colisão bomba-personagem melhorada
        colisoes_ameaca = pygame.sprite.spritecollide(self.personagem, self.ameacas, False)
        for ameaca in colisoes_ameaca:
            # Verifica se a bomba realmente colidiu com o personagem (não apenas se está acima)
            if self.personagem.rect.colliderect(ameaca.rect):
                if self.estado != "morto":
                    self.personagem.vidas -= 15
                    self.explosao.play()

                    offset_x = 0
                    offset_y = self.escala.escalar(37) 
                    explosao_pos = (ameaca.rect.centerx + offset_x, ameaca.rect.centery + offset_y)

                    explosao = ExplosaoAerea(explosao_pos, self.assets["explosao_aerea"], colunas=5, linhas=1, tamanho=(self.escala.escalar(80), self.escala.escalar(80)), escala=self.escala)
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
 
        # Colisão tiro-zumbi (o tiro é removido automaticamente pelo groupcollide)
        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, False)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                # Verifica se foi headshot (região superior do zumbi - aproximadamente 30% do topo)
                tiro_y = tiro.rect.centery
                zumbi_top = zumbi.rect.top
                zumbi_bottom = zumbi.rect.bottom
                regiao_cabeca = zumbi_top + (zumbi_bottom - zumbi_top) * 0.3  # 30% superior é a cabeça
                
                is_headshot = tiro_y < regiao_cabeca
                
                self.zumbies_atingidos += 1
                self.zumbi_grunindo.play()
                
                if is_headshot:
                    # Headshot mata instantaneamente
                    self.headshots += 1
                    self.ultimo_headshot_tempo = pygame.time.get_ticks()  # Para feedback visual
                    impacto = Impacto(zumbi.image_rect.center, self.assets["zumbi_morto"], 5, "zumbi")
                    self.impactos.add(impacto)
                    zumbi.kill()
                    self.personagem.zumbies_mortos += 1
                else:
                    # Tiro normal
                    zumbi.vidas -= 1
                    if zumbi.vidas <= 0:
                        impacto = Impacto(zumbi.image_rect.center, self.assets["zumbi_morto"], 5, "zumbi")
                        self.impactos.add(impacto)
                        zumbi.kill()
                        self.personagem.zumbies_mortos += 1
                    else:
                        if zumbi.estado != 'dano':
                            zumbi.trocar_animacao(self.assets["zumbi_ferido"], 4, dano=True, novo_estado='dano')


        # Colisão tiro-corredor (o tiro é removido automaticamente pelo groupcollide)
        colisao_tiro_corredor = pygame.sprite.groupcollide(self.tiros, self.corredores, True, False)
        for tiro, corredores_atingidos in colisao_tiro_corredor.items():    
            for corredor in corredores_atingidos:
                # Verifica se foi headshot (região superior do corredor - aproximadamente 30% do topo)
                tiro_y = tiro.rect.centery
                corredor_top = corredor.rect.top
                corredor_bottom = corredor.rect.bottom
                regiao_cabeca = corredor_top + (corredor_bottom - corredor_top) * 0.3  # 30% superior é a cabeça
                
                is_headshot = tiro_y < regiao_cabeca
                
                self.zumbies_atingidos += 1
                self.zumbi_grunindo.play()
                
                if is_headshot:
                    # Headshot mata instantaneamente
                    self.headshots += 1
                    self.ultimo_headshot_tempo = pygame.time.get_ticks()  # Para feedback visual
                    impacto = Impacto(corredor.image_rect.center, self.assets["zumbi_morte_corredor"], 5, "zumbi")
                    self.impactos.add(impacto) 
                    corredor.kill()
                    self.personagem.zumbies_mortos += 1
                else:
                    # Tiro normal
                    corredor.vidas -= 1
                    if corredor.vidas <= 0:
                        impacto = Impacto(corredor.image_rect.center, self.assets["zumbi_morte_corredor"], 5, "zumbi")
                        self.impactos.add(impacto) 
                        corredor.kill()
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
                        novo_tiro = Tiro(x + self.escala.escalar(50), y - self.escala.escalar(40), destino_x, destino_y, self.assets['bala'], self.escala)
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
            if zumbie.rect.x < -self.escala.escalar(150):
                if self.estado_geral == "normal" and self.estado == "vivo":
                    if not pygame.mixer.get_busy() or not self.sirene.get_num_channels():
                        self.sirene.play()
                        self.sirene.set_volume(0.5)
                        self.acionamento = pygame.time.get_ticks()
                        self.estado_geral = "invasao"
                    break  # Evita múltiplas execuções
        self.corredores.update()
        for corredores in self.corredores:
            if corredores.rect.x < -self.escala.escalar(150):
                if self.estado_geral == "normal" and self.estado == "vivo":
                    if not pygame.mixer.get_busy() or not self.sirene.get_num_channels():
                        self.sirene.play()
                        self.sirene.set_volume(0.5)
                        self.acionamento = pygame.time.get_ticks()
                        self.estado_geral = "invasao"
                    break  # Evita múltiplas execuções
        if self.estado_geral == "invasao" and self.acionamento is not None:
            agora = pygame.time.get_ticks()
            if agora - self.acionamento >= self.duracao*1000:
                from telas import TelaGameOver02
                self.jogo.trocar_tela(TelaGameOver02(self.jogo, self.tela))
        self.tiros.update()
        self.impactos.update()
        self.ameacas.update()
        

        # Verificar movimento horizontal - velocidade reduzida
        velocidade_movimento = self.escala.escalar(2)  # Velocidade reduzida
        if self.moving_left or self.moving_right:
            if self.moving_left and self.personagem.rect.left > 0:
                self.personagem.mover(velocidade_movimento, 0)
            if self.moving_right and self.personagem.rect.right < self.tela["largura"]:
                self.personagem.mover(-velocidade_movimento, 0)

        # Verificar movimento vertical - limitado à calçada (aproximadamente 80% da altura da tela)
        # O personagem não pode subir além da calçada, mas pode se mover verticalmente até lá
        limite_calcada = int(self.tela["altura"] * 0.80)  # Calçada está a 80% da altura
        if self.moving_up or self.moving_down:
            # W - mover para cima: pode mover até o limite da calçada
            # Verifica se após mover, o bottom do personagem ainda estará na ou acima da calçada
            if self.moving_up:
                novo_bottom = self.personagem.rect.bottom - velocidade_movimento
                if novo_bottom >= limite_calcada:
                    self.personagem.mover(0, -velocidade_movimento)
            # S - mover para baixo: pode mover até o fundo da tela
            if self.moving_down and self.personagem.rect.bottom < self.tela["altura"]:
                self.personagem.mover(0, velocidade_movimento)
        if self.personagem.vidas < 0:
            self.personagem.vidas = 0
    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.assets["img_fundo"], (0, 0))
        self.fps_monitor.calcula_fps()
        
        # FPS - canto inferior direito
        texto_fps = self.assets["fonte"].render(f'FPS: {self.fps_monitor.fps:.2f}', True, (255, 255, 255))
        fps_x = self.tela["largura"] - texto_fps.get_width() - self.escala.escalar(10)
        fps_y = self.tela["altura"] - texto_fps.get_height() - self.escala.escalar(10)
        janela.blit(texto_fps, (fps_x, fps_y))
        
        # Placa decorativa
        janela.blit(self.assets["placa"], (self.tela["largura"] - self.escala.escalar(1600), self.escala.escalar(400)))
        
        # Vida - canto superior direito
        vida_icono = self.assets["vida"]
        vida_texto = self.assets["fonte"].render(f'{self.personagem.vidas}', True, (255, 0, 0))
        
        # Calcular posição total (ícone + espaço + texto)
        vida_largura_total = vida_icono.get_width() + self.escala.escalar(5) + vida_texto.get_width()
        vida_x_inicio = self.tela["largura"] - vida_largura_total - self.escala.escalar(10)
        vida_y = self.escala.escalar(10)
        
        # Alinhar verticalmente: centro do ícone com centro do texto
        vida_icono_y = vida_y
        vida_texto_y = vida_y + (vida_icono.get_height() - vida_texto.get_height()) // 2
        
        janela.blit(vida_icono, (vida_x_inicio, vida_icono_y))
        janela.blit(vida_texto, (vida_x_inicio + vida_icono.get_width() + self.escala.escalar(5), vida_texto_y))

        # Cronômetro - centro superior
        self.cronometro.desenha(janela, (self.tela["largura"] // 2) - self.escala.escalar(50), self.escala.escalar(10))
        
        # Feedback visual de headshot (aparece por 1 segundo)
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_headshot_tempo < 1000:  # Mostra por 1 segundo
            fonte_headshot = pygame.font.Font("assets/font/PressStart2P.ttf", self.escala.escalar(36))
            texto_headshot = fonte_headshot.render("HEADSHOT!", True, (255, 215, 0))
            headshot_x = (self.tela["largura"] - texto_headshot.get_width()) // 2
            headshot_y = self.escala.escalar(100)
            # Fundo semi-transparente
            fundo_headshot = pygame.Surface((texto_headshot.get_width() + self.escala.escalar(20), 
                                            texto_headshot.get_height() + self.escala.escalar(10)))
            fundo_headshot.set_alpha(220)
            fundo_headshot.fill((0, 0, 0))
            janela.blit(fundo_headshot, (headshot_x - self.escala.escalar(10), headshot_y - self.escala.escalar(5)))
            janela.blit(texto_headshot, (headshot_x, headshot_y))
        
        # Mensagem de munições vazias no topo da tela
        if self.personagem.municoes == 0 and self.personagem.municoes_totais == 0:
            mensagem_sem_municao = self.assets["fonte"].render("SEM MUNICOES!", True, (255, 0, 0))
            mensagem_x = (self.tela["largura"] - mensagem_sem_municao.get_width()) // 2
            mensagem_y = self.escala.escalar(50)
            # Fundo semi-transparente para melhor visibilidade
            fundo_mensagem = pygame.Surface((mensagem_sem_municao.get_width() + self.escala.escalar(20), 
                                            mensagem_sem_municao.get_height() + self.escala.escalar(10)))
            fundo_mensagem.set_alpha(200)
            fundo_mensagem.fill((0, 0, 0))
            janela.blit(fundo_mensagem, (mensagem_x - self.escala.escalar(10), mensagem_y - self.escala.escalar(5)))
            janela.blit(mensagem_sem_municao, (mensagem_x, mensagem_y))
        elif self.personagem.municoes == 0 and self.personagem.municoes_totais > 0:
            mensagem_recarregar = self.assets["fonte"].render("PRESSIONE 'R' PARA RECARREGAR", True, (255, 200, 0))
            mensagem_x = (self.tela["largura"] - mensagem_recarregar.get_width()) // 2
            mensagem_y = self.escala.escalar(50)
            # Fundo semi-transparente para melhor visibilidade
            fundo_mensagem = pygame.Surface((mensagem_recarregar.get_width() + self.escala.escalar(20), 
                                            mensagem_recarregar.get_height() + self.escala.escalar(10)))
            fundo_mensagem.set_alpha(200)
            fundo_mensagem.fill((0, 0, 0))
            janela.blit(fundo_mensagem, (mensagem_x - self.escala.escalar(10), mensagem_y - self.escala.escalar(5)))
            janela.blit(mensagem_recarregar, (mensagem_x, mensagem_y))
        
        # Munições - abaixo da vida
        municao_icono = self.assets["municoes"]
        # Muda cor do texto se estiver sem munições
        cor_municao = (255, 0, 0) if self.personagem.municoes == 0 else (255, 255, 255)
        municao_texto = self.assets["fonte"].render(f'{self.personagem.municoes}/{self.personagem.municoes_totais}', True, cor_municao)
        
        # Calcular posição total (ícone + espaço + texto)
        municao_largura_total = municao_icono.get_width() + self.escala.escalar(5) + municao_texto.get_width()
        municao_x_inicio = self.tela["largura"] - municao_largura_total - self.escala.escalar(10)
        municao_y = vida_y + max(vida_icono.get_height(), vida_texto.get_height()) + self.escala.escalar(10)
        
        # Alinhar verticalmente: centro do ícone com centro do texto
        municao_icono_y = municao_y
        municao_texto_y = municao_y + (municao_icono.get_height() - municao_texto.get_height()) // 2
        
        janela.blit(municao_icono, (municao_x_inicio, municao_icono_y))
        janela.blit(municao_texto, (municao_x_inicio + municao_icono.get_width() + self.escala.escalar(5), municao_texto_y))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mira_rect = self.mira.get_rect(center=(mouse_x, mouse_y))
        janela.blit(self.mira, mira_rect)
        for zumbi in self.zumbies:
            zumbi.desenha(janela)
        for corredores in self.corredores:
            corredores.desenha(janela)
            
        if self.personagem in self.grupo_pesonagem:
            self.personagem.desenha(janela)
        self.tiros.draw(janela)
        self.ameacas.draw(janela)
        self.impactos.draw(janela)
        pygame.display.update()