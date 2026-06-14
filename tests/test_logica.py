import os
import tempfile

from src.dados import (
    carregar_ranking,
    converter_linha_ranking,
    limpar_nome_jogador,
    salvar_pontuacao_ranking,
)
from src.config import (
    CAMINHO_ESTRADA,
    DISTANCIA_MINIMA_PERSONAGENS,
    INTERVALO_ENTRE_ONDAS,
    INTERVALO_SPAWN,
    LIMITE_ARQUEIROS,
    LIMITE_BARBARO,
    LIMITE_GUERREIROS,
    MOEDAS_INICIAIS,
    MOEDAS_POR_VIDA_PERDIDA,
    ONDAS_COM_SUPREMO,
    TOTAL_ONDAS,
    VIDA_INIMIGO_SUPREMO,
    WAYPOINTS,
)
from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, posicao_no_caminho
from src.jogo import (
    avancar_onda_se_preciso,
    contar_personagens,
    criar_estado_inicial,
    criar_inimigo_supremo,
    atualizar_inimigos,
    dano_inimigo_na_base,
    gerar_inimigos,
    iniciar_partida,
    limite_do_personagem,
    moedas_por_vida_perdida,
    onda_tem_supremo,
    colocar_personagem,
    posicao_ocupada_por_personagem,
    tentar_evoluir_personagem,
    total_inimigos_da_onda,
    verificar_fim_de_jogo,
    vida_supremo_da_onda,
    vida_slime_da_onda,
)
from src.movimentaçao import Inimigo, Personagem


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


def test_posicao_no_caminho():
    """Deve identificar quando uma posicao fica dentro da estrada."""
    assert posicao_no_caminho(CAMINHO_ESTRADA[0].center) is True


def test_posicao_fora_do_caminho():
    """Deve permitir posicionamento fora da estrada."""
    assert posicao_no_caminho((100, 100)) is False


def test_inimigo_recebe_dano_e_desativa():
    """Deve remover o slime quando a vida chega a zero."""
    inimigo = Inimigo(WAYPOINTS, vida=10)
    inimigo.receber_dano(10)
    assert inimigo.ativo is False


def test_guerreiro_ataca_somente_na_frente():
    """Deve fazer o guerreiro atacar apenas um inimigo a frente dele."""
    guerreiro = Personagem("guerreiro", (100, 345))
    inimigo_frente = Inimigo(WAYPOINTS)
    inimigo_frente.x = 150
    inimigo_frente.y = 345

    inimigo_atras = Inimigo(WAYPOINTS)
    inimigo_atras.x = 50
    inimigo_atras.y = 345

    assert guerreiro.encontrar_alvo([inimigo_frente]) == inimigo_frente
    assert guerreiro.encontrar_alvo([inimigo_atras]) is None


def test_arqueiro_ataca_em_area():
    """Deve fazer o arqueiro encontrar um inimigo dentro do alcance circular."""
    arqueiro = Personagem("arqueiro", (100, 100))
    inimigo = Inimigo(WAYPOINTS)
    inimigo.x = 180
    inimigo.y = 100

    assert arqueiro.encontrar_alvo([inimigo]) == inimigo


def test_barbaro_ataca_em_area_curta():
    """Deve fazer o barbaro atacar inimigos perto dele."""
    barbaro = Personagem("barbaro", (100, 100))
    inimigo = Inimigo(WAYPOINTS)
    inimigo.x = 150
    inimigo.y = 100

    assert barbaro.encontrar_alvo([inimigo]) == inimigo


def test_barbaro_causa_dano_em_todos_no_range():
    """Deve causar dano em todos os inimigos dentro do alcance do barbaro."""
    barbaro = Personagem("barbaro", (100, 100))
    inimigo_1 = Inimigo(WAYPOINTS, vida=100)
    inimigo_2 = Inimigo(WAYPOINTS, vida=100)
    inimigo_fora = Inimigo(WAYPOINTS, vida=100)

    inimigo_1.x, inimigo_1.y = 120, 100
    inimigo_2.x, inimigo_2.y = 150, 100
    inimigo_fora.x, inimigo_fora.y = 300, 100

    barbaro.atualizar([inimigo_1, inimigo_2, inimigo_fora], dt=1)

    vida_esperada = 100 - barbaro.dados["dano"]
    assert inimigo_1.vida == vida_esperada
    assert inimigo_2.vida == vida_esperada
    assert inimigo_fora.vida == 100


