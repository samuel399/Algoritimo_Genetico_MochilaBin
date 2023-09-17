import random


#função que lê o arquivo de input e atribui o numero de itens, pesos, valores e capacidade da mochila
def recebe_input(nome_arqv):
    arqv = open(nome_arqv, 'r')
    itens = arqv.readline()
    peso = []
    fim = ''
    valor = []

    for linha in arqv:
        fim = linha
        if len(linha.split()) != 1:
            valor.append(linha.split()[1])
            peso.append(linha.split()[2])
    return itens, peso, valor, fim

# Defina os parâmetros do problema

num_itens, pesos, valores, capacidade_mochila = recebe_input("input/input_.in")#Digitar numero do input no lugar do _ --> input1.in


# Função de aptidão: Avalia uma solução (representada como uma lista binária)
def aptidao(solucao):
    valor_total = 0
    peso_total = 0
    for i in range(int(num_itens)):
        if solucao[i] == 1:
            valor_total += int(valores[i])
            peso_total += int(pesos[i])
    if peso_total > int(capacidade_mochila):
        return 0  # Penalize soluções inválidas
    return valor_total


# Função para criar uma solução inicial aleatória
def criar_solucao():
    return [random.randint(0, 1) for _ in range(int(num_itens))]


# Operador de crossover: Dois pontos de corte
def crossover(pai1, pai2):
    ponto_corte1 = random.randint(1, int(num_itens) - 2)
    ponto_corte2 = random.randint(ponto_corte1 + 1, int(num_itens) - 1)
    filho1 = pai1[:ponto_corte1] + pai2[ponto_corte1:ponto_corte2] + pai1[ponto_corte2:]
    filho2 = pai2[:ponto_corte1] + pai1[ponto_corte1:ponto_corte2] + pai2[ponto_corte2:]
    return filho1, filho2


# Operador de mutação: Inversão de bits
def mutacao(solucao):
    posicao = random.randint(0, int(num_itens) - 1)
    solucao[posicao] = 1 - solucao[posicao]  # Inverte o bit
    return solucao


# Algoritmo Genético
tamanho_populacao = 5000
taxa_crossover = 0.7
taxa_mutacao = 1
num_geracoes = 5000

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
arquivo = open("Output/output_.out", 'w', encoding='UTF-8')# Colocar o numero do output para ser gerado --> output4.out

arquivo.write("Output _ Melhor Solução: \n")# Colocar numero do output, igual o de cima. --> Output 4 Melhor Solução: 
arquivo.write(f"Melhor Geração: {melhor_geracao_global}\nValor total: {melhor_valor_global} \nItens na mochila: {melhor_solucao_global}\n\n")
arquivo.write(f"Tamanho da População: {tamanho_populacao}\nNumero de Gerações: {num_geracoes}\nTaxa de Mutação: {taxa_mutacao}\nTaxa de crossover: {taxa_crossover}\n")
