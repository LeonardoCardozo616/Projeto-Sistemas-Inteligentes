import random
import csv
#Algoritmo Genetico
#gera uma população de cromossomos
def gera_populacao(tam):
    populacao = [] #cria lista pop
    for i in range(tam): #loop de 0 até tam da pop
        genes = [0, 1] #genes de cada cromossomo podem ter valores 0 ou 1
        cromossomo = [] #cada cromossomo é uma lista que será preenchida por 0(item fora) e 1(item pego)
        for i in range(len(Itens)): #loop de 0 até qtd de itens
            cromossomo.append(random.choice(genes)) #adiciona ao cromossomo um gene(de valor 0 ou 1, escolhido aleatoriamente)
        populacao.append(cromossomo) #adiciona o cromossomo a população
    #print(f"Populacao aleatoria de {tam} cromossomos gerada") #print de contexto
    return populacao # retorna a populção

#calcula o fitness de um cromossomo
def calcula_fit(cromossomo): #recebe o cromossomo o qual sera calculado 
    cromo_peso = 0 #peso e valor do cromossomo inicializam como 0
    cromo_valor = 0
    for i in range(len(cromossomo)): #loop de pós 0 até qtd de genes no cromossomo()
        if cromossomo[i] == 1: #caso o valor do gene seja 1(item na mochila)
            cromo_peso += Itens[i][0] #soma o peso do item ao peso total do cromossomo atual
            cromo_valor += Itens[i][1] #soma o valor do item ao valor total do cromossomo atual
    if cromo_peso > W: #caso o peso total do cromossomo extrapole o peso máximo da mochila, retorna valor 0
        return 1
    else: #caso contrário, retorna o valor do cromossomo atual
        return cromo_valor 

   
#escolhe pais para o crossover de forma "aleatória"    
def pega_cromossomo(populacao): 
    valor_fit = [] #inicializa uma lista com o valor do fit de cada cromossomo
    pais = []
    for cromossomo in populacao: #para cada cromossomo na população ele adiciona seu fitness à lista valor_fit
        pais.append(cromossomo)
        valor_fit.append(calcula_fit(cromossomo))
    #print("Valor fits: ", sum(valor_fit)) #<- print explicação
    #print("valor fit", valor_fit) #<- print explicação
    if sum(valor_fit) ==0: #teste para verificar se uma solução é gerada, erros ocorrem baseados no tamanho da população
        print("Nenhuma solucao possivel gerada")
        exit(1)
    else:
        valor_fit = [float(i)/sum(valor_fit) for i in valor_fit] # a lista valor fit passa a receber a divisao do (fit calculado)/(soma de todos os fits) ex (23/61)
        #print(valor_fit) #<- print explicação
        #estes valores servirão para a randomização valorada/pesada, ou seja, cada cromossomo possui um peso que influencia em sua probabilidade de ser escolhido
        
        pai1 = random.choices(pais, weights=valor_fit, k=1)[0] #os pais são escolhidos aleatoriamente, no entanto, quanto maior/melhor seu fit
        #não permite dois pais iguais
        pai1_pos=pais.index(pai1)
        valor_fit.pop(pai1_pos)
        pais.remove(pai1)
        
        pai2 = random.choices(pais, weights=valor_fit, k=1)[0] #maior a chance de serem escolhidos
        
        #print(f"Pais escolhidos{pai1} e {pai2}") #<- print explicação
        return pai1, pai2

#aqui é onde realizamos o crossover
def crossover(pai1,pai2):
    ponto_cross = random.randint(0, len(Itens)-1) #o ponto onde será realizado o crossover é definido aleatoriamente, podendo variar do item 0 até a qtd de itens
    #os itens até do ponto de cross permanecerão inalterados
    #print(ponto_cross) #<- print explicação
    #print(f"filhos antes do cross{pai1} e {pai2}") #<- print explicação
    filho1 = pai1[0:ponto_cross] + pai2[ponto_cross:] # soma os genes do pai1 até o ponto de cross com os genes do pai2 após        
    filho2 = pai2[0:ponto_cross] + pai1[ponto_cross:] #linha acima porém invertido pai2 + pai1           
    #print(f"filhos após do cross{filho1} e {filho2}") #<- print explicação
    
    return filho1, filho2 #retorna os filhos

