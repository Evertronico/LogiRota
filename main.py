"""
LogiRota - Semana 1: persistencia.

Pontos, ruas e pedidos agora vivem no banco (logirota.db) e sobrevivem
ao fechar o programa.

    python main.py
"""

import sqlite3

from logirota import banco
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# Dados iniciais: gravados no banco SO na primeira execucao.
PONTOS_INICIAIS = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),
    Ponto("Farmacia Ilha", "Ilha", 25, 25),  # isolado de proposito
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
    """Cadastro inicial so se o banco ainda nao tem pontos - evita
    duplicar dados a cada execucao."""
    if banco.listar_pontos():
        return
    for ponto in PONTOS_INICIAIS:
        banco.salvar_ponto(ponto)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)
    print("(primeira execucao: dados iniciais gravados no banco)\n")


def carregar_pontos():
    """Converte tuplas do banco em objetos Ponto - responsabilidade do
    dominio/main, nao da persistencia."""
    return [Ponto(nome, bairro, x, y)
            for nome, bairro, x, y in banco.listar_pontos()]


def montar_grafo(pontos):
    grafo = GrafoLista(pontos)
    for origem, destino in banco.listar_ruas():
        grafo.adicionar_rua(origem, destino)
    return grafo


def mostrar_pontos(pontos):
    print("\nPontos cadastrados:")
    for ponto in pontos:
        print(f"  - {ponto}")


def mostrar_ruas():
    print("\nRuas cadastradas:")
    for origem, destino in banco.listar_ruas():
        print(f"  - {origem} <-> {destino}")


def mostrar_pedidos():
    pedidos = banco.listar_pedidos_pendentes()
    print("\nPedidos pendentes:")
    if not pedidos:
        print("  (nenhum pedido pendente)")
    for _id, destino, status in pedidos:
        print(f"  #{_id} {destino} ({status})")


def cadastrar_pedido(pontos):
    nomes = [p.nome for p in pontos]
    print("\nDestinos disponiveis:")
    for i, nome in enumerate(nomes, start=1):
        print(f"  {i}. {nome}")
    escolha = input("Numero do destino: ").strip()
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(nomes):
        print("  opcao invalida.")
        return
    destino = nomes[int(escolha) - 1]
    try:
        numero = banco.salvar_pedido(destino)
    except sqlite3.IntegrityError:
        print("  destino nao cadastrado.")
        return
    print(f"  pedido #{numero} cadastrado para {destino}.")


def main():
    banco.inicializar()
    popular_se_vazio()

    pontos = carregar_pontos()
    grafo = montar_grafo(pontos)  # sera usado a partir da Semana 2

    print("LogiRota - persistencia de dados")
    while True:
        print("\n1) Listar pontos   2) Listar ruas   3) Novo pedido")
        print("4) Pedidos pendentes   0) Sair")
        opcao = input("Opcao: ").strip()
        if opcao == "1":
            mostrar_pontos(pontos)
        elif opcao == "2":
            mostrar_ruas()
        elif opcao == "3":
            cadastrar_pedido(pontos)
        elif opcao == "4":
            mostrar_pedidos()
        elif opcao == "0":
            break
        else:
            print("  opcao invalida.")


if __name__ == "__main__":
    main()