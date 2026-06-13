import pygame

from src.config import (
    ALTURA_TELA,
    AMARELO,
    AZUL,
    BOTAO_REINICIAR,
    BOTAO_SAIR,
    BRANCO,
    BOTOES_PERSONAGENS,
    CAMINHO_ESTRADA,
    CINZA,
    LARANJA,
    MARROM,
    PAINEL_PERSONAGENS,
    PRETO,
    ROXO,
    TIPOS_PERSONAGENS,
    TOTAL_ONDAS,
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


def posicao_na_interface(posicao):
    # Impede colocar personagens em cima do painel da loja.
    return PAINEL_PERSONAGENS.collidepoint(posicao)


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
        f"Pontos: {estado['pontos']}  "
        f"Onda: {estado['onda_atual']}/{TOTAL_ONDAS}  "
        f"Recorde: {estado['recorde']}"
    )
    tela.blit(fonte.render(texto_hud, True, PRETO), (30, 25))

    # Desenha a area da loja, onde ficam os icones dos personagens.
    pygame.draw.rect(tela, CINZA, PAINEL_PERSONAGENS, border_radius=12)
    pygame.draw.rect(tela, PRETO, PAINEL_PERSONAGENS, width=2, border_radius=12)
    tela.blit(fonte.render("Personagens", True, PRETO), (920, 35))
    tela.blit(fonte.render("Max: 3 G / 2 A", True, PRETO), (920, 60))

    # Desenha os icones/botoes para escolher guerreiro ou arqueiro.
    for tipo, botao in BOTOES_PERSONAGENS.items():
        selecionado = estado["selecionado"] == tipo
        cor_fundo = AMARELO if selecionado else BRANCO
        dados = TIPOS_PERSONAGENS[tipo]
        centro = botao.center

        pygame.draw.rect(tela, cor_fundo, botao, border_radius=10)
        pygame.draw.rect(tela, PRETO, botao, width=2, border_radius=10)

        letra = "G" if tipo == "guerreiro" else "A"
        cor_icone = LARANJA if tipo == "guerreiro" else ROXO
        pygame.draw.circle(tela, cor_icone, (centro[0], centro[1] - 8), 15)
        pygame.draw.circle(tela, PRETO, (centro[0], centro[1] - 8), 15, 2)
        texto_letra = fonte.render(letra, True, PRETO)
        tela.blit(texto_letra, texto_letra.get_rect(center=(centro[0], centro[1] - 8)))

        texto = fonte.render(f"${dados['custo']}", True, PRETO)
        tela.blit(texto, texto.get_rect(center=(centro[0], centro[1] + 18)))

    # Explica a acao atual sem precisar de menu extra.
    texto_acao = fonte.render("Clique em uma unidade e depois fora da estrada.", True, PRETO)
    tela.blit(texto_acao, (30, ALTURA_TELA - 70))

    if estado["mensagem"]:
        tela.blit(fonte.render(estado["mensagem"], True, PRETO), (30, ALTURA_TELA - 35))

    desenhar_ranking(tela, fonte, estado["ranking"])


def desenhar_ranking(tela, fonte, ranking):
    # Mostra as melhores pontuacoes salvas no arquivo data/ranking.txt.
    x = 920
    y = 185
    tela.blit(fonte.render("Ranking", True, PRETO), (x, y))

    if not ranking:
        tela.blit(fonte.render("Sem pontuacoes", True, PRETO), (x, y + 35))
        return

    for indice, entrada in enumerate(ranking[:5], start=1):
        resultado = abreviar_resultado(entrada["resultado"])
        texto = fonte.render(
            f"{indice}. {entrada['pontos']} pts {resultado} O{entrada['ondas']}",
            True,
            PRETO,
        )
        tela.blit(texto, (x, y + 30 + indice * 28))


def abreviar_resultado(resultado):
    # Usa letras curtas para caber no painel do ranking.
    if resultado == "vitoria":
        return "V"
    if resultado == "derrota":
        return "D"
    return "-"


def desenhar_fim_de_jogo(tela, fonte_grande, estado):
    # Mostra a mensagem final quando o jogador ganha ou perde.
    if estado["status"] == "jogando":
        return

    texto = "VITORIA!" if estado["status"] == "vitoria" else "DERROTA!"
    texto_renderizado = fonte_grande.render(texto, True, PRETO)
    fundo = pygame.Rect(0, 0, 460, 230)
    fundo.center = (600, 155)

    pygame.draw.rect(tela, CINZA, fundo, border_radius=14)
    pygame.draw.rect(tela, PRETO, fundo, width=3, border_radius=14)
    tela.blit(texto_renderizado, texto_renderizado.get_rect(center=(600, 95)))

    # Depois do fim, o jogo fica aberto para reiniciar ou sair.
    desenhar_botao_fim(tela, fonte_grande, BOTAO_REINICIAR, "Reiniciar")
    desenhar_botao_fim(tela, fonte_grande, BOTAO_SAIR, "Sair")


def desenhar_botao_fim(tela, fonte_grande, botao, texto):
    # Desenha um botao simples usado na tela final.
    pygame.draw.rect(tela, BRANCO, botao, border_radius=10)
    pygame.draw.rect(tela, PRETO, botao, width=2, border_radius=10)
    fonte_botao = pygame.font.SysFont(None, 34)
    texto_renderizado = fonte_botao.render(texto, True, PRETO)
    tela.blit(texto_renderizado, texto_renderizado.get_rect(center=botao.center))
