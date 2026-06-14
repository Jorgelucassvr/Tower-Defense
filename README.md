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

All Stars Tower Defenser é um protótipo de Tower Defense feito em Pygame. O jogador posiciona personagens pelo mapa para impedir que 10 ondas de slimes atravessem a estrada e cheguem ao final do percurso. O balanceamento atual foi deixado propositalmente difícil: as moedas são limitadas, os inimigos ganham bastante vida por onda e as evoluções precisam ser escolhidas com cuidado.

Nesta versão básica existem três personagens:

- Guerreiro: custa 50 moedas e ataca apenas inimigos que passam na sua frente.
- Arqueiro: custa 100 moedas e ataca inimigos dentro de uma área circular maior.
- Barbaro: custa 60 moedas e causa dano em todos os inimigos dentro da sua área circular curta.
- Os personagens podem evoluir uma vez ao passar o mouse por cima deles e clicar no botão "Up".

Cada slime eliminado gera 10 moedas e pontos para o jogador. Quando um inimigo chega ao final, o jogador perde vida, mas recebe 10 moedas por vida perdida. Nas ondas 5 e 10 aparece um inimigo supremo, maior e mais forte que os slimes comuns. O primeiro boss tem metade da vida do boss final. O jogo salva o recorde em `data/recorde.txt` e o ranking com nome do jogador em `data/ranking.txt`.

## Objetivo do jogador

O objetivo é sobreviver às 10 ondas e derrotar ou segurar os inimigos supremos mantendo pelo menos uma vida. O jogador perde se os inimigos chegarem ao final do caminho e as vidas acabarem.

## Regras do jogo

- O jogador começa com 120 moedas e 3 vidas.
- O guerreiro custa 50 moedas.
- O arqueiro custa 100 moedas.
- O barbaro custa 60 moedas.
- O limite é de 4 guerreiros, 2 arqueiros e 3 barbaros no mapa.
- Cada personagem pode evoluir uma vez, gastando moedas.
- Os personagens podem ser colocados em qualquer parte do mapa, menos na estrada e em cima de outro personagem.
- O jogo possui 10 ondas.
- A primeira onda possui 5 slimes verdes e cada onda seguinte ganha 1 slime extra.
- A próxima onda começa 1 segundo depois que a anterior acaba.
- A vida dos slimes aumenta a cada onda.
- Nas ondas 5 e 10 aparece um inimigo supremo depois dos slimes comuns.
- O boss da onda 5 tem metade da vida do boss da onda 10.
- Cada slime possui barra de vida acima da cabeça.
- Cada eliminação rende 10 moedas.
- Cada vida perdida rende 10 moedas de compensação.
- Slimes geram 100 pontos.
- O inimigo supremo gera 500 pontos.
- Cada slime que chega ao final tira 1 vida.
- O inimigo supremo tira 3 vidas se chegar ao final, gerando 30 moedas de compensação.
- O jogador vence quando todas as ondas acabam e ainda existe pelo menos 1 vida.
- O jogador perde quando as vidas chegam a 0.
- A pontuação final entra no ranking salvo em arquivo.
- O ranking mostra nome, pontos, resultado (`V` para vitoria e `D` para derrota) e onda alcancada.
- No fim da partida, a janela continua aberta e o jogador escolhe entre reiniciar ou sair.

## Controles

- Mouse: usado para selecionar personagens e posicioná-los no mapa.
- Digite seu nome na tela inicial para aparecer no ranking.
- Clique em "PLAY": inicia a partida pela tela inicial.
- Clique em "Guerreiro": seleciona o guerreiro.
- Clique em "Arqueiro": seleciona o arqueiro.
- Clique em "Barbaro": seleciona o barbaro.
- Clique fora da estrada e longe de outro personagem: coloca o personagem selecionado, se houver moedas suficientes.
- Passe o mouse sobre um personagem: mostra o botão "Up" para evoluir.
- Clique em "Up": evolui o personagem, se houver moedas suficientes.
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

- Guerreiro, arqueiro, barbaro, slimes e inimigo supremo: `src/movimentaçao.py`
  Para mudar dano, alcance, evolução, velocidade ou vida, prefira alterar os valores em `src/config.py`.

- Mapa, estrada, loja de personagens, ranking e interface: `src/funcoes.py`
  Para mudar o desenho do mapa ou os textos da tela, edite `desenhar_mapa`, `desenhar_menu_inicial`, `desenhar_interface`, `desenhar_ranking` e `desenhar_fim_de_jogo`.

- Custos, moedas, vidas, pontos, ondas, cores e caminho dos inimigos: `src/config.py`
  Para mudar o preco do guerreiro, arqueiro, barbaro ou evolucoes, edite `TIPOS_PERSONAGENS`. Para mudar o limite de unidades, edite `LIMITE_GUERREIROS`, `LIMITE_ARQUEIROS` e `LIMITE_BARBARO`. Para mudar ondas, vida, dano na base, recompensa ou pontuacao, edite `TOTAL_ONDAS`, `ONDAS_COM_SUPREMO`, `INIMIGOS_POR_ONDA`, `VIDA_SLIME_BASE`, `VIDA_EXTRA_POR_ONDA`, `DANO_SLIME_BASE`, `DANO_SUPREMO_BASE`, `MOEDAS_POR_VIDA_PERDIDA`, `PONTOS_POR_SLIME` e `PONTOS_INIMIGO_SUPREMO`. Para mudar distancia minima entre personagens, edite `DISTANCIA_MINIMA_PERSONAGENS`. Para mudar o caminho dos slimes, edite `CAMINHO_ESTRADA` e `WAYPOINTS`.

- Recorde e ranking salvos em arquivo: `src/dados.py`, `data/recorde.txt` e `data/ranking.txt`
  O ranking usa o formato `nome;pontos;resultado;ondas`. Para trocar o tipo de dado salvo, ajuste `salvar_recorde`, `carregar_recorde`, `salvar_pontuacao_ranking`, `carregar_ranking` e o valor enviado em `src/jogo.py`.

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
