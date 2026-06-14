import math

import pygame

from src.config import (
    LARANJA,
    MOEDAS_POR_ELIMINACAO,
    PONTOS_INIMIGO_SUPREMO,
    PONTOS_POR_SLIME,
    PRETO,
    ROXO,
    TIPOS_PERSONAGENS,
    VERDE_ESCURO,
    VERDE_SLIME,
    VERDE_SUPREMO,
    VERMELHO,
)


class Inimigo:
    # Esta classe controla o slime: posicao, vida e movimento pelo caminho.
    def __init__(
        self,
        waypoints,
        atraso=0,
        velocidade=85,
        raio=15,
        vida=45,
        tipo="slime",
    ):
        self.waypoints = waypoints
        self.velocidade = velocidade
        self.raio = raio
        self.vida_maxima = vida
        self.vida = vida
        self.tipo = tipo
        self.cor = VERDE_SUPREMO if tipo == "supremo" else VERDE_SLIME
        self.moedas = MOEDAS_POR_ELIMINACAO
        self.pontos = PONTOS_INIMIGO_SUPREMO if tipo == "supremo" else PONTOS_POR_SLIME
        self.x = float(waypoints[0][0] - atraso)
        self.y = float(waypoints[0][1])
        self.indice_alvo = 1
        self.ativo = True
        self.chegou_ao_fim = False

    def receber_dano(self, dano):
        # Diminui a vida do slime quando ele e atingido.
        self.vida -= dano
        if self.vida <= 0:
            self.ativo = False

    def atualizar(self, dt):
        # Se nao houver mais pontos, o inimigo para de se mover.
        if not self.ativo or self.indice_alvo >= len(self.waypoints):
            if self.indice_alvo >= len(self.waypoints):
                self.chegou_ao_fim = True
            self.ativo = False
            return

        alvo_x, alvo_y = self.waypoints[self.indice_alvo]
        delta_x = alvo_x - self.x
        delta_y = alvo_y - self.y
        distancia = math.hypot(delta_x, delta_y)
        passo = self.velocidade * dt

        # Quando o inimigo esta perto do alvo, ele encaixa no ponto e muda de direcao.
        if distancia <= passo:
            self.x = alvo_x
            self.y = alvo_y
            self.indice_alvo += 1
            return

        # Normaliza a direcao para mover com velocidade constante.
        direcao_x = delta_x / distancia
        direcao_y = delta_y / distancia

        self.x += direcao_x * passo
        self.y += direcao_y * passo

    def desenhar(self, tela):
        # Desenha o inimigo como uma bolinha verde; o supremo e maior e mais escuro.
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, VERDE_ESCURO, (int(self.x), int(self.y)), self.raio, 2)
        self.desenhar_barra_vida(tela)

    def desenhar_barra_vida(self, tela):
        # Mostra a vida do slime acima da cabeca.
        largura = 54 if self.tipo == "supremo" else 36
        altura = 6
        x_barra = int(self.x - largura / 2)
        y_barra = int(self.y - self.raio - 12)
        proporcao = max(self.vida, 0) / self.vida_maxima

        pygame.draw.rect(tela, VERMELHO, (x_barra, y_barra, largura, altura))
        pygame.draw.rect(tela, VERDE_ESCURO, (x_barra, y_barra, largura * proporcao, altura))
        pygame.draw.rect(tela, PRETO, (x_barra, y_barra, largura, altura), 1)


