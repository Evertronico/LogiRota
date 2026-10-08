"""
Caminho mínimo — Aula 08.

Dijkstra sobre o GrafoLista/GrafoMatriz de logirota/grafo.py: dado um ponto de
partida, descobre a menor distância até todos os outros e quem é o
predecessor de cada um no melhor caminho. reconstruir_caminho() percorre os
predecessores de trás para frente e devolve a lista de nomes da rota.

Versão ingênua, O(v²): a cada passo, procura à mão o ponto ainda não fechado
com a menor distância — sem heapq.

Reaproveita de logirota/grafo.py:
    vizinhos_com_peso
"""

INFINITO = float("inf")


def dijkstra(grafo, nomes, origem):
    """Devolve (distancia, predecessor), dois dicionários indexados por nome.

    Ponto que nenhuma rua alcança fica com distância infinita.
    """
    distancia = {nome: INFINITO for nome in nomes}
    predecessor = {nome: None for nome in nomes}
    distancia[origem] = 0
    fechados = set()

    while len(fechados) < len(nomes):
        atual = None
        menor = INFINITO
        for nome in nomes:
            if nome not in fechados and distancia[nome] < menor:
                atual = nome
                menor = distancia[nome]

        if atual is None:
            break  # o que sobrou é inalcançável a partir da origem

        fechados.add(atual)
        for vizinho, peso in grafo.vizinhos_com_peso(atual):
            nova = distancia[atual] + peso
            if nova < distancia[vizinho]:
                distancia[vizinho] = nova
                predecessor[vizinho] = atual

    return distancia, predecessor


def reconstruir_caminho(predecessor, origem, destino):
    """Lista de nomes de origem até destino; lista vazia se não há caminho."""
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = predecessor[atual]
    caminho.reverse()

    if caminho[0] != origem:
        return []
    return caminho
