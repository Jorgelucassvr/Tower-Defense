import pygame

from src.config import (
    ALTURA_TELA,
    AMARELO,
    AZUL,
    BRANCO,
    BOTOES_PERSONAGENS,
    CAMINHO_ESTRADA,
    CINZA,
    MARROM,
    PRETO,
    TIPOS_PERSONAGENS,
    VERDE,
    VERMELHO,
)


def calcular_pontos(pontos_atual, pontos_ganhos):
    # Soma pontos ou moedas ao valor atual.
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    # Reduz a vida do jogador quando um inimigo chega ao fim.
    return vida_atual - dano


def jogador_perdeu(vidas):
    # Verifica se a condicao de derrota foi atingida.
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    # Mantem um valor dentro de um intervalo permitido.
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    # Testa colisao entre dois retangulos do Pygame.
    return retangulo_1.colliderect(retangulo_2)


def posicao_no_caminho(posicao):
    # Retorna True quando o mouse esta sobre a estrada.
    return any(trecho.collidepoint(posicao) for trecho in CAMINHO_ESTRADA)


def desenhar_mapa(tela):
    # Preenche a tela com a cor do gramado.
    tela.fill(VERDE)

    # Desenha cada trecho da estrada.
    for trecho in CAMINHO_ESTRADA:
        pygame.draw.rect(tela, MARROM, trecho, border_radius=18)

    # Marca a entrada e a saida do percurso.
    pygame.draw.circle(tela, AZUL, (35, 345), 22)
    pygame.draw.circle(tela, VERMELHO, (1160, 395), 22)


def desenhar_interface(tela, fonte, estado):
    # Mostra as informacoes principais do jogador.
    texto_hud = (
        f"Moedas: {estado['moedas']}  "
        f"Vidas: {estado['vidas']}  "
        f"Eliminacoes: {estado['eliminacoes']}  "
        f"Onda: {estado['spawnados']}/5  "
        f"Recorde: {estado['recorde']}"
    )
    tela.blit(fonte.render(texto_hud, True, PRETO), (30, 25))

    # Desenha os botoes para escolher guerreiro ou arqueiro.
    for tipo, botao in BOTOES_PERSONAGENS.items():
        selecionado = estado["selecionado"] == tipo
        cor_fundo = AMARELO if selecionado else BRANCO
        dados = TIPOS_PERSONAGENS[tipo]

        pygame.draw.rect(tela, cor_fundo, botao, border_radius=10)
        pygame.draw.rect(tela, PRETO, botao, width=2, border_radius=10)

        texto = fonte.render(f"{dados['nome']} ${dados['custo']}", True, PRETO)
        tela.blit(texto, texto.get_rect(center=botao.center))

    # Explica a acao atual sem precisar de menu extra.
    texto_acao = fonte.render("Clique em uma unidade e depois fora da estrada.", True, PRETO)
    tela.blit(texto_acao, (30, ALTURA_TELA - 70))

    if estado["mensagem"]:
        tela.blit(fonte.render(estado["mensagem"], True, PRETO), (30, ALTURA_TELA - 35))


def desenhar_fim_de_jogo(tela, fonte_grande, estado):
    # Mostra a mensagem final quando o jogador ganha ou perde.
    if estado["status"] == "jogando":
        return

    texto = "VITORIA!" if estado["status"] == "vitoria" else "DERROTA!"
    texto_renderizado = fonte_grande.render(texto, True, PRETO)
    fundo = pygame.Rect(0, 0, 420, 120)
    fundo.center = (600, 120)

    pygame.draw.rect(tela, CINZA, fundo, border_radius=14)
    pygame.draw.rect(tela, PRETO, fundo, width=3, border_radius=14)
    tela.blit(texto_renderizado, texto_renderizado.get_rect(center=fundo.center))
