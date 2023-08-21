import random

class KnapsackPackage(object):
     """ Criação da Mochila """
     def __init__(self, max):
         self.max = max
         self.weight = 0
         self.value = 0

     def adicionarItem(self, weight, value):
          if((self.weight + weight) <= self.max):
               self.weight += weight
               self.value += value

     def removerItem(self, weight, value):
          self.weight -= weight
          self.value -= value
 
if __name__ == "__main__":
     W = [15, 10, 2, 4] # Peso dos Itens
     V = [30, 25, 2, 6] # Valor dos Itens
     M = 37 # Carga máxima da mochila
     n = 4 # Número de Itens
     
     mochila = KnapsackPackage(M)
     print(mochila.value)
