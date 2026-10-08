"""
LogiRota - Semana 1: persistencia e modelagem de dados.
Reaproveita a analise BFS/DFS da Aula 07 sem alterar os TADs.

    python main.py
"""

from logirota.banco import (
    inicializar, listar_pontos, listar_ruas, listar_pedidos_pendentes,
    salvar_ponto, salvar_rua,
)
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto


# Cadastro herdado das aulas anteriores, usado SOMENTE na primeira execucao.
PONTOS_INICIAIS = [
    ("Mercado Barra", "Barra", 2, 8),
    ("Farmacia Bela Vista", "Bela Vista", 6, 3),
    ("Oficina Safira", "Safira", 9, 5),
    ("Padaria Distrito", "Distrito", 12, 1),
    ("Loja Boa Familia", "Boa Familia", 14, 0),
    ("Posto Central", "Centro", 5, 5),
    ("Escola Norte", "Zona Norte", 3, 9),
    ("Farmacia Ilha", "Ilha", 25, 25),
]

RUAS_INICIAIS = [
    ("Escola Norte", "Mercado Barra"),
    ("Mercado Barra", "Farmacia Bela Vista"),
    ("Mercado Barra", "Posto Central"),
    ("Farmacia Bela Vista", "Posto Central"),
    ("Posto Central", "Oficina Safira"),
    ("Posto Central", "Padaria Distrito"),
    ("Oficina Safira", "Padaria Distrito"),
    ("Padaria Distrito", "Loja Boa Familia"),
]


def cadastrar_dados_iniciais():
    """Migra o cadastro das aulas anteriores uma vez, se nao houver pontos."""
    if listar_pontos():
        return

    for nome, bairro, x, y in PONTOS_INICIAIS:
        salvar_ponto(Ponto(nome, bairro, x, y))
    for origem, destino in RUAS_INICIAIS:
        salvar_rua(origem, destino)


def montar():
    """Remonta a malha SOMENTE a partir das tuplas retornadas pelo banco."""
    pontos = [Ponto(nome, bairro, x, y)
              for nome, bairro, x, y in listar_pontos()]
    grafo = GrafoLista(pontos)
    for origem, destino in listar_ruas():
        grafo.adicionar_rua(origem, destino)
    return grafo, pontos


def main():
    inicializar()
    cadastrar_dados_iniciais()
    grafo, pontos = montar()

    print("LogiRota - BFS, DFS e persistencia SQLite\n")
    print(f"pontos cadastrados: {len(pontos)}")
    print(f"ruas cadastradas: {len(listar_ruas())}")
    pedidos = listar_pedidos_pendentes()
    print(f"pedidos pendentes: {len(pedidos)}")
    for pedido_id, destino, status in pedidos:
        print(f"  #{pedido_id}: {destino} ({status})")

    origem = "Posto Central"
    nomes = [ponto.nome for ponto in pontos]
    if origem not in nomes:
        return

    print(f"\npartindo de '{origem}':\n")
    print(f"  BFS (fila) .: {' -> '.join(bfs(grafo, origem))}")
    print(f"  DFS (pilha) : {' -> '.join(dfs(grafo, origem))}")
    print("\n  mesmo grafo, mesma origem: a ordem muda porque a estrutura")
    print("  auxiliar muda - fila devolve por camadas, pilha mergulha fundo.")

    componentes = componentes_conexos(grafo, nomes)
    print(f"\ncomponentes conexos da malha ({len(componentes)}):")
    for grupo in componentes:
        print(f"  {{{', '.join(grupo)}}}")
    if len(componentes) > 1:
        isolados = [grupo[0] for grupo in componentes if len(grupo) == 1]
        if isolados:
            print(f"\n  atencao: {', '.join(isolados)} nao tem rua cadastrada -")
            print("  nenhuma entrega alcanca esse ponto partindo dos demais.")


if __name__ == "__main__":
    main()
