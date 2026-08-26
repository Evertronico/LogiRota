"""
Árvore Binária de Busca (ABB) — Módulo 3 aplicado ao LogiRota.

Na Aula 02 a árvore era montada à mão: cada ligação era decidida pelo
programador, nó a nó. Aqui a árvore passa a se organizar sozinha. A regra
é única e vale em toda a estrutura: para qualquer nó, tudo o que está à
esquerda tem chave menor, e tudo o que está à direita tem chave maior ou
igual. Essa regra é o que torna a busca eficiente — a cada comparação,
um lado inteiro da árvore é descartado sem ser visitado.

O índice organiza objetos Ponto do LogiRota pela chave `nome`: cada
Ponto vira um No (mesma classe da Aula 02), e o resultado é um índice
alfabético de pontos de entrega.

Reaproveita de logirota/arvore.py:
    No, esquerda, direita, altura, desenhar
"""

from logirota.arvore import No


def inserir(raiz, ponto):
    """Insere `ponto` na ABB indexada por `ponto.nome`.

    Compara a chave do novo ponto com a chave da raiz para decidir o
    lado, desce recursivamente até encontrar uma subárvore vazia e
    religa o resultado. Devolve a raiz (nova, se `raiz` era None).
    """
    if raiz is None:
        return No(ponto)
    if ponto.nome < raiz.valor.nome:
        raiz.esquerda = inserir(raiz.esquerda, ponto)
    else:
        raiz.direita = inserir(raiz.direita, ponto)
    return raiz


def buscar(raiz, nome):
    """Busca por `nome`. Custo proporcional à altura, não ao total de nós.

    Cada comparação decide um único lado a seguir: a outra subárvore
    inteira é descartada sem ser visitada.
    """
    if raiz is None:
        return None
    if nome == raiz.valor.nome:
        return raiz.valor
    if nome < raiz.valor.nome:
        return buscar(raiz.esquerda, nome)
    return buscar(raiz.direita, nome)


def construir_indice(pontos):
    """Insere uma lista de pontos, um a um, e devolve a raiz da ABB.

    A ordem de chegada dos pontos não é escolha do índice — mas, como a
    Aula 02 já mostrou para árvores em geral, a forma resultante depende
    inteiramente dela.
    """
    raiz = None
    for ponto in pontos:
        raiz = inserir(raiz, ponto)
    return raiz
