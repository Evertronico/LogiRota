"""
Busca em largura, busca em profundidade e conectividade — Módulo 3 aplicado.

A malha viária do LogiRota (Aula 06) é um grafo: a partir de um ponto de
partida, BFS e DFS respondem "quais pontos são alcançáveis, e em que
ordem são visitados". As duas percorrem os MESMOS vértices e arestas; o
que muda é a estrutura auxiliar que decide quem é explorado a seguir —
fila (FIFO) para BFS, pilha (LIFO) para DFS. bfs() e dfs() são o mesmo
algoritmo com uma única linha trocada.

componentes_conexos() reaproveita bfs() para responder uma pergunta de
negócio direta: a malha inteira é alcançável a partir de qualquer ponto,
ou existem zonas isoladas para as quais nenhuma rua cadastrada leva?

Reaproveita:
    FilaDePedidos de logirota/fila.py       (BFS)
    PilhaDeOperacoes de logirota/pilha.py   (DFS)
    GrafoMatriz/GrafoLista.vizinhos()       de logirota/grafo.py
"""

from logirota.fila import FilaDePedidos
from logirota.pilha import PilhaDeOperacoes


def bfs(grafo, origem):
    """Visita todos os pontos alcançáveis a partir de origem, em largura:
    todo vizinho de um ponto é visitado antes de qualquer vizinho dos
    vizinhos. A fila garante essa ordem — quem entra primeiro, sai
    primeiro e tem seus vizinhos explorados primeiro.
    """
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
    """Visita todos os pontos alcançáveis a partir de origem, em
    profundidade: mergulha por um caminho até não ter mais para onde
    ir, só então volta e tenta outro. A pilha garante essa ordem — o
    último ponto empilhado é o próximo a ser explorado.
    """
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
    """Agrupa os pontos em componentes conexos: dentro de um grupo,
    todo ponto alcança todo ponto; de um grupo para outro, nenhuma rua
    cadastrada leva.

    Reaproveita bfs() para descobrir, a partir de um ponto ainda não
    visitado, tudo que ele alcança; o que sobrar de fora inicia um novo
    componente. Uma malha totalmente conectada devolve um único grupo.
    """
    visitados = set()
    componentes = []
    for nome in nomes:
        if nome in visitados:
            continue
        grupo = bfs(grafo, nome)
        visitados.update(grupo)
        componentes.append(grupo)
    return componentes
