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

All Stars Tower Defenser é um protótipo de Tower Defense feito em Pygame. O jogador posiciona personagens pelo mapa para impedir que uma onda de slimes atravesse a estrada e chegue ao final do percurso.

Nesta versão básica existem dois personagens:

- Guerreiro: custa 50 moedas e ataca apenas inimigos que passam na sua frente.
- Arqueiro: custa 100 moedas e ataca inimigos dentro de uma área circular maior.

Cada slime eliminado gera 10 moedas para o jogador. O jogo salva o recorde de eliminações no arquivo `data/recorde.txt`.

## Objetivo do jogador

O objetivo é sobreviver à onda de 5 slimes. O jogador vence se eliminar ou segurar todos os slimes mantendo pelo menos uma vida. O jogador perde se os slimes chegarem ao final do caminho e as vidas acabarem.

## Regras do jogo

- O jogador começa com 150 moedas e 3 vidas.
- O guerreiro custa 50 moedas.
- O arqueiro custa 100 moedas.
- Os personagens podem ser colocados em qualquer parte do mapa, menos na estrada.
- A onda possui 5 slimes verdes.
- Cada slime possui barra de vida acima da cabeça.
- Cada eliminação rende 10 moedas.
- Cada slime que chega ao final tira 1 vida.
- O jogador vence quando a onda acaba e ainda existe pelo menos 1 vida.
- O jogador perde quando as vidas chegam a 0.

## Controles

- Mouse: usado para selecionar personagens e posicioná-los no mapa.
- Clique em "Guerreiro": seleciona o guerreiro.
- Clique em "Arqueiro": seleciona o arqueiro.
- Clique fora da estrada: coloca o personagem selecionado, se houver moedas suficientes.

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

- Janela, loop principal e estados do jogo: `src/jogo.py`
  Para alterar a regra geral da partida, edite as funcoes `atualizar_estado`, `verificar_fim_de_jogo` e `executar_jogo`.

- Guerreiro, arqueiro e slimes: `src/movimentaçao.py`
  Para mudar dano, alcance, velocidade ou vida, prefira alterar os valores em `src/config.py`.

- Mapa, estrada e interface: `src/funcoes.py`
  Para mudar o desenho do mapa ou os textos da tela, edite `desenhar_mapa`, `desenhar_interface` e `desenhar_fim_de_jogo`.

- Custos, moedas, vidas, cores e caminho dos inimigos: `src/config.py`
  Para mudar o preco do guerreiro ou arqueiro, edite `TIPOS_PERSONAGENS`. Para mudar o caminho dos slimes, edite `CAMINHO_ESTRADA` e `WAYPOINTS`.

- Recorde salvo em arquivo: `src/dados.py` e `data/recorde.txt`
  Para trocar o tipo de dado salvo, ajuste `salvar_recorde`, `carregar_recorde` e o valor enviado em `src/jogo.py`.

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
