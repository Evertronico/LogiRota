"""
LogiRota — versão 7 (Aula 07).

A Aula 06 construiu a malha viária como grafo. Esta versão percorre essa
mesma malha de duas formas — BFS e DFS — e usa a busca para responder
uma pergunta de negócio: existe algum ponto de entrega para o qual
nenhuma rua cadastrada leva?

    python3 main.py
"""

from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# # Dados iniciais: so sao gravados no banco se ele estiver vazio.
# PONTOS_INICIAIS = [
#     ("Mercado Barra", "Barra", 2, 8),
#     ("Farmacia Bela Vista", "Bela Vista", 6, 3),
#     ("Oficina Safira", "Safira", 9, 5),
#     ("Padaria Distrito", "Distrito", 12, 1),
#     ("Loja Boa Familia", "Boa Familia", 14, 0),
#     ("Posto Central", "Centro", 5, 5),
#     ("Escola Norte", "Zona Norte", 3, 9),
#     ("Farmacia Ilha", "Ilha", 25, 25),
# ]

# RUAS_INICIAIS = [
#     ("Escola Norte", "Mercado Barra"),
#     ("Mercado Barra", "Farmacia Bela Vista"),
#     ("Mercado Barra", "Posto Central"),
#     ("Farmacia Bela Vista", "Posto Central"),
#     ("Posto Central", "Oficina Safira"),
#     ("Posto Central", "Padaria Distrito"),
#     ("Oficina Safira", "Padaria Distrito"),
#     ("Padaria Distrito", "Loja Boa Familia"),
# ]


def popular_se_vazio():
    if len(banco.listar_pontos()) > 0:
        return
    for nome, bairro, x, y in PONTOS_INICIAIS:
        banco.salvar_ponto(nome, bairro, x, y)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)
    banco.salvar_pedido("Mercado Barra")


def montar():
    # converte as tuplas do banco em objetos Ponto (responsabilidade do main)
    pontos = [Ponto(nome, bairro, x, y)
              for nome, bairro, x, y in banco.listar_pontos()]
    grafo = GrafoLista(pontos)
    for origem, destino in banco.listar_ruas():
        grafo.adicionar_rua(origem, destino)
    return grafo, pontos


def main():
    print("LogiRota - BFS, DFS e conectividade da malha\n")

    banco.inicializar()
    popular_se_vazio()

    grafo, PONTOS = montar()
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

    print("\npedidos pendentes:")
    for id_pedido, destino, status in banco.listar_pedidos_pendentes():
        print(f"  #{id_pedido} {destino} ({status})")

    if len(componentes) > 1:
        isolados = [g[0] for g in componentes if len(g) == 1]
        print(f"\n  atencao: {', '.join(isolados)} nao tem rua cadastrada -")
        print("  nenhuma entrega alcanca esse ponto partindo dos demais.")


if __name__ == "__main__":
    main()
