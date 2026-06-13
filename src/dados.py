def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0


def carregar_ranking(caminho_arquivo):
    # Le o ranking do arquivo e devolve uma lista com as maiores pontuacoes.
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        return []

    ranking = []
    for linha in linhas:
        linha = linha.strip()
        if linha.isdigit():
            ranking.append(int(linha))

    return sorted(ranking, reverse=True)


def salvar_pontuacao_ranking(caminho_arquivo, pontuacao, limite=5):
    # Adiciona a nova pontuacao e salva apenas as melhores posicoes.
    ranking = carregar_ranking(caminho_arquivo)
    ranking.append(pontuacao)
    ranking = sorted(ranking, reverse=True)[:limite]

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        for valor in ranking:
            arquivo.write(f"{valor}\n")

    return ranking
