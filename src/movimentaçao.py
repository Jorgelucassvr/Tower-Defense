import math

import pygame

from src.config import CINZA


class Inimigo:
    # Esta classe controla a posicao e a movimentacao do inimigo.
    def __init__(self, waypoints, velocidade=140, raio=14):
        self.waypoints = waypoints
        self.velocidade = velocidade
        self.raio = raio
        self.resetar()

    def resetar(self):
        # Coloca o inimigo novamente no primeiro ponto do caminho.
        self.x = float(self.waypoints[0][0])
        self.y = float(self.waypoints[0][1])
        self.indice_alvo = 1
        self.ativo = True

    def atualizar(self, dt):
        # Se nao houver mais pontos, o inimigo para de se mover.
        if not self.ativo or self.indice_alvo >= len(self.waypoints):
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
        # Desenha o inimigo como um circulo cinza.
        pygame.draw.circle(tela, CINZA, (int(self.x), int(self.y)), self.raio)
