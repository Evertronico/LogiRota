
from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

PONTOS_INICIAIS = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),

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

def montar():
    banco.inicializar()

    if not banco.listar_pontos():
        for ponto in PONTOS_INICIAIS:
            banco.salvar_ponto(ponto)
        for a, b in RUAS_INICIAIS:
            banco.salvar_rua(a, b)

    pontos = [Ponto(nome, bairro, x, y)
              for nome, bairro, x, y in banco.listar_pontos()]
    grafo = GrafoLista(pontos)
    for a, b in banco.listar_ruas():
        grafo.adicionar_rua(a, b)
    return grafo, pontos

def main():
    print("LogiRota - BFS, DFS e conectividade da malha\n")

    grafo, pontos = montar()
    pedidos_pendentes = banco.listar_pedidos_pendentes()
    print(f"Pedidos pendentes salvos no banco: {len(pedidos_pendentes)}\n")
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

if __name__ == "__main__":
    main()

