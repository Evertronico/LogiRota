"""
Percursos em árvore — Módulo 3 aplicado ao LogiRota.

Até aqui os algoritmos tocavam nós isolados: `altura` mede um caminho,
`buscar` visita só o que precisa. Um percurso é diferente — visita TODOS
os nós da árvore, exatamente uma vez cada, numa ordem definida. A ordem
não é acidente: cada uma das três variações clássicas responde a uma
pergunta diferente sobre a mesma árvore.

Os percursos são genéricos — funcionam sobre qualquer No, seja ele um
nó da ABB de pontos (Aula 03) ou um nó da hierarquia de zonas (Aula 02).

Reaproveita de logirota/arvore.py:
    No, esquerda, direita
"""


def em_ordem(no, saida=None):
    """Esquerda, raiz, direita.

    Numa ABB, em-ordem visita as chaves em ordem crescente — é o
    percurso que prova, na prática, que a estrutura mantém os
    elementos ordenados sem que nada precise ser ordenado depois.
    """
    if saida is None:
        saida = []
    if no is not None:
        em_ordem(no.esquerda, saida)
        saida.append(no.valor)
        em_ordem(no.direita, saida)
    return saida


def pre_ordem(no, saida=None):
    """Raiz, esquerda, direita.

    Visita cada nó antes de seus filhos: serve para relatórios que
    apresentam o todo antes das partes, como um manifesto que lista
    uma zona e só depois desce aos bairros que ela contém.
    """
    if saida is None:
        saida = []
    if no is not None:
        saida.append(no.valor)
        pre_ordem(no.esquerda, saida)
        pre_ordem(no.direita, saida)
    return saida


def pos_ordem(no, saida=None):
    """Esquerda, direita, raiz.

    Visita cada nó só depois de seus filhos: serve para relatórios de
    fechamento, em que uma zona só é dada como concluída depois que
    todas as suas subzonas já foram — a ordem inversa da pré-ordem.
    """
    if saida is None:
        saida = []
    if no is not None:
        pos_ordem(no.esquerda, saida)
        pos_ordem(no.direita, saida)
        saida.append(no.valor)
    return saida
