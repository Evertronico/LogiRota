"""

Dijkstra mantem dois grupos de pontos:
  fechados  distancia final ja garantida
  abertos   distancia provisoria, que ainda pode encurtar
A cada passo fecha o ponto aberto de menor distancia conhecida e usa esse
fechamento para tentar encurtar a distancia dos vizinhos ainda abertos
(isso se chama "relaxar" a aresta).

Reaproveita de logirota/grafo.py:
    vizinhos_com_peso()
"""

INFINITO = float("inf")


def _mais_proximo_em_aberto(distancia, fechados):
    """Nome do ponto ainda aberto com menor distancia conhecida.

    Devolve None se todos os abertos tem distancia infinita - ou seja,
    nenhum deles e alcancavel a partir da origem.
    """
    melhor = None
    for nome, valor in distancia.items():
        if nome in fechados or valor == INFINITO:
            continue
        if melhor is None or valor < distancia[melhor]:
            melhor = nome
    return melhor


def dijkstra(grafo, nomes, origem):
    """Menor distancia da origem ate todos os pontos de `nomes`.

    Devolve (distancia, predecessor):
      distancia[nome]    menor soma de pesos ate `nome` (inf se inalcancavel)
      predecessor[nome]  ponto de onde se chegou em `nome` (None na origem
                         e nos inalcancaveis)
    Custo: O(v^2) - a busca linear do mais proximo roda v vezes.
    """
    if origem not in nomes:
        raise KeyError(f"ponto '{origem}' nao existe na malha")

    distancia = {nome: INFINITO for nome in nomes}
    predecessor = {nome: None for nome in nomes}
    distancia[origem] = 0.0
    fechados = set()

    while len(fechados) < len(nomes):
        atual = _mais_proximo_em_aberto(distancia, fechados)
        if atual is None:
            break
        fechados.add(atual)
        for vizinho, peso in grafo.vizinhos_com_peso(atual):
            nova_distancia = distancia[atual] + peso
            if nova_distancia < distancia[vizinho]:
                distancia[vizinho] = nova_distancia
                predecessor[vizinho] = atual

    return distancia, predecessor


def reconstruir_caminho(predecessor, origem, destino):
    """Caminho origem -> destino, seguindo os predecessores de tras para
    frente e invertendo a lista no final.

    Devolve lista vazia se `destino` nao e alcancavel a partir de `origem`.
    """
    caminho = [destino]
    atual = destino
    while atual != origem:
        atual = predecessor[atual]
        if atual is None:
            return []
        caminho.append(atual)
    caminho.reverse()
    return caminho