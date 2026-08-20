"""
Balanceamento de ABB - Módulo 3 aplicado ao LogiRota.

A aula 03 mostrou o problema: a ordem de inserção decide
a forma da árvore, e uma sequência já ordenada degenera
o índice até ele virar, na prática, uma lista encadeada
disfarçada de árvore. Esta aula ataca o problema com uma
única operação - a rotação - aplicada logo após cada 
inserção, sem violar em nenhum instante a regra da ABB

Fator de balanceamento de um nó: altura da subárvore 
direita menos a da subárvore esquerda. Zero é o ideal;
1 ou -1 ainda é aceitável; 2 ou -2 é desequilíbrio, e 
é o gatilho da rotação.

Reaproveita de logirota/arvore.py:
    No, altura
Reaproveita a regra de comparação de logirota/abb.py
(ponto.nome) - `inserir_balanceado` não é uma estrutura nova,
é `abb.inserir` com uma checagem extra ao subir da recursão.

Escopo desta aula: os dois casos retos (tudo para um lado
só), que se resolvem com uma única rotação. Os dois casos
mistos - que exigem rotação dupla - ficam como desafio extra
opcional.
"""

from logirota.arvore import No, altura

def fator_balanceamento(no):
    """Altura da subárvore direita menos a da esquerda.
    
    Positivo pesa para a direita, negativo para a esquerda.
    Um nó ausente (None) não desequlibra nada: fator zero
    por convenção
    """
    if no is None:
        return 0;
    return altura(no.direita) - altura(no.esquerda)

def rotacionar_direita(no):
    """Corrige desequilibrio à esquerda: o filo à esquerda
    sobe.

    `no` desce e vira filho direito do próprio filho esquerdo.
    A subárvore direita do filho esquerdo - que ainda 
    respeita a ordem da ABB em relação a `no` - passa a
    ser a subárvore esquerda de `no`. Só esses dois ponteiros
    mudam.
    """
    novo_topo = no.esquerda
    no.esquerda = novo_topo.direita
    novo_topo.direita = no
    return novo_topo

def rotacionar_esquerda(no):
    """Corrige desequilíbio à direita: o filho direito
    sobe.

    Espelho exato de `rotacionar_direita`: `no` desce e
    vira filho esquerdo do próprio filho direito.
    """
    novo_topo = no.direita
    no.direita = novo_topo.esquerda
    novo_topo.esquerda = no
    return novo_topo

def inserir_balanceado(raiz, ponto):
    """Insere `ponto` como `abb.inserir`, mas corrige o
    fator de balanceamento de cada nó no caminho de volta
    da recursão.

    A checagem acontece depois de cada chamada recursiva, 
    ou seja, de baixo para cima: o nó mais próximo da 
    inserção é corrigido primeiro, e a rotação já devolve
    aquele ramo com a altura de antes da inserção - por 
    isso, nos casos retor, uma única rotação não basta.
    """
    if raiz is None:
        return No(ponto)
    if ponto.nome < raiz.valor.nome:
        raiz.esquerda = inserir_balanceado(raiz.esquerda, ponto)
    else:
        raiz.direita = inserir_balanceado(raiz.direita, ponto)

    fb = fator_balanceamento(raiz)
    if fb == -2: # pesado à esquerda
        raiz = rotacionar_direita(raiz)
    elif fb == 2: # pesado à direita
        raiz = rotacionar_esquerda(raiz)
    return raiz

def constuir_indice_balanceado(pontos):
    """Mesma ideia de `abb.construir_indice`, agora
    rebalanceando o indice a cada inserção, e não só
    no final.
    """
    raiz = None
    for ponto in pontos:
        raiz = inserir_balanceado(raiz, ponto)
    return raiz