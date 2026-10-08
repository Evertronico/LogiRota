
class GrafoMatriz:

    def __init__(self, pontos):
        self._pontos = list(pontos)
        self._indice = {p.nome: i for i, p in enumerate(self._pontos)}
        n = len(self._pontos)
        self._matriz = [[None] * n for _ in range(n)]

    def adicionar_rua(self, nome_a, nome_b):

        i, j = self._indice[nome_a], self._indice[nome_b]
        peso = self._pontos[i].distancia_ate(self._pontos[j])
        self._matriz[i][j] = peso
        self._matriz[j][i] = peso

    def sao_vizinhos(self, nome_a, nome_b):

        i, j = self._indice[nome_a], self._indice[nome_b]
        return self._matriz[i][j] is not None

    def vizinhos(self, nome):

        i = self._indice[nome]
        return [self._pontos[j].nome for j in range(len(self._pontos))
                if self._matriz[i][j] is not None]

    def total_celulas(self):

        return len(self._pontos) ** 2

class GrafoLista:

    def __init__(self, pontos):
        self._pontos = {p.nome: p for p in pontos}
        self._vizinhos = {nome: [] for nome in self._pontos}

    def adicionar_rua(self, nome_a, nome_b):
        peso = self._pontos[nome_a].distancia_ate(self._pontos[nome_b])
        self._vizinhos[nome_a].append((nome_b, peso))
        self._vizinhos[nome_b].append((nome_a, peso))

    def sao_vizinhos(self, nome_a, nome_b):

        for vizinho, _ in self._vizinhos[nome_a]:
            if vizinho == nome_b:
                return True
        return False

    def vizinhos(self, nome):

        return [vizinho for vizinho, _peso in self._vizinhos[nome]]

    def total_arestas_armazenadas(self):

        return sum(len(v) for v in self._vizinhos.values())

