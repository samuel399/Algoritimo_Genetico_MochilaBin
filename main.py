import random


def recebe_input(nome_arqv):
    print("teste")
# Defina os parâmetros do problema
num_itens = 20  # Número de itens disponíveis

# Pesos e valores dos itens
pesos = [3485, 326, 416, 4992, 4649, 795, 1457, 4815, 4446, 5422, 2791, 3359, 3667, 1598, 3007, 3544, 6334, 766, 3994, 1893]
valores = [5094, 6506, 5248, 2421, 322, 5237, 3043, 845, 4955, 2252, 2009, 6901, 6122, 5094, 738, 4574, 3715, 5882, 5367, 1984]

capacidade_mochila = 7001  # Capacidade máxima da mochila

# Função de aptidão: Avalia uma solução (representada como uma lista binária)
def aptidao(solucao):
    valor_total = 0
    peso_total = 0
    for i in range(num_itens):
        if solucao[i] == 1:
            valor_total += valores[i]
            peso_total += pesos[i]
    if peso_total > capacidade_mochila:
        return 0  # Penalize soluções inválidas
    return valor_total

# Função para criar uma solução inicial aleatória
def criar_solucao():
    return [random.randint(0, 1) for _ in range(num_itens)]

# Operador de crossover: Dois pontos de corte
def crossover(pai1, pai2):
    ponto_corte1 = random.randint(1, num_itens - 2)
    ponto_corte2 = random.randint(ponto_corte1 + 1, num_itens - 1)
    filho1 = pai1[:ponto_corte1] + pai2[ponto_corte1:ponto_corte2] + pai1[ponto_corte2:]
    filho2 = pai2[:ponto_corte1] + pai1[ponto_corte1:ponto_corte2] + pai2[ponto_corte2:]
    return filho1, filho2

# Operador de mutação: Inversão de bits
def mutacao(solucao):
    posicao = random.randint(0, num_itens - 1)
    solucao[posicao] = 1 - solucao[posicao]  # Inverte o bit
    return solucao

# Algoritmo Genético
tamanho_populacao = 250
taxa_crossover = 0.7
taxa_mutacao = 0.13586
num_geracoes = 400

populacao = [criar_solucao() for _ in range(tamanho_populacao)]

melhor_solucao_global = None
melhor_valor_global = 0  # Inicialize com um valor mínimo
melhor_geracao_global = 0

for geracao in range(num_geracoes):
    # Avaliação da população
    aptidoes = [aptidao(solucao) for solucao in populacao]
    
    # Seleção dos pais
    pais = random.choices(populacao, weights=[aptidao(solucao) + 1 for solucao in populacao], k=tamanho_populacao)

    # Criação da nova geração
    nova_populacao = []

    for i in range(0, tamanho_populacao, 2):
        pai1 = pais[i]
        pai2 = pais[i + 1]

        if random.random() < taxa_crossover:
            filho1, filho2 = crossover(pai1, pai2)
        else:
            filho1, filho2 = pai1[:], pai2[:]

        if random.random() < taxa_mutacao:
            filho1 = mutacao(filho1)
        if random.random() < taxa_mutacao:
            filho2 = mutacao(filho2)

        nova_populacao.extend([filho1, filho2])
        

    populacao = nova_populacao
    num = 0
    # Encontre a melhor solução da geração atual
    melhor_solucao = max(populacao, key=aptidao)
    melhor_valor = aptidao(melhor_solucao)
   
    print(f"Geração {geracao}: Melhor Solução: {melhor_solucao}\n Melhor Valor: {melhor_valor}")
    
    # Atualize o registro da melhor solução global, se necessário
    if melhor_valor > melhor_valor_global:
        melhor_solucao_global = melhor_solucao
        melhor_valor_global = melhor_valor
        melhor_geracao_global = geracao

# No final da execução
print("Melhor solução encontrada:")
print("Melhor Geração: ", melhor_geracao_global)
print("Itens na mochila:", melhor_solucao_global)
print("Valor total:", melhor_valor_global)