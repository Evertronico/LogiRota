class FilaDePedidos:
    def __init__(self):
        self._itens = []

    def enfileirar(self, pedido):
        self._itens.append(pedido)

    def desenfileirar(self):
        if self.vazia():
            raise IndexError("fila de pedidos vazia")
        return self._itens.pop(0)

    def frente(self):
        if self.vazia():
            raise IndexError("fila de pedidos vazia")
        return self._itens[0]

    def vazia(self):
        return len(self._itens) == 0

    def __len__(self):
        return len(self._itens)