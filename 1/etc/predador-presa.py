#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:33:25 2020

@author: anathayna
"""


import random
import sys
import copy
random.seed(None)

#CLASSE NÓ
# Cada nó é formado por:
#   Um indivíduo de uma espécie, que pode ser:
#       - 1 = Predador
#       - 2 = Presa
#       - 0 = Nenhum dos dois, é espaço vazio
#   A quantidade de vida desse indivíduo
#   A posição (x, y) deste nó no tabuleiro
class No:

    especie = None
    x = None
    y = None
    vida = None

    def __init__(self, espec=None):
        if espec is not None:
            self.especie = espec
        else:
            self.especie = 0
        self.x = None
        self.y = None
        self.vida = self.especie*2

    # Define a localização deste Nó no mapa
    def set_localizacao(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    # Define a espécie que este Nó representará
    def set_especie(self, num):
        if num == 0 or num == 1 or num == 2:
            self.especie = num
            if num is 0:  # Nada
                self.vida = None
            if num is 1:  # Predador
                self.vida = 2
            if num is 2:  # Presa
                self.vida = 4
        else:
            sys.stderr.write('A espécie não está correta, não faça contas com ela.')
            self.especie = 0

    # Algum indivíduo se moveu para este Nó
    def mover_aqui(self, especie, vida):
        if especie == 0 or especie == 1 or especie == 2:
            self.especie = especie
            if especie is 0:  # Nada
                self.vida = vida
            if especie is 1:  # Predador
                self.vida = vida
            if especie is 2:  # Presa
                self.vida = vida
        else:
            sys.stderr.write('A espécie não está correta, não faça contas com ela.')
            self.especie = 0

    # Este Nó é uma presa e ela acabou de ser devorada :(
    # seguindo as regras no método verifica_vizinhos
    def presa_comida(self):
        self.especie = 1

    # Alguma presa em um Nó adjacente se reproduziu \o/ e este Nó contém a sua prole
    # seguindo as regras no método verifica_vizinhos
    def presa_reproduz(self):
        self.especie = 2
        self.vida = 1

#CLASSE MAPA
# Representa o mapa onde acontecerá a simulação
# O mapa é representado por um tabuleiro de células de tamanho (altura x largura)
class Mapa:
    altura = 100
    largura = 100
    tabuleiro = []

    # Construtor da classe
    # Ao criar um novo mapa, o prenchemos aleatoriamente
    def __init__(self):
        presas = 0
        predadores = 0
        vazios = 0
        #Preenche cada célula do tabuleiro aleatoriamente entre Predador(1), Presa(2) ou espaço vazio(0)
        for x in range(self.largura):
            linha = []
            for y in range(self.altura):
                i = random.randint(0, 10)
                if i <= 7:
                    linha.append(No(2))
                    presas += 1
                elif i <= 9:
                    linha.append(No(1))
                    predadores += 1
                else:
                    linha.append(No(0))
                    vazios += 1

            self.tabuleiro.append(linha)

        print('Mapa criado')
        print('Presas: ', presas)
        print('Predadores: ', predadores)
        print('Espaços vazios: ', vazios)
        print('Largura: ', len(self.tabuleiro))
        print('Altura da linha 5: ', len(self.tabuleiro[5]))

    def get_tabuleiro(self):
        return self.tabuleiro

    # A cada turno de jogo, processa cada célula do tabuleiro e seus vizinhos
    def turno(self):
        tab = self.tabuleiro
        [[self.verifica_vizinhos(x, y, tab[x][y]) for y in range(0, self.altura)] for x in range(0, self.largura)]

    # Retorna os vizinhos de um nó. 
    # Se o nó estiver na borda, devolve os nós que estiverem em volta dele
    def get_vizinhos(self, x, y):
        cima = self.tabuleiro[x][(y - 1) % self.altura]
        cima_direita = self.tabuleiro[(x + 1) % self.largura][(y - 1) % self.altura]
        direita = self.tabuleiro[(x + 1) % self.largura][y]
        baixo_direita = self.tabuleiro[(x + 1) % self.largura][(y + 1) % self.altura]
        baixo = self.tabuleiro[x][(y + 1) % self.altura]
        baixo_esquerda = self.tabuleiro[(x - 1) % self.largura][(y + 1) % self.altura]
        esquerda = self.tabuleiro[(x - 1) % self.largura][y]
        cima_esquerda = self.tabuleiro[(x - 1) % self.largura][(y - 1) % self.altura]

        vizinhos = [cima, cima_direita, direita, baixo_direita, baixo, baixo_esquerda, esquerda, cima_esquerda]
        return vizinhos

    # AUTOMATO CELULAR DO MODELO PREDADOR PRESA
    # Função onde a magia acontece...
    # O mundo é uma grade de células, com 3 possibilidades: 
    #       Predador (Vermelho, 1), Presa (Verde, 2) ou Vazio (Preto, 0).
    # Tanto o predador quanto a presa têm uma vida definida, que muda com o tempo.
    #
    # A simulação funciona em etapas, com as seguintes regras:
    #    -Para a presa:
    #        -Tenta se mover em uma direção aleatória.
    #        -Vida aumenta.
    #        -Quando a vida atinge um limite:
    #           -Eles se reproduzirão, criando uma nova "presa"
    #           -Sua vida é redefinida para 1
    #    -Para o predador:
    #        -Tenta se mover em uma direção aleatória.
    #        -Vida aumenta.
    #        -Quando a vida atinge 0, eles morrem e se transformam em "Nada".
    #        -Se o quadrado adjacente for uma presa:
    #            -Eles vão comer, transformando-o em um "predador" (se reproduzindo)
    #            -Sua vida aumentará com a quantidade de vida que a presa consumida tinha
    def verifica_vizinhos(self, x, y, no):
        # Se o nó estiver vazio, nenhuma verificação será realizada
        if no.especie is 0:
            return

        if no.especie is 1:
            # Este nó um predador. Procura presas, se não houver presa reduzir a saúde ou morrer
            vizinhos = self.get_vizinhos(x, y)
            presas = []
            vazios_ = []

            for viz in vizinhos:
                if viz.especie is 2:
                    presas.append(viz)
                if viz.especie is 0:
                    vazios_.append(viz)
            tam_vazios = len(vazios_)

            if len(presas) is 0:
                if no.vida > 0 and tam_vazios > 0:
                    no.vida -= 1
                    vazios_[random.randint(0, (tam_vazios-1))].mover_aqui(1, no.vida)
                    no.set_especie(0)
                    return

            else:
                alvo = presas[random.randint(0, (len(presas)-1))]
                if no.vida >= alvo.vida:
                    alvo.presa_comida()

            if no.vida is None or no.vida <= 0:
                no.especie = 0
                return

        if no.especie is 2:
            # Este nó tem uma presa. Verifica se há superpopulação e a altera a saúde
            vizinhos = self.get_vizinhos(x, y)
            espacos_vazios = []
            for viz in vizinhos:
                if viz.especie is 0:
                    espacos_vazios.append(viz)
            cont = len(espacos_vazios)
            if cont >= 7 or cont < 1:
                no.vida -= 2
            if no.vida is None or no.vida is 0:
                no.especie = 0
                return
            if no.vida > 6 and len(espacos_vazios) >= 1:
                espacos_vazios[random.randint(0, (len(espacos_vazios))-1)].presa_reproduz()
                no.vida = 4
                return
            no.vida += 1