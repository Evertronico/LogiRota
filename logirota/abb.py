from logirota.arvore import No

# definição para inserir um ponto na ABB
def inserir(raiz, ponto):
    if raiz is None:
        return No(ponto)
    if ponto.nome < raiz.valor.nome:
        raiz.esquerda = inserir(raiz.esquerda, ponto)
    else:
        raiz.direita = inserir(raiz.direita, ponto)
    return raiz

# definição que busca por 'nome'
def buscar(raiz, nome):
    if raiz is None:
        return None
    if nome == raiz.valor.nome:
        return raiz.valor
    if nome < raiz.valor.nome:
        return buscar(raiz.esquerda, nome)
    return buscar(raiz.direita, nome)

# insere uma lista de pontos, um por um, e devolve a raiz da ABB
def construir_indice(pontos):
    raiz = None
    for ponto in pontos:
        raiz = inserir(raiz, ponto)
    return raiz