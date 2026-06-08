# Configuracoes centrais do jogo (tela, cores e caminhos de arquivos).
import pygame


# Tamanho da janela principal do prototipo.
LARGURA_TELA = 1200
ALTURA_TELA = 750
FPS = 60

TITULO_JOGO = "Tower-Defenser - Pygame"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
VERDE = (74, 140, 86)
MARROM = (163, 120, 72)
AZUL = (70, 130, 255)
VERMELHO = (220, 70, 70)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"

# Cada retangulo representa um pedaço visivel da estrada.
CAMINHO_ESTRADA = [
    pygame.Rect(0, 300, 280, 90),
    pygame.Rect(190, 300, 90, 220),
    pygame.Rect(190, 430, 420, 90),
    pygame.Rect(520, 180, 90, 340),
    pygame.Rect(520, 180, 330, 90),
    pygame.Rect(760, 180, 90, 260),
    pygame.Rect(760, 350, 440, 90),
]

# Os pontos ficam no centro da estrada para o inimigo andar alinhado.
WAYPOINTS = [
    (0, 345),
    (235, 345),
    (235, 475),
    (565, 475),
    (565, 225),
    (805, 225),
    (805, 395),
    (1200, 395),
]

# Botao simples para servir como elemento interativo da entrega.
BOTAO_REINICIAR = pygame.Rect(930, 30, 220, 60)
