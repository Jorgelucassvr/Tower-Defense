# Nome do Jogo

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

Descreva brevemente a ideia principal do jogo.

Exemplo: No jogo, os inimigos aparecem em ondas e seguem um caminho até a base do jogador. O objetivo é impedir que eles cheguem ao final do percurso. Para isso, o jogador posiciona torres pelo cenário. Cada torre ataca automaticamente os inimigos que passam perto dela.
Conforme o jogador derrota os inimigos, ele ganha moedas. Essas moedas podem ser usadas para comprar novas torres ou melhorar as torres já existentes. A cada nova onda, os inimigos ficam mais fortes ou aparecem em maior quantidade

> O jogo consiste em controlar um personagem que deve coletar moedas e evitar obstáculos. O jogador ganha pontos ao coletar itens e perde vidas ao colidir com obstáculos. A partida termina quando o tempo acaba ou quando o jogador perde todas as vidas.

## Objetivo do jogador

Explique o que o jogador precisa fazer para vencer ou avançar no jogo.

Exemplo: O objetivo do jogo é sobreviver ao maior número possível de ondas, protegendo a base e usando bem as moedas para posicionar e melhorar as torres.

> O objetivo é coletar a maior quantidade possível de itens antes que o tempo acabe, evitando colisões com os obstáculos.

## Regras do jogo

Liste as principais regras do jogo.

Exemplo: Regras do jogo
O jogador começa com uma quantidade inicial de moedas.
As torres só podem ser colocadas em locais permitidos no mapa.
Os inimigos seguem um caminho fixo até a base.
Cada inimigo que chega à base faz o jogador perder vida.
O jogador perde se a vida da base chegar a zero.
O jogador ganha moedas ao derrotar inimigos.
As moedas podem ser usadas para comprar ou melhorar torres.
O jogo fica mais difícil a cada onda de inimigos

- O jogador se movimenta usando as setas do teclado.
- Cada item coletado aumenta a pontuação.
- Colidir com um obstáculo reduz a quantidade de vidas.
- A partida termina quando o jogador perde todas as vidas ou quando o tempo acaba.

## Controles

Informe as teclas ou comandos utilizados no jogo.

Exemplo: Os controles do jogo são simples:
Mouse: usado para selecionar torres e posicioná-las no mapa.
Clique esquerdo: escolhe uma torre ou confirma o local onde ela será colocada.
Clique em uma torre: abre as opções de melhoria ou venda.
Botão “Iniciar onda”: começa a próxima onda de inimigos.
Tecla ESC: cancela a seleção de uma torre.
Tecla P: pausa o jogo.
Tecla R: reinicia a partida.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
