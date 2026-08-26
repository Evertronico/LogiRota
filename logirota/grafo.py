"""
Grafo — malha viária do LogiRota. Módulo 3 aplicado ao projeto.

Até aqui, cada Ponto vivia isolado dentro de um índice (ABB) organizado
por nome — uma hierarquia, sem ligação entre um ponto e outro. Nesta
aula os mesmos Pontos passam a ser vértices de um grafo: a malha viária
que liga um endereço de entrega a outro por uma rua.

Vocabulário fixado aqui:

  vértice     um Ponto da malha
  aresta      uma rua entre dois vértices
  peso        o custo de percorrer a aresta — aqui, `Ponto.distancia_ate`
  não dirigido    se há rua de A para B, há rua de B para A (o caso do LogiRota)
  dirigido        a rua teria sentido único; fora do escopo desta aula

Duas representações clássicas, comparadas sobre os mesmos dados:

  GrafoMatriz   espaço O(v²), vizinhança em tempo constante
  GrafoLista    espaço O(v + a), vizinhança proporcional ao grau do vértice

Reaproveita de logirota/ponto.py:
    Ponto, distancia_ate
"""


class GrafoMatriz:
    """Malha viária representada por matriz de adjacência.

    Cada vértice ocupa uma linha e uma coluna; a célula [i][j] guarda o
    peso da aresta entre eles, ou None se não há rua direta. O espaço
    reservado é v² células, cadastrada a rua ou não.
    """

    def __init__(self, pontos):
        self._pontos = list(pontos)
        self._indice = {p.nome: i for i, p in enumerate(self._pontos)}
        n = len(self._pontos)
        self._matriz = [[None] * n for _ in range(n)]

    def adicionar_rua(self, nome_a, nome_b):
        """Liga dois pontos por uma rua nos dois sentidos."""
        i, j = self._indice[nome_a], self._indice[nome_b]
        peso = self._pontos[i].distancia_ate(self._pontos[j])
        self._matriz[i][j] = peso
        self._matriz[j][i] = peso

    def sao_vizinhos(self, nome_a, nome_b):
        """Um único acesso indexado decide a vizinhança: custo O(1),
        igual para qualquer par, cadastrado ou não."""
        i, j = self._indice[nome_a], self._indice[nome_b]
        return self._matriz[i][j] is not None

    def total_celulas(self):
        """Células alocadas, ocupadas ou não — o custo de espaço real."""
        return len(self._pontos) ** 2


class GrafoLista:
    """Malha viária representada por lista de adjacência.

    Cada vértice guarda apenas os vizinhos que realmente tem, numa
    lista de pares (vizinho, peso). O espaço cresce com o número de
    ruas cadastradas, não com o quadrado dos vértices.
    """

    def __init__(self, pontos):
        self._pontos = {p.nome: p for p in pontos}
        self._vizinhos = {nome: [] for nome in self._pontos}

    def adicionar_rua(self, nome_a, nome_b):
        peso = self._pontos[nome_a].distancia_ate(self._pontos[nome_b])
        self._vizinhos[nome_a].append((nome_b, peso))
        self._vizinhos[nome_b].append((nome_a, peso))

    def sao_vizinhos(self, nome_a, nome_b):
        """Percorre a lista do vértice até achar (ou não) o outro lado:
        custo proporcional ao grau do vértice, não ao total de vértices."""
        for vizinho, _ in self._vizinhos[nome_a]:
            if vizinho == nome_b:
                return True
        return False

    def total_arestas_armazenadas(self):
        """Entradas guardadas de fato — o custo de espaço real."""
        return sum(len(v) for v in self._vizinhos.values())
