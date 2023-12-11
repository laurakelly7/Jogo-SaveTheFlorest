import pygame, sys
from pygame.locals import *
from elementos_mapa import Nuvems, Arvore, Boladefogo
from player import Canhao
from objetos.vida import Vida

# -------------------  RESOLUÇÃO DA TELA DO JOGO -------------------


largura = 854
altura = 480

jogo = True
jogando = True

# ------------------- ABERTURA DO PYGAME -------------------


pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Save The Forest')


# ------------------- TELA INICIAL DO JOGO -------------------


# ------------------- MAPA -------------------

todas_as_sprites_nuvems = pygame.sprite.Group()
grupo_arvores = pygame.sprite.Group()
grupo_bola_fogo = pygame.sprite.Group()
grupo_vida = pygame.sprite.Group()
grupo_player = pygame.sprite.Group()

mapa = pygame.image.load(
    'imagens_animacoes/MAPA/mapa.png'
).convert_alpha()

mapa = pygame.transform.scale(mapa, (largura, altura))
time = pygame.time.Clock()

def gerar_fonte(tamanho):
    fonte = pygame.font.Font('times-new-roman-14.ttf', tamanho)
    return fonte

# ------------------- ABERTURA DO PYGAME -------------------

while jogo:
    vida = Vida(grupo_vida)
    canhao = Canhao(grupo_player)
    jogando = True

    while jogando:
        time.tick(60)
        time.get_time()
        teclas = pygame.key.get_pressed()

        # Tecla Espaço
        teclado_espaco = False
        restartar = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                restartar = True
                if event.key == pygame.K_SPACE:
                    teclado_espaco = True

        if vida.vida == 0:
            grupo_player.remove(grupo_player)
            grupo_bola_fogo.remove(grupo_bola_fogo)
            grupo_arvores.remove(grupo_arvores)
            todas_as_sprites_nuvems.remove(todas_as_sprites_nuvems)

            texto1 = gerar_fonte(100).render('Game Over', True, (255, 255, 255))
            rect_texto1 = texto1.get_rect()
            rect_texto1.center = (largura / 2, altura / 2 - 150)

            texto2 = gerar_fonte(30).render('Clique qualquer tecla para jogar novamente', True, (255, 255, 255))
            rect_texto2 = texto2.get_rect()
            rect_texto2.center = (largura/2, altura/2)

            if restartar:
                grupo_vida.remove(grupo_vida)
                jogando = False
            tela.blit(mapa, (0, 0))
            tela.blit(texto1, rect_texto1)
            tela.blit(texto2, rect_texto2)
            pygame.display.update()
            continue

        canhao.update(teclado_espaco)

        # Arvores
        Arvore.criar_arvores(grupo_arvores, vida)
        Boladefogo.gerar_bola_fogo(grupo_bola_fogo)
        vida.update()

        # Nuvens
        Nuvems.criar_nuvem(todas_as_sprites_nuvems)
        for nuvem in todas_as_sprites_nuvems:
            if nuvem.rect.x >= 900:
                todas_as_sprites_nuvems.remove(nuvem)

        for bola_fogo in grupo_bola_fogo:
            if bola_fogo.sumir:
                grupo_bola_fogo.remove(bola_fogo)
            elif bola_fogo.rect.y >= 300:
                bola_fogo.atingida = True

        colisao_arvore = pygame.sprite.groupcollide(
                grupo_bola_fogo, grupo_arvores, True, False, pygame.sprite.collide_mask
            )
        colisao_bola = pygame.sprite.groupcollide(
                canhao.bola, grupo_bola_fogo, True, False, pygame.sprite.collide_mask
            )

        if colisao_arvore:
            arvore = colisao_arvore.values()
            for obj in arvore:
                for item in obj:
                    item.atingida = True
        if colisao_bola:
            fogo = colisao_bola.values()
            for obj in fogo:
                for item in obj:
                    item.atingida = True

        todas_as_sprites_nuvems.update()

        # Desenhar na tela
        tela.blit(mapa, (0, 0))
        todas_as_sprites_nuvems.draw(tela)
        grupo_arvores.draw(tela), grupo_player.draw(tela)
        grupo_bola_fogo.draw(tela), canhao.bola.draw(tela)
        grupo_vida.draw(tela)
        pygame.display.update()
