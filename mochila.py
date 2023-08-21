import random

class KnapsackPackage(object):
     """ Criação da Mochila """
     def __init__(self, weight, value, n):
         self.weight = [weight[i] for i in range(n)]
         self.value = [value[i] for i in range(n)]
         self.n = n 
         self.cost = [value[i] / weight[i] for i in range(n)] 
 
if __name__ == "__main__":
     W = [15, 10, 2, 4] # Peso dos Itens
     V = [30, 25, 2, 6] # Valor dos Itens
     M = 37 # Carga máxima da mochila
     n = 4 # Número de Itens
     mochila = KnapsackPackage(W, V, n)
     print(mochila.cost)
