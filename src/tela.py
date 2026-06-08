import pygame

pygame.init()

LARGURA = 900
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tower Defense - Protótipo")

clock = pygame.time.Clock()
rodando = True

while rodando:
    dt = clock.tick(FPS) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((34, 139, 34))

    pygame.draw.rect(tela, (181, 136, 99), (100, 250, 700, 80))
    pygame.draw.circle(tela, (255, 0, 0), (500, 290), 20)

    pygame.display.flip()

pygame.draw
pygame.quit()