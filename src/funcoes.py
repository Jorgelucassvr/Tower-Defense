import pygame

from src.config import (
    ALTURA_TELA,
    AZUL,
    BOTAO_REINICIAR,
    BRANCO,
    CAMINHO_ESTRADA,
    MARROM,
    PRETO,
    VERDE,
    VERMELHO,
)


def desenhar_mapa(tela):
    # Preenche a tela com a cor do gramado.
    tela.fill(VERDE)

    # Desenha cada trecho da estrada.
    for trecho in CAMINHO_ESTRADA:
        pygame.draw.rect(tela, MARROM, trecho, border_radius=18)

    # Marca a entrada e a saida do percurso.
    pygame.draw.circle(tela, AZUL, (35, 345), 22)
    pygame.draw.circle(tela, VERMELHO, (1160, 395), 22)


def desenhar_interface(tela, fonte, inimigo_ativo):
    # Desenha um botao clicavel para reiniciar o inimigo.
    pygame.draw.rect(tela, BRANCO, BOTAO_REINICIAR, border_radius=12)
    pygame.draw.rect(tela, PRETO, BOTAO_REINICIAR, width=2, border_radius=12)

    texto_botao = fonte.render("Reiniciar inimigo", True, PRETO)
    tela.blit(texto_botao, texto_botao.get_rect(center=BOTAO_REINICIAR.center))

    # Exibe uma instrucao curta para o jogador entender a interacao.
    texto_instrucao = fonte.render("Clique no botao para recomecar a rota.", True, PRETO)
    tela.blit(texto_instrucao, (40, 35))

    # Mostra o status do inimigo para facilitar os testes.
    status = "Em movimento" if inimigo_ativo else "Chegou ao fim"
    texto_status = fonte.render(f"Status do inimigo: {status}", True, PRETO)
    tela.blit(texto_status, (40, ALTURA_TELA - 45))
