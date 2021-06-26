import resource
import argparse
import timeit
import itertools
from heapq import heappush, heappop, heapify
from collections import deque
from estado import Estado

estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
node_meta = Estado
initial_estado = list()
largura_tabuleiro = 0
altura_tabuleiro = 0

nodes_expandidos = 0
profundidade_max_busca = 0
tamanho_limite_busca = 0

movimentos = list()
custo = set()


def bfs(start_estado):

    global tamanho_limite_busca, node_meta, profundidade_max_busca

    explorado, fila = set(), deque([Estado(start_estado, None, None, 0, 0, 0)])

    while fila:

        node = fila.popleft()

        explorado.add(node.map)

        if node.estado == estado_meta:
            node_meta = node
            return fila

        vizinhos = expandir(node)

        for vizinho in vizinhos:
            if vizinho.map not in explorado:
                fila.append(vizinho)
                explorado.add(vizinho.map)

                if vizinho.profundidade > profundidade_max_busca:
                    profundidade_max_busca += 1

        if len(fila) > tamanho_limite_busca:
            tamanho_limite_busca = len(fila)


def dfs(start_estado):

    global tamanho_limite_busca, node_meta, profundidade_max_busca

    explorado, stack = set(), list([Estado(start_estado, None, None, 0, 0, 0)])

    while stack:

        node = stack.pop()

        explorado.add(node.map)

        if node.estado == estado_meta:
            node_meta = node
            return stack

        vizinhos = reversed(expandir(node))

        for vizinho in vizinhos:
            if vizinho.map not in explorado:
                stack.append(vizinho)
                explorado.add(vizinho.map)

                if vizinho.profundidade > profundidade_max_busca:
                    profundidade_max_busca += 1

        if len(stack) > tamanho_limite_busca:
            tamanho_limite_busca = len(stack)

def ast(start_estado):

    global tamanho_limite_busca, node_meta, profundidade_max_busca

    explorado, heap, heap_entry, counter = set(), list(), {}, itertools.count()

    chave = h(start_estado)

    root = Estado(start_estado, None, None, 0, 0, chave)

    entry = (chave, 0, root)

    heappush(heap, entry)

    heap_entry[root.map] = entry

    while heap:

        node = heappop(heap)

        explorado.add(node[2].map)

        if node[2].estado == estado_meta:
            node_meta = node[2]
            return heap

        vizinhos = expandir(node[2])

        for vizinho in vizinhos:

            vizinho.chave = vizinho.custo + h(vizinho.estado)

            entry = (vizinho.chave, vizinho.movimento, vizinho)

            if vizinho.map not in explorado:

                heappush(heap, entry)

                explorado.add(vizinho.map)

                heap_entry[vizinho.map] = entry

                if vizinho.profundidade > profundidade_max_busca:
                    profundidade_max_busca += 1

            elif vizinho.map in heap_entry and vizinho.chave < heap_entry[vizinho.map][2].chave:

                hindex = heap.index((heap_entry[vizinho.map][2].chave,
                                     heap_entry[vizinho.map][2].movimento,
                                     heap_entry[vizinho.map][2]))

                heap[int(hindex)] = entry

                heap_entry[vizinho.map] = entry

                heapify(heap)

        if len(heap) > tamanho_limite_busca:
            tamanho_limite_busca = len(heap)


def ida(start_estado):

    global custo

    limiar = h(start_estado)

    while 1:
        resposta = dls_mod(start_estado, limiar)

        if type(resposta) is list:
            return resposta
            break

        limiar = resposta

        custo = set()


def dls_mod(start_estado, limiar):

    global tamanho_limite_busca, node_meta, profundidade_max_busca, custo

    explorado, stack = set(), list([Estado(start_estado, None, None, 0, 0, limiar)])

    while stack:

        node = stack.pop()

        explorado.add(node.map)

        if node.estado == estado_meta:
            node_meta = node
            return stack

        if node.chave > limiar:
            custo.add(node.chave)

        if node.profundidade < limiar:

            vizinhos = reversed(expandir(node))

            for vizinho in vizinhos:
                if vizinho.map not in explorado:

                    vizinho.chave = vizinho.custo + h(vizinho.estado)
                    stack.append(vizinho)
                    explorado.add(vizinho.map)

                    if vizinho.profundidade > profundidade_max_busca:
                        profundidade_max_busca += 1

            if len(stack) > tamanho_limite_busca:
                tamanho_limite_busca = len(stack)

    return min(custo)

