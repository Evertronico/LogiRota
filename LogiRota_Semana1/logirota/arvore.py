class No:

    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita

    def eh_folha(self):
        return self.esquerda is None and self.direita is None

    def __str__(self):
        return str(self.valor)

def altura(no):
    
    if no is None:
        return -1
    return 1 + max(altura(no.esquerda), altura(no.direita))

def total_nos(no):
    if no is None:
        return 0
    return 1 + total_nos(no.esquerda) + total_nos(no.direita)

def folhas(no):
    if no is None:
        return []
    if no.eh_folha():
        return [no.valor]
    return folhas(no.esquerda) + folhas(no.direita)

def desenhar(no, recuo=0):
    if no is None:
        return
    desenhar(no.direita, recuo + 1)
    print("      " * recuo + str(no.valor))
    desenhar(no.esquerda, recuo + 1)