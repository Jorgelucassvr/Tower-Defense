import pygame

from src.config import ALTURA_TELA, BOTAO_REINICIAR, FPS, LARGURA_TELA, TITULO_JOGO, WAYPOINTS
from src.funcoes import desenhar_interface, desenhar_mapa
from src.movimentaçao import Inimigo


def criar_janela():
    # Inicializa o pygame e monta a janela principal.
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    return tela


def processar_eventos(inimigo):
    # Le os eventos da janela e trata o clique no botao interativo.
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if BOTAO_REINICIAR.collidepoint(evento.pos):
                inimigo.resetar()

    return True


def atualizar_estado(inimigo, dt):
    # Atualiza apenas a movimentacao do inimigo neste prototipo inicial.
    inimigo.atualizar(dt)


def desenhar_tela(tela, fonte, inimigo):
    # Primeiro desenhamos o mapa, depois a interface, e por ultimo o inimigo.
    desenhar_mapa(tela)
    desenhar_interface(tela, fonte, inimigo.ativo)
    inimigo.desenhar(tela)
    pygame.display.flip()


def executar_jogo():
    # Esta funcao concentra o loop principal do jogo.
    tela = criar_janela()
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 32)
    inimigo = Inimigo(WAYPOINTS)

    rodando = True
    while rodando:
        # dt representa o tempo entre um frame e outro.
        dt = relogio.tick(FPS) / 1000

        rodando = processar_eventos(inimigo)
        atualizar_estado(inimigo, dt)
        desenhar_tela(tela, fonte, inimigo)

    pygame.quit()
