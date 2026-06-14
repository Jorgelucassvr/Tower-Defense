import os


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuacao recorde em arquivo texto."""
    criar_pasta_se_preciso(caminho_arquivo)

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se nao existir valor valido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0


def carregar_ranking(caminho_arquivo):
    # Le o ranking e devolve uma lista de dicionarios ordenada por pontuacao.
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        return []

    ranking = []
    for linha in linhas:
        entrada = converter_linha_ranking(linha)
        if entrada is not None:
            ranking.append(entrada)

    return ordenar_ranking(ranking)


def converter_linha_ranking(linha):
    # Aceita o formato com nome e tambem arquivos antigos.
    partes = linha.strip().split(";")
    if len(partes) == 1 and partes[0].isdigit():
        return {"nome": "Jogador", "pontos": int(partes[0]), "resultado": "Partida", "ondas": 0}

    if len(partes) == 3 and partes[0].isdigit() and partes[2].isdigit():
        return {
            "nome": "Jogador",
            "pontos": int(partes[0]),
            "resultado": partes[1],
            "ondas": int(partes[2]),
        }

    if len(partes) != 4 or not partes[1].isdigit() or not partes[3].isdigit():
        return None

    return {
        "nome": partes[0] or "Jogador",
        "pontos": int(partes[1]),
        "resultado": partes[2],
        "ondas": int(partes[3]),
    }


def ordenar_ranking(ranking):
    # Ordena da maior para a menor pontuacao.
    return sorted(ranking, key=lambda entrada: entrada["pontos"], reverse=True)


def salvar_pontuacao_ranking(caminho_arquivo, nome, pontuacao, resultado, ondas, limite=5):
    # Adiciona a pontuacao final ao ranking e salva somente o top 5.
    criar_pasta_se_preciso(caminho_arquivo)
    ranking = carregar_ranking(caminho_arquivo)
    ranking.append({
        "nome": limpar_nome_jogador(nome),
        "pontos": pontuacao,
        "resultado": resultado,
        "ondas": ondas,
    })
    ranking = ordenar_ranking(ranking)[:limite]

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        for entrada in ranking:
            arquivo.write(
                f"{entrada['nome']};{entrada['pontos']};{entrada['resultado']};{entrada['ondas']}\n"
            )

    return ranking


def limpar_nome_jogador(nome):
    # Evita nomes vazios e remove o separador usado no arquivo do ranking.
    nome_limpo = nome.strip().replace(";", "")[:12]
    if nome_limpo == "":
        return "Jogador"
    return nome_limpo


def criar_pasta_se_preciso(caminho_arquivo):
    # Garante que a pasta de destino exista antes de salvar arquivos.
    pasta = os.path.dirname(caminho_arquivo)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