def test_vida_aumenta_com_a_onda():
    """Deve aumentar a vida dos slimes conforme a onda avanca."""
    assert vida_slime_da_onda(2) > vida_slime_da_onda(1)
    assert vida_slime_da_onda(5) > vida_slime_da_onda(2)


def test_inimigo_supremo_e_mais_forte():
    """Deve criar o supremo com mais vida e tamanho que o slime comum."""
    slime = Inimigo(WAYPOINTS)
    supremo = criar_inimigo_supremo()

    assert supremo.tipo == "supremo"
    assert supremo.vida_maxima > slime.vida_maxima
    assert supremo.raio > slime.raio


def test_primeiro_supremo_tem_metade_da_vida_do_final():
    """Deve deixar o boss da onda 5 com metade da vida do boss da onda 10."""
    primeiro_boss = criar_inimigo_supremo(5)
    boss_final = criar_inimigo_supremo(10)

    assert vida_supremo_da_onda(5) == VIDA_INIMIGO_SUPREMO // 2
    assert primeiro_boss.vida_maxima == boss_final.vida_maxima // 2


def test_inimigo_supremo_tira_tres_vidas():
    """Deve fazer o supremo causar 3 de dano ao chegar na base."""
    slime = Inimigo(WAYPOINTS)
    supremo = criar_inimigo_supremo()

    assert dano_inimigo_na_base(slime) == 1
    assert dano_inimigo_na_base(supremo) == 3


def test_moedas_por_vida_perdida():
    """Deve pagar moedas para cada vida perdida conforme o config."""
    assert moedas_por_vida_perdida(1) == MOEDAS_POR_VIDA_PERDIDA
    assert moedas_por_vida_perdida(3) == MOEDAS_POR_VIDA_PERDIDA * 3


def test_slime_passando_da_moedas_por_vida_perdida():
    """Deve dar moedas quando um slime passa e tira 1 vida."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 0
    inimigo = Inimigo(WAYPOINTS)
    inimigo.indice_alvo = len(WAYPOINTS)
    inimigos = [inimigo]

    atualizar_inimigos(estado, inimigos, dt=0)

    assert estado["vidas"] == 2
    assert estado["moedas"] == MOEDAS_POR_VIDA_PERDIDA
    assert inimigos == []


def test_supremo_passando_da_bonus_de_moedas_configurado():
    """Deve dar moedas quando o supremo passa e tira 3 vidas."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 0
    supremo = criar_inimigo_supremo()
    supremo.indice_alvo = len(WAYPOINTS)
    inimigos = [supremo]

    atualizar_inimigos(estado, inimigos, dt=0)

    assert estado["vidas"] == 0
    assert estado["moedas"] == MOEDAS_POR_VIDA_PERDIDA * 3
    assert inimigos == []


