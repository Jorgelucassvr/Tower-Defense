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
VERDE_SUPREMO = (22, 120, 54)
MARROM = (163, 120, 72)
AZUL = (70, 130, 255)
VERMELHO = (220, 70, 70)
AMARELO = (240, 198, 73)
ROXO = (128, 96, 190)
LARANJA = (226, 131, 59)
VERDE_ESCURO = (30, 110, 50)
BARBARO_COR = (125, 82, 48)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_RANKING = "data/ranking.txt"
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

# Regras principais
# Balanceamento dificil: poucas moedas, inimigos resistentes e evolucoes caras.
MOEDAS_INICIAIS = 120
VIDAS_INICIAIS = 3
DANO_SLIME_BASE = 1
DANO_SUPREMO_BASE = 3
MOEDAS_POR_ELIMINACAO = 17
MOEDAS_POR_VIDA_PERDIDA = 17
PONTOS_POR_SLIME = 100
PONTOS_INIMIGO_SUPREMO = 500
TOTAL_ONDAS = 10
ONDAS_COM_SUPREMO = (5, 10)
INIMIGOS_POR_ONDA = 5
INTERVALO_SPAWN = 1.0
INTERVALO_ENTRE_ONDAS = 1.0
VIDA_SLIME_BASE = 85
VIDA_EXTRA_POR_ONDA = 75
VIDA_INIMIGO_SUPREMO = 1550
LIMITE_GUERREIROS = 3
LIMITE_ARQUEIROS = 2
LIMITE_BARBARO = 3
DISTANCIA_MINIMA_PERSONAGENS = 44

# INIMIGOS_POR_ONDA define a quantidade base de slimes por onda.

# Dados dos personagens que o jogador pode colocar no mapa.
TIPOS_PERSONAGENS = {
    "guerreiro": {
        "nome": "Guerreiro",
        "custo": 55,
        "alcance": 150,
        "dano": 35,
        "tempo_ataque": 0.7,
    },
    "guerreirolv2": {
        "nome": "Guerreiro supremo",
        "custo": 110,
        "alcance": 156,
        "dano": 50,
        "tempo_ataque": 0.6,
    },
    "arqueiro": {
        "nome": "Arqueiro",
        "custo": 100,
        "alcance": 210,
        "dano": 25,
        "tempo_ataque": 0.7,
    },
    "arqueirolv2": {
        "nome": "Arqueiro supremo",
        "custo": 200,
        "alcance": 265,
        "dano": 40,
        "tempo_ataque": 0.45,
    },
    "barbaro": {
        "nome": "Barbaro",
        "custo": 60,
        "alcance": 85,
        "dano": 25,
        "tempo_ataque": 1.0,
    },
    "barbarolv2": {
        "nome": "Barbaro supremo",
        "custo": 120,
        "alcance": 115,
        "dano": 37,
        "tempo_ataque": 0.85,
    },
}

# Area da loja, onde ficam os icones dos personagens.
PAINEL_PERSONAGENS = pygame.Rect(900, 15, 285, 155)

# Botoes de selecao dos personagens dentro da loja.
BOTOES_PERSONAGENS = {
    "guerreiro": pygame.Rect(915, 85, 80, 60),
    "arqueiro": pygame.Rect(1005, 85, 80, 60),
    "barbaro": pygame.Rect(1095, 85, 80, 60),
}

# Botoes mostrados quando a partida acaba.
BOTAO_PLAY = pygame.Rect(500, 330, 200, 65)
CAMPO_NOME = pygame.Rect(430, 280, 340, 42)
BOTAO_REINICIAR = pygame.Rect(430, 185, 160, 50)
BOTAO_SAIR = pygame.Rect(610, 185, 160, 50)
