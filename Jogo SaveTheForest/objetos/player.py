import pygame, os
from elementos_mapa import Relogio


class Bola(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.diretorio = r'imagens_animacoes/CANHAO/BOLA_CANHAO/'
        self.listagem = os.listdir(self.diretorio)
        self.aparece = [
            pygame.image.load(self.diretorio + imagem).convert_alpha() for imagem in self.listagem[0:]
        ]

        self.em_movimento = False
        self.atual = 0
        self.image = self.aparece[self.atual]
        self.rect = self.image.get_rect()

    def update(self):

        if self.atual >= len(self.aparece) - 1:
            self.atual = 0
        self.atual += 0.2
        if self.em_movimento:
            self.image = self.aparece[int(self.atual)]
        else:
            self.image = self.aparece[0]
        self.rect.y -= 2


class Canhao(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.diretorio = r'imagens_animacoes/CANHAO/CANHAO_MOVENDO/'
        self.listagem = os.listdir(self.diretorio)
        self.aparece = [
            pygame.image.load(self.diretorio + imagem).convert_alpha() for imagem in self.listagem[0:]
        ]

        self.em_movimento = False
        self.atual = 0
        self.image = self.aparece[self.atual]
        self.rect = self.image.get_rect()
        self.rect.center = (500, 340)
        self.bola = pygame.sprite.Group()

    def update(self, teclou_espaco):
        self.mover_canhao(teclou_espaco)

        if self.atual >= len(self.aparece) - 1:
            self.atual = 0

        self.atual += 0.2
        if self.em_movimento:
            self.image = self.aparece[int(self.atual)]
        else:
            self.image = self.aparece[0]

    def mover_canhao(self, teclou_espaco, relogio=Relogio()):
        tecla = pygame.key.get_pressed()

        for bolas in self.bola:
            if bolas.rect.y <= -100:
                self.bola.remove(bolas)
            bolas.update()

        if tecla[pygame.K_d]:
            if self.rect.right >= 853:
                self.rect.centerx -= 3
                self.em_movimento = False
            else:
                self.em_movimento = True
            self.rect.centerx += 3

        elif tecla[pygame.K_a]:
            if self.rect.left <= 0:
                self.rect.centerx += 3
                self.em_movimento = False
            else:
                self.em_movimento = True
            self.rect.centerx -= 3

        elif teclou_espaco:
            if not relogio.cronometro(0.4) > 0:
                bola = Bola(self.bola)
                bola.rect.center = self.rect.center
                bola.rect.y -= 30
                relogio.restartar_tempo()

        else:
            self.em_movimento = False
