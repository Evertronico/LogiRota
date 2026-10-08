class PilhaDeOperacoes:

    def __init__(self):
        self._itens = []

    def empilhar(self, operacao):
        self._itens.append(operacao)

    def desempilhar(self):
        if self.vazia():
            raise IndexError("nada a desfazer")
        return self._itens.pop()

    def topo(self):
        if self.vazia():
            raise IndexError("nada a desfazer")
        return self._itens[-1]

    def vazia(self):
        return len(self._itens) == 0

    def __len__(self):
        return len(self._itens)