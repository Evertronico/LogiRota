"""
Fila de pedidos — Módulo 2 aplicado ao projeto.

FIFO: o primeiro pedido a chegar é o primeiro a ser roteirizado. A fila é a
estrutura correta aqui porque a ordem de atendimento é a ordem de chegada.

Implementação própria, sem `collections.deque`: a estrutura em estudo só pode
ser usada pronta depois de ter sido escrita à mão.
"""


class FilaDePedidos:
    """Operações: enfileirar, desenfileirar, frente, vazia, len."""

    def __init__(self):
        self._itens = []

    def enfileirar(self, pedido):
        """Insere no fim da fila."""
        self._itens.append(pedido)

    def desenfileirar(self):
        """Remove e devolve o pedido mais antigo."""
        if self.vazia():
            raise IndexError("fila de pedidos vazia")
        # pop(0) desloca todos os elementos restantes: custo proporcional a n.
        # Esse custo será medido na Aula 09 e é o motivo de existirem
        # implementações encadeadas de fila.
        return self._itens.pop(0)

    def frente(self):
        """Consulta o próximo sem removê-lo."""
        if self.vazia():
            raise IndexError("fila de pedidos vazia")
        return self._itens[0]

    def vazia(self):
        return len(self._itens) == 0

    def __len__(self):
        return len(self._itens)
