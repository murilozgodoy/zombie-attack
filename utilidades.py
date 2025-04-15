import pygame

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