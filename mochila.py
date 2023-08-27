import random

class KnapsackPackage(object):
     """ Criação da Mochila """
     def __init__(self, W):
         self.W = W
         self.weight = 0
         self.value = 0

     def adicionarItem(self, weight, value):
          if((self.weight + weight) <= self.W):
               self.weight += weight
               self.value += value

     def removerItem(self, weight, value):
          self.weight -= weight
          self.value -= value

def beam_search(P, V, W, k):
     peso = []
     valor = []

     # Adiciona todos os itens com valores abaixo do Máximo
     for i in range(len(P)):
          if P[i] <= W:
               peso.append(P[i])
               valor.append(V[i])
     
     lista = random.sample(peso, k)

def itensLeves(I: list, W: int): # Recolhe todos os itens com capacidade menor que W;
     itens = []
     for i in I:
          if i[0] <= W:
               itens.append(i)
     return itens

def valor_total(itens: list) -> int:
     valor = 0
     for i in itens:
          valor += i[1]
     
     return valor

def hill_climbing(I: list, W: int) -> list:
     itens = itensLeves(I, W) # Itens com capacidade menor que W;
     lista = [] # Lista com os itens ecolhidos;
     pesoAtual = 0 # Variável responsável em verificar se a quantidade de itens não ultrapassa a capacidade W da mochila;
     while pesoAtual <= W:
          lista.append(itens.pop(random.randrange(len(itens)))) # Retira um item aleatório da lista itens;
          if pesoAtual + lista[len(lista)-1][0] <= W: # Se a soma dos pesos for menor que W:
               pesoAtual += lista[len(lista)-1][0] # O item é incluso;
          else:
               lista.pop() # Senão, o item é removido e não será mais visto;
          
          if len(itens) == 0: # Caso não haja mais itens:
               break # O laço é encerrado;
     return lista


if __name__ == "__main__":
     W = 20 # Carga máxima da mochila
     Itens = [(15, 30), (10, 25), (2, 2), (4, 6), (6, 15)]
     solução = hill_climbing(Itens, W)
     print("Itens: ", solução)
     print("Valor total: ", valor_total(solução))
