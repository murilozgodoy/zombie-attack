import pygame
from random import randint
class KitMedico:
    def __init__(self,tela):
        self.image = pygame.image.load("assets/img/kitmedico.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        y =  randint(190, 350)
        x =  randint(100, 500)
        self.rect = pygame.Rect(tela["largura"]- x, tela["altura"]-y, 100, 100)
        
