# Configuracoes centrais do jogo (tela, cores, regras e caminhos de arquivos).
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
VERDE_SLIME = (57, 190, 88)
MARROM = (163, 120, 72)
AZUL = (70, 130, 255)
VERMELHO = (220, 70, 70)
AMARELO = (240, 198, 73)
ROXO = (128, 96, 190)
LARANJA = (226, 131, 59)
VERDE_ESCURO = (30, 110, 50)

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

# Regras principais do prototipo.
MOEDAS_INICIAIS = 150
VIDAS_INICIAIS = 3
MOEDAS_POR_ELIMINACAO = 10
TOTAL_INIMIGOS_ONDA = 5
INTERVALO_SPAWN = 1.0

# Dados dos dois personagens que o jogador pode colocar no mapa.
TIPOS_PERSONAGENS = {
    "guerreiro": {
        "nome": "Guerreiro",
        "custo": 50,
        "alcance": 130,
        "dano": 18,
        "tempo_ataque": 0.75,
    },
    "arqueiro": {
        "nome": "Arqueiro",
        "custo": 100,
        "alcance": 210,
        "dano": 12,
        "tempo_ataque": 0.45,
    },
}

# Botoes de selecao dos personagens.
BOTOES_PERSONAGENS = {
    "guerreiro": pygame.Rect(910, 25, 125, 50),
    "arqueiro": pygame.Rect(1050, 25, 125, 50),
}
