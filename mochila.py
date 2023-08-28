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

def beam_search(I: list, W: int, k: int) -> list:
     valorMaximo = 0
     respostas = []
     for i in range(k):
          itens = itensLeves(I, W)
          lista = [] # Lista com os itens ecolhidos;
          pesoAtual = 0 # Variável responsável em verificar se a quantidade de itens não ultrapassa a capacidade W da mochila;
          soma = 0
          while pesoAtual <= W:
               lista.append(itens.pop(random.randrange(len(itens)))) # Retira um item aleatório da lista itens;
               if pesoAtual + lista[len(lista)-1][0] <= W: # Se a soma dos pesos for menor que W:
                    pesoAtual += lista[len(lista)-1][0] # O item é incluso;
                    soma += lista[len(lista)-1][1]
               else:
                    lista.pop() # Senão, o item é removido e não será mais visto;
          
               if len(itens) == 0: # Caso não haja mais itens:
                    break # O laço é encerrado;
          
          if valor_total(lista) > valorMaximo:
               valorMaximo = valor_total(lista)
          respostas.append(lista)
     
     solução = []
     for index, resp in enumerate(respostas):
          print(f"Resposta {index + 1}: {resp}")
          if valor_total(resp) == valorMaximo:
               solução = resp
     
     return solução

if __name__ == "__main__":
     W = 20 # Carga máxima da mochila
     Itens = [(15, 30), (10, 25), (2, 2), (4, 6), (6, 15), (7, 20), (20, 38)]
     k = 5

     print("Hill Climbing:")
     solução = hill_climbing(Itens, W)
     print("Itens: ", solução)
     print("Valor total: ", valor_total(solução))

     print()
     print("Local Beam Search:")

     solução2 = beam_search(Itens, W, k)
     print("Itens: ", solução2)
     print("Valor total:", valor_total(solução2))
