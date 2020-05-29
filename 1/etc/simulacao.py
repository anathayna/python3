#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:33:28 2020

@author: anathayna
"""


import sys
import pygame
import random
from threading import Thread
import predadorpresa

# Parâmetros do tamanho da simulação (cada célula em 5 pixels)
random.seed(None)
tamanho = largura, altura = 500, 500
largura_tabuleiro = largura/5
altura_tabuleiro = altura/5
parado = False

# Estes são os códigos de cor que o pygame usa ((R,G,B))
preto = ((0,0,0))
vermelho = ((255,0,0))
azul = ((0,0,255))
cores = [preto, vermelho, azul]

pygame.init()
tela = pygame.display.set_mode(tamanho)
pp = predadorpresa.Mapa()

# Pinta um quadrado de 3x3 pixels para cada nó
#  como cada nó tem 5 pixels, 2 pixels ficam para a borda da célula
def pintar(x, y, num_cor):
    tela.set_at((x, y), cores[num_cor])
    tela.set_at((x + 1, y), cores[num_cor])
    tela.set_at((x, y + 1), cores[num_cor])
    tela.set_at((x + 1, y + 1), cores[num_cor])
    tela.set_at((x + 2, y), cores[num_cor])
    tela.set_at((x, y + 2), cores[num_cor])
    tela.set_at((x + 2, y + 2), cores[num_cor])
    tela.set_at((x + 2, y + 1), cores[num_cor])
    tela.set_at((x + 1, y + 2), cores[num_cor])

# Pinta as espécies em cada ponto do tabuleiro
def pintar_mapa(tabuleiro):
    pa = pintar
    tamanho = len(tabuleiro)
    for x in range(0, tamanho):
        for y in range(0, tamanho):
            pa(x*5, y*5, tabuleiro[x][y].especie)

# Loop de jogo, pinta o mapa e calcula o próximo turno
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            parado = True
            sys.exit(0)
    pintar_mapa(pp.get_tabuleiro())
    pygame.display.flip()
    pp.turno()