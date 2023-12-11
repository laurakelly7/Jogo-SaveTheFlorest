import pygame, os, random, time


class Relogio():
    def __init__(self):
        self.tempo_inicial = time.time()

    def restartar_tempo(self):
        self.tempo_inicial = time.time()

    def tempo_passado(self):
        return time.time() - self.tempo_inicial

    def cronometro(self, tempo_desejado: float):
        tempo_percorrido = time.time() - self.tempo_inicial
        restante = tempo_desejado - tempo_percorrido
        return restante


class Nuvems(pygame.sprite.Sprite):
   def __init__(self, diretorio, rect, *groups ):
       super().__init__(*groups)
       self.diretorio = diretorio
       self.listagem = os.listdir(self.diretorio)
       self.aparece = [
           pygame.image.load(self.diretorio + imagem).convert_alpha() for imagem in self.listagem[0:]
       ]
       self.atual = 0
       self.image = self.aparece[int(self.atual)]
       self.rect = self.image.get_rect()
       self.rect.center = rect
       self.posicao = rect

   def update(self):
       if self.atual >= len(self.aparece) - 1:
           self.atual = 0
       self.image = self.aparece[int(self.atual)]

       self.rect.x += 1
       self.atual += 0.1

   @staticmethod
   def criar_nuvem(grupo, relogio=Relogio()):
       diretorio = os.listdir('imagens_animacoes/NUVEMS/')
       escolhido = random.choice(diretorio)

       if not len(grupo) == 2:
           if not relogio.cronometro(6) > 0:
               Nuvems(
                   'imagens_animacoes/NUVEMS/' + escolhido + '/',
                   (-200, random.randint(30, 250)), grupo
               )
               relogio.restartar_tempo()


class Boladefogo(pygame.sprite.Sprite):
    def __init__(self, posicao, *groups):
        super().__init__(*groups)
        self.carregar_caindo = os.listdir('imagens_animacoes/FOGO/')
        self.carregar_colidindo = os.listdir('imagens_animacoes/COLISAO_FOGO/')

        self.listagem_caindo = [
            pygame.image.load('imagens_animacoes/FOGO/' + imagem).convert_alpha()
            for imagem in self.carregar_caindo[0:]
        ]
        self.colidindo = [
            pygame.image.load('imagens_animacoes/COLISAO_FOGO/' + imagem).convert_alpha()
            for imagem in self.carregar_colidindo[0:]
        ]

        self.atual = 0
        self.atingida = False
        self.sumir = False

        self.image = self.listagem_caindo[self.atual]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (posicao, -30)

    def update(self):

        if self.atingida:
            if self.atual >= len(self.carregar_colidindo) - 1:
                self.atual = 0
                self.sumir = True
            self.image = self.colidindo[int(self.atual)]
        else:
            if self.atual >= len(self.listagem_caindo) - 1:
                self.atual = 0
            self.image = self.listagem_caindo[int(self.atual)]
            self.rect.y += 1
        self.atual += 0.1

    @staticmethod
    def gerar_bola_fogo(grupo_bola_fogo, relogio=Relogio()):
        if not len(grupo_bola_fogo) == 3:
            if not relogio.cronometro(2) > 0:
                posicao = random.randint(40, 800)
                Boladefogo(posicao, grupo_bola_fogo)
                relogio.restartar_tempo()
        grupo_bola_fogo.update()


class Arvore(pygame.sprite.Sprite):
    def __init__(self, escolhida, *groups):
        super().__init__(*groups)
        self.diretorio1 = os.listdir(f'imagens_animacoes/ARVORES/{escolhida}/')
        self.diretorio2 = os.listdir(f'imagens_animacoes/ARVORES_PEG_FOGO/{escolhida}/')
        self.diretorio3 = os.listdir(f'imagens_animacoes/ARVORES_QUEIMADAS/{escolhida}/')

        self.listagem_normal = [
            pygame.image.load(f'imagens_animacoes/ARVORES/{escolhida}/' + imagem).convert_alpha()
            for imagem in self.diretorio1[0:]
        ]
        self.listagem_queimando = [
            pygame.image.load(f'imagens_animacoes/ARVORES_PEG_FOGO/{escolhida}/' + imagem).convert_alpha()
            for imagem in self.diretorio2[0:]
        ]
        self.listagem_quimada = [
            pygame.image.load(f'imagens_animacoes/ARVORES_QUEIMADAS/{escolhida}/' + imagem).convert_alpha()
            for imagem in self.diretorio3[0:]
        ]

        self.atual = 0
        self.image = self.listagem_normal[self.atual]
        pygame.transform.scale(self.image, (144 * 1.4, 102 * 1.4))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.atingida = False
        self.queimada = False
        self.sumir = False
        self.relogio = Relogio()

    def update(self):

        if self.atual >= len(self.diretorio1) - 1:
            self.atual = 0

        if self.queimada:
            if self.atual >= len(self.listagem_quimada) - 1:
                self.atual = 0
            self.image = self.listagem_quimada[int(self.atual)]
            if not self.relogio.cronometro(5) > 0:
                self.sumir = True
        elif self.atingida:
            self.image = self.listagem_queimando[int(self.atual)]
            if not self.relogio.cronometro(6) > 0:
                self.queimada = True
                self.relogio.restartar_tempo()
            self.atual += 0.03
        else:
            self.image = self.listagem_normal[int(self.atual)]
            self.relogio.restartar_tempo()
            self.atual += 0.01
        self.image = pygame.transform.scale(self.image, (144 * 1.4, 102 * 1.4))
        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def criar_arvores(grupo_arvores, vida):

        if not len(grupo_arvores) >= 2:
            diretorio = os.listdir('imagens_animacoes/ARVORES/')
            sorteada = random.choice(diretorio)
            posicao_arvore = random.randint(30, 800)

            if len(grupo_arvores):
                rect_arvore_existente = grupo_arvores.sprites()[0].rect.x
                while True:
                    verificacao = (rect_arvore_existente - 200) <= posicao_arvore <= (rect_arvore_existente + 200)
                    if verificacao:
                        posicao_arvore = random.randint(30, 800)
                    else:
                        break
            arvore = Arvore(sorteada, grupo_arvores)
            arvore.rect.center = (posicao_arvore, 290)
        else:
            for arvore in grupo_arvores:
                if arvore.sumir:
                    grupo_arvores.remove(arvore)
                    if vida.vida > 0:
                        vida.vida -= 1
                else:
                    arvore.update()