#função onde é realizada a mutação
def mutacao(cromossomo): 
    #print("Ocorreu uma mutação") #<- print explicação
    #print(f"Cromossomo pre-muta{cromossomo}") #<- print explicação
    ponto_muta = random.randint(0,len(Itens)-1) #o gene onde será realizado a mutação é definido aleatoriamente, podendo variar do item 0 até a qtd de itens
    if cromossomo[ponto_muta] == 0: #caso o gene do ponto de mutação seja 0, será trocado para 1 e vice versa
        cromossomo[ponto_muta] = 1
    else:
        cromossomo[ponto_muta] = 0
    #print(f"Cromossmo pos-muta{cromossomo}") #<- print explicação
    return cromossomo

#Aqui, escolhemos a melhor resposta obtida
def escolher_melhor(populacao):
    valor_fit = [] #inicializa uma lista valor fit
    for cromossomo in populacao:
        valor_fit.append(calcula_fit(cromossomo)) #calcula o fitness de todos os cromossomos
    #print(valor_fit) #<- print explicação
    valor_max = max(valor_fit) #recebe o maior valor obtido
    #print(f"vmx {valor_max}") #<- print explicação
    pos_max = valor_fit.index(valor_max) #recebe a posição do cromossomo que obteve a maior pontuação
    #print(f"Pos {pos_max}") #<- print explicação
    #print(populacao[pos_max]) #<- print explicação
    melhor_resultado = populacao[pos_max]
    peso_total = 0
    valor_total = 0
    for i in range(len(melhor_resultado)): #pega o peso e valor do melhor resultado
     if melhor_resultado[i] == 1:
          peso_total += Itens[i][0]
          valor_total += Itens[i][1]
    if peso_total>W:
          #algoritmo_genetico()
          return 0
    else:
         print(f"peso total: {peso_total}")           
         return valor_total #retorna o cromossomo com a melhor pontuação

#Parametros do AG
def algoritmo_genetico():
     tam_pop = 15 #tamanho da pop(num de cromossomos)
     chance_muta = 0.2 #chance de mutação
     geracoes = 10 #numero de gerações

     populacao = gera_populacao(tam_pop) #gera a população

     for i in range(geracoes): #loop que executa conforme o numero de gerações
          pai1, pai2 = pega_cromossomo(populacao) #escolhe dois pais     
          filho1, filho2 = crossover(pai1, pai2) #realiza o crossover
          if random.uniform(0, 1) <= chance_muta: #verifica se há chance de mutação e a realiza caso ocorra
               filho1 = mutacao(filho1)
          if random.uniform(0, 1) <= chance_muta:
               filho2 = mutacao(filho2)
          populacao = [filho1, filho2] + populacao[2:] #substitui a população antiga pela nova #ver conceito de substituição
     
     melhor_resultado = escolher_melhor(populacao) #seleciona o melhor resultado
     return melhor_resultado


#Hill Climbing e Busca em Feixe
def itensLeves(I: list, W: int): # Recolhe todos os itens com capacidade menor que W;
     itens = []
     for i in I:
          if i[0] <= W:
               itens.append(i)
     return itens

def valor_total(itens: list, n: int) -> int:
     valor = 0
     if n == 1:
          for i in itens:
               valor += i[1]
     elif n == 0:
          for j in itens:
               valor += j[0]
     return valor

def melhor_resposta(respostas: list, valorMax: int):
     for index, resp in enumerate(respostas):
          print(f"Resposta {index + 1}: {resp}")
          if valor_total(resp, 1) == valorMax:
               solução = resp
     return solução

