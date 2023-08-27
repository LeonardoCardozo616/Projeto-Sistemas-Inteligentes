import random

# Definindo os dados do problema da mochila (valores e pesos dos itens)
itens = [
    {"valor": 8, "peso": 4},
    {"valor": 10, "peso": 5},
    {"valor": 15, "peso": 8},
    {"valor": 4, "peso": 3},
    {"valor": 7, "peso": 2}
]
capacidade_mochila = 10

# Parâmetros do algoritmo
tamanho_feixe = 2  # Número de soluções no feixe
num_iteracoes = 10  # Número de iterações do algoritmo

# Função de avaliação de uma solução (maior valor é melhor)
def avaliar(solucao):
    valor_total = sum(item["valor"] for item in solucao)
    peso_total = sum(item["peso"] for item in solucao)
    
    if peso_total > capacidade_mochila:
        valor_total *= 0.5  # Penalização por violar a capacidade
    
    return valor_total

# Geração de soluções iniciais aleatórias
def gerar_solucao_inicial():
    # Embaralhe a lista de itens para escolher de forma aleatória
    random.shuffle(itens)
    
    # Determine o tamanho da solução inicial (até o tamanho da lista de itens)
    tamanho_solucao = random.randint(1, len(itens))
    
    # Selecione os primeiros itens da lista embaralhada como a solução inicial
    solucao_inicial = itens[:tamanho_solucao]
    
    return solucao_inicial

    # return random.sample(itens, random.randint(1, len(itens)))

# Geração de vizinhos (troca de um item aleatório)
def gerar_vizinho(solucao):
    vizinho = solucao.copy()
    item_a_trocar = random.choice(vizinho)
    novo_item = random.choice(itens)
    vizinho.remove(item_a_trocar)
    vizinho.append(novo_item)
    return vizinho

# MAIN - Inicialização do feixe com soluções iniciais
feixe = [gerar_solucao_inicial() for _ in range(tamanho_feixe)]
print(feixe)

# Algoritmo de busca em feixe local
for _ in range(num_iteracoes):
    novos_vizinhos = [gerar_vizinho(solucao) for solucao in feixe]
    feixe.extend(novos_vizinhos)
    feixe = sorted(feixe, key=avaliar, reverse=True)[:tamanho_feixe]

# Encontrando a melhor solução do feixe
melhor_solucao = max(feixe, key=avaliar)

# Resultado
print("Melhor solução encontrada:")
for item in melhor_solucao:
    print(f"Valor: {item['valor']}, Peso: {item['peso']}")
print("Valor total:", avaliar(melhor_solucao))
