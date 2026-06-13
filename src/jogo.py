import pygame

from src.config import (
    BOTAO_REINICIAR,
    BOTAO_SAIR,
    BOTOES_PERSONAGENS,
    CAMINHO_RANKING,
    CAMINHO_RECORDE,
    FPS,
    INIMIGOS_POR_ONDA,
    INTERVALO_ENTRE_ONDAS,
    INTERVALO_SPAWN,
    ALTURA_TELA,
    LARGURA_TELA,
    LIMITE_ARQUEIROS,
    LIMITE_GUERREIROS,
    MOEDAS_INICIAIS,
    TIPOS_PERSONAGENS,
    TITULO_JOGO,
    TOTAL_ONDAS,
    VIDA_EXTRA_POR_ONDA,
    VIDA_INIMIGO_SUPREMO,
    VIDA_SLIME_BASE,
    VIDAS_INICIAIS,
    WAYPOINTS,
)
from src.dados import carregar_ranking, carregar_recorde, salvar_pontuacao_ranking, salvar_recorde
from src.funcoes import (
    desenhar_fim_de_jogo,
    desenhar_interface,
    desenhar_mapa,
    jogador_perdeu,
    posicao_na_interface,
    posicao_no_caminho,
)
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
        "pontos": 0,
        "eliminacoes": 0,
        "recorde": carregar_recorde(CAMINHO_RECORDE),
        "ranking": carregar_ranking(CAMINHO_RANKING),
        "selecionado": "guerreiro",
        "mensagem": "Escolha uma unidade e coloque fora da estrada.",
        "status": "jogando",
        "onda_atual": 1,
        "spawnados_onda": 0,
        "tempo_spawn": 0,
        "tempo_entre_ondas": 0,
        "supremo_spawnado": False,
        "recorde_salvo": False,
    }


def processar_eventos(estado, inimigos, personagens):
    # Le eventos do mouse para escolher e posicionar personagens.
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado["status"] != "jogando":
                return processar_evento_fim_de_jogo(evento.pos, estado, inimigos, personagens)

            for tipo, botao in BOTOES_PERSONAGENS.items():
                if botao.collidepoint(evento.pos):
                    estado["selecionado"] = tipo
                    estado["mensagem"] = f"{TIPOS_PERSONAGENS[tipo]['nome']} selecionado."
                    break
            else:
                colocar_personagem(evento.pos, estado, personagens)

    return True


def processar_evento_fim_de_jogo(posicao, estado, inimigos, personagens):
    # No fim da partida, o jogador escolhe se reinicia ou fecha a janela.
    if BOTAO_REINICIAR.collidepoint(posicao):
        estado.clear()
        estado.update(criar_estado_inicial())
        inimigos.clear()
        personagens.clear()
        return True

    if BOTAO_SAIR.collidepoint(posicao):
        return False

    return True


def contar_personagens(personagens, tipo):
    # Conta quantos personagens de um tipo ja estao no mapa.
    return sum(1 for personagem in personagens if personagem.tipo == tipo)


def limite_do_personagem(tipo):
    # Define o limite de cada personagem.
    if tipo == "guerreiro":
        return LIMITE_GUERREIROS
    return LIMITE_ARQUEIROS


def colocar_personagem(posicao, estado, personagens):
    # Tenta colocar o guerreiro ou arqueiro no mapa.
    tipo = estado["selecionado"]
    custo = TIPOS_PERSONAGENS[tipo]["custo"]
    limite = limite_do_personagem(tipo)

    if posicao_no_caminho(posicao) or posicao_na_interface(posicao):
        estado["mensagem"] = "Coloque o personagem fora da estrada e da loja."
        return

    if contar_personagens(personagens, tipo) >= limite:
        estado["mensagem"] = f"Limite de {limite} {TIPOS_PERSONAGENS[tipo]['nome']} atingido."
        return

    if estado["moedas"] < custo:
        estado["mensagem"] = "Moedas insuficientes."
        return

    personagens.append(Personagem(tipo, posicao))
    estado["moedas"] -= custo
    estado["mensagem"] = f"{TIPOS_PERSONAGENS[tipo]['nome']} colocado."


def vida_slime_da_onda(onda):
    # A vida aumenta de forma simples conforme as ondas avancam.
    return VIDA_SLIME_BASE + (onda - 1) * VIDA_EXTRA_POR_ONDA


def criar_slime_da_onda(onda):
    # Cria um slime normal com vida baseada na onda atual.
    return Inimigo(WAYPOINTS, vida=vida_slime_da_onda(onda))


