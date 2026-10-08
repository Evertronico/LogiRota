"""
LogiRota — Semana 1 (Projeto Final): persistência de dados. Daniel.

Até a Aula 07 os pontos e as ruas viviam em listas fixas no código e se
perdiam ao fechar o programa. A partir desta versão o banco de dados é a
fonte de verdade: a malha e os pedidos são lidos de logirota/banco.py, e
o que for cadastrado numa execução aparece na execução seguinte.

    python3 main.py                            mostra a malha e os pedidos
    python3 main.py --pedido "Oficina Safira"  cadastra um pedido pendente

Com DATABASE_URL definida o banco é o PostgreSQL do docker-compose.yml;
sem ela, o arquivo SQLite logirota.db (ver README.md).
"""

import sys

from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# Malha inicial das aulas anteriores: gravada no banco só na primeira
# execução (banco vazio). Depois disso o programa lê tudo do banco.
PONTOS_INICIAIS = [
    ("Mercado Barra", "Barra", 2, 8),
    ("Farmacia Bela Vista", "Bela Vista", 6, 3),
    ("Oficina Safira", "Safira", 9, 5),
    ("Padaria Distrito", "Distrito", 12, 1),
    ("Loja Boa Familia", "Boa Familia", 14, 0),
    ("Posto Central", "Centro", 5, 5),
    ("Escola Norte", "Zona Norte", 3, 9),
    # Cadastrado no sistema, mas nenhuma rua liga este ponto aos demais.
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


def popular_se_vazio():
    """Grava a malha inicial apenas se o banco ainda não tem pontos —
    sem essa checagem, cada execução duplicaria o cadastro."""
    if not banco.banco_vazio():
        return False
    for nome, bairro, x, y in PONTOS_INICIAIS:
        banco.salvar_ponto(nome, bairro, x, y)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)
    return True


def carregar_pontos():
    """Converte as tuplas do banco em objetos Ponto — tarefa do domínio,
    não da camada de persistência."""
    return [Ponto(nome, bairro, x, y) for nome, bairro, x, y in banco.listar_pontos()]


def montar(pontos, ruas):
    grafo = GrafoLista(pontos)
    for a, b in ruas:
        grafo.adicionar_rua(a, b)
    return grafo


def cadastrar_pedido(destino, nomes):
    if destino not in nomes:
        print(f"ponto '{destino}' nao existe. Pontos cadastrados:")
        for nome in nomes:
            print(f"  - {nome}")
        return
    id_pedido = banco.salvar_pedido(destino)
    print(f"pedido #{id_pedido} cadastrado para '{destino}'.\n")


def main():
    print("LogiRota - persistencia de dados (Semana 1)\n")

    banco.inicializar()
    if popular_se_vazio():
        print(f"primeira execucao: malha inicial gravada em {banco.descrever_banco()}.\n")
    else:
        print(f"malha carregada de {banco.descrever_banco()}.\n")

    pontos = carregar_pontos()
    nomes = [ponto.nome for ponto in pontos]

    if len(sys.argv) == 3 and sys.argv[1] == "--pedido":
        cadastrar_pedido(sys.argv[2], nomes)

    ruas = banco.listar_ruas()
    grafo = montar(pontos, ruas)
    origem = "Posto Central"

    print(f"{len(pontos)} pontos e {len(ruas)} ruas no banco.")
    print(f"partindo de '{origem}':")
    print(f"  BFS (fila) .: {' -> '.join(bfs(grafo, origem))}")
    print(f"  DFS (pilha) : {' -> '.join(dfs(grafo, origem))}")

    componentes = componentes_conexos(grafo, nomes)
    isolados = [g[0] for g in componentes if len(g) == 1]
    if isolados:
        print(f"  atencao: {', '.join(isolados)} sem rua cadastrada.")

    pendentes = banco.listar_pedidos_pendentes()
    print(f"\npedidos pendentes ({len(pendentes)}):")
    if not pendentes:
        print('  nenhum - cadastre com: python3 main.py --pedido "Oficina Safira"')
    for id_pedido, destino, status in pendentes:
        print(f"  #{id_pedido} {destino} ({status})")


if __name__ == "__main__":
    main()
