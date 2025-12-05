"""
Módulo de escalonamento para compatibilidade com diferentes resoluções.
Define uma resolução base (1920x1080) e calcula fatores de escala.
"""
import pygame

class Escalonamento:
    # Resolução base de referência (Full HD)
    LARGURA_BASE = 1920
    ALTURA_BASE = 1080
    
    def __init__(self, largura_atual, altura_atual):
        """
        Inicializa o sistema de escalonamento.
        
        Args:
            largura_atual: Largura da tela atual
            altura_atual: Altura da tela atual
        """
        self.largura_atual = largura_atual
        self.altura_atual = altura_atual
        
        # Calcula fatores de escala
        self.escala_x = largura_atual / self.LARGURA_BASE
        self.escala_y = altura_atual / self.ALTURA_BASE
        
        # Usa a menor escala para manter proporções (ou pode usar média)
        # Usando a menor escala evita que elementos fiquem maiores que a tela
        self.escala = min(self.escala_x, self.escala_y)
        
        # Alternativa: usar escala uniforme baseada na largura (melhor para jogos laterais)
        # self.escala = self.escala_x
    
    def escalar(self, valor):
        """
        Escala um valor único usando o fator de escala.
        
        Args:
            valor: Valor a ser escalado
            
        Returns:
            Valor escalado
        """
        return int(valor * self.escala)
    
    def escalar_x(self, valor):
        """
        Escala um valor usando apenas o fator X.
        
        Args:
            valor: Valor a ser escalado
            
        Returns:
            Valor escalado
        """
        return int(valor * self.escala_x)
    
    def escalar_y(self, valor):
        """
        Escala um valor usando apenas o fator Y.
        
        Args:
            valor: Valor a ser escalado
            
        Returns:
            Valor escalado
        """
        return int(valor * self.escala_y)
    
    def escalar_tupla(self, tupla):
        """
        Escala uma tupla (x, y) usando os fatores de escala apropriados.
        
        Args:
            tupla: Tupla (x, y) a ser escalada
            
        Returns:
            Tupla escalada (x, y)
        """
        return (self.escalar_x(tupla[0]), self.escalar_y(tupla[1]))
    
    def escalar_rect(self, rect):
        """
        Escala um pygame.Rect.
        
        Args:
            rect: pygame.Rect ou tupla (x, y, largura, altura)
            
        Returns:
            pygame.Rect escalado
        """
        if isinstance(rect, tuple):
            x, y, w, h = rect
            return pygame.Rect(
                self.escalar_x(x),
                self.escalar_y(y),
                self.escalar_x(w),
                self.escalar_y(h)
            )
        else:
            return pygame.Rect(
                self.escalar_x(rect.x),
                self.escalar_y(rect.y),
                self.escalar_x(rect.width),
                self.escalar_y(rect.height)
            )
    
    def obter_posicao_relativa(self, x_percent, y_percent):
        """
        Obtém uma posição baseada em porcentagem da tela.
        
        Args:
            x_percent: Porcentagem horizontal (0.0 a 1.0)
            y_percent: Porcentagem vertical (0.0 a 1.0)
            
        Returns:
            Tupla (x, y) com a posição
        """
        return (
            int(self.largura_atual * x_percent),
            int(self.altura_atual * y_percent)
        )

