import pygame, os


class Vida(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.diretorio = os.listdir('imagens_animacoes/VIDA/VIDA_PERDENDO/')
        self.listagem = [
            pygame.image.load('imagens_animacoes/VIDA/VIDA_PERDENDO/' + imagem).convert_alpha()
            for imagem in self.diretorio[0:]
        ]
        self.image = self.listagem[0]
        self.image = pygame.transform.smoothscale(self.image, (180/2, 78/2))
        self.rect = self.image.get_rect()
        self.rect.center = (800, 20)
        self.vida = 2
        self.atual = 0

    def update(self):
        if self.vida:
            if self.vida == 1:
                if self.atual >= 4:
                    self.atual = 4
                else:
                    self.atual += 0.05
            else:
                self.atual = 0
        else:
            if self.atual >= 8:
                self.atual = 8
            else:
                self.atual += 0.05
        self.image = self.listagem[int(self.atual)]
        self.image = pygame.transform.smoothscale(self.image, (180 / 2, 78 / 2))
