import pygame

from src.config import (
    BOTOES_PERSONAGENS,
    CAMINHO_RECORDE,
    FPS,
    INTERVALO_SPAWN,
    ALTURA_TELA,
    LARGURA_TELA,
    MOEDAS_INICIAIS,
    MOEDAS_POR_ELIMINACAO,
    TIPOS_PERSONAGENS,
    TITULO_JOGO,
    TOTAL_INIMIGOS_ONDA,
    VIDAS_INICIAIS,
    WAYPOINTS,
)
from src.dados import carregar_recorde, salvar_recorde
from src.funcoes import desenhar_fim_de_jogo, desenhar_interface, desenhar_mapa, jogador_perdeu, posicao_no_caminho
from src.movimentaçao import Inimigo, Personagem


def criar_janela():
    # Inicializa o pygame e monta a janela principal.
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    return tela


def criar_estado_inicial():
    # Cria um dicionario com as informacoes principais da partida.
    return {
        "moedas": MOEDAS_INICIAIS,
        "vidas": VIDAS_INICIAIS,
        "eliminacoes": 0,
        "recorde": carregar_recorde(CAMINHO_RECORDE),
        "selecionado": "guerreiro",
        "mensagem": "Escolha uma unidade e coloque fora da estrada.",
        "status": "jogando",
        "spawnados": 0,
        "tempo_spawn": 0,
        "recorde_salvo": False,
    }


def processar_eventos(estado, personagens):
    # Le eventos do mouse para escolher e posicionar personagens.
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado["status"] != "jogando":
                continue

            for tipo, botao in BOTOES_PERSONAGENS.items():
                if botao.collidepoint(evento.pos):
                    estado["selecionado"] = tipo
                    estado["mensagem"] = f"{TIPOS_PERSONAGENS[tipo]['nome']} selecionado."
                    break
            else:
                colocar_personagem(evento.pos, estado, personagens)

    return True


def colocar_personagem(posicao, estado, personagens):
    # Tenta colocar o guerreiro ou arqueiro no mapa.
    tipo = estado["selecionado"]
    custo = TIPOS_PERSONAGENS[tipo]["custo"]

    if posicao_no_caminho(posicao):
        estado["mensagem"] = "Nao pode colocar personagem no caminho."
        return

    if estado["moedas"] < custo:
        estado["mensagem"] = "Moedas insuficientes."
        return

    personagens.append(Personagem(tipo, posicao))
    estado["moedas"] -= custo
    estado["mensagem"] = f"{TIPOS_PERSONAGENS[tipo]['nome']} colocado."


def gerar_inimigos(estado, inimigos, dt):
    # Cria uma unica onda com 5 slimes, um por vez.
    if estado["spawnados"] >= TOTAL_INIMIGOS_ONDA:
        return

    estado["tempo_spawn"] += dt
    if estado["tempo_spawn"] >= INTERVALO_SPAWN:
        inimigos.append(Inimigo(WAYPOINTS))
        estado["spawnados"] += 1
        estado["tempo_spawn"] = 0


def atualizar_inimigos(estado, inimigos, dt):
    # Move os slimes e aplica dano ao jogador quando chegam ao fim.
    for inimigo in inimigos[:]:
        inimigo.atualizar(dt)

        if not inimigo.ativo:
            if inimigo.chegou_ao_fim:
                estado["vidas"] -= 1
                estado["mensagem"] = "Um slime chegou ao final!"
            elif inimigo.vida <= 0:
                estado["moedas"] += MOEDAS_POR_ELIMINACAO
                estado["eliminacoes"] += 1
                estado["mensagem"] = f"+{MOEDAS_POR_ELIMINACAO} moedas por eliminacao."

            inimigos.remove(inimigo)


def atualizar_personagens(personagens, inimigos, dt):
    # Atualiza o ataque automatico de cada personagem colocado.
    for personagem in personagens:
        personagem.atualizar(inimigos, dt)


def verificar_fim_de_jogo(estado, inimigos):
    # Define vitoria ou derrota e salva o recorde quando a partida termina.
    if estado["status"] != "jogando":
        return

    if jogador_perdeu(estado["vidas"]):
        estado["status"] = "derrota"
        estado["mensagem"] = "Fim de jogo: voce perdeu todas as vidas."

    onda_acabou = estado["spawnados"] == TOTAL_INIMIGOS_ONDA and len(inimigos) == 0
    if onda_acabou and estado["vidas"] > 0:
        estado["status"] = "vitoria"
        estado["mensagem"] = "Voce segurou a onda de slimes!"

    if estado["status"] != "jogando" and not estado["recorde_salvo"]:
        if estado["eliminacoes"] > estado["recorde"]:
            estado["recorde"] = estado["eliminacoes"]
            salvar_recorde(CAMINHO_RECORDE, estado["recorde"])
        estado["recorde_salvo"] = True


def atualizar_estado(estado, inimigos, personagens, dt):
    # Atualiza todas as regras principais da partida.
    if estado["status"] != "jogando":
        return

    gerar_inimigos(estado, inimigos, dt)
    atualizar_personagens(personagens, inimigos, dt)
    atualizar_inimigos(estado, inimigos, dt)
    verificar_fim_de_jogo(estado, inimigos)


def desenhar_tela(tela, fonte, fonte_grande, estado, inimigos, personagens):
    # Primeiro desenhamos o mapa, depois personagens, inimigos e interface.
    desenhar_mapa(tela)
    for personagem in personagens:
        personagem.desenhar(tela, fonte)
    for inimigo in inimigos:
        inimigo.desenhar(tela)
    desenhar_interface(tela, fonte, estado)
    desenhar_fim_de_jogo(tela, fonte_grande, estado)
    pygame.display.flip()


def executar_jogo():
    # Esta funcao concentra o loop principal do jogo.
    tela = criar_janela()
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 32)
    fonte_grande = pygame.font.SysFont(None, 72)
    estado = criar_estado_inicial()
    inimigos = []
    personagens = []

    rodando = True
    while rodando:
        # dt representa o tempo entre um frame e outro.
        dt = relogio.tick(FPS) / 1000

        rodando = processar_eventos(estado, personagens)
        atualizar_estado(estado, inimigos, personagens, dt)
        desenhar_tela(tela, fonte, fonte_grande, estado, inimigos, personagens)

    pygame.quit()
