class No:
    # um nó da árvore: um valor e o máximo dois fihos
    def __init__(self, valor, esquerda=None, direita=None):
        # inicializa o nó com valor e filhos
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita

    # método responsável por verificar se o nó é uma folha
    def eh_folha(self):
        return self.esquerda is None and self.direita is None

    # retorna a representação em string do nó
    def __str__(self):
        return str(self.valor)

# função para verificar a altura da árvore a partir de um nó
def altura(no):
    # altura do nó: ligações até a folha mais distante
    # a definição é recursiva porque a estrutura é recursiva
    # cada filho é, ele próprio, a raiz de uma árvore menor
    if no is None:
        return 0
    return 1 + max(altura(no.esquerda), altura(no.direita))

# definição que verifica quantos nós existem em uma árvore
def total_nos(no):
    if no is None:
        return 0
    return 1 + total_nos(no.esquerda) + total_nos(no.direita)

# definição que recupera os valores das folhas de uma árvore
def folhas(no):
    # valores das folhas - no LogiRota os bairros que recebem entregas
    if no is None:
        return []
    if no.eh_folha():
        return [no.valor]
    return folhas(no.esquerda) + folhas(no.direita)

# definição para desenhar a árvore
def desenhar(no, recuo=0):
    # imprime a árvore deitada com a raiz à esquerda
    # percorre direita, depois raiz, depois esquerda
    # por isso o desenho sai com o filho em cima
    if no is None:
        return
    desenhar(no.direita, recuo + 1)
    print("    " * recuo + str(no))
    desenhar(no.esquerda, recuo + 1)