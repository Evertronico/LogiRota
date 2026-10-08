from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
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


def popular_banco_se_vazio():
    if not banco.banco_vazio():
        return
    for nome, bairro, x, y in PONTOS_INICIAIS:
        banco.salvar_ponto(nome, bairro, x, y)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)


def carregar_malha():
    """Le o banco e monta os objetos de dominio (tupla -> Ponto)."""
    pontos = [Ponto(n, b, x, y) for n, b, x, y in banco.listar_pontos()]
    grafo = GrafoLista(pontos)
    for origem, destino in banco.listar_ruas():
        grafo.adicionar_rua(origem, destino)
    return pontos, grafo


def cadastrar_pedido(pontos):
    nomes = [p.nome for p in pontos]
    print("\nPontos disponiveis:")
    for i, nome in enumerate(nomes, start=1):
        print(f"  {i}. {nome}")
    escolha = input("Numero do destino (Enter cancela): ").strip()
    if not escolha:
        return
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(nomes):
        print("Opcao invalida.")
        return
    destino = nomes[int(escolha) - 1]
    banco.salvar_pedido(destino)
    print(f"Pedido para '{destino}' cadastrado.")


def listar_pedidos():
    pedidos = banco.listar_pedidos_pendentes()
    print(f"\nPedidos pendentes ({len(pedidos)}):")
    if not pedidos:
        print("  nenhum pedido pendente.")
    for _id, destino, status in pedidos:
        print(f"  #{_id} {destino} ({status})")


def mostrar_malha(pontos, grafo):
    origem = "Posto Central"
    print(f"\nBFS a partir de '{origem}': {' -> '.join(bfs(grafo, origem))}")
    print(f"DFS a partir de '{origem}': {' -> '.join(dfs(grafo, origem))}")
    componentes = componentes_conexos(grafo, [p.nome for p in pontos])
    print(f"Componentes conexos ({len(componentes)}):")
    for grupo in componentes:
        print(f"  {{{', '.join(grupo)}}}")


def main():
    banco.inicializar()
    popular_banco_se_vazio()
    pontos, grafo = carregar_malha()

    print("LogiRota - persistencia em banco de dados")
    print(f"{len(pontos)} pontos e {len(banco.listar_ruas())} ruas carregados do banco.")

    while True:
        print("\n1. Cadastrar pedido")
        print("2. Listar pedidos pendentes")
        print("3. Ver malha (BFS, DFS, componentes)")
        print("0. Sair")
        opcao = input("Opcao: ").strip()
        if opcao == "1":
            cadastrar_pedido(pontos)
        elif opcao == "2":
            listar_pedidos()
        elif opcao == "3":
            mostrar_malha(pontos, grafo)
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