class Personagem:
    # Representa uma unidade colocada pelo jogador: guerreiro ou arqueiro.
    def __init__(self, tipo, posicao):
        self.tipo = tipo
        self.x, self.y = posicao
        self.dados = TIPOS_PERSONAGENS[tipo]
        self.cooldown = 0

    def proximo_tipo(self):
        # Define para qual versao o personagem evolui.
        evolucoes = {
            "guerreiro": "guerreirolv2",
            "arqueiro": "arqueirolv2",
        }
        return evolucoes.get(self.tipo)

    def pode_evoluir(self):
        # Retorna True apenas para personagens que ainda nao evoluiram.
        return self.proximo_tipo() is not None

    def custo_evolucao(self):
        # Usa o custo do tipo evoluido como preco da melhoria.
        proximo = self.proximo_tipo()
        if proximo is None:
            return 0
        return TIPOS_PERSONAGENS[proximo]["custo"]

    def evoluir(self):
        # Troca os dados do personagem pela versao mais forte.
        proximo = self.proximo_tipo()
        if proximo is None:
            return False

        self.tipo = proximo
        self.dados = TIPOS_PERSONAGENS[self.tipo]
        return True

    def mouse_sobre_personagem(self, posicao_mouse):
        # Verifica se o mouse esta sobre o circulo do personagem.
        distancia = math.hypot(posicao_mouse[0] - self.x, posicao_mouse[1] - self.y)
        return distancia <= 22

    def botao_evolucao(self):
        # Botao pequeno que aparece acima do personagem quando o mouse passa por ele.
        return pygame.Rect(int(self.x - 45), int(self.y - 55), 90, 28)

    def mostrar_botao_evolucao(self, posicao_mouse):
        # Mantem o botao visivel ao passar pelo personagem ou pelo proprio botao.
        if not self.pode_evoluir():
            return False
        return self.mouse_sobre_personagem(posicao_mouse) or self.botao_evolucao().collidepoint(posicao_mouse)

    def atualizar(self, inimigos, dt):
        # Controla o intervalo entre ataques da unidade.
        if self.cooldown > 0:
            self.cooldown -= dt

        alvo = self.encontrar_alvo(inimigos)
        if alvo and self.cooldown <= 0:
            alvo.receber_dano(self.dados["dano"])
            self.cooldown = self.dados["tempo_ataque"]

    def encontrar_alvo(self, inimigos):
        # O arqueiro ataca em circulo; o guerreiro ataca apenas a frente.
        for inimigo in inimigos:
            if not inimigo.ativo:
                continue

            distancia = math.hypot(inimigo.x - self.x, inimigo.y - self.y)
            if self.tipo.startswith("arqueiro") and distancia <= self.dados["alcance"]:
                return inimigo

            esta_na_frente = inimigo.x >= self.x and abs(inimigo.y - self.y) <= 45
            if self.tipo.startswith("guerreiro") and esta_na_frente and distancia <= self.dados["alcance"]:
                return inimigo

        return None

    def desenhar(self, tela, fonte):
        # Desenho visual do personagem e o seu alcance.
        cor = LARANJA if self.tipo.startswith("guerreiro") else ROXO
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), 18)
        pygame.draw.circle(tela, PRETO, (int(self.x), int(self.y)), 18, 2)

        if self.tipo.startswith("arqueiro"):
            pygame.draw.circle(tela, PRETO, (int(self.x), int(self.y)), self.dados["alcance"], 1)
        else:
            area_frente = pygame.Rect(self.x, self.y - 45, self.dados["alcance"], 90)
            pygame.draw.rect(tela, PRETO, area_frente, 1)

        letra = self.letra()
        texto = fonte.render(letra, True, PRETO)
        tela.blit(texto, texto.get_rect(center=(self.x, self.y)))

    def desenhar_botao_evolucao(self, tela, fonte):
        # Desenha o botao de evolucao quando ele estiver ativo.
        if not self.pode_evoluir():
            return

        botao = self.botao_evolucao()
        pygame.draw.rect(tela, (255, 245, 180), botao, border_radius=8)
        pygame.draw.rect(tela, PRETO, botao, width=2, border_radius=8)
        texto = fonte.render(f"Up ${self.custo_evolucao()}", True, PRETO)
        tela.blit(texto, texto.get_rect(center=botao.center))

    def letra(self):
        # Mostra uma letra curta dentro do personagem.
        if self.tipo == "guerreiro":
            return "G"
        if self.tipo == "guerreirolv2":
            return "G2"
        if self.tipo == "arqueiro":
            return "A"
        return "A2"