def criar_inimigo_supremo():
    # Cria o ultimo inimigo do jogo: maior, mais lento e com muita vida.
    return Inimigo(
        WAYPOINTS,
        velocidade=60,
        raio=25,
        vida=VIDA_INIMIGO_SUPREMO,
        tipo="supremo",
    )


def onda_atual_terminou(estado, inimigos):
    # Confere se todos os inimigos previstos da onda atual ja sairam da tela.
    normais_prontos = estado["spawnados_onda"] >= INIMIGOS_POR_ONDA
    chefe_pronto = estado["onda_atual"] < TOTAL_ONDAS or estado["supremo_spawnado"]
    return normais_prontos and chefe_pronto and len(inimigos) == 0


def gerar_inimigos(estado, inimigos, dt):
    # Gera slimes da onda atual e, na ultima onda, cria o inimigo supremo.
    if estado["onda_atual"] > TOTAL_ONDAS:
        return

    estado["tempo_spawn"] += dt
    if estado["tempo_spawn"] < INTERVALO_SPAWN:
        return

    if estado["spawnados_onda"] < INIMIGOS_POR_ONDA:
        inimigos.append(criar_slime_da_onda(estado["onda_atual"]))
        estado["spawnados_onda"] += 1
        estado["tempo_spawn"] = 0
        return

    if estado["onda_atual"] == TOTAL_ONDAS and not estado["supremo_spawnado"]:
        inimigos.append(criar_inimigo_supremo())
        estado["supremo_spawnado"] = True
        estado["tempo_spawn"] = 0
        estado["mensagem"] = "Inimigo supremo apareceu!"


def avancar_onda_se_preciso(estado, inimigos, dt):
    # Depois que uma onda termina, espera um pouco e inicia a proxima.
    if not onda_atual_terminou(estado, inimigos):
        estado["tempo_entre_ondas"] = 0
        return

    if estado["onda_atual"] >= TOTAL_ONDAS:
        return

    estado["tempo_entre_ondas"] += dt
    if estado["tempo_entre_ondas"] >= INTERVALO_ENTRE_ONDAS:
        estado["onda_atual"] += 1
        estado["spawnados_onda"] = 0
        estado["tempo_spawn"] = 0
        estado["tempo_entre_ondas"] = 0
        estado["mensagem"] = f"Onda {estado['onda_atual']} iniciada."


def atualizar_inimigos(estado, inimigos, dt):
    # Move os slimes e aplica dano ao jogador quando chegam ao fim.
    for inimigo in inimigos[:]:
        inimigo.atualizar(dt)

        if not inimigo.ativo:
            if inimigo.chegou_ao_fim:
                estado["vidas"] -= 1
                nome = "O supremo" if inimigo.tipo == "supremo" else "Um slime"
                estado["mensagem"] = f"{nome} chegou ao final!"
            elif inimigo.vida <= 0:
                estado["moedas"] += inimigo.moedas
                estado["pontos"] += inimigo.pontos
                estado["eliminacoes"] += 1
                estado["mensagem"] = f"+{inimigo.moedas} moedas e +{inimigo.pontos} pontos."

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

    onda_acabou = estado["onda_atual"] == TOTAL_ONDAS and onda_atual_terminou(estado, inimigos)
    if onda_acabou and estado["vidas"] > 0:
        estado["status"] = "vitoria"
        estado["mensagem"] = "Voce venceu todas as ondas!"

    if estado["status"] != "jogando" and not estado["recorde_salvo"]:
        if estado["pontos"] > estado["recorde"]:
            estado["recorde"] = estado["pontos"]
            salvar_recorde(CAMINHO_RECORDE, estado["recorde"])
        estado["ranking"] = salvar_pontuacao_ranking(CAMINHO_RANKING, estado["pontos"])
        estado["recorde_salvo"] = True


def atualizar_estado(estado, inimigos, personagens, dt):
    # Atualiza todas as regras principais da partida.
    if estado["status"] != "jogando":
        return

    gerar_inimigos(estado, inimigos, dt)
    atualizar_personagens(personagens, inimigos, dt)
    atualizar_inimigos(estado, inimigos, dt)
    avancar_onda_se_preciso(estado, inimigos, dt)
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

        rodando = processar_eventos(estado, inimigos, personagens)
        atualizar_estado(estado, inimigos, personagens, dt)
        desenhar_tela(tela, fonte, fonte_grande, estado, inimigos, personagens)

    pygame.quit()
