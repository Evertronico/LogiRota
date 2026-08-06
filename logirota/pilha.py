"""
Pilha de operações — Módulo 2 aplicado ao projeto.

LIFO: desfazer significa reverter sempre a última operação registrada, e não
a primeira. É a estrutura correta aqui porque a ordem de desfazimento é o
inverso exato da ordem de execução.
"""


class PilhaDeOperacoes:
    """Operações: empilhar, desempilhar, topo, vazia, len."""

    def __init__(self):
        self._itens = []

    def empilhar(self, operacao):
        """Registra uma operação no topo."""
        self._itens.append(operacao)

    def desempilhar(self):
        """Remove e devolve a operação mais recente."""
        if self.vazia():
            raise IndexError("nada a desfazer")
        # pop() no fim da lista não desloca nada: custo constante.
        # Compare com FilaDePedidos.desenfileirar, que usa pop(0).
        return self._itens.pop()

    def topo(self):
        """Consulta a última operação sem removê-la."""
        if self.vazia():
            raise IndexError("nada a desfazer")
        return self._itens[-1]

    def vazia(self):
        return len(self._itens) == 0

    def __len__(self):
        return len(self._itens)
