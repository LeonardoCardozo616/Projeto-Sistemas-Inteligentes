def knapsack_beam_search(items, capacity, beam_width):
  """
  Busca de feixe para resolver o problema da mochila.

  Argumentos:
    items: Uma lista de objetos. Cada objeto tem um peso e um valor.
    capacity: A capacidade da mochila.
    beam_width: A largura do feixe.

  Retorno:
    Uma lista de objetos que cabem na mochila e maximizam o valor total.
  """

  # Inicialize a pilha de feixe com o estado inicial.
  beam = [[], 0]

  # Itere enquanto a pilha de feixe não estiver vazia.
  while beam:
        # Obtenha o estado atual da pilha de feixe.
        state = beam.pop(0)
        value = beam.pop(0)

        # Se o estado for o estado final, retorne-o.
        if state == capacity:
          return state

        # Obtenha todos os estados filho do estado atual.
        child_states = []
        for item in items:
          if state and item.weight <= capacity - state[-1]:
            child_states.append([state + [item], value - item.cost])


        # Classifique os estados filho pela sua pontuação.
        child_states.sort(key=lambda state: state[1], reverse=True)

        # Adicione os primeiros `beam_width` estados filho à pilha de feixe.
        beam = beam[:beam_width] + child_states[:beam_width]

    # Se a pilha de feixe estiver vazia, o estado final não foi encontrado.
    
  return None

items = [
  {
    "weight": 10,
    "value": 60,
  },
  {
    "weight": 20,
    "value": 100,
  },
  {
    "weight": 30,
    "value": 120,
  },
]

capacity = 50

beam_width = 3

print(knapsack_beam_search(items, capacity, beam_width))