def test_derrota_preserva_bonus_do_supremo_na_mensagem():
    """Deve mostrar o bonus de moedas quando o supremo causa derrota."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 0
    supremo = criar_inimigo_supremo()
    supremo.indice_alvo = len(WAYPOINTS)
    inimigos = [supremo]

    atualizar_inimigos(estado, inimigos, dt=0)
    verificar_fim_de_jogo(estado, inimigos)

    assert estado["status"] == "derrota"
    assert estado["moedas"] == MOEDAS_POR_VIDA_PERDIDA * 3
    assert f"+{MOEDAS_POR_VIDA_PERDIDA * 3} moedas" in estado["mensagem"]


def test_ranking_salva_melhores_pontuacoes():
    """Deve salvar o ranking em ordem decrescente e respeitar o limite."""
    arquivo = tempfile.NamedTemporaryFile(delete=False)
    arquivo.close()

    try:
        salvar_pontuacao_ranking(arquivo.name, "Ana", 100, "derrota", 2)
        salvar_pontuacao_ranking(arquivo.name, "Bia", 300, "vitoria", 5)
        salvar_pontuacao_ranking(arquivo.name, "Caio", 200, "derrota", 4)

        ranking = carregar_ranking(arquivo.name)
        assert [entrada["pontos"] for entrada in ranking] == [300, 200, 100]
        assert ranking[0]["nome"] == "Bia"
        assert ranking[0]["resultado"] == "vitoria"
        assert ranking[0]["ondas"] == 5
    finally:
        os.remove(arquivo.name)


def test_ranking_antigo_com_apenas_numero_continua_valido():
    """Deve carregar arquivos antigos que tinham somente a pontuacao."""
    entrada = converter_linha_ranking("250\n")

    assert entrada["pontos"] == 250
    assert entrada["resultado"] == "Partida"
    assert entrada["nome"] == "Jogador"


def test_limpar_nome_jogador():
    """Deve limpar separador e usar nome padrao quando vazio."""
    assert limpar_nome_jogador("Lucas;Teste") == "LucasTeste"
    assert limpar_nome_jogador("   ") == "Jogador"


def test_limite_de_personagens():
    """Deve limitar cada classe de aliado."""
    assert limite_do_personagem("guerreiro") == LIMITE_GUERREIROS
    assert limite_do_personagem("arqueiro") == LIMITE_ARQUEIROS
    assert limite_do_personagem("barbaro") == LIMITE_BARBARO


def test_contar_personagens_por_tipo():
    """Deve contar separadamente guerreiros e arqueiros colocados."""
    personagens = [
        Personagem("guerreiro", (10, 10)),
        Personagem("guerreirolv2", (20, 20)),
        Personagem("arqueiro", (30, 30)),
        Personagem("barbarolv2", (40, 40)),
    ]

    assert contar_personagens(personagens, "guerreiro") == 2
    assert contar_personagens(personagens, "arqueiro") == 1
    assert contar_personagens(personagens, "barbaro") == 1


def test_posicao_ocupada_por_personagem():
    """Deve identificar quando uma posicao esta perto demais de outro personagem."""
    personagens = [Personagem("guerreiro", (100, 100))]

    assert posicao_ocupada_por_personagem((100, 100), personagens) is True
    assert posicao_ocupada_por_personagem(
        (100 + DISTANCIA_MINIMA_PERSONAGENS + 5, 100),
        personagens,
    ) is False


def test_nao_coloca_personagem_em_cima_de_outro():
    """Nao deve gastar moedas nem adicionar personagem em espaco ocupado."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 500
    estado["selecionado"] = "arqueiro"
    personagens = [Personagem("guerreiro", (100, 100))]

    colocar_personagem((100, 100), estado, personagens)

    assert len(personagens) == 1
    assert estado["moedas"] == 500
    assert estado["mensagem"] == "Espaco ocupado por outro personagem."


def test_estado_inicial_abre_no_menu():
    """Deve abrir o jogo na tela inicial antes de comecar a partida."""
    estado = criar_estado_inicial()

    assert estado["status"] == "inicio"
    assert "mensagem" in estado


def test_iniciar_partida_muda_status_para_jogando():
    """Deve iniciar uma partida limpa quando o jogador clica em Play."""
    estado = criar_estado_inicial()
    inimigos = [Inimigo(WAYPOINTS)]
    personagens = [Personagem("guerreiro", (10, 10))]

    iniciar_partida(estado, inimigos, personagens)

    assert estado["status"] == "jogando"
    assert inimigos == []
    assert personagens == []


def test_intervalo_entre_ondas_tem_valor_positivo():
    """Deve ter um intervalo configurado antes da proxima onda."""
    assert INTERVALO_ENTRE_ONDAS > 0


def test_moedas_iniciais_deixam_jogo_mais_dificil():
    """Deve iniciar com menos moedas para exigir escolhas."""
    assert MOEDAS_INICIAIS <= 150


