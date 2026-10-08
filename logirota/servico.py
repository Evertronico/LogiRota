"""
Camada de serviço do LogiRota — a ponte entre a persistência e o domínio.

banco.py devolve tuplas e não conhece Ponto nem grafo; ponto.py e grafo.py não
conhecem o banco. Quem junta os dois é este módulo: lê as tuplas, transforma em
Pontos, monta o grafo e chama o Dijkstra. A interface (main.py) só chama
funções daqui — nunca calcula distância sozinha.

Reaproveita:
    Ponto de LogiRota/ponto.py
    GrafoLista de LogiRota/grafo.py
    dijkstra, reconstruir_caminho de LogiRota/caminho.py
    funções de LogiRota/banco.py
"""

from LogiRota import banco
from LogiRota.caminho import dijkstra, reconstruir_caminho
from LogiRota.grafo import GrafoLista
from LogiRota.ponto import Ponto


class SemRotaError(Exception):
    """Os dois pontos existem, mas nenhuma sequência de ruas liga um ao outro."""


def semear_se_vazio(pontos, ruas):
    """Grava os pontos e ruas fixos só na primeira execução (banco vazio).

    Devolve True se gravou, False se o banco já tinha dados.
    """
    if banco.contar_pontos() > 0:
        return False
    for ponto in pontos:
        banco.salvar_ponto(ponto)
    for nome_a, nome_b in ruas:
        banco.salvar_rua(nome_a, nome_b)
    return True


def carregar_pontos():
    """Converte as tuplas do banco em objetos Ponto."""
    return [Ponto(nome, bairro, x, y) for nome, bairro, x, y in banco.listar_pontos()]


def carregar_ruas():
    """Ruas são de mão dupla: (A, B) e (B, A) contam como a mesma rua."""
    vistas = set()
    ruas = []
    for origem, destino in banco.listar_ruas():
        chave = frozenset((origem, destino))
        if chave not in vistas:
            vistas.add(chave)
            ruas.append((origem, destino))
    return ruas


def cadastrar_ponto(nome, bairro, x, y):
    """Devolve False se já existe um ponto com esse nome."""
    return banco.salvar_ponto(Ponto(nome, bairro, x, y))


def cadastrar_rua(nome_a, nome_b):
    """Liga dois pontos já cadastrados. Devolve False se a rua já existia (em qualquer sentido)."""
    if nome_a == nome_b:
        raise ValueError("Uma rua precisa ligar dois pontos diferentes.")
    if frozenset((nome_a, nome_b)) in {frozenset(r) for r in carregar_ruas()}:
        return False
    return banco.salvar_rua(nome_a, nome_b)


def caminho_entre(origem, destino):
    """Menor caminho entre dois pontos cadastrados: devolve (lista_de_nomes, distancia_km).

    ValueError se algum nome não existe; SemRotaError se não há ruas ligando os dois.
    """
    pontos = carregar_pontos()
    nomes = [p.nome for p in pontos]
    for nome in (origem, destino):
        if nome not in nomes:
            raise ValueError(f"Ponto '{nome}' nao esta cadastrado.")

    grafo = GrafoLista(pontos)
    for nome_a, nome_b in carregar_ruas():
        grafo.adicionar_rua(nome_a, nome_b)

    distancia, predecessor = dijkstra(grafo, nomes, origem)
    caminho = reconstruir_caminho(predecessor, origem, destino)
    if not caminho:
        raise SemRotaError(f"Nenhuma rua liga '{origem}' a '{destino}'.")
    return caminho, distancia[destino]
