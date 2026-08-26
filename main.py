"""
LogiRota — versão 6 (Aula 06).

O índice de pontos (ABB, Aulas 03–05) responde "onde está o ponto X".
A malha viária responde uma pergunta diferente: "que ruas ligam X a
outros pontos, e com que distância". Isso é um grafo, não uma árvore —
não há raiz, e dois pontos podem se alcançar sem hierarquia entre eles.

    python3 main.py
"""

from logirota.grafo import GrafoLista, GrafoMatriz
from logirota.ponto import Ponto

# Os mesmos 7 pontos de entrega das aulas anteriores — agora vértices.
PONTOS = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),
]

# Ruas da malha: pares de nomes com ligacao direta. O peso de cada uma
# nasce de Ponto.distancia_ate -- nao e um numero digitado a mao.
RUAS = [
    ("Escola Norte", "Mercado Barra"),
    ("Mercado Barra", "Farmacia Bela Vista"),
    ("Mercado Barra", "Posto Central"),
    ("Farmacia Bela Vista", "Posto Central"),
    ("Posto Central", "Oficina Safira"),
    ("Posto Central", "Padaria Distrito"),
    ("Oficina Safira", "Padaria Distrito"),
    ("Padaria Distrito", "Loja Boa Familia"),
]


def montar(grafo):
    for a, b in RUAS:
        grafo.adicionar_rua(a, b)
    return grafo


def main():
    print("LogiRota - malha viaria: duas representacoes\n")

    matriz = montar(GrafoMatriz(PONTOS))
    lista = montar(GrafoLista(PONTOS))

    print(f"vertices (pontos) ..............: {len(PONTOS)}")
    print(f"ruas cadastradas ................: {len(RUAS)}")
    print(f"celulas da matriz (v ao quadrado): {matriz.total_celulas()}")
    print(f"entradas da lista (2 x ruas) .....: {lista.total_arestas_armazenadas()}")

    print("\nvizinhanca -- mesma pergunta, duas representacoes:")
    pares = [
        ("Mercado Barra", "Posto Central"),
        ("Escola Norte", "Padaria Distrito"),
        ("Oficina Safira", "Loja Boa Familia"),
    ]
    for a, b in pares:
        vm = matriz.sao_vizinhos(a, b)
        vl = lista.sao_vizinhos(a, b)
        print(f"  {a} <-> {b}: matriz={vm}  lista={vl}")

    # As duas representacoes respondem exatamente a mesma pergunta.
    # O que muda e o espaco: a matriz reserva v^2 celulas mesmo para
    # os pares sem rua; a lista so guarda o que existe de fato, ao
    # custo de percorrer os vizinhos de um vertice para responder.


if __name__ == "__main__":
    main()
