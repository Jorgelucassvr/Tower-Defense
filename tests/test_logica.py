from src.config import CAMINHO_ESTRADA, WAYPOINTS
from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, posicao_no_caminho
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
