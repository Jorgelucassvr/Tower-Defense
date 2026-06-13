# All Stars Tower Defenser

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Nome do integrante 1: jorge lucas vieira
- Nome do integrante 2: lucas otavio costa mafia 
- Nome do integrante 3:
- Nome do integrante 4

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

All Stars Tower Defenser é um protótipo de Tower Defense feito em Pygame. O jogador posiciona personagens pelo mapa para impedir que 5 ondas de slimes atravessem a estrada e cheguem ao final do percurso.

Nesta versão básica existem dois personagens:

- Guerreiro: custa 50 moedas e ataca apenas inimigos que passam na sua frente.
- Arqueiro: custa 100 moedas e ataca inimigos dentro de uma área circular maior.

Cada slime eliminado gera 10 moedas e pontos para o jogador. Na quinta onda aparece um inimigo supremo, maior e mais forte que os slimes comuns. O jogo salva o recorde em `data/recorde.txt` e o ranking de pontuação em `data/ranking.txt`.

## Objetivo do jogador

O objetivo é sobreviver às 5 ondas e derrotar ou segurar o inimigo supremo mantendo pelo menos uma vida. O jogador perde se os inimigos chegarem ao final do caminho e as vidas acabarem.

## Regras do jogo

- O jogador começa com 150 moedas e 3 vidas.
- O guerreiro custa 50 moedas.
- O arqueiro custa 100 moedas.
- O limite é de 3 guerreiros e 2 arqueiros no mapa.
- Os personagens podem ser colocados em qualquer parte do mapa, menos na estrada.
- O jogo possui 5 ondas.
- Cada onda possui 5 slimes verdes.
- A vida dos slimes aumenta a cada onda.
- Na quinta onda aparece um inimigo supremo depois dos slimes comuns.
- Cada slime possui barra de vida acima da cabeça.
- Cada eliminação rende 10 moedas.
- Slimes geram 100 pontos.
- O inimigo supremo gera 500 pontos.
- Cada inimigo que chega ao final tira 1 vida.
- O jogador vence quando todas as ondas acabam e ainda existe pelo menos 1 vida.
- O jogador perde quando as vidas chegam a 0.
- A pontuação final entra no ranking salvo em arquivo.
- O ranking mostra pontos, resultado (`V` para vitoria e `D` para derrota) e onda alcancada.
- No fim da partida, a janela continua aberta e o jogador escolhe entre reiniciar ou sair.

## Controles

- Mouse: usado para selecionar personagens e posicioná-los no mapa.
- Clique em "Guerreiro": seleciona o guerreiro.
- Clique em "Arqueiro": seleciona o arqueiro.
- Clique fora da estrada: coloca o personagem selecionado, se houver moedas suficientes.
- A área "Personagens" no canto direito funciona como loja/seleção de ícones.
- No fim do jogo, clique em "Reiniciar" para jogar de novo ou "Sair" para fechar.

## Como executar o projeto

```bash
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Funcionalidades principais no codigo

- Janela, loop principal, ondas e estados do jogo: `src/jogo.py`
  Para alterar a regra geral da partida, edite as funcoes `atualizar_estado`, `gerar_inimigos`, `avancar_onda_se_preciso`, `verificar_fim_de_jogo` e `executar_jogo`.

- Guerreiro, arqueiro, slimes e inimigo supremo: `src/movimentaçao.py`
  Para mudar dano, alcance, velocidade ou vida, prefira alterar os valores em `src/config.py`.

- Mapa, estrada, loja de personagens, ranking e interface: `src/funcoes.py`
  Para mudar o desenho do mapa ou os textos da tela, edite `desenhar_mapa`, `desenhar_interface`, `desenhar_ranking` e `desenhar_fim_de_jogo`.

- Custos, moedas, vidas, pontos, ondas, cores e caminho dos inimigos: `src/config.py`
  Para mudar o preco do guerreiro ou arqueiro, edite `TIPOS_PERSONAGENS`. Para mudar o limite de unidades, edite `LIMITE_GUERREIROS` e `LIMITE_ARQUEIROS`. Para mudar ondas, vida ou pontuacao, edite `TOTAL_ONDAS`, `INIMIGOS_POR_ONDA`, `VIDA_SLIME_BASE`, `VIDA_EXTRA_POR_ONDA`, `PONTOS_POR_SLIME` e `PONTOS_INIMIGO_SUPREMO`. Para mudar o caminho dos slimes, edite `CAMINHO_ESTRADA` e `WAYPOINTS`.

- Recorde e ranking salvos em arquivo: `src/dados.py`, `data/recorde.txt` e `data/ranking.txt`
  O ranking usa o formato `pontos;resultado;ondas`. Para trocar o tipo de dado salvo, ajuste `salvar_recorde`, `carregar_recorde`, `salvar_pontuacao_ranking`, `carregar_ranking` e o valor enviado em `src/jogo.py`.

- Testes de logica: `tests/test_logica.py`
  Para adicionar testes novos, crie funcoes iniciando com `test_`.

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
