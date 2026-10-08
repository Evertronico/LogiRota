"""
LogiRota — versão 7 (Aula 07).

A Aula 06 construiu a malha viária como grafo. Esta versão percorre essa
mesma malha de duas formas — BFS e DFS — e usa a busca para responder
uma pergunta de negócio: existe algum ponto de entrega para o qual
nenhuma rua cadastrada leva?

    python3 main.py
"""

from logirota.busca import bfs, componentes_conexos, dfs
from logirota import banco
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# Dados da aula usados somente para a primeira carga do banco vazio.
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


def montar():
    pontos = [Ponto(*registro) for registro in banco.listar_pontos()]
    ruas = banco.listar_ruas()
    grafo = GrafoLista(pontos)
    for a, b in ruas:
        grafo.adicionar_rua(a, b)
    return pontos, grafo, len(ruas)


def carregar_dados_iniciais_se_necessario():
    """Migra os dados da aula uma vez, sem sobrescrever um banco existente."""
    if banco.listar_pontos():
        return

    for ponto in PONTOS_INICIAIS:
        banco.salvar_ponto(ponto)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)


def main():
    print("LogiRota - BFS, DFS e conectividade da malha\n")

    banco.inicializar()
    carregar_dados_iniciais_se_necessario()
    pontos, grafo, total_ruas = montar()
    pedidos_pendentes = banco.listar_pedidos_pendentes()

    if not pontos:
        print("Nenhum ponto cadastrado no banco de dados.")
        return

    origem = next(
        (ponto.nome for ponto in pontos if ponto.nome == "Posto Central"),
        pontos[0].nome,
    )

    ordem_bfs = bfs(grafo, origem)
    ordem_dfs = dfs(grafo, origem)

    print(f"pontos carregados do banco: {len(pontos)}")
    print(f"ruas carregadas do banco: {total_ruas}")
    print(f"pedidos pendentes carregados do banco: {len(pedidos_pendentes)}")
    for pedido_id, destino, _status in pedidos_pendentes:
        print(f"  pedido {pedido_id}: {destino}")

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


if __name__ == "__main__":
    main()