def hill_climbing(I: list, W: int) -> list:
     itens = itensLeves(I, W) # Itens com capacidade menor que W;
     lista = [] # Lista com os itens ecolhidos;
     pesoAtual = 0 # Variável responsável em verificar se a quantidade de itens não ultrapassa a capacidade W da mochila;
     while len(itens) != 0:
          lista.append(itens.pop(random.randrange(len(itens)))) # Retira um item aleatório da lista itens;
          if pesoAtual + lista[-1][0] <= W: # Se a soma dos pesos for menor que W:
               pesoAtual += lista[-1][0] # O item é incluso;
          else:
               lista.pop() # Senão, o item é removido e não será mais visto;
     return lista

def beam_search(I: list, W: int, k: int) -> list:
     valorMaximo = 0 # 
     respostas = [] # lista que as respostas de cada estado
     for i in range(k):
          itens = itensLeves(I, W)
          mochila = [] # Lista com os itens ecolhidos;
          pesoAtual = 0 # Variável responsável em verificar se a quantidade de itens não ultrapassa a capacidade W da mochila;
          while len(itens) != 0:
               mochila.append(itens.pop(random.randrange(len(itens)))) # Retira um item aleatório da lista itens;
               if pesoAtual + mochila[-1][0] <= W: # Se a soma dos pesos for menor que W:
                    pesoAtual += mochila[-1][0] # O item é incluso;
               else:
                    mochila.pop() # Senão, o item é removido e não será mais visto;
          
          if valor_total(mochila, 1) > valorMaximo:
               valorMaximo = valor_total(mochila, 1) # Encontrando o maior valor
          respostas.append(mochila) # Adicionando os máximos locais
     
     solução = melhor_resposta(respostas, valorMaximo)
     return solução

if __name__ == "__main__":
     W = 20 # Carga máxima da mochila
     # Definimos os itens com peso e valor respectivamente
     Itens = [(15, 30), (10, 25), (2, 2), (4, 6), (6, 15), (7, 20), (20, 38)]
     k = 4 # Quantidade de estados iniciais
     
     '''Arq_HC = "Arq_HC.csv" #remove esse coment pra funcionar o salvar em csv
     Arq_BS = "Arq_BS.csv"
     Arq_AG = "Arq_AG.csv" 
     with open(Arq_HC, mode='w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow([])
     with open(Arq_BS, mode='w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow([])
     with open(Arq_AG, mode='w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow([])
     for i in range(100):
          
          print("Hill Climbing:")
          solução = hill_climbing(Itens, W)
          print("Itens: ", solução)
          VHC = valor_total(solução, 1)
          print("Valor total: ", valor_total(solução, 1))
          with open(Arq_HC, mode='a', newline='') as file:
               writer = csv.writer(file)
               # Escreva o valor no arquivo CSV
               writer.writerow([VHC])

          
          print()
          print("Local Beam Search:")
          solução2 = beam_search(Itens, W, k)
          print("Itens: ", solução2)
          VBS = valor_total(solução2, 1)
          print("Valor total:", valor_total(solução2, 1))
          with open(Arq_BS, mode='a', newline='') as file:
               writer = csv.writer(file)
               # Escreva o valor no arquivo CSV
               writer.writerow([VBS])
          
          
          print()
          print("Algoritmo Genético")
          solução3 = algoritmo_genetico()
          print("Valor Total:", solução3)
          with open(Arq_AG, mode='a', newline='') as file:
               writer = csv.writer(file)
               # Escreva o valor no arquivo CSV
               writer.writerow([solução3])

'''
     print()
     print("Hill Climbing:")
     solução = hill_climbing(Itens, W)
     print("Itens: ", solução)
     print("Valor total: ", valor_total(solução, 1))

     print()
     print("Local Beam Search:")

     solução2 = beam_search(Itens, W, k)
     print("Itens: ", solução2)
     print("Valor total:", valor_total(solução2, 1))
     
     print()
     print("Algoritmo Genético")
     
     solução3 = algoritmo_genetico()
     print("Valor Total:", solução3)
     