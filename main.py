"""
LogiRota — versão 7 (Aula 07).

A Aula 06 construiu a malha viária como grafo. Esta versão percorre essa
mesma malha de duas formas — BFS e DFS — e usa a busca para responder
uma pergunta de negócio: existe algum ponto de entrega para o qual
nenhuma rua cadastrada leva?

    python3 main.py
"""

from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# Os mesmos 7 pontos de entrega das aulas anteriores.
PONTOS = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),
    # Cadastrado no sistema, mas nenhuma rua liga este ponto aos demais.
    Ponto("Farmacia Ilha", "Ilha", 25, 25),
]

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


def montar():
    grafo = GrafoLista(PONTOS)
    for a, b in RUAS:
        grafo.adicionar_rua(a, b)
    return grafo


def main():
    print("LogiRota - BFS, DFS e conectividade da malha\n")

    grafo = montar()
    origem = "Posto Central"

    ordem_bfs = bfs(grafo, origem)
    ordem_dfs = dfs(grafo, origem)

    print(f"partindo de '{origem}':\n")
    print(f"  BFS (fila) .: {' -> '.join(ordem_bfs)}")
    print(f"  DFS (pilha) : {' -> '.join(ordem_dfs)}")
    print("\n  mesmo grafo, mesma origem: a ordem muda porque a estrutura")
    print("  auxiliar muda - fila devolve por camadas, pilha mergulha fundo.")

    nomes = [ponto.nome for ponto in PONTOS]
    componentes = componentes_conexos(grafo, nomes)

    print(f"\ncomponentes conexos da malha ({len(componentes)}):")
    for grupo in componentes:
        print(f"  {{{', '.join(grupo)}}}")

    if len(componentes) > 1:
        isolados = [g[0] for g in componentes if len(g) == 1]
        print(f"\n  atencao: {', '.join(isolados)} nao tem rua cadastrada -")
        print("  nenhuma entrega alcanca esse ponto partindo dos demais.")


if __name__ == "__main__":
    main()
