"""
LogiRota — Semana 1: persistência em SQLite.

Pontos, ruas e pedidos agora vivem em logirota.db. As listas fixas abaixo
só servem para popular o banco na primeira execução; depois disso o
programa lê tudo do banco.

    python3 main.py
"""

from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# so semente: usada apenas se o banco estiver vazio
PONTOS_INICIAIS = [
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


def popular_se_vazio():
    # checa antes de inserir, senao duplicaria a cada execucao
    # pontos primeiro: ruas referenciam pontos (foreign key)
    if not banco.listar_pontos():
        for ponto in PONTOS_INICIAIS:
            banco.salvar_ponto(ponto)
    if not banco.listar_ruas():
        for origem, destino in RUAS_INICIAIS:
            banco.salvar_rua(origem, destino)


def carregar_pontos():
    # tupla -> Ponto: essa conversao e do dominio, nao do banco
    return [Ponto(nome, bairro, x, y)
            for nome, bairro, x, y in banco.listar_pontos()]


def montar(pontos):
    grafo = GrafoLista(pontos)
    for a, b in banco.listar_ruas():
        grafo.adicionar_rua(a, b)
    return grafo


def main():
    banco.inicializar()
    popular_se_vazio()

    print("LogiRota - BFS, DFS e conectividade da malha\n")

    pontos = carregar_pontos()
    grafo = montar(pontos)
    origem = "Posto Central"

    ordem_bfs = bfs(grafo, origem)
    ordem_dfs = dfs(grafo, origem)

    print(f"partindo de '{origem}':\n")
    print(f"  BFS (fila) .: {' -> '.join(ordem_bfs)}")
    print(f"  DFS (pilha) : {' -> '.join(ordem_dfs)}")
    print("\n  mesmo grafo, mesma origem: a ordem muda porque a estrutura")
    print("  auxiliar muda - fila devolve por camadas, pilha mergulha fundo.")

    nomes = [ponto.nome for ponto in pontos]
    componentes = componentes_conexos(grafo, nomes)

    print(f"\ncomponentes conexos da malha ({len(componentes)}):")
    for grupo in componentes:
        print(f"  {{{', '.join(grupo)}}}")

    if len(componentes) > 1:
        isolados = [g[0] for g in componentes if len(g) == 1]
        print(f"\n  atencao: {', '.join(isolados)} nao tem rua cadastrada -")
        print("  nenhuma entrega alcanca esse ponto partindo dos demais.")

    # pedidos: mostra o que ja estava salvo, depois deixa cadastrar mais um
    pedidos = banco.listar_pedidos_pendentes()
    print(f"\npedidos pendentes ({len(pedidos)}):")
    for id_pedido, destino in pedidos:
        print(f"  #{id_pedido} -> {destino}")

    novo = input("\nnovo pedido - destino (enter para pular): ").strip()
    if novo in nomes:
        id_pedido = banco.salvar_pedido(novo)
        print(f"  pedido #{id_pedido} salvo -> {novo}")
    elif novo:
        print("  ponto nao cadastrado, nada salvo.")


if __name__ == "__main__":
    main()