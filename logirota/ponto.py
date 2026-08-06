"""
TAD Ponto — um endereço de coleta ou entrega na malha do LogiRota.

Módulo 1 aplicado: o TAD declara valores e operações; a representação interna
(dois números para a posição) é decisão de implementação e fica oculta.

Na Aula 06 cada Ponto vira um vértice do grafo da malha viária, e
`distancia_ate` vira o peso da aresta.
"""


class Ponto:
    """Valores: nome, bairro e posição no plano.

    Operações: nome, bairro, distancia_ate(outro).
    """

    def __init__(self, nome, bairro, x, y):
        self._nome = nome
        self._bairro = bairro
        self._x = x
        self._y = y

    @property
    def nome(self):
        return self._nome

    @property
    def bairro(self):
        return self._bairro

    def distancia_ate(self, outro):
        """Distância em linha reta até outro ponto, em quilômetros."""
        dx = self._x - outro._x
        dy = self._y - outro._y
        return round((dx * dx + dy * dy) ** 0.5, 2)

    def __str__(self):
        return f"{self._nome} ({self._bairro})"
