import random

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

     print("Hill Climbing:")
     solução = hill_climbing(Itens, W)
     print("Itens: ", solução)
     print("Valor total: ", valor_total(solução, 1))

     print()
     print("Local Beam Search:")

     solução2 = beam_search(Itens, W, k)
     print("Itens: ", solução2)
     print("Valor total:", valor_total(solução2, 1))
