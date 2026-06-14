import os
import tempfile

from src.dados import (
    carregar_ranking,
    converter_linha_ranking,
    limpar_nome_jogador,
    salvar_pontuacao_ranking,
)
from src.config import CAMINHO_ESTRADA, INTERVALO_ENTRE_ONDAS, MOEDAS_INICIAIS, WAYPOINTS
from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, posicao_no_caminho
from src.jogo import (
    contar_personagens,
    criar_estado_inicial,
    criar_inimigo_supremo,
    dano_inimigo_na_base,
    iniciar_partida,
    limite_do_personagem,
    tentar_evoluir_personagem,
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


def test_inimigo_supremo_tira_tres_vidas():
    """Deve fazer o supremo causar 3 de dano ao chegar na base."""
    slime = Inimigo(WAYPOINTS)
    supremo = criar_inimigo_supremo()

    assert dano_inimigo_na_base(slime) == 1
    assert dano_inimigo_na_base(supremo) == 3


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
    """Deve limitar o jogo a 3 guerreiros e 2 arqueiros."""
    assert limite_do_personagem("guerreiro") == 3
    assert limite_do_personagem("arqueiro") == 2


def test_contar_personagens_por_tipo():
    """Deve contar separadamente guerreiros e arqueiros colocados."""
    personagens = [
        Personagem("guerreiro", (10, 10)),
        Personagem("guerreirolv2", (20, 20)),
        Personagem("arqueiro", (30, 30)),
    ]

    assert contar_personagens(personagens, "guerreiro") == 2
    assert contar_personagens(personagens, "arqueiro") == 1


def test_estado_inicial_abre_no_menu():
    """Deve abrir o jogo na tela inicial antes de comecar a partida."""
    estado = criar_estado_inicial()

    assert estado["status"] == "inicio"


def test_iniciar_partida_muda_status_para_jogando():
    """Deve iniciar uma partida limpa quando o jogador clica em Play."""
    estado = criar_estado_inicial()
    inimigos = [Inimigo(WAYPOINTS)]
    personagens = [Personagem("guerreiro", (10, 10))]

    iniciar_partida(estado, inimigos, personagens)

    assert estado["status"] == "jogando"
    assert inimigos == []
    assert personagens == []


def test_intervalo_entre_ondas_e_cinco_segundos():
    """Deve esperar 5 segundos antes da proxima onda."""
    assert INTERVALO_ENTRE_ONDAS == 5.0


def test_moedas_iniciais_deixam_jogo_mais_dificil():
    """Deve iniciar com menos moedas para exigir escolhas."""
    assert MOEDAS_INICIAIS == 120


def test_personagem_pode_evoluir_para_lv2():
    """Deve trocar o personagem base pela versao evoluida."""
    personagem = Personagem("guerreiro", (100, 100))

    assert personagem.pode_evoluir() is True
    assert personagem.evoluir() is True
    assert personagem.tipo == "guerreirolv2"
    assert personagem.pode_evoluir() is False


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
