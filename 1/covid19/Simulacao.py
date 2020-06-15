import matplotlib.pyplot as plt
import sys
import pygame
import random
import COVID19

# Parâmetros do tamanho da simulação (cada célula em 5 pixels)

# Proporção da janela & tabuleiro 1/7
proporcaoJanela = 7
proporcaoTabuleiro = 7

# taxa de mortalidade: 1% a 12%
# ------ isolamento: entre 0 e 100
# (cenários: quarentena, lockdown)

# 1400 -> 40%
# 600 -> 60%

#### Simulação 1 -> Praticamente sem isolamento
#### Simulação 2 -> Com isolamento
#### Simulação 3 -> Com isolamento e lockDown

taxaDeMortalidade = None
taxaDeIsolamento = None
barreira = None
simulacao = None

print("""
          O modelo desenvolvido trabalha com a ideia de uma infecção populacional, 
          a partir de um paciente Zero inserido em seu meio. O número de indivíduos 
          é alterado conforme a escolha do tipo de simulação (Sem isolamento, com 
          isolamento e Lockdown). Ao final da simulação, é gerado um gráfico demonstrando 
          as curvas de infecção, mortes e recuperação. A partir das simulações e análises, 
          é possível tomar as devidas medidas preventivas e essenciais  para conter uma 
          possível epidemia.
          
      """)

while True:
    print("""
          Selecione a simulação desejada e a taxa de mortalidade (%)
          
          1 - Simulação Sem isolamente
          2 - Simulação Isolamente de 60%
          3 - Simulação Lockdown e Distânciamento Social
          
          0 a 100 - Mortalidade
          
          """)
    print("opção da simulação: ")
    x = input()
    print("taxa de mortalidade: ")
    y = input()
    
          
    if x.isdigit() and y.isdigit():
        option = int(x)
        taxa = int(y)
        
        if option > 0 and option < 4 and taxa >= 0 and taxa <= 100:
            taxaDeMortalidade = taxa
            
            if option == 1:
                simulacao = "SEM ISOLAMENTO"
                taxaDeIsolamento = 1500
                barreira = 1
            
            elif option == 2:
                simulacao = "ISOLAMENTO DE 60%"
                taxaDeIsolamento = 350
                barreira = 1
            
            elif option == 3:
                simulacao = "LOCKDOWN E DISTÂNCIAMENTO SOCIAL"
                taxaDeIsolamento = 400
                barreira = 90
            
            break
            
        else:
            print("opção inválida")
              
    else:
        print("opção inválida")


random.seed(None)
tamanho = largura, altura = 100*proporcaoJanela, 100*proporcaoJanela+90
tamanhoTabuleiro = largura, altura = largura/proporcaoTabuleiro, altura/proporcaoTabuleiro
parado = False

# Estes são os códigos de cor que o pygame usa ((R,G,B))
preto = ((0,0,0))
vermelho = ((255,0,0))
azul = ((0,0,255))
verde = ((0,255,0))
white = ((255,255,255))
cores = [preto, azul, vermelho, verde, white, preto]

pygame.init()
tela = pygame.display.set_mode(tamanho)
ppm = COVID19.Mapa(taxaDeIsolamento, barreira)

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

# Pinta os indivíduo em cada ponto do tabuleiro
def pintar_mapa(tabuleiro):
    pa = pintar
    tamanho = len(tabuleiro)
    for x in range(0, tamanho):
        for y in range(0, tamanho):
            pa(x*proporcaoJanela, y*proporcaoJanela, tabuleiro[x][y].individuo)

# Loop de jogo, pinta o mapa e calcula o próximo turno
myfont = pygame.font.SysFont("monospace", 21)

sucetiveisArray = []
infectadosArray = []
mortosArray = []
recuperadosArray = []
tempoArray = []
tempo = 0
plotGraf = True
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            parado = True
            sys.exit(0)
    pintar_mapa(ppm.get_tabuleiro())
    pygame.display.flip()
    turno = ppm.turno(taxaDeMortalidade)
    label0 = myfont.render("SUSCETIVEIS: " + str(len(turno[0])) + "   ", 1, (255,255,0), (0,0,0))
    label1 = myfont.render("INFECTADOS: " + str(len(turno[1])) + "   ", 1, (255,255,0), (0,0,0))
    label2 = myfont.render("MORTOS: " + str(len(turno[2])) + "   ", 1, (255,255,0), (0,0,0))
    label3 = myfont.render("RECUPERADOS: " + str(len(turno[3])) + "   ", 1, (255,255,0), (0,0,0))
    if tempo == 0:
        label4 = myfont.render("QUANT. DE INDIVIDUOS: " + str(turno[4]), 1, (255,255,0), (0,0,0))
    label5 = myfont.render("TAXA DE MORTALIDADE: " + str(taxaDeMortalidade) + "%", 1, (255,255,0), (0,0,0))
    label6 = myfont.render("SIMULAÇÃO SELECIONADA: " + str(simulacao), 1, (255,255,0), (0,0,0))

    tela.blit(label0, (10, 100*proporcaoJanela+1))
    tela.blit(label1, (10, 100*proporcaoJanela+21))
    tela.blit(label3, (10, 100*proporcaoJanela+41))
    tela.blit(label2, (10, 100*proporcaoJanela+61))
    tela.blit(label4, (200, 100*proporcaoJanela+1))
    tela.blit(label5, (200, 100*proporcaoJanela+21))
    tela.blit(label6, (200, 100*proporcaoJanela+61))

    if len(turno[1]) == 0 and plotGraf:
        graf = plt.figure(facecolor='w')
        plotGraf = False
        plt.title('Simulação de Contaminação - COVID19')
        plt.xlabel('Tempo/dias')
        plt.ylabel('Indivíduos')
        plt.plot(tempoArray, sucetiveisArray, 'b', label='Suscetíveis')
        plt.plot(tempoArray, infectadosArray, 'r', label='Infectados')
        plt.plot(tempoArray, recuperadosArray, 'g', label='Recuperados com imunidade')
        plt.plot(tempoArray, mortosArray, 'k', label='Mortos')
        plt.legend()
        plt.show()
        graf.savefig('SIMULACAO ' + str(simulacao) + '.png')
    else:
        tempoArray.append(tempo)
        sucetiveisArray.append(len(turno[0]))
        infectadosArray.append(len(turno[1]))
        mortosArray.append(len(turno[2]))
        recuperadosArray.append(len(turno[3]))
        tempo += 1