def test_total_inimigos_aumenta_por_onda():
    """Deve adicionar um slime extra a cada nova onda."""
    assert total_inimigos_da_onda(1) == 5
    assert total_inimigos_da_onda(3) == 7


def test_jogo_tem_dez_ondas_com_boss_na_cinco_e_dez():
    """Deve ter 10 ondas e boss somente nas ondas 5 e 10."""
    assert TOTAL_ONDAS == 10
    assert ONDAS_COM_SUPREMO == (5, 10)
    assert onda_tem_supremo(5) is True
    assert onda_tem_supremo(10) is True
    assert onda_tem_supremo(4) is False


def test_gera_supremo_na_onda_cinco_e_dez():
    """Deve criar um boss depois dos slimes nas ondas especiais."""
    for onda in ONDAS_COM_SUPREMO:
        estado = criar_estado_inicial("jogando")
        estado["onda_atual"] = onda
        estado["spawnados_onda"] = total_inimigos_da_onda(onda)
        estado["tempo_spawn"] = INTERVALO_SPAWN
        inimigos = []

        gerar_inimigos(estado, inimigos, dt=0)

        assert len(inimigos) == 1
        assert inimigos[0].tipo == "supremo"
        assert inimigos[0].vida_maxima == vida_supremo_da_onda(onda)
        assert estado["supremo_spawnado"] is True


def test_nao_gera_supremo_em_onda_comum():
    """Nao deve criar boss em ondas fora da lista especial."""
    estado = criar_estado_inicial("jogando")
    estado["onda_atual"] = 4
    estado["spawnados_onda"] = total_inimigos_da_onda(4)
    estado["tempo_spawn"] = INTERVALO_SPAWN
    inimigos = []

    gerar_inimigos(estado, inimigos, dt=0)

    assert inimigos == []
    assert estado["supremo_spawnado"] is False


def test_avancar_onda_reinicia_controle_do_supremo():
    """Deve permitir outro boss depois que a onda 5 termina."""
    estado = criar_estado_inicial("jogando")
    estado["onda_atual"] = 5
    estado["spawnados_onda"] = total_inimigos_da_onda(5)
    estado["supremo_spawnado"] = True

    avancar_onda_se_preciso(estado, [], dt=INTERVALO_ENTRE_ONDAS)

    assert estado["onda_atual"] == 6
    assert estado["supremo_spawnado"] is False


def test_personagem_pode_evoluir_para_lv2():
    """Deve trocar o personagem base pela versao evoluida."""
    personagem = Personagem("guerreiro", (100, 100))

    assert personagem.pode_evoluir() is True
    assert personagem.evoluir() is True
    assert personagem.tipo == "guerreirolv2"
    assert personagem.pode_evoluir() is False


def test_barbaro_pode_evoluir_para_lv2():
    """Deve trocar o barbaro base pela versao evoluida."""
    personagem = Personagem("barbaro", (100, 100))

    assert personagem.evoluir() is True
    assert personagem.tipo == "barbarolv2"


def test_evolucao_gasta_moedas():
    """Deve descontar moedas quando o jogador clica no botao de evolucao."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 150
    personagem = Personagem("guerreiro", (100, 100))
    personagens = [personagem]
    custo = personagem.custo_evolucao()

    clicou = tentar_evoluir_personagem(personagem.botao_evolucao().center, estado, personagens)

    assert clicou is True
    assert personagem.tipo == "guerreirolv2"
    assert estado["moedas"] == 150 - custo


def test_evolucao_sem_moedas_nao_altera_personagem():
    """Nao deve evoluir quando o jogador nao tem moedas suficientes."""
    estado = criar_estado_inicial("jogando")
    estado["moedas"] = 0
    personagem = Personagem("arqueiro", (100, 100))

    tentar_evoluir_personagem(personagem.botao_evolucao().center, estado, [personagem])

    assert personagem.tipo == "arqueiro"
    assert estado["moedas"] == 0
