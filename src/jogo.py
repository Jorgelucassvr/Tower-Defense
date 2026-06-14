import pygame

from src.config import (
    BOTAO_PLAY,
    BOTAO_REINICIAR,
    BOTAO_SAIR,
    BOTOES_PERSONAGENS,
    CAMINHO_RANKING,
    CAMINHO_RECORDE,
    DANO_SLIME_BASE,
    DANO_SUPREMO_BASE,
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
from src.dados import (
    carregar_ranking,
    carregar_recorde,
    limpar_nome_jogador,
    salvar_pontuacao_ranking,
    salvar_recorde,
)
from src.funcoes import (
    desenhar_fim_de_jogo,
    desenhar_interface,
    desenhar_menu_inicial,
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


def criar_estado_inicial(status="inicio"):
    # Cria um dicionario com as informacoes principais da partida.
    return {
        "moedas": MOEDAS_INICIAIS,
        "vidas": VIDAS_INICIAIS,
        "pontos": 0,
        "eliminacoes": 0,
        "recorde": carregar_recorde(CAMINHO_RECORDE),
        "ranking": carregar_ranking(CAMINHO_RANKING),
        "nome_jogador": "Jogador",
        "selecionado": "guerreiro",
        "mensagem": "Escolha uma unidade e coloque fora da estrada.",
        "status": status,
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

        if estado["status"] == "inicio" and evento.type == pygame.KEYDOWN:
            processar_digitacao_nome(evento, estado)
            continue

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado["status"] == "inicio":
                processar_evento_menu_inicial(evento.pos, estado, inimigos, personagens)
                continue

            if estado["status"] != "jogando":
                return processar_evento_fim_de_jogo(evento.pos, estado, inimigos, personagens)

            if tentar_evoluir_personagem(evento.pos, estado, personagens):
                continue

            for tipo, botao in BOTOES_PERSONAGENS.items():
                if botao.collidepoint(evento.pos):
                    estado["selecionado"] = tipo
                    estado["mensagem"] = f"{TIPOS_PERSONAGENS[tipo]['nome']} selecionado."
                    break
            else:
                colocar_personagem(evento.pos, estado, personagens)

    return True


def processar_evento_menu_inicial(posicao, estado, inimigos, personagens):
    # O jogo so comeca depois que o jogador clica no botao Play.
    if BOTAO_PLAY.collidepoint(posicao):
        iniciar_partida(estado, inimigos, personagens)


def processar_digitacao_nome(evento, estado):
    # Permite digitar o nome que sera usado no ranking.
    if evento.key == pygame.K_BACKSPACE:
        if estado["nome_jogador"] == "Jogador":
            estado["nome_jogador"] = ""
            return
        estado["nome_jogador"] = estado["nome_jogador"][:-1]
        return

    if evento.key in (pygame.K_RETURN, pygame.K_TAB):
        return

    if len(estado["nome_jogador"]) >= 12:
        return

    if evento.unicode.isprintable() and evento.unicode != ";":
        if estado["nome_jogador"] == "Jogador":
            estado["nome_jogador"] = ""
        estado["nome_jogador"] += evento.unicode


def processar_evento_fim_de_jogo(posicao, estado, inimigos, personagens):
    # No fim da partida, o jogador escolhe se reinicia ou fecha a janela.
    if BOTAO_REINICIAR.collidepoint(posicao):
        iniciar_partida(estado, inimigos, personagens)
        return True

    if BOTAO_SAIR.collidepoint(posicao):
        return False

    return True


def iniciar_partida(estado, inimigos, personagens):
    # Limpa a partida atual e inicia uma nova rodada jogavel.
    nome = limpar_nome_jogador(estado.get("nome_jogador", "Jogador"))
    estado.clear()
    estado.update(criar_estado_inicial("jogando"))
    estado["nome_jogador"] = nome
    inimigos.clear()
    personagens.clear()


def contar_personagens(personagens, tipo):
    # Conta base e evoluido juntos para respeitar o limite da classe.
    return sum(1 for personagem in personagens if personagem.tipo.startswith(tipo))


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


def tentar_evoluir_personagem(posicao, estado, personagens):
    # Evolui o personagem quando o jogador clica no botao que aparece no hover.
    for personagem in personagens:
        if not personagem.pode_evoluir():
            continue

        if not personagem.botao_evolucao().collidepoint(posicao):
            continue

        custo = personagem.custo_evolucao()
        if estado["moedas"] < custo:
            estado["mensagem"] = "Moedas insuficientes para evoluir."
            return True

        estado["moedas"] -= custo
        personagem.evoluir()
        estado["mensagem"] = f"{personagem.dados['nome']} evoluido!"
        return True

    return False


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
    tempo_restante = max(0, int(INTERVALO_ENTRE_ONDAS - estado["tempo_entre_ondas"]) + 1)
    estado["mensagem"] = f"Proxima onda em {tempo_restante}s."

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
                dano_base = dano_inimigo_na_base(inimigo)
                estado["vidas"] -= dano_base
                nome = "O supremo" if inimigo.tipo == "supremo" else "Um slime"
                estado["mensagem"] = f"{nome} chegou ao final e tirou {dano_base} vida(s)!"
            elif inimigo.vida <= 0:
                estado["moedas"] += inimigo.moedas
                estado["pontos"] += inimigo.pontos
                estado["eliminacoes"] += 1
                estado["mensagem"] = f"+{inimigo.moedas} moedas e +{inimigo.pontos} pontos."

            inimigos.remove(inimigo)


def dano_inimigo_na_base(inimigo):
    # O slime tira 1 vida; o inimigo supremo tira 3 vidas.
    if inimigo.tipo == "supremo":
        return DANO_SUPREMO_BASE
    return DANO_SLIME_BASE


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
        estado["ranking"] = salvar_pontuacao_ranking(
            CAMINHO_RANKING,
            estado["nome_jogador"],
            estado["pontos"],
            estado["status"],
            estado["onda_atual"],
        )
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
    if estado["status"] == "inicio":
        desenhar_menu_inicial(tela, fonte, fonte_grande, estado)
        pygame.display.flip()
        return

    desenhar_mapa(tela)
    for personagem in personagens:
        personagem.desenhar(tela, fonte)
        if personagem.mostrar_botao_evolucao(pygame.mouse.get_pos()):
            personagem.desenhar_botao_evolucao(tela, fonte)
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