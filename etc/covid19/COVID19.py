import random
import sys
random.seed(None)

#CLASSE NÓ
# Cada nó é formado por:
#   Um indivíduo, que pode ser:
#       - 1 = Suscetível
#       - 2 = Infectado
#       - 3 = Recuperado
#       - 0 = Nenhum, é espaço vazio, ou seja, Morto
#   A quantidade de vida desse indivíduo
#   A posição (x, y) deste nó no tabuleiro
class No:

    individuo = None
    x = None
    y = None
    vida = None

    def __init__(self, indiv=None):
        if indiv is not None:
            self.individuo = indiv
        else:
            self.individuo = 0
        self.x = None
        self.y = None
        self.vida = self.individuo*2

    # Define a localização deste Nó no mapa
    def set_localizacao(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    # Define a espécie que este Nó representará
    def set_especie(self, num):
        if num == 0 or num == 1 or num == 2:
            self.individuo = num
            if num == 0:  # Nada/Morto
                self.vida = None
            if num == 1:  # Suscetível
                self.vida = 2
            if num == 2:  # Infectado
                self.vida = 2
        else:
            sys.stderr.write('A espécie não está correta, não faça contas com ela.')
            self.individuo = 0

    # Algum indivíduo se moveu para este Nó
    def mover_aqui(self, individuo, vida):
        if individuo == 0 or individuo == 1 or individuo == 2 or individuo == 3:
            self.individuo = individuo
            if individuo == 0:  # Nada
                self.vida = vida
            if individuo == 1:  # Suscetível
                self.vida = vida
            if individuo == 2:  # Infectado
                self.vida = vida
            if individuo == 3:  # Recuperado
                self.vida = vida
        else:
            sys.stderr.write('A espécie não está correta, não faça contas com ela.')
            self.individuo = 0

    # Este Nó é uma pessoa suscetível e ela acabou de ser infectada :(
    # seguindo as regras no método verifica_vizinhos
    def pessoa_se_infecta(self):
        self.individuo = 2

#CLASSE MAPA
# Representa o mapa onde acontecerá a simulação
# O mapa é representado por um tabuleiro de células de tamanho (altura x largura)
class Mapa:
    altura = 100
    largura = 100
    tabuleiro = []  
    
    # Construtor da classe
    # Ao criar um novo mapa, o prenchemos aleatoriamente
    def __init__(self, isolamento, barreira):
        suscetiveis = 0
        infectados = 0
        vazios = 0
        #Preenche cada célula do tabuleiro aleatoriamente entre Suscetível(1), Infectado(2) ou espaço vazio(0)
        for x in range(self.largura):
            linha = []
            for y in range(self.altura):
                i = random.randint(0, 20000)
                if y == 0 or y == 99 or x == 0 or x == 99:
                    linha.append(No(4))
                elif y == 50 and x < barreira:
                    linha.append(No(4))
                elif x == 50 and y == 75:
                    linha.append(No(2))
                    infectados += 1
                elif i <= isolamento:
                    linha.append(No(1))
                    suscetiveis += 1
                else:
                    linha.append(No(0))
                    vazios += 1

            self.tabuleiro.append(linha)

        print('Mapa criado')
        print('Suscetiveis: ', suscetiveis)
        print('Infectados: ', infectados)
        print('Espaços vazios: ', vazios)

    def get_tabuleiro(self):
        return self.tabuleiro

    # A cada turno de jogo, processa cada célula do tabuleiro e seus vizinhos
    def turno(self, taxaDeMortalidade):
        suscetiveis = []
        infectados = []
        mortos = []
        recuperados = []
        individuos = 0
        tab = self.tabuleiro
        [[self.verifica_vizinhos(x, y, tab[x][y], taxaDeMortalidade) for y in range(0, self.altura)] for x in range(0, self.largura)]
        for y in range(0, self.altura):
            for x in range(0, self.largura):
                no = tab[x][y]
                if no.individuo == 1:  # suscetíveis
                    suscetiveis.append(no)
                    individuos += 1
                if no.individuo == 2:  # infectados
                    infectados.append(no)
                    individuos += 1
                if no.individuo == 3:  # recuperados
                    recuperados.append(no)
                if no.individuo == 5:  # mortos
                    mortos.append(no)
        conts = [suscetiveis, infectados, mortos, recuperados, individuos]
        return conts
        

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

     # AUTOMATO CELULAR DO MODELO COVID-19 
     # O mundo é uma grade de células, com 3 possibilidades: 
     #       Suscetível (Azul, 1), Infectado (Vermelho, 2) ou Recuperado (Verde, 0).
     # Tanto o Suscetível quanto o Infectado têm uma vida definida, que muda com o tempo.
     #
     # A simulação funciona em etapas, com as seguintes regras:
     #    -Para o Suscetível:
     #        -Se move em uma direção aleatória.
     #    -Para o Infectado:
     #        -Se move em uma direção aleatória.
     #        -O tempo de infecção vai diminuindo.
     #        -Quando a infecção atinge o fim, eles se recuperam ou morrem dependendo da taxa de mortalidade.
     #        -Se o quadrado adjacente for uma suscetível:
     #           -Eles contagiam um suscetível, criando um novo "infectado" (se multiplicando)
     #    -Para o Recuperado:
     #        -Se move em uma direção aleatória.
     #        -Não pode ser infectado novamente
    
    def verifica_vizinhos(self, x, y, no, taxaDeMortalidade):
        # Se o nó estiver vazio, nenhuma verificação será realizada
        if no.individuo == 0:
            return

        if no.individuo == 1:
            # Este nó ' um índividuo suscetível'
            vizinhos = self.get_vizinhos(x, y)
            vazios = []
            for viz in vizinhos:
                if viz.individuo == 0:
                    vazios.append(viz)
            tam_vazios = len(vazios)
            if tam_vazios > 0:
                vazios[random.randint(0, (tam_vazios-1))].mover_aqui(1, no.vida)
                no.set_especie(0)
                return

        if no.individuo == 2:
            no.vida += 1
            # Este nó é 'um índividuo infectado'. Procura suscetíveis e infecta
            vizinhos = self.get_vizinhos(x, y)
            vazios = []
            suscetiveis = []
            for viz in vizinhos:
                if viz.individuo == 0:
                    vazios.append(viz)
                if viz.individuo == 1:
                    suscetiveis.append(viz)
            tam_vazios = len(vazios)
            if no.vida >= 200:
                i = random.randint(0, 100)
                if i <= taxaDeMortalidade:
                    no.individuo = 5
                    return
                else:
                    no.individuo = 3
                    return
            if len(suscetiveis) == 0:
                if tam_vazios > 0:
                    vazios[random.randint(0, (tam_vazios-1))].mover_aqui(2, no.vida)
                    no.set_especie(0)
                    return
            else:
                alvo = suscetiveis[random.randint(0, (len(suscetiveis)-1))]
                alvo.pessoa_se_infecta()
            

        if no.individuo == 3:
            # Este nó 'um índividuo recuperado'
            vizinhos = self.get_vizinhos(x, y)
            vazios = []
            for viz in vizinhos:
                if viz.individuo == 0:
                    vazios.append(viz)
            tam_vazios = len(vazios)
            if tam_vazios > 0:
                vazios[random.randint(0, (tam_vazios-1))].mover_aqui(3, no.vida)
                no.set_especie(0)
                return
