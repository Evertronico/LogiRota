def em_ordem(no, saida=None):
    if saida is None:
        saida = []
    if no is not None:
        em_ordem(no.esquerda, saida)
        saida.append(no.valor)
        em_ordem(no.direita, saida)
    return saida

def pre_ordem(no, saida=None):
    if saida is None:
        saida = []
    if no is not None:
        saida.append(no.valor)
        pre_ordem(no.esquerda, saida)
        pre_ordem(no.direita, saida)
    return saida

def pos_ordem(no, saida=None):
    if saida is None:
        saida = []
    if no is not None:
        pos_ordem(no.esquerda, saida)
        pos_ordem(no.direita, saida)
        saida.append(no.valor)
    return saida