import pygame

class ExplosaoAerea(pygame.sprite.Sprite):
    def __init__(self, center, spritesheet, colunas, linhas, tamanho=(80, 120), escala=None):
        super().__init__()
        self.escala = escala
        if escala:
            tamanho = (escala.escalar(tamanho[0]), escala.escalar(tamanho[1]))
        self.frames = self.carregar_frames(spritesheet, colunas, linhas, tamanho)
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=center)
        self.tempo_anterior = pygame.time.get_ticks()
        self.intervalo = 80  

    def carregar_frames(self, spritesheet, colunas, linhas, tamanho):
        image = spritesheet.convert_alpha()
        largura_total, altura_total = image.get_size()
        largura_quadro = largura_total // colunas
        altura_quadro = altura_total // linhas

        frames_list = []
        for linha in range(linhas):
            for coluna in range(colunas):
                x = coluna * largura_quadro
                y = linha * altura_quadro
                frame = image.subsurface((x, y, largura_quadro, altura_quadro))
                frame_redimensionado = pygame.transform.scale(frame, tamanho)
                frames_list.append(frame_redimensionado)

        return frames_list

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_anterior > self.intervalo:
            self.tempo_anterior = agora
            self.frame_atual += 1
            if self.frame_atual < len(self.frames):
                self.image = self.frames[self.frame_atual]
            else:
                self.kill()