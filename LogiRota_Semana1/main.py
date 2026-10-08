from logirota import banco
from logirota.busca import bfs, dfs, componentes_conexos
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

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

def preparar_banco():
    banco.inicializar()
    if not banco.listar_pontos():
        for nome, bairro, x, y in PONTOS_INICIAIS:
            banco.salvar_ponto(Ponto(nome, bairro, x, y))
        for origem, destino in RUAS_INICIAIS:
            banco.salvar_rua(origem, destino)

def montar():
    pontos = [Ponto(*dados) for dados in banco.listar_pontos()]
    grafo = GrafoLista(pontos)
    for origem, destino in banco.listar_ruas():
        grafo.adicionar_rua(origem, destino)
    return grafo, pontos

def main():
    preparar_banco()
    grafo, pontos = montar()
    print("LogiRota - Semana 1: dados carregados do SQLite")
    print(f"Pontos: {len(pontos)} | Ruas: {len(banco.listar_ruas())}")
    origem = "Posto Central"
    if origem in [p.nome for p in pontos]:
        print("BFS:", " -> ".join(bfs(grafo, origem)))
        print("DFS:", " -> ".join(dfs(grafo, origem)))
    grupos = componentes_conexos(grafo, [p.nome for p in pontos])
    print("Componentes conexos:", len(grupos))
    pedidos = banco.listar_pedidos_pendentes()
    print("Pedidos pendentes:", len(pedidos))
    for numero, destino, status in pedidos:
        print(f"  #{numero} - {destino} ({status})")

if __name__ == "__main__":
    main()