def expandir(node):

    global nodes_expandidos
    nodes_expandidos += 1

    vizinhos = list()

    vizinhos.append(Estado(movimento(node.estado, 1), node, 1, node.profundidade + 1, node.custo + 1, 0))
    vizinhos.append(Estado(movimento(node.estado, 2), node, 2, node.profundidade + 1, node.custo + 1, 0))
    vizinhos.append(Estado(movimento(node.estado, 3), node, 3, node.profundidade + 1, node.custo + 1, 0))
    vizinhos.append(Estado(movimento(node.estado, 4), node, 4, node.profundidade + 1, node.custo + 1, 0))

    nodes = [vizinho for vizinho in vizinhos if vizinho.estado]

    return nodes


def movimento(estado, position):

    new_estado = estado[:]

    index = new_estado.index(0)

    if position == 1:  # cima

        if index not in range(0, altura_tabuleiro):

            temp = new_estado[index - altura_tabuleiro]
            new_estado[index - altura_tabuleiro] = new_estado[index]
            new_estado[index] = temp

            return new_estado
        else:
            return None

    if position == 2:  # baixo

        if index not in range(largura_tabuleiro - altura_tabuleiro, largura_tabuleiro):

            temp = new_estado[index + altura_tabuleiro]
            new_estado[index + altura_tabuleiro] = new_estado[index]
            new_estado[index] = temp

            return new_estado
        else:
            return None

    if position == 3:  # esquerda

        if index not in range(0, largura_tabuleiro, altura_tabuleiro):

            temp = new_estado[index - 1]
            new_estado[index - 1] = new_estado[index]
            new_estado[index] = temp

            return new_estado
        else:
            return None

    if position == 4:  # direita

        if index not in range(altura_tabuleiro - 1, largura_tabuleiro, altura_tabuleiro):

            temp = new_estado[index + 1]
            new_estado[index + 1] = new_estado[index]
            new_estado[index] = temp

            return new_estado
        else:
            return None


def h(estado):

    return sum(abs(b % altura_tabuleiro - g % altura_tabuleiro) + abs(b//altura_tabuleiro - g//altura_tabuleiro)
               for b, g in ((estado.index(i), estado_meta.index(i)) for i in range(1, largura_tabuleiro)))


def retroceder():

    current_node = node_meta

    while initial_estado != current_node.estado:

        if current_node.movimento == 1:
            mova = 'cima'
        elif current_node.movimento == 2:
            mova = 'baixo'
        elif current_node.movimento == 3:
            mova = 'esquerda'
        else:
            mova = 'direita'

        movimentos.insert(0, mova)
        current_node = current_node.pai

    return movimentos


def saida(limite, time):

    global movimentos

    movimentos = retroceder()

    print("caminho: " + str(movimentos))
    print("\ncusto do caminho: " + str(len(movimentos)))
    print("\nnós expandidos: " + str(nodes_expandidos))
    print("\ndimensão de margem: " + str(len(limite)))
    print("\ndimensão máxima de margem: " + str(tamanho_limite_busca))
    print("\nprofundidade de busca: " + str(node_meta.profundidade))
    print("\nprofundidade máxima de busca: " + str(profundidade_max_busca))
    print("\ntempo de execução: " + format(time, '.8f'))
    print("\nuso máximo de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f') + "\n")


def read(configuration):

    global largura_tabuleiro, altura_tabuleiro

    data = configuration.split(",")

    for element in data:
        initial_estado.append(int(element))

    largura_tabuleiro = len(initial_estado)

    altura_tabuleiro = int(largura_tabuleiro ** 0.5)
    
def isunsolvable(initial_estado):
    count=0
    for i in range(8):
        for j in range(i,9):
            if (initial_estado[i] > initial_estado[j] and              
                initial_estado[j]!=0):
                count+=1
    if count%2==1:
        return True
    else:
        return False    

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('algoritmo')
    parser.add_argument('tabuleiro')
    args = parser.parse_args()

    read(args.tabuleiro)
    
    if(isunsolvable(initial_estado)):
        print("sem solução possível")
        
    else:
        function = function_map[args.algoritmo]
        
        start = timeit.default_timer()
        
        limite = function(initial_estado)
        
        stop = timeit.default_timer()
        
        saida(limite, stop-start)


function_map = {
    'bfs': bfs,
    'dfs': dfs,
    'ast': ast,
    'ida': ida
}

if __name__ == '__main__':
    main()
 
