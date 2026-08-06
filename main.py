"""
LogiRota — versão 1 (Aula 01).

Núcleo de roteirização e análise de malha de entregas.

Nesta versão o sistema já tem os pontos da malha, a fila de pedidos e a pilha
de desfazer. Ainda não há rota: a malha ainda é uma lista, não um grafo.

    python3 main.py
"""

from logirota.fila import FilaDePedidos
from logirota.pilha import PilhaDeOperacoes
from logirota.ponto import Ponto

PONTOS = [
    Ponto("Centro de Distribuicao", "Centro", 0, 0),
    Ponto("Farmacia Sao Paulo", "Barra", 3, 4),
    Ponto("Mercado Bom Preco", "Safira", 6, 2),
    Ponto("Escola Municipal", "Bela Vista", 1, 7),
]


def main():
    print("LogiRota — malha de entregas\n")

    origem = PONTOS[0]
    for destino in PONTOS[1:]:
        print(f"  {origem} -> {destino}: {origem.distancia_ate(destino)} km")

    # A fila devolve na ordem de chegada.
    fila = FilaDePedidos()
    for destino in PONTOS[1:]:
        fila.enfileirar(destino)

    print(f"\nFila com {len(fila)} pedidos. Proximo: {fila.frente()}")

    # A pilha devolve na ordem inversa.
    desfazer = PilhaDeOperacoes()
    while not fila.vazia():
        atendido = fila.desenfileirar()
        desfazer.empilhar(atendido)
        print(f"  atendido: {atendido}")

    print("\nDesfazendo (ordem inversa):")
    while not desfazer.vazia():
        print(f"  desfeito: {desfazer.desempilhar()}")

    print("\nA malha ainda e uma lista. A partir da Aula 06 ela vira um grafo.")


if __name__ == "__main__":
    main()
