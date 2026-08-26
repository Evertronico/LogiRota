"""
Árvore binária — Módulo 3 aplicado ao LogiRota.

A operação organiza a cidade em zonas: a região central se divide em duas
sub-regiões, que se dividem em bairros. Isso é uma hierarquia, e hierarquia
é exatamente o que a árvore representa.

Nesta aula a árvore é montada à mão, para fixar a anatomia. A partir da
Aula 03 ela passa a se organizar sozinha, por comparação de chaves.

Vocabulário fixado aqui:

  raiz      nó sem pai — o início da hierarquia
  filho     nó ligado abaixo de outro
  folha     nó sem filhos — o fim de um ramo
  altura    número de ligações do nó até a folha mais distante
"""


class No:
    """Um nó da árvore: um valor e no máximo dois filhos."""

    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita

    def eh_folha(self):
        return self.esquerda is None and self.direita is None

    def __str__(self):
        return str(self.valor)


def altura(no):
    """Altura do nó: ligações até a folha mais distante.

    A definição é recursiva porque a estrutura é recursiva: cada filho é,
    ele próprio, a raiz de uma árvore menor.

    Convenção: árvore vazia tem altura -1, folha tem altura 0.
    """
    if no is None:
        return -1
    return 1 + max(altura(no.esquerda), altura(no.direita))


def total_nos(no):
    """Quantos nós existem na árvore."""
    if no is None:
        return 0
    return 1 + total_nos(no.esquerda) + total_nos(no.direita)


def folhas(no):
    """Valores das folhas — no LogiRota, os bairros que recebem entrega."""
    if no is None:
        return []
    if no.eh_folha():
        return [no.valor]
    return folhas(no.esquerda) + folhas(no.direita)


def desenhar(no, recuo=0):
    """Imprime a árvore deitada, com a raiz à esquerda.

    Percorre direita, depois raiz, depois esquerda — por isso o desenho
    sai com o filho direito em cima. Percursos são o tema da Aula 04.
    """
    if no is None:
        return
    desenhar(no.direita, recuo + 1)
    print("      " * recuo + str(no.valor))
    desenhar(no.esquerda, recuo + 1)
