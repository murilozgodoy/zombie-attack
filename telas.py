import pygame,pygame.freetype
from personagens import Personagens, Zumbies, Tiro, Impacto
from Aerea import AmeacaAerea
from explosao import ExplosaoAerea
from ranking import add_score, load_ranking
from utilidades import Cronometro, FPS
import random

class Tela:
    def trata_eventos(self, eventos):
        pass
    def atualiza(self):
        pass
    def desenha(self, janela):
        pass

class TelaNome(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela

        # configurações de fonte e cores
        self.font = pygame.font.Font("assets/font/PressStart2P.ttf", 32)
        self.prompt_surf = self.font.render("Digite seu nome:", True, (222,177,61))

        self.input_text = ""
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active   = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

        # retângulo do input (metade da largura, altura 50px)
        w, h = tela["largura"] // 2, 50
        x = (tela["largura"] - w) // 2
        y = (tela["altura"]  - h) // 2
        self.input_rect = pygame.Rect(x, y, w, h)
        self.active = False  # só digita quando clica dentro

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # ativa/desativa ao clicar no retângulo
                if self.input_rect.collidepoint(evento.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive

            if evento.type == pygame.KEYDOWN and self.active:
                if evento.key == pygame.K_RETURN:
                    # usuário confirmou o nome: guarda e segue
                    self.jogo.player_name = self.input_text.strip() or "Jogador"
                    self.jogo.trocar_tela(TelaJogo(self.jogo, self.tela))
                elif evento.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    # limita tamanho se quiser
                    if len(self.input_text) < 20:
                        self.input_text += evento.unicode

    def desenha(self, janela):
        janela.fill((0, 0, 0))

        # desenha prompt
        prompt_x = (self.tela["largura"] - self.prompt_surf.get_width()) // 2
        janela.blit(self.prompt_surf, (prompt_x, self.input_rect.y - 60))

        # renderiza o texto atual
        txt_surf = self.font.render(self.input_text, True, (255,255,255))
        # redimensiona o rect se o texto ficou maior
        width = max(self.input_rect.w, txt_surf.get_width()+10)
        self.input_rect.w = width

        # desenha caixa e texto
        pygame.draw.rect(janela, self.color, self.input_rect, 2, border_radius=5)
        janela.blit(txt_surf, (self.input_rect.x+5, self.input_rect.y+8))

        pygame.display.flip()




class TelaInicial(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.fonte = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        imagem = pygame.image.load("assets/img/Inicial.png")
        self.image = pygame.transform.scale(imagem, (tela["largura"], tela["altura"]))
        self.jogar = pygame.image.load("assets/img/Botao_jogar.png")
        self.botao_jogar_rect = pygame.Rect((tela["largura"] - 640) // 2, (tela["altura"] - 175) // 2, 570, 160)
        self.botao_instrucoes_rect = pygame.Rect((tela["largura"] - 640) // 2, (tela["altura"] + 235) // 2, 570, 160)
        

    def trata_eventos(self, eventos):
        for evento in eventos:
            if self.botao_jogar_rect.collidepoint(pygame.mouse.get_pos()):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    from telas import TelaJogo
                    self.jogo.trocar_tela(TelaNome(self.jogo, self.tela))
            if self.botao_instrucoes_rect.collidepoint(pygame.mouse.get_pos()):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    from telas import TelaInstrucoes
                    self.jogo.trocar_tela(TelaInstrucoes(self.jogo, self.tela))

    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        pygame.draw.rect(janela, (255, 255, 255), self.botao_jogar_rect)
        pygame.draw.rect(janela, (255, 0, 255), self.botao_instrucoes_rect)
        pygame.display.flip()

class TelaGameOver(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        pygame.mixer.quit()
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

class TelaInstrucoes(Tela):
    def __init__(self, jogo, tela):
        self.jogo = jogo
        self.tela = tela
        self.image = pygame.transform.scale(pygame.image.load("assets/img/fundo.png"), (self.tela["largura"], self.tela['altura']))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
                from telas import TelaInicial
                self.jogo.trocar_tela(TelaInicial(self.jogo, self.tela))
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_s: #coloquei qualquer tecla, depois mudamos para a tecla que quisermos#
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.tela))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))

   
        fonte_titulo = pygame.font.SysFont('arialblack', 36)
        fonte_texto = pygame.font.SysFont('lucidaconsole', 22)
        fonte_acao = pygame.font.SysFont('lucidaconsole', 22) 

        cor_caixa = (30, 30, 30)
        cor_texto = (220, 220, 220)
        cor_titulo = (222, 177, 61)

        instrucoes = [
            "Mire com o mouse nos zumbis e atire pressionando o botão esquerdo.",
            "Ande para os lados pressionando as teclas 'A' (esquerda) e 'D' (direita).",
            "Não deixe os zumbis invadirem sua base de proteção.",
            "Evite que os carniçais de combate se aproximem de você, já que conseguem te atacar.",
            "Sobreviva até o tempo acabar para vencer!"
        ]

        largura_caixa = 1120
        altura_caixa = 450 
        x_caixa = (self.tela["largura"] - largura_caixa) // 2
        y_caixa = (self.tela["altura"] - altura_caixa) // 2
        pygame.draw.rect(janela, cor_caixa, (x_caixa, y_caixa, largura_caixa, altura_caixa), border_radius=10)


        titulo = fonte_titulo.render("COMO JOGAR", True, cor_titulo)
        janela.blit(titulo, (x_caixa + (largura_caixa - titulo.get_width()) // 2, y_caixa + 25))

        y_texto = y_caixa + 115
        for linha in instrucoes:
            texto = fonte_texto.render(linha, True, cor_texto)
            janela.blit(texto, (x_caixa + (largura_caixa - texto.get_width()) // 2, y_texto))
            y_texto += 40

        y_texto += 45
        texto_acao = fonte_acao.render("PRESSIONE 'S' PARA TENTAR SOBREVIVER AO APOCALIPSE OU 'I' PARA VOLTAR AO INÍCIO!", True, cor_titulo)
        janela.blit(texto_acao, (x_caixa + (largura_caixa - texto_acao.get_width()) // 2, y_texto))

        pygame.display.flip()


class TelaVitoria(Tela):
    def __init__(self, jogo, tela, usuario):
        pygame.mixer.quit()
        self.jogo   = jogo
        self.tela   = tela
        self.usuario = usuario
        self.fonte  = pygame.font.Font("assets/font/PressStart2P.ttf", 30)
        self.image  = pygame.transform.scale(
            pygame.image.load("assets/img/vitoria_3.png"),
            (tela["largura"], tela['altura'])
        )

        # --- registra no ranking e obtém lista atualizada ---
        # use self.jogo.player_name como nome do jogador
        self.ranking = add_score(self.jogo.player_name, usuario["zumbies_mortos"])

        # pré-render de estatísticas
        self.zumbies_mortos = self.fonte.render(
            f'Zumbis mortos: {usuario["zumbies_mortos"]}', True, (255,255,255))
        
        self.zumbies_mortos = self.fonte.render(f'Zumbis mortos: {self.usuario["zumbies_mortos"]}', True, (255, 255, 255))
        self.zumbies_mortos = pygame.transform.scale(self.zumbies_mortos, (500, 100))
        
        self.vidas = self.fonte.render(f'Vida: {self.usuario["vida"]}', True, (255, 255, 255))
        self.vidas = pygame.transform.scale(self.vidas, (500, 100))


        self.municoes = self.fonte.render(f'Munições: {self.usuario["municoes_totais"] + self.usuario["municoes"]}', True, (255, 255, 255))
        self.municoes = pygame.transform.scale(self.municoes, (500, 100))

        self.acertos = self.fonte.render(f'% de Acertos: {self.usuario["acertos"]:.2f}', True, (255, 255, 255))
        self.acertos = pygame.transform.scale(self.acertos, (500, 100))

    def trata_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from telas import TelaJogo
                self.jogo.trocar_tela(TelaJogo(self.jogo, self.jogo.tela_atual.tela.copy()))


    def desenha(self, janela):
        janela.fill((0, 0, 0))
        janela.blit(self.image, (0, 0))
        janela.blit(self.vidas, ((self.tela["largura"] - 750), (self.tela["altura"] - 900)))
        janela.blit(self.zumbies_mortos, ((self.tela["largura"] - 750), (self.tela["altura"] - 700)))
        janela.blit(self.municoes, ((self.tela["largura"] - 750), (self.tela["altura"] - 500)))
        janela.blit(self.acertos, ((self.tela["largura"] - 750), (self.tela["altura"] - 300)))
        # Exibe o ranking (top 5)
        emoji_font = pygame.freetype.Font("C:/Windows/Fonts/seguiemj.ttf", 32)
        x_rank, y_rank = 100, 300
        emoji_font.render_to(janela, (100, 296), "🏆", fgcolor=(222,177,61))
        titulo = self.fonte.render("  Top 5 Jogadores", True, (222,177,61))
        janela.blit(titulo, (x_rank, y_rank))
        y_rank += 40

        for pos, entry in enumerate(self.ranking[:5], start=1):
            txt = self.fonte.render(
                f'{pos}. {entry["name"]}: {entry["score"]}',
                True, (255,255,255)
            )
            janela.blit(txt, (x_rank, y_rank))
            y_rank += 30

        pygame.display.flip()
        
        
class TelaJogo(Tela):
    def __init__(self, jogo,tela):
        pygame.mixer.init()
        self.jogo = jogo
        # self.zumbies_mortos = 0
        self.tela = tela
        self.zumbies = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.impactos = pygame.sprite.Group()
        self.ameacas = pygame.sprite.Group()
        self.ultimo_spawn_ameaca = pygame.time.get_ticks()
        self.intervalo_ameaca = random.randint(1000, 3000)
        # self.corredores = pygame.sprite.Group()
        self.recarregar_sound = pygame.mixer.Sound("assets/snd/recarregar.wav")
        # self.arma_vazia = pygame.mixer.Sound("assets/snd/sem_municao.wav")
        # self.arma_vazia.set_volume(1.0)
        self.tiro_sound = pygame.mixer.Sound("assets\snd\som_tiro.wav")
        self.tiro_sound.set_volume(0.07)
        self.som_ambiente = pygame.mixer.Sound("assets\snd\som_ambiente.wav")
        self.som_ambiente.set_volume(0.1)
        self.som_ambiente.play(-1)
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
            "personagem_dead": pygame.transform.scale(self.sprites["personagem_morre"],(self.sprites["personagem_morre"].get_width()*5,self.sprites["personagem_morre"].get_height()*5)),
            "pesonagem_recarregar": pygame.transform.scale(self.sprites["personagem_recarregar"],(self.sprites["personagem_recarregar"].get_width()*5,self.sprites["personagem_recarregar"].get_height()*5)),
            "zombie_walk_corredor": pygame.transform.scale(self.sprites["zumbi_andar_corredor"], (self.sprites["zumbi_andar_corredor"].get_width()*4.5, self.sprites["zumbi_andar_corredor"].get_height()*4.5)),
            "explosao_aerea": pygame.image.load("assets/img/explosao.png"),
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
        self.intervalo_geracao = 4000 # 4000 porque seriam 3000 milisegundos
        self.cooldown_gameover = 5000
        self.estado = "vivo"
        self.tempo_morte = None  # Marca quando morreu
        self.personagem_recarregando = False
        self.zumbies_atingidos = 0


        self.usuario = {
            "vida": self.personagem.vidas,
            "municoes": self.personagem.municoes,
            "municoes_totais": self.personagem.municoes_totais,
            "zumbies_mortos": self.personagem.zumbies_mortos,
            "acertos": (150-(self.personagem.municoes_totais + self.personagem.municoes))/self.zumbies_atingidos if not self.zumbies_atingidos == 0 else 0,

        }
    def trata_eventos(self, eventos):
        agora = pygame.time.get_ticks()
        if self.estado == "morto":
            return
        if self.personagem_recarregando:
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
                # Teste para tela de vitoria 
                if evento.key == pygame.K_t:
                    self.usuario["vida"] = self.personagem.vidas
                    self.usuario["municoes"] = self.personagem.municoes
                    self.usuario["municoes_totais"] = self.personagem.municoes_totais
                    self.usuario["zumbies_mortos"] = self.personagem.zumbies_mortos
                    self.usuario["acertos"] = ((150-(self.personagem.municoes_totais + self.personagem.municoes))/self.zumbies_atingidos) *100 if not self.zumbies_atingidos == 0 else 0
                    self.jogo.trocar_tela(TelaVitoria(self.jogo,self.tela,self.usuario))
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
                if self.zumbies_atingidos == 0:
                    self.usuario["acertos"] = 0
                else:
                    self.usuario["acertos"] = ((150-(self.personagem.municoes_totais + self.personagem.municoes))/self.zumbies_atingidos) *100
                self.jogo.trocar_tela(TelaVitoria(self.jogo,self.tela,self.usuario))
            else:
                self.jogo.trocar_tela(TelaGameOver(self.jogo,self.tela))

        agora = pygame.time.get_ticks()
        if agora - self.ultima_geracao > self.intervalo_geracao:
            self.ultima_geracao = agora
            novo_zumbi = Zumbies(self.assets["zombie_walk"], 10, self.tela)
            self.zumbies.add(novo_zumbi)
        # if agora - self.ultima_geracao_corredores > (self.intervalo_geracao + 1000):
        #     self.ultima_geracao_corredores = agora
        #     corredor = Zumbies_Corredores(self.assets["zombie_walk_corredor"], 8, self.tela)
        #     self.corredores.add(corredor)


        agora = pygame.time.get_ticks()
        if agora - self.ultimo_spawn_ameaca > self.intervalo_ameaca:
            self.ultimo_spawn_ameaca = agora
            self.intervalo_ameaca = random.randint(1000, 3000)
            nova_ameaca = AmeacaAerea(self.tela["largura"])
            self.ameacas.add(nova_ameaca)

    
        colisao_zumbi_personagem = pygame.sprite.groupcollide(self.grupo_pesonagem,self.zumbies,False,False)
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

        colisoes_ameaca = pygame.sprite.spritecollide(self.personagem, self.ameacas, False)
        for ameaca in colisoes_ameaca:
            self.personagem.vidas -= 15

          
            explosao = ExplosaoAerea(ameaca.rect.center, self.assets["explosao_aerea"], colunas=4, linhas=2, tamanho=(80, 80))
            self.impactos.add(explosao)

           
            ameaca.kill()

            # Se o personagem morreu
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
                self.jogo.trocar_tela(TelaGameOver(self.jogo, self.tela))
 
        colisao_tiro_zumbi = pygame.sprite.groupcollide(self.tiros, self.zumbies, True, False)
        for tiro, zumbis_atingidos in colisao_tiro_zumbi.items():
            for zumbi in zumbis_atingidos:
                zumbi.vidas -= 1
                self.zumbies_atingidos += 1
                if zumbi.vidas <= 0:
                    impacto = Impacto(zumbi.image_rect.center,self.assets["zumbi_morto"],5,"zumbi")
                    self.impactos.add(impacto) 
                    self.zumbies.remove(zumbi)
                    self.tiros.remove(tiro)
                    self.personagem.zumbies_mortos += 1
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
        self.tiros.update()
        self.impactos.update()
        self.ameacas.update()
        # self.corredores.update()
        

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
            pygame.draw.rect(janela,(0,255,0),zumbi.rect)
            zumbi.desenha(janela)
        # for corredores in self.corredores:
        #     pygame.draw.rect(janela,(0,255,0),corredores.rect)
        #     corredores.desenha(janela)
            
        if self.personagem in self.grupo_pesonagem:
            self.personagem.desenha(janela)
        # self.zumbies.draw(janela)
        self.tiros.draw(janela)
        self.ameacas.draw(janela)
        self.impactos.draw(janela)
        pygame.display.update()