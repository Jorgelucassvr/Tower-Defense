import pygame

pygame.init()

LARGURA = 1200
ALTURA = 750
FPS = 60

VERDE = (74, 140, 86)
MARROM = (163, 120, 72)
AZUL = (70, 130, 255)
VERMELHO = (220, 70, 70)
CINZA = (220, 220, 220)
PRETO = (20, 20, 20)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mapa Tower Defense 1200x750")
clock = pygame.time.Clock()

def desenhar_mapa(surface):
    surface.fill(VERDE)

    # Caminho principal
    caminho = [
        pygame.Rect(0, 300, 280, 90),
        pygame.Rect(190, 300, 90, 220),
        pygame.Rect(190, 430, 420, 90),
        pygame.Rect(520, 180, 90, 340),
        pygame.Rect(520, 180, 330, 90),
        pygame.Rect(760, 180, 90, 260),
        pygame.Rect(760, 350, 440, 90),
    ]

    for trecho in caminho:
        pygame.draw.rect(surface, MARROM, trecho, border_radius=18)

    # Entrada e saída
    pygame.draw.circle(surface, AZUL, (35, 345), 22)
    pygame.draw.circle(surface, VERMELHO, (1160, 395), 22)




    # Contorno simples
    pygame.draw.rect(surface, PRETO, (0, 0, LARGURA, ALTURA), 4)

rodando = True
while rodando:
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    desenhar_mapa(tela)
    pygame.display.flip()

pygame.quit()