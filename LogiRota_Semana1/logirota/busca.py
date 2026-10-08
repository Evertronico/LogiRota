from logirota.fila import FilaDePedidos
from logirota.pilha import PilhaDeOperacoes

def bfs(grafo, origem):
    visitados = {origem}
    ordem = []
    fila = FilaDePedidos()
    fila.enfileirar(origem)
    while not fila.vazia():
        atual = fila.desenfileirar()
        ordem.append(atual)
        for vizinho in grafo.vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.enfileirar(vizinho)
    return ordem

def dfs(grafo, origem):
    visitados = {origem}
    ordem = []
    pilha = PilhaDeOperacoes()
    pilha.empilhar(origem)
    while not pilha.vazia():
        atual = pilha.desempilhar()
        ordem.append(atual)
        for vizinho in grafo.vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.empilhar(vizinho)
    return ordem

def componentes_conexos(grafo, nomes):
    visitados = set()
    componentes = []
    for nome in nomes:
        if nome in visitados:
            continue
        grupo = bfs(grafo, nome)
        visitados.update(grupo)
        componentes.append(grupo)
    return componentes