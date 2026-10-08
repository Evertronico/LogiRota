from logirota.arvore import No, altura

def fator_balanceamento(no):
    if no is None:
        return 0
    return altura(no.direita) - altura(no.esquerda)

def rotacionar_direita(no):
    novo_topo = no.esquerda
    no.esquerda = novo_topo.direita
    novo_topo.direita = no
    return novo_topo

def rotacionar_esquerda(no):
    novo_topo = no.direita
    no.direita = novo_topo.esquerda
    novo_topo.esquerda = no
    return novo_topo

def inserir_balanceado(raiz, ponto):
    if raiz is None:
        return No(ponto)
    if ponto.nome < raiz.valor.nome:
        raiz.esquerda = inserir_balanceado(raiz.esquerda, ponto)
    else:
        raiz.direita = inserir_balanceado(raiz.direita, ponto)

    fb = fator_balanceamento(raiz)
    if fb == -2:                       # pesado à esquerda
        raiz = rotacionar_direita(raiz)
    elif fb == 2:                      # pesado à direita
        raiz = rotacionar_esquerda(raiz)
    return raiz

def construir_indice_balanceado(pontos):
    raiz = None
    for ponto in pontos:
        raiz = inserir_balanceado(raiz, ponto)
    return raiz